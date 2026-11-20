from math import gcd

def key_inverse_two(key):
    det = key[0][0] * key[1][1] - key[0][1] * key[1][0]
    adj = [[ key[1][1], -key[0][1]],
           [-key[1][0],  key[0][0]]]

    if gcd(det, 26) != 1:
        #print("this matrix is not invertible")
        inverse = None
    else:
        det_inv = pow(det, -1, 26)          
        inverse = [[adj[0][0] * det_inv % 26, adj[0][1] * det_inv % 26],
                   [adj[1][0] * det_inv % 26, adj[1][1] * det_inv % 26]]

    return inverse



def det_three(key):
    det = key[0][0]*(key[1][1]*key[2][2] - key[1][2]*key[2][1]) \
        - key[0][1]*(key[1][0]*key[2][2] - key[1][2]*key[2][0]) \
        + key[0][2]*(key[1][0]*key[2][1] - key[1][1]*key[2][0])

    det = det % 26
    if gcd(det, 26) != 1:      
        return None
    return det


def adj_three(key):

    cofactors = []
    for i in range(3):
        row = []
        for j in range(3):
        
            m = [[key[r][c] for c in range(3) if c != j]
                 for r in range(3) if r != i]
            minor = m[0][0] * m[1][1] - m[0][1] * m[1][0]
            row.append((-1) ** (i + j) * minor)    
        cofactors.append(row)

    
    adj = [[cofactors[j][i] for j in range(3)] for i in range(3)]
    return adj

def key_inverse_three(key):
    det = det_three(key)
    if det is None:
        return None

    det_inv = pow(det, -1, 26)
    adj = adj_three(key)

    inverse = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(adj[i][j] * det_inv % 26)
        inverse.append(row)

    return inverse



def encryption(mssg, key, n):
    letters = []
    for i in mssg:
        if 'A' <= i <= 'Z':
            e = ord(i) - 65
        elif 'a' <= i <= 'z':
            e = ord(i) - 97
        else:
            continue
        letters.append(e)

    while len(letters) % n != 0:           
        letters.append(23)                  

    r = []
    while letters:
        block = letters[:n]        # first n numbers      
        letters = letters[n:]      # remove letters from list          

        for i in range(n):
            t = 0
            for j in range(n):
                t += key[i][j] * block[j]
            r.append(chr(t % 26 + 65))

    return ''.join(r)




def decryption(mssg, key, n):
    if n == 2:
        new_key = key_inverse_two(key)
    else:
        new_key = key_inverse_three(key)

    if new_key is None:                    
        return None

    return encryption(mssg, new_key, n)    




def hill_cypher():

    print("Hey, let's verify the key first")
    n = 0
    while n not in (2, 3):
        try:
            n = int(input("\nMatrix size (2 or 3): "))
        except ValueError:
            n = 0

    key = None
    while key is None:
        mode = 0
        while mode not in (1, 2):
            try:
                mode = int(input("\nEnter the key as numbers (1) or as text (2)? "))
            except ValueError:
                mode = 0

        m = []
        if mode == 1:
            print(f"Enter the {n}x{n} key matrix, row by row:")
            for i in range(n):
                row = []
                for j in range(n):
                    try:
                        row.append(int(input(f"  key[{i}][{j}] = ")))
                    except ValueError:
                        row.append(None)
                m.append(row)

            if any(x is None for row in m for x in row):
                print("Numbers only, try again.")
                continue
        else:
            text = input(f"Enter a key of exactly {n * n} letters: ")
            nums = [ord(c.upper()) - 65 for c in text if 'a' <= c.lower() <= 'z']

            if len(nums) != n * n:
                print(f"The key must contain exactly {n * n} letters, try again.")
                continue

            m = [nums[i * n:(i + 1) * n] for i in range(n)]
            print("Key matrix:", m)

        inverse = key_inverse_two(m) if n == 2 else key_inverse_three(m)
        if inverse is None:
            print("This matrix is not invertible mod 26, try again.")
        else:
            key = m

    choice = 0
    while choice not in (1, 2):
        try:
            choice = int(input("\nDo you want to encrypt (1) or decrypt (2) a text? "))
        except ValueError:
            choice = 0

    if choice == 1:
        mssg = input("\nEnter the message: ")
        print("Encrypted:", encryption(mssg, key, n))
    else:
        mssg = input("\nEnter the encrypted message: ")
        print("Decrypted:", decryption(mssg, key, n))


# hill_cypher()

# valide example
"""
key = [2 8 15
       7 4 17
       8 13 6]

mssg = safe messages 
encrypted = HDSIOEYQOCAA
"""