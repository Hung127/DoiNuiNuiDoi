from hill_cipher import HillCipher


def main():
    cipher = HillCipher(block_size=5)
    text = input("Enter something: ")
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)
    print("Plaintext:", text)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

if __name__ == "__main__":
    main()
