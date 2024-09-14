import argparse
import random

#REMEMBER: Redownload the Project 1 files.


# This is a convenience function for main(). You don't need to touch it.
def prime_test(N: int, k: int) -> tuple[str, str]:
    return fermat(N, k), miller_rabin(N, k)


# You will need to implement this function and change the return value. 
def mod_exp(x: int, y: int, N: int) -> int: # 1
    if y == 0:
        return 1
    z = mod_exp(x, (y//2), N)
    if (y % 2) == 0:
        return (z**2 % (N))
    else:
        return (x * (z**2 % (N)))

#def test_mod():
#   print(mod_exp(2, 41, 5))

# You will need to implement this function and change the return value. 
def fprobability(k: int) -> float: # 3

    return 0


# You will need to implement this function and change the return value.
def mprobability(k: int) -> float: # 5
    return 0


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.
def fermat(N: int, k: int) -> str: # 2
    for a in range(1,k):
        if a != (1 % N):
            return "no"
    return "yes"


# You will need to implement this function and change the return value, which should be
# either 'prime' or 'composite'.
#
# To generate random values for a, you will most likely want to use
# random.randint(low, hi) which gives a random integer between low and
# hi, inclusive.
def miller_rabin(N: int, k: int) -> str: # 4
    return "???"

def roundDown(n: int):
    test = n % 2
    if (test == 1):
        n = n - 1
    return n
    


def main(number: int, k: int):
    print(fermat(36, 12))
    print("test mod:")
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
