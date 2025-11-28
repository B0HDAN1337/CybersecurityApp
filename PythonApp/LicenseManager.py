import datetime
from CaesarChiper import CaesarCipher

class LicenseManager:
    def __init__(self):
        self.cipher = CaesarCipher(3)
        self.encrypted_key = self.cipher.encrypt("ABC123")

    def is_blocked(self):
        now = datetime.datetime.now()
        print(f"{self.encrypted_key}")
        return now.hour >= 19

    def check_key(self, user_key):
        return self.cipher.encrypt(user_key) == self.encrypted_key
