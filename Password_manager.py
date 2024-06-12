# uncompleted project.



import os
import hashlib
from cryptography.fernet import Fernet
from getpass import getpass

# Constants
PASSWORD_FILE = 'passwords.enc'
KEY_FILE = 'secret.key'
MASTER_PASSWORD_FILE = 'master_password.hash'

# Generate and load encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

# Encrypt and decrypt messages
def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

# Initialize password file
def initialize_password_file(key):
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'wb') as password_file:
            password_file.write(encrypt_message("", key))

# Add and view passwords
def add_password(service, username, password, key):
    with open(PASSWORD_FILE, 'rb') as password_file:
        encrypted_data = password_file.read()
    decrypted_data = decrypt_message(encrypted_data, key)
    decrypted_data += f"{service}:{username}:{password}\n"
    with open(PASSWORD_FILE, 'wb') as password_file:
        password_file.write(encrypt_message(decrypted_data, key))

def view_passwords(key):
    with open(PASSWORD_FILE, 'rb') as password_file:
        encrypted_data = password_file.read()
    decrypted_data = decrypt_message(encrypted_data, key)
    if decrypted_data:
        print("Stored passwords:")
        for line in decrypted_data.strip().split('\n'):
            if line:
                service, username, password = line.split(':')
                print(f"Service: {service}, Username: {username}, Password: {password}")
    else:
        print("No passwords stored yet.")

# Hash and verify passwords
def hash_password(password):
    salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + pwdhash

def verify_password(stored_password, provided_password):
    salt = stored_password[:16]
    stored_pwdhash = stored_password[16:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_pwdhash

# Set master password
def set_master_password():
    master_password = getpass()
    confirm_password = getpass("Confirm master password: ")
    if master_password == confirm_password:
        with open(MASTER_PASSWORD_FILE, 'wb') as f:
            f.write(hash_password(master_password))
        print("Master password set successfully.")
    else:
        print("Passwords do not match. Please try again.")

# Recreate master password
def recreate_master_password():
    set_master_password()

# Main program
def main():
    key = load_key()
    initialize_password_file(key)
    
    if not os.path.exists(MASTER_PASSWORD_FILE):
        print("Set a master password:")
        set_master_password()
    
    stored_password = open(MASTER_PASSWORD_FILE, 'rb').read()
    
    while True:
        print("\nPassword Manager")
        print("1. Add username and password")
        print("2. View usernames and passwords")
        print("3. Recreate master password")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            service = input("Enter the service name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            add_password(service, username, password, key)
            print("Username and password added successfully.")
        elif choice == '2':
            entered_password = getpass("Enter the master password: ")
            if verify_password(stored_password, entered_password):
                view_passwords(key)
            else:
                print("Invalid master password.")
        elif choice == '3':
            recreate_master_password()
            stored_password = open(MASTER_PASSWORD_FILE, 'rb').read()  # Update stored password after recreation
        elif choice == '4':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

