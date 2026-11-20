def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def to_bits(hexstr):
    return [int(b) for b in bin(int(hexstr, 16))[2:].zfill(64)]

def to_hex(bits):
    return hex(int("".join(map(str, bits)), 2))[2:].zfill(16).upper()

def to_str(bits):
    return "".join(map(str, bits))

def bin2dec(binary):
    decimal, i = 0, 0
    while binary != 0:
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal

def dec2bin(num):
    res = bin(num).replace("0b", "")
    if len(res) % 4 != 0:
        div = int(len(res) / 4)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def decimal_to_hex(decimal):
    return format(decimal, "X") 


def hex_to_binary(h):
    return bin(int(h, 16))[2:]