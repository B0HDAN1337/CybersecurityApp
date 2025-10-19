import bcrypt

def check_password(password_input, stored_hash):
    return bcrypt.checkpw(password_input.encode(), stored_hash)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
