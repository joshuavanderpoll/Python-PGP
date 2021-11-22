import getpass
import os

from pgpy import *

ERROR = "\033[91m"
SUCCESS = "\033[92m"
WARNING = "\033[93m"
INFO = "\033[94m"
HEADER = "\033[95m"


def main():
    os.system("clear")
    banner()
    ask_command()


def banner():
    print(HEADER + "  ___      _   _                ___  ___ ___\n"
          " | _ \\_  _| |_| |_  ___ _ _    | _ \\/ __| _ \\\n"
          " |  _/ || |  _| ' \\/ _ \\ ' \\   |  _/ (_ |  _/\n"
          " |_|  \\_, |\\__|_||_\\___/_||_|  |_|  \\___|_|\n"
          "      |__/\n")


def ask_command():
    cmd = input(INFO + "[?] Select your option (encrypt/decrypt): ")

    if cmd == "encrypt" or cmd == "en" or cmd == "enc" or cmd == "e":
        encrypt()
    elif cmd == "decrypt" or cmd == "de" or cmd == "dec" or cmd == "d":
        decrypt()
    else:
        print(ERROR + "[-] Incorrect command.")
        ask_command()


def encrypt():
    path = input(INFO + "[?] Enter the path to the file your would like to encrypt: ")
    if not os.path.isfile(path):
        print(ERROR + "[!] There is no file found on that path.")
        return encrypt()

    with open(path, 'r') as file:
        raw_message = file.read()

    message = PGPMessage.new(raw_message)

    public_key_path = input(INFO + "[?] Enter the path of your public key file [public.asc]: ")
    if public_key_path == "":
        public_key_path = "public.asc"
    if not os.path.isfile(public_key_path):
        print(ERROR + "[!] There is no file found on that path.")
        return encrypt()

    public_key, _ = PGPKey.from_file(public_key_path)
    encrypted = public_key.encrypt(message)

    print("\n")
    print(SUCCESS + str(encrypted))
    print("\n")


def decrypt():
    path = input(INFO + "[?] Enter the path to the file your would like to decrypt: ")
    if not os.path.isfile(path):
        print(ERROR + "[!] There is no file found on that path.")
        return decrypt()

    try:
        message = PGPMessage.from_file(filename=path)
    except ValueError as e:
        print(ERROR + "[!] This file is not an encrypted PGP message. Error: " + str(e))
        return decrypt()

    private_key_path = input(INFO + "[?] Enter the path of your private key file [private.asc]: ")
    if private_key_path == "":
        private_key_path = "private.asc"
    if not os.path.isfile(private_key_path):
        print(ERROR + "[!] There is no file found on that path.")
        return decrypt()

    private_key, _ = PGPKey.from_file(private_key_path)
    private_key_pass = getpass.getpass(INFO + "[?] Enter your private key passphrase: ")

    try:
        with private_key.unlock(private_key_pass):
            decrypted_msg = (private_key.decrypt(message)).message
    except errors.PGPDecryptionError as e:
        print(ERROR + "[!] Could not decrypt message. Incorrect passphrase? Error: " + str(e))
        return decrypt()

    print("\n")
    print(SUCCESS + decrypted_msg)
    print("\n")


if __name__ == "__main__":
    main()
