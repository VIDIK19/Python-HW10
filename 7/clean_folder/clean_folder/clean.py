import os

def main():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)

    for file in files:
        print(file)

if __name__ == "__main__":
    main()