import networkx as nx
import matplotlib.pyplot as plt
import itertools

class Node:
    def __init__(self, id:int, fn:str, args:list, find:int, ccpar:set):
        self.id = id 
        self.fn = fn
        self.args = args
        self.find = find
        self.ccpar = ccpar

class DAG:
    def __init__(self):
        self.nodes = []
        self.equalities = []
        self.inequalities = []
        self.forbidden_list = set()

    def NODE(self, node_id:int):
        for node in self.nodes:
            if node.id == node_id:
                return node
        print('Node not found')

    def FIND(self, node_id:int):
        node = self.NODE(node_id)
        if node.find == node_id: return node_id
        return self.FIND(node.find)

    ## union is done only on the node with larger ccpar
    def UNION(self, n1:int, n2:int):
        n1 = self.NODE(self.FIND(n1))
        n2 = self.NODE(self.FIND(n2))
        if len(n1.ccpar) > len(n2.ccpar):
            n1.find = n2.find
            n2.ccpar = n1.ccpar.union(n2.ccpar)
            n1.ccpar = set()
        else:
            n2.find = n1.find
            n1.ccpar = n2.ccpar.union(n1.ccpar)
            n2.ccpar = set()

    def CCPAR(self, node_id:int):
        return self.NODE(self.FIND(node_id)).ccpar
    
    def CONGRUENT(self, node_id1:int, node_id2:int):
        n1 = self.NODE(node_id1)
        n2 = self.NODE(node_id2)
        res = True if (n1.fn == n2.fn and len(n1.args) == len(n2.args) and [self.FIND(n1.args[i]) == self.FIND(n2.args[i]) for i in range(len(n1.args))]) else False
        return res
    
    def MERGE(self, node_id1:int, node_id2:int):
        if self.FIND(node_id1) != self.FIND(node_id2):
            p1 = self.CCPAR(node_id1)
            p2 = self.CCPAR(node_id2)
            self.UNION(node_id1, node_id2)
            for t1, t2 in list(itertools.product(p1, p2)):
                if self.FIND(t1) != self.FIND(t2) and self.CONGRUENT(t1, t1):
                    self.MERGE(t1, t2)
    
    def add_forbidden_list(self, forbidden_list:set):
        for fl in forbidden_list:
            self.forbidden_list.add(fl)

    def add_equalities(self, equalities:list):
        for eq in equalities:
            self.equalities.append(eq)

    def add_inequalities(self, inequalities:list):
        for ineq in inequalities:
            self.inequalities.append(ineq)

    def add_node(self, node:Node):
        self.nodes.append(node)
    
    def set_ccpar(self):
        for node in self.nodes:
            self.link_nodes(node.id)
            pass

    def link_nodes(self, id):
        father_args = self.NODE(id).args
        for arg in father_args:
            target = self.NODE(arg)
            target.ccpar.add(id)

    def print_node(self, node_id:int):
        node = self.NODE(node_id)
        print(f"Node \tid: {node.id}\n\tfn: {node.fn}\n\targs: {node.args}\n\tfind: {node.find}\n\tccpar: {node.ccpar}\n")
    
    def print_nodes(self):
        for node in self.nodes:
            self.print_node(node.id)
    
    def node_string(self, id):
        target = self.NODE(id)
        if len(target.args) == 0:
            return f"{target.fn}"
        else:
            args_str = ', '.join(self.node_string(arg) for arg in target.args)
            return f"{target.fn} ({args_str})"
    
    def solve(self):
        for eq in self.equalities:
            val1, val2 = eq[0], eq[1]
            if (val1, val2) in self.forbidden_list: return "UNSAT -> forbidden list"
            if (val2, val1) in self.forbidden_list: return "UNSAT -> forbidden list"
            self.MERGE(eq[0], eq[1])
        for ineq in self.inequalities:
            val1, val2 = self.FIND(ineq[0]), self.FIND(ineq[1])
            if val1 == val2:
                return "UNSAT"
        return "SAT"

    def visualize_dag(self, find=False):
        G = nx.DiGraph()

        for node in self.nodes:
            G.add_node(node)#, label=f"id: {node.id}, fn: {node.fn}")

        for node in self.nodes:
            for child in node.ccpar:
                G.add_edge(self.NODE(child), node)

        labels = {node: f"id: {node.id}, fn: {node.fn}" for node in self.nodes}

       
        pos = nx.spring_layout(G)
        pos = {node: (x, -y) for node, (x, y) in pos.items()}

        if find:
            dotted_edges = []
            for node in self.nodes:
                if not node.id == node.find:
                    dotted_edges.append((node, self.NODE(node.find)))
            nx.draw_networkx_edges(G, pos, edgelist=dotted_edges, style="dotted", connectionstyle="arc,rad=0.3")

        nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color="lightblue", font_size=10, font_color="black", edge_color="gray", arrows=True)
        plt.show()