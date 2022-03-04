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
        z = random.randint(2**(length-1), 2**length-1)
        if is_prime(z):
            return z


def is_prime(number):
    for k in range(50):
        if not miller_rabin(number):
            return False
    return True


def generate_pg():
    print("generating values")
    while True:
        q = generate_prime(160)
        for i in range(50):
            k = random.randint((2**(1024-1))//q, (2**1024 - 1)//q)
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
    return x, square_multiply(g, x, p)


def sign(p, q, g, x, m):
    print("signing message")
    hash_m = int(hashlib.sha3_256(m).hexdigest(), 16)
    while True:
        while True:
            j = random.randint(2, q - 1)
            r = square_multiply(g, j, p) % q
            if r != 0:
                break
        f, i, h = euclidean_algorithm(q, j)
        s = ((i % q) * (hash_m + r * x)) % q
        if s != 0:
            return r, s


def verify(p, q, g, y, r, s, m):
    print("verifying message")
    hash_m = int(hashlib.sha3_256(m).hexdigest(), 16)
    if not 1 < r < q or not 0 < s < q:
        print("error")
        return False
    f, i, h = euclidean_algorithm(q, s)
    w = i % q
    u_1 = hash_m * w % q
    u_2 = r * w % q
    v = square_multiply(g, u_1, p) * square_multiply(y, u_2, p) % q
    return v == r


if __name__ == '__main__':
    m = "".encode()
    p, q, g = generate_pg()
    x, y = generate_key(g, q, p)
    r, s = sign(p, q, g, x, m)
    print(verify(p, q, g, y, r, s, m))
