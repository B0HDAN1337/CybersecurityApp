class CaesarCipher:
    def __init__(self, shift=3):
        self.shift = shift

    def encrypt(self, text, shift=None):
        if shift is None:
            shift = self.shift
        
        result = ""
        for char in text:
            if 'a' <= char <= 'z':
                result += chr((ord(char) - ord('a') + self.shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                result += chr((ord(char) - ord('A') + self.shift) % 26 + ord('A'))
            else:
                result += char
        return result

    def decrypt(self, text):
        return self.encrypt(text, -self.shift)
