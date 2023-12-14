import os
import shutil
import sys

def normalize(name):
    cyrillic_to_latin = {
        "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g", "д": "d", "е": "e", "є": "ie",
        "ж": "zh", "з": "z", "и": "y", "і": "i", "ї": "i", "й": "i", "к": "k", "л": "l",
        "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch", "ю": "iu", "я": "ia"
    }

    for cyr, lat in cyrillic_to_latin.items():
        name = name.replace(cyr, lat)
        name = name.replace(cyr.upper(), lat.upper())

    normalized_name = ''.join(
        char if (char.isalnum() or char == '.') else '_' for char in name)

    return normalized_name

def process_folder(folder_path):
    known_extensions = {
        'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'video': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }

    for entry in os.scandir(folder_path):
        if entry.is_dir():
            if entry.name not in ['archives', 'video', 'audio', 'documents', 'images']:
                process_folder(entry.path)
                if not os.listdir(entry.path):
                    os.rmdir(entry.path)
            continue

        file_ext = entry.name.split('.')[-1].upper()
        new_name = normalize(entry.name)
        new_path = os.path.join(folder_path, new_name)

        os.rename(entry.path, new_path)

        moved = False
        for folder, extensions in known_extensions.items():
            if file_ext in extensions:
                if folder == 'archives':
                    archive_output_folder = os.path.join(
                        folder_path, folder, os.path.splitext(new_name)[0])
                    os.makedirs(archive_output_folder, exist_ok=True)
                    shutil.unpack_archive(new_path, archive_output_folder)
                else:
                    os.makedirs(os.path.join(folder_path, folder), exist_ok=True)
                    shutil.move(new_path, os.path.join(folder_path, folder))
                moved = True
                break

        if not moved:
            print(f"Unknown extension for file: {new_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python sort.py <шлях до папки>")
    else:
        target_folder = sys.argv[1]
        process_folder(target_folder)
