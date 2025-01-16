import csv
import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

API_URL = "http://localhost:8001/asr"
AUDIO_DIR = "cv-valid-dev/cv-valid-dev"
CSV_FILE = "out.csv"


"""
Assignment Thinking Process Walkthrough:
1. Realised API call is 1-1, aka for singular record will return single respective output; 
    while possible to invoke API one by one across all 4K records, but will be extremely slow and efficient
2. Process speed up via multi-processing - running API call across different CPU cores (local device used has 16 cores);
    eventual processing speed was about 1 minute per 100 records (one batch)
3. Data processing - while possible to process and store all 4K generated outputs in one shot, 
    but risky approach as any failure will lead to whole process to restart;
    hence applied batch processing to process then store the outputs, so these can serve as checkpoints
    should code crash halfway for any reason (batch size selected as 100)
    (Also as precautionary safety net, failures are already handled as earlier function already returns None types rather than
     potentially crashing)
"""


def transcribe_file(audio_path):
    """
    Transcribes a single audio file.

    Args:
        audio_path: Path to the audio file.

    Returns:
        A tuple containing the file ID and the transcription (or None on error).
    """
    filename = os.path.basename(audio_path)
    file_id = filename.split("-")[1].split(".")[0]
    files = {"file": (filename, open(audio_path, "rb"))}

    print(file_id)
    # print(files)

    try:
        filename = os.path.basename(audio_path)
        file_id = filename.split("-")[1].split(".")[0] 
        files = {"file": (filename, open(audio_path, "rb"))}
        response = requests.post(f"{API_URL}", files=files)
        response.raise_for_status() 
        data = response.json()
        return int(file_id), str(data.get("transcription"))
    except requests.exceptions.RequestException as e:
        print(f"Error transcribing {audio_path}: {e}")
        return None


def process_audio_directory(audio_dir, start_index=0, end_index=None):
    """
    Transcribes audio files in the given directory concurrently using ThreadPoolExecutor.

    Args:
        audio_dir (str): Path to the directory containing audio files.
        batch_size (int): Number of files to process in each batch.

    Returns:
        list: A list of tuples, where each tuple represents a file with 
              "file_id" and "generated_text" keys.
    """
    if end_index is None:
        end_index = len(audio_paths) 

    audio_paths = [os.path.join(audio_dir, filename) for filename in os.listdir(audio_dir)][start_index:end_index]
    results = []

    # Determine the number of CPU cores
    cpu_count = multiprocessing.cpu_count() 
    max_workers = cpu_count   # Adjust based on needs
    print(max_workers)

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(transcribe_file, path) for path in audio_paths]
        for future in futures:
            try:
                file_id, transcription = future.result()
                results.append((file_id, transcription))
            except Exception as e:
                print(f"Error processing: {e}")
                results.append((None, None))

    end_time = time.time()
    total_processing_time = end_time - start_time

    print(f"Total processing time: {total_processing_time:.2f} seconds")
    print(results)

    return results


def write_csv(csv_file, fieldnames, rows):
    """
    Writes a list of dictionaries to a CSV file.

    Args:
        csv_file (str): Path to the output CSV file.
        fieldnames (list): List of field names for the CSV file.
        rows (list): Nested array, where each sub-array represents a row in the CSV file.
    """
    file_exists = os.path.exists(csv_file)

    with open(csv_file, "a", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
         
        if not file_exists:
            writer.writeheader() 
        
        for row in rows:
            row_dict = {fieldnames[0]: row[0], fieldnames[1]: row[1]}
            writer.writerow(row_dict)

if __name__ == "__main__":
    fieldnames = ["file_id", "generated_text"]
    all_files = [os.path.join(AUDIO_DIR, filename) for filename in os.listdir(AUDIO_DIR)]

    batch_size = 100
    num_files = len(all_files)

    for i in range(0, num_files, batch_size):
        start_index = i
        end_index = min(i + batch_size, num_files)  # prevent out-of-bounds error

        output = process_audio_directory(AUDIO_DIR, start_index, end_index)
        write_csv(CSV_FILE, fieldnames, output)
        print(f"Batch starting with Record {i} processed.")