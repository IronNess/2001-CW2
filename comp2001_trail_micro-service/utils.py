import bcrypt

def hash_password(password):
    # Encode the password to bytes, then hash it
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')  # decode the hash to store it as a string in the database

# Example usage
users_passwords = {
    "Grace Hopper": "ISAD123!",
    "Tim Berners-Lee": "COMP2001!",
    "Ada Lovelace": "insecurePassword"
}

# Hash passwords and print them
for user, password in users_passwords.items():
    hashed_password = hash_password(password)
    print(f"User: {user}, Hashed Password: {hashed_password}")
