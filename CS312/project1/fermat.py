import argparse
import random

#REMEMBER: Redownload the Project 1 files.
#Add more composite tests


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)

# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int: # 1 #n
    #x = bottom val
    #y = exponet val
    #N = number of bits
    if y == 0:
        return 1
    z = mod_exp(x, (y//2), N)   # n^2
    if (y % 2) == 0:
        return ((z**2) % (N)) #n^2
    else:
        return ((x * (z**2)) % (N)) # n^2

#def test_mod():
#   print(mod_exp(2, 41, 5))

# You will need to implement this function and change the return value.
def fprobability(k: int) -> float: # 3
    percent = 1 / (2**k)
    return percent #percentage

# You will need to implement this function and change the return value.
def mprobability(k: int) -> float: # 5 # NO IDEA IF THIS ACTUALLY WORKS
    percent = 1 / (2**k)
    return percent


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.
def fermat(N: int, k: int) -> str: # 2
    for a in range(1,k): #O(n)
        #a^(N-1) mod N ≠ 1
        #if (a**(N-1)) % N != 1:
        if (a >= N):
            break
        if mod_exp(a, N-1, N) != 1: #O(n^3)
            return "composite"
    return "prime"

# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.

#def miller_rabin(N: int, k: int) -> str: # 4
#    return "???"

prime_bases = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
    163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
    251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
    349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
    443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547,
    557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
    647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751
]

def miller_rabin(toTest, k):
    #quick check for being even...
    if(toTest % 2 == 0):
        if(toTest == 2):
            return "prime"
        else:
            return "composite"
    #more efficient algorithm, we're going to run tests on toTest - 1
    for n in range(k):
        a = prime_bases[n]
        # we already know that the bases are prime
        if(a == toTest):
            return "prime"
        # (toTest - 1) = 2^(s) * d, solving for d
        d = toTest - 1
        s = 0
        while((d % 2) == 0):#O(logn)
            d = (d // 2)
            s = s + 1

        # if a^d == 1 OR (toTest - 1), IS prime, otherwise it could be composite?
        x = mod_exp(a,d,toTest) #O(n^3)
        #square this thing s times, and try again^
        for _ in range(s):
            y = mod_exp(x,2,toTest) #square it
            if((y == 1) and (x != 1) and (x != (toTest - 1))):
                return "composite"
            x = y

    return "prime"
    # if we make it this many times through the loop without
    # finding reason to believe the number is composite, we'll assume it's prime

def main(number: int, k: int):
    print(miller_rabin(423, 100))
    print(fermat(423, 100))

    fermat_call, miller_rabin_call = prime_test(number, k)
    fermat_prob = fprobability(k)
    mr_prob = mprobability(k)

    print(f'Is {number} prime?')
    print(f'Fermat: {fermat_call} (prob={fermat_prob})')
    print(f'Miller-Rabin: {miller_rabin_call} (prob={mr_prob})')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('k', type=int)
    args = parser.parse_args()
    main(args.number, args.k)
