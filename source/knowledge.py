from pysat.solvers import Glucose3
import copy

class knowledgeBase:
    def __init__(self):
        self.KB = []
    
    @staticmethod
    def standardize_clause(clause):
        return sorted(list(set(clause)))
    
    def add_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause not in self.KB:
            self.KB.append(clause)
    
    def del_clause(self, clause):
        clause = self.standardize_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)
    
    def infer(self, not_alpha):
        glu = Glucose3()
        clause_list = copy.deepcopy(self.KB)
        neg_alpha = not_alpha
        for it in clause_list:
            glu.add_clause(it)
        for it in neg_alpha:
            glu.add_clause(it)
        sol = glu.solve()
        if sol:
            return False
        return True