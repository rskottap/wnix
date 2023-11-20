__all__ = [
    'Grep',
    'grep',
    'greps',
]

import assure
import embd

SIMILARITY_DEFINITIONS = [
    'a @ b',
    'a @ b(a)',
    'a @ b(b)',
    'a(a) @ b',
    'a(a) @ b(a)',
    'a(a) @ b(b)',
    'a(b) @ b',
    'a(b) @ b(a)',
    'a(b) @ b(b)',
]

class Grep:

    @classmethod
    def all(cls, queries, keys, *, n=None):
        """ Evaluate possible definitions of grep interactively
            by varying the definition of similarity """
        return [cls(queries, keys, n=n, sims=sims) for sims in cls.sims()]

    @classmethod
    def sims(cls):
        return SIMILARITY_DEFINITIONS

    def __init__(self, queries, keys, *, n=1, sims='a @ b'):
        q = embd.promote(queries)
        k = embd.promote(keys)
        if sims not in SIMILARITY_DEFINITIONS:
            raise ValueError(f"sims must be one of: {self.sims()}")
        s = (lambda a,b: eval(sims))(q,k)
        import numpy as np
        i = np.argsort(-s)
        g = 0*s
        g.iloc[:, :] = s.columns.values[i]
        g.columns = list(range(1, len(g.columns)+1))
        g.columns.name = sims
        g = g.iloc[:, 0:n]

        # attributes
        self.queries = queries
        self.keys = keys
        self.q = q
        self.k = k
        self.s = s
        self.i = i
        self.g = g

    def __repr__(self):
        return repr(self.g)

    def __getitem__(self, n):
        return self.g[n]

    def csv(self, n=1):
        import pandas as pd
        g = self.g
        g = g.iloc[:, 0:n]
        q = g.index.tolist()
        k = g.to_csv(index=False, header=False)
        d = pd.DataFrame(q, index=k.splitlines())
        o = d.to_csv(index=True,header=False,sep=':').strip()
        return o

    def tolist(self):
        return self.g.values.ravel().tolist()

    def intersect(self, s):
        return set(self.tolist()) & set(s)

grep = Grep
greps = Grep.all
