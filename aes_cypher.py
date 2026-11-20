from help_functions import decimal_to_hex
from tables import SBOX , RCON , INV_SBOX
 

def hex_xor(a, b):
    result = int(a, 16) ^ int(b, 16)
    return hex(result)[2:].zfill(2)


def multiply_hex(a, b):
    a = int(a, 16)
    b = int(b, 16)
    result = 0

    for i in range(8):
        if b % 2 == 1:
            result ^= a

        if a >= 128:
            a = (a * 2) % 256
            a ^= 0x1B
        else:
            a *= 2

        b //= 2

    return format(result, '02x')

def letter_to_numbers(mssg):
    letters = []
    for i in mssg:
        if 'A' <= i <= 'Z':
            e = ord(i) - 65
        elif 'a' <= i <= 'z':
            e = ord(i) - 97
        elif '0' <= i <= '9':
            e = ord(i) - 48 + 26   # digits 0-9 become 26-35, right after the letters
        else:
            continue
        letters.append(e)
    return letters


def numbers_to_letters(matrix):
    text = ""
    for j in range(4):
        for i in range(4):
            n = int(matrix[i][j], 16)
            if n < 26:
                text += chr(n + 97)
            else:
                text += chr(n - 26 + 48)
    return text


# key expansion 

def rot_word(word):
    return word[1:] + word[:1]


def sub_word(word):
    return [SBOX[b >> 4][b & 15] for b in word]


def xor_words(a, b):
    result = []

    for i in range(4):
        result.append(a[i] ^ b[i])

    return result



def key_expansion(key):

    # Convert key into bytes
    key = [int(key[i:i+2], 16) for i in range(0, 32, 2)]

    # Divide key into 4 words
    words = []
    for i in range(0, 16, 4):
        words.append(key[i:i+4])

    # Generate 40 remaining words
    for i in range(4, 44):

        temp = words[i-1]

        if i % 4 == 0:
            temp = rot_word(temp)
            temp = sub_word(temp)
            temp = xor_words(temp, RCON[i//4 - 1])

        new_word = xor_words(words[i-4], temp)
        words.append(new_word)

    # Generate 11 round keys
    round_keys = []

    for i in range(0, 44, 4):
        matrix = [[0]*4 for _ in range(4)]

        for j in range(4):
            for k in range(4):
                matrix[k][j] = words[i+j][k]

        round_keys.append(matrix)

    return words, round_keys





def build_matrix(numbers):   # numbers must be a list and its for key and mssg 
    matrix = [["00"] * 4 for _ in range(4)]

    k = 0
    for j in range(4):
        for i in range(4):
            matrix[i][j] = decimal_to_hex(numbers[k]).zfill(2)
            k += 1

    return matrix


def initial_round(key_matrix, mssg_matrix):
    matrix = [["00"] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            matrix[i][j] = hex_xor(key_matrix[i][j], mssg_matrix[i][j])

    return matrix



def subbyte(matrix):
    new_matrix = [["00"] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            k = matrix[i][j]

            row = int(k[0], 16)
            col = int(k[1], 16)

            new_matrix[i][j] = format(SBOX[row][col], "02x")

    return new_matrix


def shiftrows(matrix):
    new_matrix = []
    for i in range(4):
        row = matrix[i]
        new_matrix.append(row[i:] + row[:i])   # rotate row i left by i positions
    return new_matrix


MIX = [
    ["02", "03", "01", "01"],
    ["01", "02", "03", "01"],
    ["01", "01", "02", "03"],
    ["03", "01", "01", "02"]
]



def mix_column(matrix):
    new_matrix = [["00"] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                multiplication = multiply_hex(MIX[i][k], matrix[k][j])
                new_matrix[i][j] = hex_xor(new_matrix[i][j], multiplication)

    return new_matrix


def add_round_key(matrix , key):
    new_matrix = [["00"] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            new_matrix[i][j]=hex_xor(matrix[i][j] , key[i][j])

    return new_matrix



def encrypt_aes(mssg, key):

    
    numbers = letter_to_numbers(mssg)
    key_numbers = letter_to_numbers(key)

    if len(numbers) != 16 or len(key_numbers) != 16:
        raise ValueError("Message and key must contain exactly 16 letters")

    
    hexa_mssg = build_matrix(numbers)

    
    key_hex = ""
    for n in key_numbers:
        key_hex += decimal_to_hex(n).zfill(2)

    # Generate all round keys
    words, round_keys = key_expansion(key_hex)

    
    result = initial_round(hexa_mssg, build_matrix(key_numbers))

    
    for i in range(1, 10):

        result = subbyte(result)
        result = shiftrows(result)
        result = mix_column(result)

        # Convert round key integers to hexadecimal
        round_key = []
        for row in round_keys[i]:
            round_key.append([format(b, "02x") for b in row])

        result = add_round_key(result, round_key)

    # Final round (round 10)
    result = subbyte(result)
    result = shiftrows(result)

    round_key = []
    for row in round_keys[10]:
        round_key.append([format(b, "02x") for b in row])

    result = add_round_key(result, round_key)

    return result

    
    


# decryption 

def inv_subbyte(matrix):
    new_matrix = [["00"] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            k = matrix[i][j]

            row = int(k[0], 16)
            col = int(k[1], 16)

            new_matrix[i][j] = format(INV_SBOX[row][col], "02x")

    return new_matrix


def inv_shiftrows(matrix):
    new_matrix = []

    for i in range(4):
        row = matrix[i]
        new_matrix.append(row[-i:] + row[:-i])

    return new_matrix


INV_MIX = [
    ["0e", "0b", "0d", "09"],
    ["09", "0e", "0b", "0d"],
    ["0d", "09", "0e", "0b"],
    ["0b", "0d", "09", "0e"]
]


def inv_mix_column(matrix):
    new_matrix = [["00"] * 4 for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                multiplication = multiply_hex(INV_MIX[i][k], matrix[k][j])
                new_matrix[i][j] = hex_xor(new_matrix[i][j], multiplication)

    return new_matrix



def decrypt_aes(cipher, key):

    # Generate round keys
    words, round_keys = key_expansion(key)

    # Convert round key integers to hexadecimal
    hex_keys = []

    for matrix in round_keys:
        new_matrix = []
        for row in matrix:
            new_matrix.append([format(b, "02x") for b in row])
        hex_keys.append(new_matrix)

    result = cipher

    # Initial AddRoundKey (Round 10)
    result = add_round_key(result, hex_keys[10])

    # Rounds 9 to 1
    for i in range(9, 0, -1):

        result = inv_shiftrows(result)
        result = inv_subbyte(result)
        result = add_round_key(result, hex_keys[i])
        result = inv_mix_column(result)

    # Final round (Round 0)
    result = inv_shiftrows(result)
    result = inv_subbyte(result)
    result = add_round_key(result, hex_keys[0])

    return result


def aes_cypher():

    choice = input("You wanna encrypt (1) or decrypt (2): ")

    if choice == "1":

        mssg = input("Enter your message (must be 16 letters / 128 bits): ")
        key = input("Enter your key (must be 16 letters / 128 bits): ")

        # letter_to_numbers only keeps letters anyway, so count/pad/trim on
        # that, not on the raw length (otherwise spaces/digits in the input
        # throw the count off)
        mssg = "".join(ch for ch in mssg if ch.isalnum())
        key = "".join(ch for ch in key if ch.isalnum())

        # Check message length
        if len(mssg) < 16:

            c = input(
                "Message is less than 128 bits.\n"
                "Enter a new message (1) or fill the rest with x (2): "
            )

            while c == "1" and len(mssg) != 16:
                mssg = "".join(ch for ch in input("Enter a new message: ") if ch.isalnum())

                if len(mssg) < 16:
                    c = input("Still too short! Enter a new message (1) or fill with x (2): ")

            if c == "2":
                mssg = mssg + "x" * (16 - len(mssg))

        elif len(mssg) > 16:
            print(" this mssg is too long , we gonna ingnore the rest ")

            mssg = mssg[:16]

        print("Message:", mssg)

        if len(key) < 16:

            c = input(
                "key is less than 128 bits.\n"
                "Enter a new key (1) or fill the rest with x (2): "
            )

            while c == "1" and len(key) != 16:
                key = "".join(ch for ch in input("Enter a new key: ") if ch.isalnum())

                if len(key) < 16:
                    c = input("Still too short! Enter a new key(1) or fill with x (2): ")

            if c == "2":
                key = key + "x" * (16 - len(key))

        elif len(key) > 16:
            print(" this key is too long , we gonna ingnore the rest ")

            key = key[:16]

        print("key:", key)

        cipher = encrypt_aes(mssg, key)
        print("encrypted mssg is : ", cipher)

        # flatten the matrix into plain hex text (same column order build_matrix
        # fills it in), so it's just normal text you can copy and paste back in
        # when decrypting - no brackets, quotes or commas to retype
        cipher_hex = ""
        for j in range(4):
            for i in range(4):
                cipher_hex += cipher[i][j]

        print("same thing as plain hex text (save this, you'll need it to decrypt):", cipher_hex)

    elif choice == "2":

        # decrypt_aes needs the ciphertext as the 4x4 hex-byte matrix that
        # encrypt_aes produces, and the key as the same hex string
        # key_expansion needs (not raw letters) - so we rebuild both here
        # using functions already defined above.

        cipher_hex = input("Enter the ciphertext as plain hex text (32 characters): ").strip()

        if len(cipher_hex) != 32:
            print("Ciphertext must be exactly 32 hex characters (16 bytes). Aborting.")
            return

        # turn the hex text into the same kind of number list build_matrix
        # expects (it normally comes from letter_to_numbers), then reuse
        # build_matrix itself to lay it out as a matrix
        cipher_numbers = [int(cipher_hex[i:i+2], 16) for i in range(0, 32, 2)]
        cipher = build_matrix(cipher_numbers)

        key = input("Enter your key (must be 16 letters / 128 bits): ")
        key = "".join(ch for ch in key if ch.isalnum())

        if len(key) < 16:

            c = input(
                "key is less than 128 bits.\n"
                "Enter a new key (1) or fill the rest with x (2): "
            )

            while c == "1" and len(key) != 16:
                key = "".join(ch for ch in input("Enter a new key: ") if ch.isalnum())

                if len(key) < 16:
                    c = input("Still too short! Enter a new key(1) or fill with x (2): ")

            if c == "2":
                key = key + "x" * (16 - len(key))

        elif len(key) > 16:
            print(" this key is too long , we gonna ingnore the rest ")

            key = key[:16]

        print("key:", key)

        key_numbers = letter_to_numbers(key)
        key_hex = ""
        for n in key_numbers:
            key_hex += decimal_to_hex(n).zfill(2)

        decrypted = decrypt_aes(cipher, key_hex)
        print("decrypted mssg is : ", numbers_to_letters(decrypted))

    else:
        print("Invalid choice.")


# aes_cypher()