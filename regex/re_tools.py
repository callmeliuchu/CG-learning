
class DirectedGraph:

    def __init__(self,n):
        self.n = n
        self.edges = [[] for _ in range(n)]

    def add_edge(self,u,v):
        self.edges[u].append(v)

    def v_count(self):
        return self.n


class DirectedDFS:

    def __init__(self,graph,v):
        self.graph = graph
        self.mark = [False] * graph.n
        if isinstance(v,int):
            self.dfs(v)
        elif isinstance(v,list):
            for q in v:
                if not self.marked(q):
                    self.dfs(q)

    def dfs(self,u):
        self.mark[u] = True
        for v in self.graph.edges[u]:
            if not self.mark[v]:
                self.dfs(v)

    def marked(self,u):
        return self.mark[u]


class NFA:

    def __init__(self,regex):
        ops = []
        self.m = len(regex)
        self.regex = regex
        self.graph = DirectedGraph(self.m+1)
        for i in range(self.m):
            lp = i
            if regex[i] == '(' or regex[i] == '|':
                ops.append(i)
            elif regex[i] == ')':
                or_op = ops.pop(-1)
                if regex[or_op] == '|':
                    lp = ops.pop(-1)
                    self.graph.add_edge(lp,or_op+1)
                    self.graph.add_edge(or_op,i)
                else:
                    lp = or_op
            if i < self.m - 1 and regex[i+1] == '*':
                self.graph.add_edge(lp,i+1)
                self.graph.add_edge(i+1,lp)
            if regex[i] == '(' or regex[i] == '*' or regex[i] == ')':
                self.graph.add_edge(i,i+1)

    def recognizes(self,txt):
        pc = []
        dfs = DirectedDFS(self.graph,0)
        for v in range(self.graph.v_count()):
            if dfs.marked(v):
                pc.append(v)
        for c in txt:
            match = []
            for v in pc:
                if v < self.m:
                    if self.regex[v] == c or self.regex[v] == '.':
                        match.append(v+1)
            pc = []
            dfs = DirectedDFS(self.graph,match)
            for v in range(self.graph.v_count()):
                if dfs.marked(v):
                    pc.append(v)
        for v in pc:
            if v == self.m:
                return True
        return False


regex = '(.*hs.*)'

txt = 'cdecehshsbsdjcked'
nfa = NFA(regex)
if nfa.recognizes(txt):
    print(txt)
