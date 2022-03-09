import hashlib
import random


def miller_rabin(n):
    m = 0
    for k in range(1, n):
        m = (n-1)//2**k
        if m % 2 == 1:
            break
    a = random.randint(2, n-1)
    b = pow(a, m, n)
    if b % n == 1:
        return True
    for i in range(1, k+1):
        if b % n == n-1:
            return True
        else:
            b = pow(b, 2, n)
    return False


def euclidean_algorithm(a, b):
    k, r0, r1, s0, s1, t0, t1 = 0, a, b, 1, 0, 0, 1

    while True:
        k += 1
        qk = r0 // r1
        r2 = r0 - qk * r1
        s2 = s0 - qk * s1
        t2 = t0 - qk * t1

        r0, r1 = r1, r2
        s0, s1 = s1, s2
        t0, t1 = t1, t2

        if r2 == 0:
            return r0, s0, t0


def square_multiply(x, m, n):
    y = 1
    r = m.bit_length()
    for i in range(0, r):
        if m % 2 == 1:
            y = y * x % n
        x = pow(x, 2, n)
        m = m >> 1
    return y


def generate_prime(length):
    while True:
        list_of_primes = [1, 7, 11, 13, 17, 19, 23, 29]
        z = random.randint(2 ** (length - 6), 2 ** (length - 5) - 1)
        p = 30 * z
        is_prime = False
        i = 0
        for i in range(200):
            for j in list_of_primes:
                n = p + j + i * 30
                for k in range(50):
                    is_prime = miller_rabin(n)
                    if not is_prime:
                        break
                if is_prime and n.bit_length() == length:
                    return n


def is_prime(number):
    for k in range(50):
        if not miller_rabin(number):
            return False
    return True


def generate_pg(l, n):
    print("generating values")
    while True:
        q = generate_prime(l)
        for i in range(50):
            k = random.randint((2**(n-1))//q, (2**n - 1)//q)
            p = q * k + 1
            if is_prime(p):
                while True:
                    h = random.randint(2, p - 2)
                    g = square_multiply(h, (p-1)//q, p)
                    if g != 1:
                        return p, q, g


def generate_key(g, q, p):
    print("generating key")
    x = random.randint(2, q - 1)
    y = square_multiply(g, x, p)
    return x, y


def sign(p, q, g, x, m, hash_function):
    print("signing message")
    hash_m = int(hash_function(m).hexdigest(), 16)
    while True:
        while True:
            j = random.randint(2, q - 1)
            r = square_multiply(g, j, p) % q
            if r != 0:
                break
        inv_j = (euclidean_algorithm(j, q)[1] % q)
        s = (inv_j * (hash_m + r * x)) % q
        if s != 0:
            return r, s


def verify(p, q, g, y, r, s, m, hash_function):
    print("verifying message")
    hash_m = int(hash_function(m).hexdigest(), 16)
    if not (1 < r < q and 0 < s < q):
        print("error")
        return False
    w = euclidean_algorithm(s, q)[1] % q
    u_1 = hash_m * w % q
    u_2 = r * w % q
    v = (square_multiply(g, u_1, p) * square_multiply(y, u_2, p) % p) % q
    return v == r


if __name__ == '__main__':
    m = "".encode()
    p, q, g = generate_pg(160, 1024)
    x, y = generate_key(g, q, p)
    r, s = sign(p, q, g, x, m, hashlib.sha1)
    print(verify(p, q, g, y, r, s, m, hashlib.sha1))
