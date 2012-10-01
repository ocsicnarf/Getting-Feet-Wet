#! /usr/bin/python

import random
import time
import matplotlib.pyplot as plt
import scipy 

def cycle(list):
    return list[1:] + list[0:1]

def find_combinations(target, a, b, c):
    ''' Pick a number from each list (a, b, c) so their sum is target.
    Returns a list of triples that each sum to target, or None if none exists 
    '''
    if len(a) != len(b) or len(a) != len(c):
        raise Exception('Input lists must have same length')

    # Base case
    if len(a) == 1:
        if a[0] + b[0] + c[0] == target:
            return [(a[0], b[0], c[0])]
        else:
            return None
   
    # Try different permutations of the lists.
    for i in range(len(a)):
        a = cycle(a)
        for j in range(len(b)):
            b = cycle(b)
            
            # If the first combination works, recurse.
            if a[0] + b[0] + c[0] == target:
                rest = find_combinations(target, a[1:], b[1:], c[1:])
                if rest is not None:
                    return [(a[0], b[0], c[0])] + rest             
    
    return None


def generate_puzzle(target, numCombos):
    ''' Generates a new puzzle for a given target sum, with
    numCombos combinations.
    So far, only positive summands are generated.
    '''
    assert target >= 3
    a, b, c = [], [], []
    for i in range(numCombos):
        a.append(random.randint(1, target - 2))
        b.append(random.randint(1, target - a[i] - 1))
        c.append(target - a[i] - b[i]) 
    random.shuffle(a)
    random.shuffle(b)
    random.shuffle(c)
    return a, b, c

if __name__ == '__main__':
    # Baby example
    d = [1,2,3]
    e = [3,1,2]
    f = [1,2,3]
    print 'each triple should sum to 6'
    print find_combinations(6, d, e, f)
    print 

    # The 4th grade homework question 
    a = [33, 42, 72, 54, 10,  6, 18, 66, 48, 25, 80, 39]
    b = [61, 20, 35, 16, 29, 10, 56, 30, 47, 15, 11, 18]
    c = [54, 50,  9,  8, 25, 58, 36, 18, 22, 10, 20, 37]
    target = 99

    answer = find_combinations(target, a, b, c)
    print 'each triple should sum to 99'
    print answer
    print
    print 'if you\'re too lazy to check by hand...'
    print [sum(combo) for combo in answer]
    
    # Baby example, generated and solved
    x, y, z = generate_puzzle(6, 10)
    print find_combinations(6, x, y, z)
    print

    # Check the time complexity empirically
    print '{0}    {1}'.format("Combos", "Avg Time")
    target = 99
    runs = 10
    num_combos = [0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16]
    times = []
    for num in num_combos:
        t = []
        for i in range(runs):
            x, y, z = generate_puzzle(target, num)
            start = time.clock()
            find_combinations(target, x, y, z)
            end = time.clock()
            t.append(end - start)
        times.append(t)
        print '{0:6d}    {1:8f}'.format(num, scipy.mean(t))

    for i in range(len(num_combos)):
        xs = [num_combos[i]] * runs
        ys = times[i]
        plt.scatter(xs, ys, s=30, alpha=0.5)
        plt.scatter(num_combos[i], scipy.mean(times[i]), 
                        c='r', s=50, alpha=0.7, marker ='D')

    plt.xlim(xmin=0, xmax=max(num_combos) + 1)
    plt.semilogy()
    plt.show()





        
    
    

