from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Тут можуть бути будь-які зовнішні бібліотеки, які потрібні для вашого проекту.
    ],
    entry_points={
        'console_scripts': [
            'clean-folder=clean_folder.clean:main',  # Тут вказано, що при виклику `clean-folder` буде виконуватися функція `main` із модуля `clean` у пакеті `clean_folder`.
        ],
    }
)