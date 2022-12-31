from manim import *
import networkx as nx
from manim.utils.file_ops import open_file as open_media_file 
class hello(Scene):
    def __init__(self,d):
        super().__init__()
        self.d =d

    def construct(self): 
        g = nx.Graph(self.d)
        lt={}
        for i in range (len(list(g.nodes))):
            node= list(g.nodes)[i]
            lt[node]=[node[0]-3,6-node[1]-3,0]
        graph = Graph(list(g.nodes), list(g.edges),layout=lt, vertex_config={"fill_color": BLUE_C})
        self.add(graph)