import copy
def is_terminal(x):
    if x.isupper():
        return False
    return True
def init_first(elements):
    fset={}
    for e in elements:
        fset[e]=set()
        if is_terminal(e):
            fset[e]=e
    return fset
def init_follow(elements):
    fset={}
    for e in elements:
        if e.isupper():
            fset[e]=set()
    return fset
def construct_first(elements,expression):
    origin_fset=init_first(elements)
    new_fset=origin_fset
    while True:
        origin_fset =copy.deepcopy(new_fset)
        for lhs in expression:
            rhs_li=expression[lhs]
            for rhs in rhs_li:
                if len(rhs)>0:
                    if is_terminal(rhs[0]):
                        new_fset[lhs]=new_fset[lhs].union(rhs[0])
                    else:
                        new_fset[lhs]=new_fset[lhs].union(new_fset[rhs[0]])
                    if 'e' in new_fset[rhs[0]] and len(rhs[1:])>0:
                        expression[lhs]+=rhs[1:],
        if origin_fset==new_fset:
            break
    return new_fset
def first(expr,first_set):
    fset=set()
    if is_terminal(expr[0]) and expr[0]!='e':
        fset=fset.union(expr[0])
    else:
        fset=fset.union(first_set[expr[0]])
        if 'e' in first_set[expr[0]] and len(expr[1:])>0:
            fset=fset.union(first(expr[1:],first_set))
    return fset

def construct_follow(elements,expression,first_set):
    origin_fset=init_follow(elements)
    origin_fset['E']={'#'}
    new_fset=origin_fset
    while True:
        origin_fset =copy.deepcopy(new_fset)
        for lhs in expression:
            rhs_li=expression[lhs]
            for rhs in rhs_li:
                for i in range(len(list(rhs))-1):
                    if not is_terminal(rhs[i]):
                        new_fset[rhs[i]]=new_fset[rhs[i]].union(first_set[rhs[i+1]])-{'e'}
                        if first_set[rhs[i+1]]=={'e'}:
                            new_fset[rhs[i]]=new_fset[rhs[i]].union(new_fset[lhs])-{'e'}
                if not is_terminal(rhs[-1]):
                    new_fset[rhs[-1]]=new_fset[rhs[-1]].union(new_fset[lhs])-{'e'}
        if origin_fset==new_fset:
            break
        return new_fset

def construct_ll1_table(first_set,follow_set,origin_expression):
    ll1_table={}
    for lhs in origin_expression:
        ll1_table[lhs]={}
    print(origin_expression)
    for lhs in origin_expression:
        for rhs in origin_expression[lhs]:
            
            first_expr=first(rhs,first_set)
            for a in first_expr:
                if True:
                    ll1_table[lhs][a]=lhs+'->'+rhs
            if 'e' in first_expr:
                follow_a=''.join(list(follow_set[lhs]))
                alpha_follow_a=rhs+follow_a
                print(alpha_follow_a,lhs)
                first_expb=first(alpha_follow_a,first_set)
                print(first_expb)
                for b in first_expb:
                    if True:
                        ll1_table[lhs][b]=lhs+'->'+rhs
    print(ll1_table)

def main():
    lines='''E->TH
H->+TH
H->-TH
H->e
T->FK
K->*FK
K->/FK
K->e
F->-F
F->1
F->(E)'''

    elements=set()
    expression={}
    lines=lines.split('\n')
    for line in lines:
        elements=elements.union(list(line.replace("->",'')))
        line=line.split('->')
        if line[0] not in expression:
            expression[line[0]]=[]
        expression[line[0]]+=line[1],
    origin_expression=copy.deepcopy(expression)
    first_set=construct_first(elements,expression)
    print(origin_expression)
    follow_set=construct_follow(elements,expression,first_set)
    print(''.join(list(follow_set['E'])))
    construct_ll1_table(first_set,follow_set,origin_expression)
main()