#include "loader/stages/file_path_provider.h"

#include <absl/cleanup/cleanup.h>
#include <absl/container/flat_hash_set.h>
#include <absl/log/check.h>
#include <absl/log/log.h>
#include <absl/synchronization/mutex.h>

#include <array>
#include <cerrno>
#include <chrono>
#include <cstring>
#include <filesystem>
#include <stdexcept>
#include <string_view>
#include <thread>
#include <utility>

#include "loader/data_loader_metrics.h"
#include "proto/data_loader_config.pb.h"

namespace lczero {
namespace training {

namespace {

bool ShouldSkipName(std::string_view name) {
  return !name.empty() && name.front() == '.';
}

bool ShouldSkipPathEntry(const FilePathProvider::Path& path) {
  return ShouldSkipName(path.filename().string());
}

}  // namespace

FilePathProvider::FilePathProvider(const FilePathProviderConfig& config)
    : SingleOutputStage<File>(config.output()),
      directory_(config.directory()),
      producer_(output_queue()->CreateProducer()),
      load_metric_updater_() {
  LOG(INFO) << "Initializing FilePathProvider for directory: "
            << config.directory();
}

FilePathProvider::~FilePathProvider() {
  LOG(INFO) << "FilePathProvider shutting down.";
  Stop();
  LOG(INFO) << "FilePathProvider shutdown complete.";
}

void FilePathProvider::SetInputs(absl::Span<QueueBase* const> inputs) {
  if (!inputs.empty()) {
    throw std::runtime_error(
        "FilePathProvider expects no inputs, but received " +
        std::to_string(inputs.size()));
  }
}

void FilePathProvider::Start() {
  LOG(INFO) << "Starting FilePathProvider monitoring thread.";
  thread_pool_.Enqueue(
      [this](std::stop_token stop_token) { Worker(stop_token); });
}

void FilePathProvider::Stop() {
  if (stop_source_.stop_requested()) return;
  LOG(INFO) << "Stopping FilePathProvider.";
  stop_source_.request_stop();
  thread_pool_.Shutdown();
  producer_.Close();
}

StageMetricProto FilePathProvider::FlushMetrics() {
  StageMetricProto stage_metric;
  auto load_metrics = load_metric_updater_.FlushMetrics();
  load_metrics.set_name("load");
  *stage_metric.add_load_metrics() = std::move(load_metrics);
  *stage_metric.add_queue_metrics() =
      MetricsFromQueue("output", *output_queue());
  return stage_metric;
}

void FilePathProvider::AddDirectory(const Path& directory,
                                    std::stop_token stop_token) {
  ScanDirectory(directory, stop_token);

  LOG(INFO) << "FilePathProvider scanned " << directory;

  // Signal that initial scan is complete
  LOG(INFO) << "FilePathProvider initial scan complete";
  producer_.Put(
      {{.filepath = Path{}, .message_type = MessageType::kInitialScanComplete}},
      stop_token);
}

void FilePathProvider::ScanDirectory(const Path& directory,
                                     std::stop_token stop_token) {
  std::vector<Path> files;
  std::vector<Path> subdirectories;
  std::error_code ec;
  auto iterator = std::filesystem::directory_iterator(directory, ec);
  if (ec) {
      LOG(ERROR) << "Failed to iterate directory " << directory << ": "
              << ec.message();
      return;
  }

  for (const auto& entry : iterator) {
    const Path entry_path = entry.path();
    if (ShouldSkipPathEntry(entry_path)) continue;

    if (entry.is_regular_file(ec) && !ec) {
      files.push_back(entry_path);
    } else if (entry.is_directory(ec) && !ec) {
      subdirectories.push_back(entry_path);
    }
  }

  // Send notifications for discovered files
  constexpr size_t kBatchSize = 10000;
  std::vector<File> batch;
  batch.reserve(kBatchSize);

  auto flush_batch = [&]() {
    if (batch.empty()) return;
    producer_.Put(batch, stop_token);
    batch.clear();
  };

  for (const auto& filepath : files) {
    batch.push_back(
        {.filepath = filepath.string(), .message_type = MessageType::kFile});
    if (batch.size() >= kBatchSize) flush_batch();
  }

  // Recursively call for subdirectories
  for (const auto& subdir : subdirectories) {
    if (stop_token.stop_requested()) return;
    ScanDirectory(subdir, stop_token);
  }

  // Flush any remaining files
  flush_batch();
}


void FilePathProvider::Worker(std::stop_token stop_token) {
  // Perform directory scanning in background thread
  AddDirectory(directory_, stop_token);

  // Just idle until stopped, to mimic behavior of continuous provider
  // In real implementation for macOS we could use FSEvents/kqueue to watch,
  // but for now we just support static dataset.
  while (!stop_token.stop_requested()) {
      std::this_thread::sleep_for(std::chrono::milliseconds(100));
  }
}

}  // namespace training
}  // namespace lczero
