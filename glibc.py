import random


class GlibcRand:
    """
    Glibc random() implementation.
    """
    mod1 = 2**31 - 1
    mod2 = 2**32
    
    def __init__(self, seed):
        assert type(seed) == int
        self.state = [seed,]

        for i in range(1,31):
            self.state.append( (16807 * self.state[-1]) % self.mod1 )
        
        for i in range(31, 34):
            self.state.append( self.state[-31] )
        
        for i in range(34, 344):
            self.state.append( (self.state[-31] + self.state[-3]) % self.mod2 )
        
        self.state = self.state[-31:]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next()
    
    def next(self):
        self.state.append( (self.state[-31] + self.state[-3]) % self.mod2 )
        self.state = self.state[-31:]
        return self.state[-1] >> 1


def glibc_guess_next(state):
    """
    Guess next glibc's random() value based on previous values.
    State should be list of 31+ integers 
    """
    assert type(state) == list and len(state) >= 31
    for i in state:
        assert type(i) == int

    return (state[-31] + state[-3]) % 2**31

def test_glibc_guess_n(generator, n):
    """
    Test glibc_guess_next function and GlibcRand generator.
    correct + almost_correct should be equal to n.
    """
    assert type(generator) == GlibcRand
    assert n >= 1
    state = [generator.next() for i in range(0, 31)]
    correct = 0
    almost_correct = 0
    for i in range(0, n):
        next = generator.next()
        if next == glibc_guess_next(state):
            correct += 1
        elif abs(next - glibc_guess_next(state)) == 1:
            almost_correct += 1
        state.append(next)
        state[-31:]
    print(f'Correct:  {correct}/{n}')
    print(f'Almost Correct:  {almost_correct}/{n}')
    print('\n\n')
    return state

def distinguish_glibc_rand(rand_values):
    assert type(rand_values) == list and len(rand_values) > 31
    for i in rand_values:
        assert type(i) == int

    all = 0
    correct = 0
    almost_correct = 0
    for i in range(0, len(rand_values)-31):
        guess = glibc_guess_next(rand_values[i:i+31])
        next = rand_values[i+31]
        
        all += 1
        if guess == next:
            correct += 1
        elif abs(guess-next) == 1:
            almost_correct += 1
    
    print(f'Correct:  {correct}/{all}')
    print(f'Almost Correct:  {almost_correct}/{all}\n')
    if correct + almost_correct == all:
        print('GLIBC RANDOM')
    else:
        print('NOT GLIBC RANDOM')

if __name__ == '__main__':
    print("Glibc's random:")
    gen = GlibcRand(1)
    rand_values = [gen.next() for i in range(0, 1031)]
    distinguish_glibc_rand(rand_values)

    print("\nPython's random:")
    r = random._random.Random(1)
    rand_values2 = [r.getrandbits(31) for i in range(0, len(rand_values))]
    distinguish_glibc_rand(rand_values2)
