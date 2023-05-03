import random


def Resolution(A, B):
    A = String_to_posneg(A)
    B = String_to_posneg(B)
    """
    Returns the resolvent of clauses A and B, or False if the resolvent is a tautology or empty.
    """
    if set(A['p']).intersection(set(B['n'])) == set() and set(A['n']).intersection(set(B['p'])) == set():
        return False
    if set(A['p']).intersection(set(B['n'])) != set():
        a = random.choice(list(set(A['p']).intersection(set(B['n']))))
        A['p'].remove(a)
        B['n'].remove(a)
    else:
        a = random.choice(list(set(A['n']).intersection(set(B['p']))))
        A['n'].remove(a)
        B['p'].remove(a)
    C = {'p': A['p'].union(B['p']), 'n': A['n'].union(B['n'])}
    if C['p'].intersection(C['n']) != set():
        return False
    C = Remove_duplicates(C)
    return C


def Remove_duplicates(C):
    """
    Returns the clause C with duplicates removed.
    """
    return {'p': set(C['p']), 'n': set(C['n'])}


def String_to_posneg(clause):
    # ex. -a V b => p: {b}, n{a}
    # pos if not start with ¬
    # neg if start with ¬
    # literals with the lenght 1
    clausarray = clause.split(" ")

    res = {'p': {}, 'n': {}}
    pos = set()
    neg = set()
    for e in clausarray:
        if e.startswith('-'):
            neg.add(e[1:])
        elif not e.startswith('-') and e != 'V':
            pos.add(e)

    res = {'p': pos, 'n': neg}
    return res


def posneg_to_string(clause):
    pos_literals = clause['p']
    neg_literals = clause['n']
    literals = []

    for literal in sorted(pos_literals):
        literals.append(literal)
    for literal in sorted(neg_literals):
        literals.append("-" + literal)

    return " V ".join(literals)


def Union_sets(newSet, S):
    C = {'p': S['p'].union(newSet['p']), 'n': S['n'].union(newSet['n'])}
    return C


def Solver(KB):
    while True:
        S = set()
        KB_prime = KB.copy()
        for A in KB:
            for B in KB:
                C = Resolution(A, B)
                if C != False:
                    S.add(posneg_to_string(C))
        if not S:
            return KB

        KB = Incorporate(S, KB)

        if KB == KB_prime:
            return KB
            


def Incorporate(S, KB):
    for A in S:
        KB = Incorporate_clause(A, KB)
    return KB


def Incorporate_clause(A, KB):
    A = String_to_posneg(A)
    for B in KB:
        tempB = B
        B = String_to_posneg(B)
        if set(B['p']).issubset(set(A['p'])) and set(B['n']).issubset(set(A['n'])):
            continue
        
        
        if set(A['p']).issubset(set(B['p'])) and set(A['n']).issubset(set(B['n'])):
            KB.remove(tempB)
            if foundDup(posneg_to_string(A),KB):
                KB.append(posneg_to_string(A))
            
            

    
   
    return KB

def foundDup(A,KB):
    A = String_to_posneg(A)
    for B in KB:
        B = String_to_posneg(B)
        if set(B['p']) == set(A['p']) and set(B['n']) == set(A['n']):
            return False

    return True



KB = ["-sun V -money V ice", "-money V ice V movie", "-movie V money","-movie V -ice", "movie", "sun V money V cry"]
KB = ["-b2 V -b1", "-b3 V -b2", "-b3 V -b1", "-b3 V b2 V -b1", "-b3 V -b1 V -b2", "b1 V -b3 V -b2", "-b2 V -b1 V b3", "b1 V b2 V b3", "b1", "-b2 V b1", "b1 V b2"]
ans = Solver(KB)
#debug = Incorporate({'-sun', 'movie V -money', 'ice V movie'},['-money V ice V movie', 'movie', 'money', '-ice', 'ice V -sun', '-sun'])
print(ans)
#print(debug)
# Ice ∨ ¬Money ∨ ¬Sun
#