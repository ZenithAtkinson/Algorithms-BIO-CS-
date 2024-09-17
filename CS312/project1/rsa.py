import random
import sys
import math

# This may come in handy...
from fermat import miller_rabin
from fermat import fermat

# If you use a recursive implementation of `mod_exp` or extended-euclid,
# you recurse once for every bit in the number.
# If your number is more than 1000 bits, you'll exceed python's recursion limit.
# Here we raise the limit so the tests can run without any issue.
# Can you implement `mod_exp` and extended-euclid without recursion?
sys.setrecursionlimit(4000)

# When trying to find a relatively prime e for (p-1) * (q-1)
# use this list of 25 primes
# If none of these work, throw an exception (and let the instructors know!)
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


# Implement this function
def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    """
    The Extended Euclid algorithm
    Returns x, y , d such that:
    - d = GCD(a, b)
    - ax + by = d

    Note: a must be greater than b
    """
    if b == 0:
        return (1, 0, a)
    (x, y, z) = ext_euclid(b, a%b)
    return (y, x - ((a//b)*y), z) #The third val is the gcd


# Implement this function
def generate_large_prime(bits=512) -> int:
    """
    Generate a random prime number with the specified bit length.
    Use random.getrandbits(bits) to generate a random number of the
    specified bit length.
    """
    bits = 20
    ran_num = random.getrandbits(bits)
    while True:
        ran_num = random.getrandbits(bits)
        if fermat(ran_num, 100) == "prime":  #prime
            #print(ran_num," Is prime")
            return ran_num

# Implement this function
def generate_key_pairs(bits: int) -> tuple[int, int, int]:
    """
    Generate RSA public and private key pairs.
    Return N, e, d
    - N must be the product of two random prime numbers p and q
    - e and d must be multiplicative inverses mod (p-1)(q-1)
    """

    return 0, 0, 0

def relative_prime(q: int, p: int):
    pq = (p-1)*(q-1)
    for e in reversed(primes):
        if ext_euclid(e, pq)[2] > 1:
            return e
    return "failsafe: no e found"

# We say x is the multiplicative inverse of a modulo N if ax ≡ 1 (mod N).
#Compute d, the multiplicative inverse of e mod (p-1)(q-1)

def multi_inverse(e: int, p: int, q: int):
    pq = (p-1)*(q-1)
    d = 2
    while d * e % pq != 1:
        d += d
    return d


def main(number: int):
    #print("test: ", number)
    prime = generate_large_prime()  # Call the function to generate a large prime
    #print("Generated prime: ", prime)  # Print the generated prime number
    q = generate_large_prime()
    p = generate_large_prime()
    e = relative_prime(q,p)
    d = ext_euclid(p, q)[1]
    #e = ext_euclid(p, q)[0]
    print("q:",q)
    print("p:",p)
    print("e:",e)
    print("p*q:",p*q)

    print("euclids algorithm for p and q:", ext_euclid(p, q))
    #[2] = gcd
    #[1] =
    #[0] =
    #Relatively prime means they share no multipliers (other than 1)


if __name__ == "__main__":
    main(10)  # You can pass any number as an argument to `main`



#to get e: find a number where the gcd is 1
#to get d: d is relatively prime to p-1 and q-2
