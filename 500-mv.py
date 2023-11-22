import os
import re
import shutil
import tarfile

def find_files_without_status_500(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.log')]

    files_without_status_500 = []

    for file in files:
        file_path = os.path.join(directory, file)

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as log_file:
                status_500_found = False
                for line in log_file:
                    if re.search(r'\b500\b', line):
                        status_500_found = True
                        break

                if not status_500_found:
                    files_without_status_500.append(file)

        except UnicodeDecodeError as e:
            print(f"Error decoding {file_path}: {e}")

    return files_without_status_500

def compress_and_move_to_directory(files_to_compress, source_directory, destination_directory):
    for file in files_to_compress:
        source_file_path = os.path.join(source_directory, file)
        compressed_file_path = os.path.join(destination_directory, file + '.tgz')

        with tarfile.open(compressed_file_path, 'w:gz') as tar:
            tar.add(source_file_path, arcname=os.path.basename(source_file_path))

        print(f"{file} を {compressed_file_path} に圧縮しました。")

        new_location = os.path.join(destination_directory, os.path.basename(compressed_file_path))
        shutil.move(compressed_file_path, new_location)

        print(f"{compressed_file_path} を {new_location} に移動しました。")

        # 圧縮した後に元の .log ファイルを削除
        os.remove(source_file_path)
        print(f"{file} を削除しました。")

# Specify the original and destination directories
original_directory = '/home/c0a20050/WorldCup98/sample/unzip'
destination_directory = '/home/c0a20050/500-mv'

# Find files without status code 500
result_without = find_files_without_status_500(original_directory)

# Compress, move, and delete original files without status code 500
compress_and_move_to_directory(result_without, original_directory, destination_directory)
