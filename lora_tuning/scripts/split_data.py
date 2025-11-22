import gzip
import os


def split_data(input_file, output_dir, chunk_size=1000):
    """
    Splits a large V6 training data file into smaller chunks.

    Args:
        input_file (str): Path to the large gzipped training data file.
        output_dir (str): Directory where chunks will be saved.
        chunk_size (int): Number of records per chunk.
    """
    # Size of one training record in bytes (specific to V6 format)
    RECORD_SIZE = 8356

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Splitting {input_file} into chunks of {chunk_size} records...")

    record_buffer = []
    chunk_idx = 0

    with gzip.open(input_file, "rb") as f:
        while True:
            data = f.read(RECORD_SIZE)
            if len(data) < RECORD_SIZE:
                break

            record_buffer.append(data)

            if len(record_buffer) >= chunk_size:
                output_file = os.path.join(output_dir, f"chunk_{chunk_idx:04d}.gz")
                with gzip.open(output_file, "wb") as out_f:
                    for record in record_buffer:
                        out_f.write(record)

                record_buffer = []
                chunk_idx += 1
                if chunk_idx % 10 == 0:
                    print(f"Wrote {chunk_idx} chunks...")

    # Write remaining records
    if record_buffer:
        output_file = os.path.join(output_dir, f"chunk_{chunk_idx:04d}.gz")
        with gzip.open(output_file, "wb") as out_f:
            for record in record_buffer:
                out_f.write(record)
        print(f"Wrote {output_file}")

    print("Done splitting.")


if __name__ == "__main__":
    # Example usage: split data into small chunks
    split_data("data/train_data.gz", "data/chunks", chunk_size=256)
