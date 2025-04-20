from d_finder import mod_inv

#Calculate a^n mod m
def mod_exp(a,n,m):
    r = 1 
    a %= m
    while n > 0:
        if n % 2 == 1:
            r = (r * a) % m
        n = n >> 1
        a = (a**2) % m
    return r

"""Support two type of encoding method:
Hex:Convert each char to 2 bytes
Dec:Convert each char to 3 digits number

prime_a, prime_b: encoding primes
n: encryption modulus
e: exponent of encrypting the message
hex: control the encode method
"""
class crypt:
    #Initialize
    def __init__(self, prime_a = 401, prime_b = 101, n = 0, e = 1025, hex = False):
        self.p = prime_a
        self.q = prime_b
        self.e = e
        self.hex = hex
        self.n = n
        if n == 0:
            self.n = prime_a * prime_b

        inv = mod_inv(prime_a, prime_b, e)
        self.d = inv.mod_inverse()
        self.len = self.chunk_len()

    #Calculate the size of each encripted chunck based on the product of primes
    def chunk_len(self):
        len_hex = ((self.n.bit_length() - 1) >> 3) << 3
        len_dec = ((len(str(self.n)) - 1) // 3) * 3
        if self.hex:
            if len_hex < 8:
                raise ValueError(f"Insufficient prime, please enter larger primes")
            return len_hex
        else:
            if len_dec < 3:
                raise ValueError(f"Insufficient prime, please enter larger primes")
            return len_dec
    
    
    def extract(self, message = []):
        if self.hex:
            m = [int(i, 16) for i in message]
        else:
            m = [int(i) for i in message]
        return m
    
    #Cutting the message into chunks and pad them with zeros
    def conv_pad(self, message = ""):
        chunks = []
        if self.hex:
            hex_str = ""
            for i in message:
                if (c := ord(i)) > 127:
                    raise ValueError("Input contains non-ASCII characters.")
                hex_str += format(c,'X')
            size = self.len // 4
            padding = (size - len(hex_str) % size) % size
            hex_str = '0' * padding + hex_str

            for i in range(0, len(hex_str), size):
                chunk = hex_str[i:i + size]
                chunks.append(int(chunk, 16))
            
        else:
            dec_str = ""
            for i in message:
                if (c := ord(i)) > 127:
                    raise ValueError("Input contains non-ASCII characters.")
                dec_str += f"{c:03d}"
            size = self.len
            padding = (size - len(dec_str) % size) % size
            dec_str = '0' * padding + dec_str

            for i in range(0, len(dec_str), size):
                chunk = dec_str[i:i + size]
                chunks.append(int(chunk))
        return chunks
    
    #Encrypting the message
    def encrypt(self, message =""):
        encripted = []
        encripted_m = []
        m = self.conv_pad(message)
        for i in m:
            encripted.append(mod_exp(i, self.e, self.n))
        if self.hex:
            for i in encripted:
                encripted_m.append(format(i, 'X'))
        else:
            for i in encripted:
                encripted_m.append(str(i))
        return encripted_m
    
    #Decrypting the message
    def decrypt(self, message =[]):
        m = self.extract(message)
        decripted = [mod_exp(c, self.d, self.n) for c in m]
        decripted_m = ""
        if self.hex:
            for n in decripted:
                s = format(n, 'X')
                padding = ((self.len // 4) - len(s) % self.len) % self.len
                s = '0' * padding + s
                decripted_m += s

            chars = [chr(int(decripted_m[i:i+2], 16)) for i in range(0, len(decripted_m), 2)]
            decripted_m = ''.join(chars)
        else:    
            for n in decripted:
                s = str(n)
                s = s.zfill((len(s)+ 2) // 3 * 3)
                decripted_m += s

            chars = [chr(int(decripted_m[i:i+3])) for i in range(0, len(decripted_m), 3)]
            decripted_m = ''.join(chars)
        return decripted_m

c = crypt(1000000000039, 1000000000061, 0, 65537, True)
e = c.encrypt("")
d = c.decrypt(e)
print(e)
print(d)