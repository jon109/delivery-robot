from manim import *
import networkx as nx
from manim.utils.file_ops import open_file as open_media_file 

class hello(Scene):
    def __init__(self,d,manim,sol):
        super().__init__()
        self.sol = sol
        self.d =d
        self.manim=manim

    def construct(self): 
        g = nx.Graph(self.d)
        lt={}
        for i in range (len(list(g.nodes))):
            node= list(g.nodes)[i]
            lt[node]=[node[0]-3,6-node[1]-3,0]
        graph = Graph(list(g.nodes), list(g.edges),layout=lt, vertex_config={"fill_color": BLUE_C})
        if (self.manim==1):
            self.add(graph)
        if (self.manim==2):
            self.play(Create(graph))
            solution=self.sol
            for i in range (len(solution)-1):
                self.play(Create(Line(lt[solution[i]],lt[solution[i+1]],color=YELLOW_D)))