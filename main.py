from random import randint

def gcd(a, b):
    smaller = a if a < b else b
    for i in range(1, smaller+1):
        if((a % i == 0) and (b % i == 0)):
            gcd = i
    return gcd

def gcdExtended(a, b): 
    if a == 0:  
        return b,0,1

    gcd,s1,t1 = gcdExtended(b%a, a) 

    s = s1 - (b//a) * t1 
    t = t1 

    return gcd,s if s > 0 else s + b,t
     
# Fonte (adaptado): https://github.com/lucasvalentim/pequeno-teorema-de-fermat
def prime_candidate(n, tentativas = 20):
    if n < 1:
        return False
    while tentativas > 0:
        a = randint(2, 1000)

        while gcd(n, a) != 1:
            a = randint(2, 1000)

        if pow(a, n - 1, n) != 1:
            return False

        tentativas -= 1
    
    return True

def generate_gcd(phi):
    e = randint(2, 100000)

    while gcd(e,phi) != 1:
        e = randint(2, 100000)

    return e

def keygen():
    p,q = 0,0

    p_prime,q_prime = False,False
    while not p_prime or not q_prime:
        a = randint(2, 100000)
        p_prime = prime_candidate(a)
        if p_prime:
            p = a

        a = randint(2, 1000)
        q_prime = randint(2, 100000)
        if q_prime:
            q = a

    n = p*q
    phi = (p-1)*(q-1)
    e = generate_gcd(phi)

    _,d,t = gcdExtended(e,phi)

    print((n,e),d)

def encrypt(key,payload):
    (n,e) = key

    # TODO: Implementar criptografia de mensagem
    C = (payload ** e) % n

    return C

if __name__ == "__main__":
    keygen()

    key = (514449163,490925531) # Félix & Aguilar
