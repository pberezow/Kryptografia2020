from random import randint
from math import gcd

def gen_keys(n):
    w = [randint(1, 10)]
    multiplier = randint(2, 4)
    
    for i in range(n-1):
        w.append(randint(sum(w)+1, multiplier * sum(w)))
    
    q = randint(sum(w), multiplier * sum(w))
    r = randint(1, q-1)

    while gcd(q, r) != 1:
        r = randint(1, q-1)

    B = [(i * r) % q for i in w]

    return B, w, q, r

def encrypt(msg, B):
    """
    Encrypt single character
    """
    return sum([msg[i] * B[i] for i in range(len(msg))])

def decrypt(c, w, r, q):
    """
    Decrypt single character
    """
    pt = [0 for _ in range(len(w))]
    ct = (c * mod_inv(r, q)) % q

    while ct > 0:
        x = max(i for i in w if i <= ct)
        ct -= x
        pt[w.index(x)] = 1
    
    return pt
    
def binarize(msg):
    """
    Returns binary representation of msg as list
    """
    return [int(i) for i in "{:08b}".format(msg)]

def debinarize(bits):
    """
    Converts binary representation to a number
    """
    msg = 0
    for b in bits:
        msg <<= 1
        msg += b
    return msg

def encrypt_text(msg, B):
    """
    Encrypt string
    """
    return [encrypt(binarize(ord(c)), B) for c in msg]

def decrypt_text(ct, w, r, q):
    """
    Decrypt string
    """
    ascii_msg = [decrypt(c, w, r, q) for c in ct]
    print(ascii_msg)
    return ''.join([chr(debinarize(i)) for i in ascii_msg])

def test(msg):
    B, w, q, r = gen_keys(8)
    ct = encrypt_text(msg, B)
    print(f'Encrypted msg: {ct}')
    pt = decrypt_text(ct, w, r, q)
    print(f'Decrypted msg: {pt}')
    if pt != msg:
        print(f'Initial message ({msg}) is not equal to decrypted message ({pt})!')
        print(f'B: {B}')
        print(f'w: {w}')
        print(f'q: {q}')
        print(f'r: {r}')


def extended_gcd(a, b):
    """
    Extended Euclidean algorithm
    """
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def mod_inv(a, m):
    """
    Modular multiplicative inverse
    """
    a %= m
    gcd, x, _ = extended_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        raise Exception('Modular inverse does not exist.')


if __name__ == '__main__':
    test('Hello world!')