import random

import numpy as np
import networkx as nx

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 

    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos


    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def make_annotations(pos, font_size=10, font_color='rgb(250,250,250)', M=None):
    annotations = []
    for label, pos in pos.items():
        annotations.append(
            dict(
                text=label, # or replace labels with a different list for the text within the circle
                x=pos[0], y=2*M+pos[1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations

def get_nodes_edges_position(edges, root="total", **kargs):

    G = nx.Graph()
    G.add_edges_from(edges)

    positions = hierarchy_pos(G, root=root, width=10000)
    positions = {key:list(value) for key, value in positions.items()}

    nodes_x = [position[0] for position in positions.values()]
    nodes_y = [position[1] for position in positions.values()]

    M = max(nodes_y)
    edges_x = []
    edges_y = []

    for edge in edges:
        edges_x += [positions[edge[0]][0],positions[edge[1]][0], None]
        edges_y += [10*M+positions[edge[0]][1],10*M+positions[edge[1]][1], None]

    labels = list(positions.keys())
    annotations = make_annotations(positions, M=M)

    return nodes_x, nodes_y, edges_x, edges_y, labels, annotations

