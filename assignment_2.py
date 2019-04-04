from copy import deepcopy

class Literal:
    #name and sign of the literal, where default sign is True
    def __init__(self, name, sign = True):
        self.name = name
        self.sign = sign
    
    def __neg__(self):
        #"The class should also overload the __neg__(self,other) 
        # method to allow negative literals to be defined 
        #in clauses" (instructions)"
        return Literal(self.name, not self.sign)
    
    def __eq__(self, other):
        #"You may wish to put literals into a set regardless of their 
        # sign and not treat two literals with the same name, but 
        # different signs, as distinct" (hint)
        return self.name == other.name
    
    def __hash__(self):
        #hash function for retrieving
        return hash(self.name)
    
    def __str__(self):
        #print string name
        return self.name
    
    def __repr__(self):
        #print representation of literal
        return str(self)

def DPLL_Satisfiable(KB):
    
    #"the set of clauses in the CNF representation of s" (Fig7.17)
    clauses = KB
    
    #"a list of the proposition symbols in s" (Fig7.17)
    symbols = set()
    
    #represent the symbols (no duplicates, all signs are True)
    for clause in clauses:
        for literal in clause:
            lit = literal
            lit.sign = True
            symbols.add(lit)
    
    def DPLL(clauses, symbols, model):
        
        #modified clauses stored in new_clauses
        new_clauses = deepcopy(clauses)

        #"you could save the model using a global variable" (hint)
        global the_model
        the_model = {}
        
        #modify the clauses
        for clause in new_clauses:
            #a dump for deleting False literals later
            dump = set()
            for literal in clause:
                #if a model name matches with one of the literal names
                if literal.name in model:
                    #"A clause is true as soon as any of its 
                    # literals are true" (Fig7.17)
                    if literal.sign == model[literal.name]:
                        clause.clear()
                        clause.add(Tr)
                        break
                    elif len(clause) > 1:
                        dump.add(literal)
                    else:
                        return False
            #"A clause with any literals false can be replaced by 
            # a clause with those literals removed" (hint)
            clause.difference_update(dump)
        
        #"if every clause in clauses is true in model then return true" (Fig7.17)
        if all([Tr in i for i in new_clauses]):
            the_model = model
            return True

        #"if some clause in clauses is false in model then return false" (Fig7.17)
        if any([Fl in i for i in new_clauses]):
            return False
        
        #if there are still symbols left, keep running the recursion
        if len(symbols) > 0:
            
            #"choose an arbitrary un-assigned literal" (instructions)
            p = symbols.pop()
            
            #"assign both true and false values to it" (instructions)
            p_true = deepcopy(model)
            p_true[p.name] = True
            
            p_false = deepcopy(model)
            p_false[p.name] = False
            
            #"return DPLL(clauses, rest, model U {P=true}) or 
            # DPLL(clauses, rest, model U {P=false})" (Fig.7.17)
            return DPLL(deepcopy(clauses), deepcopy(symbols), p_true) or\
        DPLL(deepcopy(clauses), deepcopy(symbols), p_false)

        #terminate recursion since not satisfiable
        return False
    
    #run the DPLL
    sat = DPLL(KB, symbols, {})
    
    #if DPLL output is satisfiable
    if sat == True:
        for clause in KB:
            for literal in clause:
                if literal.name not in the_model:
                    #if the literal was not in the final output 
                    # model, tag label "Free"
                    the_model[literal.name] = 'Free'
                else:
                    the_model[literal.name] = str(the_model[literal.name])
    
    #"additional output to the specification in Russell & Norvig"
    #"satisfiable -- a boolean value indicating whether or not the KB is satisfiable"
    #"model - a python dictionary that has a Literal as the key and the value"
    #(instructions)
    return sat, the_model


#Defining the literals, including "True" and "False"
A = Literal('A')
B = Literal('B')
C = Literal('C')
D = Literal('D')
E = Literal('E')
F = Literal('F')
Tr = Literal('True')
Fl = Literal('False', False)

#KB given from Exercise 7.20 
KB = [{-A, B, E}, {-B, A}, {-E, A}, {-E, D}, 
      {-C, -F, -B}, {-E, B}, {-B, F}, {-B, C}]


#Run the code
DPLL_Satisfiable(KB)
