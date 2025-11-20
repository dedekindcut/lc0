#include "loader/chunk_source/rawfile_chunk_source.h"

#include <absl/log/log.h>

#include <fstream>
#include <stdexcept>

#include "utils/files.h"
#include "utils/gz.h"

namespace lczero {
namespace training {

RawFileChunkSource::RawFileChunkSource(const std::filesystem::path& filename)
    : filename_(filename) {}

RawFileChunkSource::~RawFileChunkSource() = default;

std::string RawFileChunkSource::GetChunkSortKey() const {
  return std::filesystem::path(filename_).filename().string();
}

size_t RawFileChunkSource::GetChunkCount() const { return 1; }

std::optional<std::string> RawFileChunkSource::GetChunkData(size_t index) {
  if (index != 0) return std::nullopt;
  
  std::ifstream file(filename_, std::ios::binary);
  if (!file) {
      LOG(ERROR) << "Failed to open " << filename_;
      return std::nullopt;
  }
  std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
  
  if (std::filesystem::path(filename_).extension() == ".gz") {
      try {
          return GunzipBuffer(content);
      } catch (const std::exception& e) {
          LOG(ERROR) << "Failed to gunzip " << filename_ << ": " << e.what();
          return std::nullopt;
      }
  }
  return content;
}

}  // namespace training
}  // namespace lczero
