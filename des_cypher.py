from tables import ip , E , pc1 , pc2 , shifts , S_BOXES , P , FP
from help_functions import to_bits , to_hex , to_str , bin2dec , dec2bin


def permute(bits, table):
    # make bits in a table
    return [bits[k - 1] for row in table for k in row]


# 64 -> 56
def generate_round_keys(key):
    transformed = permute(key, pc1)         
    c, d = transformed[:28], transformed[28:]

    round_keys = []
    for s in shifts:
        for _ in range(s):
            c.append(c.pop(0))
            d.append(d.pop(0))
        round_keys.append(permute(c + d, pc2))   # 56 -> 48
    return round_keys


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def sbox_substitution(bits):
    output = []
    for n in range(8):
        block = bits[n * 6:(n + 1) * 6]

        row = bin2dec(int(str(block[0]) + str(block[5])))
        col = bin2dec(int("".join(str(b) for b in block[1:5])))

        value = S_BOXES[n][row][col]
        for ch in dec2bin(value):
            output.append(int(ch))
    return output


def feistel(r, round_key):
    expanded = permute(r, E)                 # 32 -> 48
    xored = xor(expanded, round_key)         # 48
    sboxed = sbox_substitution(xored)        # 32
    return permute(sboxed, P)                # 32

def bits_to_hex(bits):
    
    return format(int(to_str(bits), 2), '0{}X'.format(len(bits) // 4))

def des(block, round_keys, show_rounds=False):
    bits = permute(block, ip)
    L, R = bits[:32], bits[32:]

    if show_rounds:
        print("After IP :", bits_to_hex(bits))
        print("L0 =", bits_to_hex(L), " R0 =", bits_to_hex(R))
        print("-" * 60)

    for i, k in enumerate(round_keys, start=1):
        L, R = R, xor(L, feistel(R, k))

        if show_rounds:
            print("Round {:2d} | K = {} | L = {} | R = {}".format(
                i, bits_to_hex(k), bits_to_hex(L), bits_to_hex(R)))

    result = permute(R + L, FP)

    if show_rounds:
        print("-" * 60)
        print("Output   :", bits_to_hex(result))
    return result               # swap halves + final permutation


def des_encrypt(message, key, show_rounds=False):
    return des(message, generate_round_keys(key), show_rounds)


def des_decrypt(cipher, key, show_rounds=False):
    return des(cipher, generate_round_keys(key)[::-1], show_rounds)


# # ---------- run ----------
# key = to_bits("AABB09182736CCDD")
# msg = to_bits("123456ABCD132536")

# cipher = des_encrypt(msg, key , show_rounds=True)
# decrypted = des_decrypt(cipher, key , show_rounds=True)

# print("cipher (bin):", to_str(cipher))
# print("cipher (hex):", to_hex(cipher))
# print("decrypted (hex):", to_hex(decrypted))


def des_cypher(mssg , key , choice ):
    while choice not in(1,2):
      choice = int(input("heyy , you wanna encrypt a text (1) or decrypt it (2) ?")) 

    
