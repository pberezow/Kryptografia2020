import random
from functools import reduce
from math import gcd

class LCG:
    a = 1103515245
    c = 12345
    m = 2**31

    def __init__(self, seed, a=None, c=None, m=None):
        self.state = seed
        if a:
            assert type(a) == int
            self.a = a
        if c:
            assert type(c) == int
            self.c = c
        if m:
            assert type(m) == int
            self.m = m
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state
        
def _determine_increment(states, modulus, multiplier):
    increment = (states[1] - states[0] * multiplier) % modulus
    return increment

def extended_gcd(a, b):
    """
    Extended Euclidean algorithm
    """
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def mod_inv(a, m):
    """
    Modular multiplicative inverse
    """
    a %= m
    gcd, x, _ = extended_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        raise Exception('Modular inverse does not exist.')

def _determine_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * mod_inv(states[1] - states[0], modulus) % modulus
    return multiplier

def _determine_modulus(states):
    diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
    zeroes = [t2*t0 - t1*t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
    modulus = abs(reduce(gcd, zeroes))
    return modulus

def determine_lcg_parameters(states):
    assert type(states) == list and len(states) >= 5
    for i in states:
        assert type(i) == int

    m = _determine_modulus(states)
    a = _determine_multiplier(states, m)
    c = _determine_increment(states, m, a)
    return (m, a, c)

def distinguish_lcg_rand(rand_values):
    m, a, c = determine_lcg_parameters(rand_values)
    
    gen = LCG(rand_values[0], a, c, m)
    
    all = 0
    correct = 0
    for i in range(1, len(rand_values)):
        all += 1
        if gen.next() == rand_values[i]:
            correct += 1
    
    print(f'Correct:  {correct}/{all}\n')
    if correct == all:
        print('LCG')
    else:
        print('NOT LCG')


if __name__ == '__main__':
    print("Linear congruential generator:")
    gen = LCG(1)
    rand_values = [gen.next() for i in range(0, 1001)]

    distinguish_lcg_rand(rand_values)

    print("\nPython's random:")
    r = random._random.Random(1)
    rand_values2 = [r.getrandbits(31) for i in range(0, len(rand_values))]

    distinguish_lcg_rand(rand_values2)    
