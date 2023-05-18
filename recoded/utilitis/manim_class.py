from manim import *
import networkx as nx
from manim.utils.file_ops import open_file as open_media_file 
import cv2


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

def run_manim(cropped, graph, shortest_path, manim, side_by_side, opencv):
    # manim
    if (manim != 0):
        scene = hello(graph, manim, shortest_path)
        scene.render()
        if (manim == 1):
            open_media_file('media\images\hello_ManimCE_v0.17.2.png')
        if (manim == 2):
            open_media_file("media\\videos\\1080p60\hello.mp4")


    if (side_by_side and opencv == 0 and manim == 0):
        cv2.imshow("cropped", cv2.resize(cropped, (0, 0), fx=1, fy=1))
        scene = hello(graph, 1,shortest_path)
        scene.render()
        open_media_file('media\images\hello_ManimCE_v0.17.2.png')