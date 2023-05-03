import random

def resolution(A, B):
    # Check for complementary literals
    if A['pos'].intersection(B['neg']) or A['neg'].intersection(B['pos']):
        return False

    # Find the random literal to resolve
    if A['pos'].intersection(B['neg']):
        a = random.choice(list(A['pos'].intersection(B['neg'])))
        A['pos'].remove(a)
        B['neg'].remove(a)
    else:
        a = random.choice(list(A['neg'].intersection(B['pos'])))
        A['neg'].remove(a)
        B['pos'].remove(a)

    # Combine the remaining literals
    C = {'pos': A['pos'].union(B['pos']), 'neg': A['neg'].union(B['neg'])}

    # Check for a tautology
    if C['pos'].intersection(C['neg']):
        return False

    # Remove duplicate literals
    C['pos'] = set([lit for lit in C['pos'] if -lit not in C['neg']])
    C['neg'] = set([lit for lit in C['neg'] if -lit not in C['pos']])

    return C

def solver(KB):
    while True:
        S = set()
        KB_prime = set(KB)
        for A in KB:
            for B in KB:
                if A != B:
                    C = resolution(A, B)
                    if C:
                        S.add(frozenset(C.items()))

        if not S:
            return KB

        KB = incorporate(S, KB)
        if KB == KB_prime:
            return KB

def incorporate(S, KB):
    for A in S:
        KB = incorporate_clause(dict(A), KB)
    return KB

def incorporate_clause(A, KB):
    for B in KB:
        if A.items() <= B.items():
            return KB
    KB = set([B for B in KB if B.items() < A.items()])
    KB.add(frozenset(A.items()))
    return KB

# Example usage
KB = [
    {'neg': {1, 2}, 'pos': {3}},
    {'neg': {2}, 'pos': {3, 4}},
    {'neg': {3}, 'pos': {2}},
    {'neg': {3, 4}, 'pos': {1}},
    {'pos': {4}},
    {'neg': {1}, 'pos': {2, 4}}
]

KB = solver(KB)
print(KB)
