import copy
class AST:
    pass
class OP(AST):
    def __init__(self,val,left=None,right=None):
        self.val=val
        self.left=left
        self.right=right

class NUM(AST):
    def __init__(self,val):
        self.val=val

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
    return ll1_table

class Tree(object):
    "Generic tree node."
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

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
F->(E)
F->1'''
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
    # print(origin_expression)
    follow_set=construct_follow(elements,expression,first_set)
    # print(''.join(list(follow_set['E'])))
    ll1_table=construct_ll1_table(first_set,follow_set,origin_expression)
    # ll1_table["H"][")"] = "H->e"
    # ll1_table["K"][")"] = "K->e"
    # ll1_table["K"]["#"] = "K->e"
    print(ll1_table)
    stack=["E"]
    expr="(1+1)*(1+1)#"
    i=0
    st=""
    treestack=[Tree("E")]
    root=treestack[0]
    while len(stack)>0:
        token= expr[i]
        symbol=stack[-1]
        stack.pop()
        node=treestack[-1]
        treestack.pop()
        if not symbol.isupper():
            symbol=stack[-1]
            stack.pop()
            treestack.pop()
        
        st+=symbol
        try:
            e=ll1_table[symbol][token]
        except :
            e=ll1_table[symbol]["e"]
        e=e.split("->")[1]
        
        if e[0]==expr[i]:
            i+=1
            stack+=list(e)[::-1]
            for x in list(e):
                node.children.append(Tree(x))
            
            treestack+=node.children
            # st+="("+e[0]+")"
        elif e!='e':
            stack+=list(e)[::-1]
            for x in list(e):
                node.children.append(Tree(x))
            
            treestack+=node.children
            print(node.children)
            # print(stack,e)
        elif e=='e':
            print(symbol,expr[i])
            if expr[i]==')':
                i+=1
    s=[root]

    def preorder(node):
        t=[]
        if not node:
            return node
        
        if len(node.children)>0:
            for x in node.children:
                
                temp=preorder(x)
                t+=temp
        t.append(node.name)        
        return t
    t=preorder(root)
    print(t)
    as_line=[i for i in t if not i.isupper() and i!="(" and i!=")"]
    print(as_line)
    stack=as_line[::-1]
    root=None
    head=None
    treestack=[]
    while len(stack)>0:
        s=stack[-1]
        stack.pop()
        node=OP(s)
        if root==None:
            
            root=node
            head=node
            treestack.append(node)
        else:
            if not root.left:
                root.left=node
            if not root.right:
                root.right=node
            else:
                root=treestack[-1]
                treestack.pop()
        if node.val in ["+","-","*","/"]:
            root =node
            treestack.append(node)
    
    def binpreorder(node):
        t=[]
        if not node:
            return node
         
        if node.left:
            temp = binpreorder(node.left)
            t+=temp
        t.append(node.val)
        if node.right:
            temp = binpreorder(node.right)
            t+=temp
               
        return t
    a= binpreorder(head)
    print(a)

    




main()