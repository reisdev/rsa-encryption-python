from random import randint

def gcd(a, b):
    if(b == 0):
        return a
    return gcd(b,a % b)

def gcdExtended(a, b): 
    gcd, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = gcd // r
        gcd, r = r, gcd - (quotient * r)
        old_s, s = s, old_s - (quotient * s)
        old_t, t = t, old_t - (quotient * t)

    return gcd,old_s if old_s > 0 else old_s + b,old_t

def powMod(a,b,n = 1):
    if(b == 0):
        return 1

    if(b % 2 == 0):
        return (powMod(a, b // 2,n) ** 2) % n
    else:
        return (a * (powMod(a, b // 2,n) ** 2)) % n

# Fonte (adaptado): https://github.com/lucasvalentim/pequeno-teorema-de-fermat
def prime_candidate(n, tentativas = 50):
    if n < 1:
        return False
    while tentativas > 0:
        a = randint(2,2**15-1)

        while gcd(n, a) != 1:
            a = randint(2,2**15-1)

        if powMod(a, n - 1, n) != 1:
            return False

        tentativas -= 1
    
    return True

def generate_gcd(phi):
    e = randint(2**14,2**15-1)

    while gcd(e,phi) != 1:
        e = randint(2**14,2**15-1)

    return e

def getBlockSize(n):
    block_size = next_size = i = 0

    while True:
        next_size += 25 * 10**(2*i)

        if next_size < n:
            block_size = i + 1
            i+=1
        else:
            break

    return block_size

def keygen():
    p,q = 0,0

    p_prime,q_prime = False,False
    while not p_prime:
        a = randint(2**14, 2**15-1)
        p_prime = prime_candidate(a)
        if p_prime:
            p = a
    
    while not q_prime:
        a = randint(2**14, 2**15-1)
        q_prime = prime_candidate(a)
        if q_prime:
            q = a

    print(p,q)
    n = p*q
    phi = (p-1)*(q-1)
    e = generate_gcd(phi)

    _,d,t = gcdExtended(e,phi)

    return (n,e),(n,d) # (public, private)

def encrypt(key,payload):
    (n,e) = key

    block_size = getBlockSize(n)

    M = [(ord(c) - 65) for c in payload]

    blocks = [M[start:start+block_size] for start in range(0,len(M),block_size)]

    C = []

    for block in blocks:
        m_i = 0

        while len(block) % block_size != 0:
            block.append(25)

        i = block_size - 1
        for char in block:
            m_i += (char * 10 ** (2*i))
            i -= 1

        c_i = powMod(m_i,e,n)

        C.append(c_i)
    return C

def decrypt(key,payload):
    (n,d) = key

    P = []
    for c_i in payload:
        P_i = powMod(c_i,d,n)

        P.append(P_i)

    M = []

    block_size = getBlockSize(n)

    for m in P:
        message = ""
        
        aux = m
        i = block_size
        while i > 0:
            c = aux % 100
            char = chr(c + 65)

            message += char

            aux //= 100
            i -=1
        
        M.append(message[::-1])
    return "".join(M)

