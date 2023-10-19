CATEGORY = {"Audio": [".mp3", ".aiff"],
            "Video": [".mp4", ".mov"]}


def get_category(filename: str) -> str:
    name, ext = filename.split(".")
    for cat, exts in CATEGORY.items():
        if ext in exts:
            return cat
    return None

if __name__ == "__main__":
    print(get_category("my_video.mp4"))
    print(get_category("text.txt"))