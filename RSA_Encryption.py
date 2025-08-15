import random, math, base64

def generateKeys(n1, n2, accuracy):
    def fermat_check(num):
        prime = False
        for _ in range(accuracy):
            a = random.randrange(2, num - 1)
            rem = pow(a, num - 1, num)
            if rem == 1:
                prime = True
            else:
                prime = False
                break
        return prime


    def isPrime(n):
        lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
            , 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179
            , 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269
            , 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367
            , 373, 379, 383, 389, 397, 401]

        for p in lowPrimes:
            if n == p:
                return True
            if n % p == 0:
                return False

        return fermat_check(n)


    def generateLargePrime(k):
        n = random.randrange((2 ** (k - 1)) + 1, 2 ** k, 2)
        while not isPrime(n):
            n = random.randrange((2 ** (k - 1)) + 1, 2 ** k, 2)
        return n


    p = generateLargePrime(n1)
    q = generateLargePrime(n2)
    while p == q:
        p = generateLargePrime(n1)
        q = generateLargePrime(n2)

    n = p * q
    φ_n = (p - 1) * (q - 1)

    e = random.randrange(2, φ_n)
    while math.gcd(e, φ_n) > 1:
        e = random.randrange(2, φ_n)

    EuclidAlgoLists = [[φ_n, e], [1, 0], [0, 1]]
    quotient = φ_n // e
    while EuclidAlgoLists[0][-1] != 1:
        EuclidAlgoLists[0].append(EuclidAlgoLists[0][-2] % EuclidAlgoLists[0][-1])
        for x in [1, 2]:
            EuclidAlgoLists[x].append(EuclidAlgoLists[x][-2] - quotient * EuclidAlgoLists[x][-1])
        quotient = EuclidAlgoLists[0][-2] // EuclidAlgoLists[0][-1]

    d = EuclidAlgoLists[2][-1]

    if d < 0:
        d += φ_n

    keys = [(d, n), (e, n)]
    return keys


def EncodeEncryption(num):
    list_ = []
    while num != 0:
        list_.append(num & 0xff)
        num >>= 8
    list_ = bytes(list_[::-1])
    encoded_bytes = base64.b64encode(list_)
    encoded = str(encoded_bytes)[2:-1]

    return encoded


def DecodeEncryption(cipher):
    num_bytes = base64.b64decode(cipher)
    num_decoded = 0
    for x in num_bytes:
        num_decoded += x
        num_decoded <<= 8
    num_decoded >>= 8

    return num_decoded


def Encrypt(message, block_size, public_key):
    rem = len(message) % block_size
    if rem != 0:
        message += " " * (block_size - rem)

    cipher_list = []
    for i in range(0, len(message), block_size):
        curr_block = message[i: i + block_size]
        num = 0
        for x in curr_block:
            num += ord(x)
            num <<= 8
        num >>= 8

        cipher_list.append(pow(num, public_key[0], public_key[1]))

    cipher = ""
    for x in cipher_list:
        cipher += EncodeEncryption(x)
        cipher += " "

    return cipher


def Decrypt(cipher, block_size, private_key):
    cipher_list = cipher.split()
    message = ""
    for x in cipher_list:
        num = pow(DecodeEncryption(x), private_key[0], private_key[1])
        block_char = ''
        while num != 0:
            block_char = chr(num & 0xff) + block_char
            num >>= 8
        message += block_char

    return message