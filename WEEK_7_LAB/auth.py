import bcrypt
import os

#implementing hash password function
def hash_password(plain_text_password):
    password_bytes= plain_text_password.encode('utf-8')
    # Generate a salt using bcrypt.gensalt()
    salt=bcrypt.gensalt()
    # Hash the password using bcrypt.hashpw()
    hashed_password_bytes= bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    return hashed_password_bytes.decode('utf-8')

#implementing password verification function
def verify_password(plain_text_password, hashed_password):
    #encode plaintext password to bytes
    password_bytes= plain_text_password.encode('utf-8')
    #encode stored hash to bytes
    hashed_bytes= hashed_password.encode('utf-8')
    #verify password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

#implementing user registration
#adding data file constants
USER_DATA_FILE="users.txt"

#implement user existence check
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    
    with open(USER_DATA_FILE, "r") as file: #"r" to read file
        for line in file:
            try:
                stored_username, _ =line.strip().split(",")
                if stored_username==username:
                    return True
            except ValueError:
                continue
    return False

#implement user registration
def register_user(username, password): #registers a new user by saving their username and hashed password
    if user_exists(username):
        return False #username not available or taken
    
    hashed_password= hash_password(password)
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{hashed_password}\n")
    return True

#implement user login
def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            try:
                stored_username, stored_hash=line.strip().split(",")
                if stored_username==username:
                    return verify_password(password, stored_hash)
            except ValueError:
                continue
    return False

#implement input validation
def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 Characters only."
    
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    
    return True, ""  #returns a tuple

#implement password validation
def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    # --- THIS WAS THE MISSING LINE THAT CAUSED THE ERROR ---
    return True, "" 

#implement main menu
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n [1] Register a new user")
    print(" [2] Login")
    print(" [3] Exit")
    print("-" * 50)

def main():
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # --- Registration Flow ---
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
                
            password = input("Enter a password: ").strip()
            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
                
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
                
            # Attempt to register
            if register_user(username, password):
                print(f"Success: User '{username}' registered successfully!")
            else:
                print(f"Error: Username '{username}' already exists.")
                
        elif choice == '2':
            # --- Login Flow ---
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            if login_user(username, password):
                print(f"\nSuccess: Welcome, {username}!")
                print("You are now logged in.")
                input("\nPress Enter to return to main menu...")
            else:
                print("\nError: Invalid username or password.")
                
        elif choice == '3':
            # --- Exit ---
            print("\nExiting...")
            break
            
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()


