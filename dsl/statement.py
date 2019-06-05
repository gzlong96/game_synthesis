


class Statement:
    """
       Attributes:
           input_types (tuple): tuple of Type (INT,LIST) representing inputs
           stmts (tuple): tuple of statements. each statement is pair of function, tuple of mixed type representing arguments
           types (tuple): tuple of Type for all variables
           prefix (str): prefix string that completely describes program
       """

    def __init__(self, stmts):
        self.stmts = tuple(stmts)
        self.prefix = self.toprefix()
        self._hash = hash(self.prefix)

    def functions(self):
        for func, args in self.stmts:
            yield func
            for arg in args:
                if isinstance(arg, Function):
                    yield arg

    def tokens(self):
        tokens = []
        for func, args in self.stmts:
            tokens.append(func)
            for arg in args:
                tokens.append(arg)

    def toprefix(self):
        toks = []
        for f, inputs in self.stmts:
            tok = ','.join(map(str, [f] + list(inputs)))
            toks.append(tok)

        return '|'.join(toks)

    def __str__(self):
        return self.prefix

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        # if len(self.types) < len(other.types):
        #    return True
        return self.prefix < other.prefix

    @classmethod
    def parse(cls, prefix):
        input_types = []
        stmts = []

        def get_stmt(term):
            stmt = []
            for inner in term.split(','):
                if inner.isdigit():
                    stmt.append(int(inner))
                else:
                    stmt.append(NAME2FUNC[inner])
            return stmt[0], tuple(stmt[1:])

        for tok in prefix.split('|'):
            if ',' in tok:
                stmts.append(get_stmt(tok))
            else:
                if tok == INT.name:
                    typ = INT
                elif tok == LIST.name:
                    typ = LIST
                else:
                    raise ValueError('invalid input type {}'.format(tok))
                input_types.append(typ)

        return Program(input_types, tuple(stmts))

    def __call__(self, *inputs):
        if not self.stmts:
            return NULLVALUE
        vals = list(inputs)
        for f, inputs in self.stmts:
            args = []
            for input in inputs:
                if isinstance(input, int):
                    args.append(vals[input])
                else:
                    args.append(input)
            val = f(*args)
            vals.append(val)
        return vals[-1]