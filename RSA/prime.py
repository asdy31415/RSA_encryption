import random
import math

# Trial division for small primes
def trial_division(n, limit=1000000):
    factors = []
    for p in small_primes(limit):
        while n % p == 0:
            factors.append(p)
            n //= p
        if p * p > n:
            break
    return factors, n

# Pollard's Rho for larger factors
def pollards_rho(n):
    if n % 2 == 0:
        return 2
    x = random.randrange(2, n)
    y = x
    c = random.randrange(1, n)
    d = 1

    while d == 1:
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        d = math.gcd(abs(x - y), n)
        if d == n:
            return pollards_rho(n)
    return d

# Generate small primes using sieve
def small_primes(limit):
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

# Primality test (Miller-Rabin)
def is_prime(n, k=7):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Main factorization function
def factor(n):
    factors = []
    small_factors, remaining = trial_division(n)
    factors.extend(small_factors)

    if remaining == 1:
        return sorted(factors)

    stack = [remaining]
    while stack:
        num = stack.pop()
        if is_prime(num):
            factors.append(num)
        else:
            f = pollards_rho(num)
            stack.append(f)
            stack.append(num // f)

    return sorted(factors)


number = 10**24 + 10**14 +2379
print(factor(number))
