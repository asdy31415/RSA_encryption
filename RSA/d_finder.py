class mod_inv:
    def __init__(self, prime_a = 3, prime_b = 5, e = 1025):
        self.p = prime_a
        self.q = prime_b
        self.n = (self.p-1)*(self.q-1)
        self.e = e
    
    def extended_gcd(self, a, b):
        if b == 0:
            return a, 1, 0  # gcd, x, y
        gcd, x1, y1 = self.extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    def mod_inverse(self):
        gcd, x, _ = self.extended_gcd(self.e, self.n)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist (e and n are not coprime)")
        return x % self.n  # Ensure positive result
