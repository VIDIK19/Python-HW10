import os
import shutil
import re
from pathlib import Path
import zipfile
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='folder_sort_log.log')

def normalize(text):
    logging.debug("Normalizing name: %s", text)
    translation = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie',
        'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia'
    }

    normalized_name = ''.join(translation.get(c, c) for c in text)
    normalized_name = re.sub(r'[^a-zA-Z0-9]', '_', normalized_name)
    return normalized_name

def categorize(extension):
    category = None
    images = ['JPEG', 'PNG', 'JPG', 'SVG']
    video = ['AVI', 'MP4', 'MOV', 'MKV']
    docs = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'ODT', 'ODS', 'CSV']
    music = ['MP3', 'OGG', 'WAV', 'AMR']
    archives = ['ZIP', 'GZ', 'TAR']

    if extension in images:
        category = "images"
    elif extension in video:
        category = "video"
    elif extension in docs:
        category = "documents"
    elif extension in music:
        category = "audio"
    elif extension in archives:
        category = "archives"
    else:
        category = "unknown"

    logging.debug("Categorizing extension: %s as %s", extension, category)
    return category

def process_folder(folder_path):
    logging.info("Processing folder: %s", folder_path)
    known_extensions = set()
    unknown_extensions = set()

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        normalized_name = normalize(item)
        normalized_path = os.path.join(folder_path, normalized_name)

        if os.path.isdir(normalized_path) and normalized_name not in ["archives", "video", "audio", "documents", "images"]:
            logging.debug("Recursively processing folder: %s", normalized_path)
            process_folder(normalized_path)
            if not os.listdir(normalized_path):
                os.rmdir(normalized_path)
        elif os.path.isfile(normalized_path):
            logging.debug("Processing file: %s", normalized_name)
            extension = Path(normalized_name).suffix[1:].upper()

            if extension in ["ZIP", "GZ", "TAR"]:
                logging.info("Extracting archive: %s", normalized_name)
                archive_folder = os.path.join(folder_path, 'archives', normalized_name)
                os.makedirs(archive_folder, exist_ok=True)

                if extension == "ZIP":
                    with zipfile.ZipFile(normalized_path, 'r') as zip_ref:
                        zip_ref.extractall(archive_folder)

                os.remove(normalized_path)
            else:
                category = categorize(extension)
                if category != "unknown":
                    known_extensions.add(extension)
                    new_path = os.path.join(folder_path, category, normalized_name)
                    os.makedirs(os.path.dirname(new_path), exist_ok=True)
                    shutil.move(normalized_path, new_path)
                    logging.info("Moving file: %s to %s", normalized_name, new_path)
                else:
                    unknown_extensions.add(extension)

    logging.info("Processed folder: %s. Known extensions: %s. Unknown extensions: %s", folder_path, known_extensions, unknown_extensions)
    return known_extensions, unknown_extensions

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logging.error("Invalid number of arguments. Please provide the path to the folder.")
        print("Вкажіть шлях до папки для сортування!")
        sys.exit(1)

    target_folder = sys.argv[1]
    logging.info("Starting script for folder: %s", target_folder)
    known, unknown = process_folder(target_folder)

    print("Відомі розширення:", known)
    print("Невідомі розширення:", unknown)
    logging.info("Script completed. Known extensions: %s, Unknown extensions: %s", known, unknown)
