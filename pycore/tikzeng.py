import os
from typing import Sequence

def to_head( projectpath):
    pathlayers = os.path.join( projectpath, 'layers/' ).replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone}
\usepackage{xcolor}
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image 
"""

def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}   
\def\SumColor{rgb:blue,5;green,15}
"""

def to_begin():
    return r"""
\newcommand{\mymidarrow}{\tikz \draw[-Stealth,line width=0.2mm,draw=\edgecolor,opacity=1] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}

\tikzstyle{connection}=[thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=1]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
\tikzstyle{mynode}=[inner sep=0pt,minimum size=0mm]

\def\skipshift{6.5}
"""

# utils
# =====
def new_color(name, color):
    return r"""
\definecolor{""" + name + r"""}{HTML}{""" + color + r"""}
"""

def insert_canvas_image(file_name, node, width, height):
    return r"""
\node[canvas is zy plane at x=0] (temp) at """+ node +""" {\includegraphics[width="""+ str(width) +"""cm,height="""+ str(height) +"""cm]{"""+ file_name +"""}};
"""

def node(name, coords, text=""):
    return r"""
\node ("""+ name +""") at """+ coords +""" {"""+ text +"""};
"""

def gen_nodes(n_nodes, xspace=3, zoffset=0):
    """
    Generate a set of consecutive `n_nodes` with
    a distance between them of `xspace`. Use
    `zoffset` to set the z-coord of all gen nodes.
    """
    nodex = [*range(n_nodes)]
    if isinstance(xspace, int):
        return {chr(ord('a') + i): f"({xspace*i},0,{str(zoffset)}+\skipshift)" for i in nodex}
    elif isinstance(xspace, Sequence):
        return dict(
            (chr(ord('a') + i), f"({xspace[i]+sum(xspace[:i])},0,{str(zoffset)}+\skipshift)")
            if i >= 1 else
            (chr(ord('a') + i), f"({xspace[i]},0,{str(zoffset)}+\skipshift)")
            for i in nodex)
    else:
        raise TypeError(f"`xspace` must be either int or Sequence, not {type(xspace)}")

def apply_offset(offset: float, coord: str, nodes: dict):
    coord_index = {'x':0, 'y':1, 'z':2}[coord]
    for k,v in nodes.items():
        pos_list = v.strip('()').split(',')
        pos_list[coord_index] = str(float(pos_list[coord_index].replace('+\skipshift', '')) + offset) + "+\skipshift"
        nodes[k] = '(' + ','.join(pos_list) + ')'

    return nodes

def get_width(layer):
    width_str = "width="
    i0 = layer.index(width_str)
    i1 = layer[i0:].index(",") + i0

    return float(layer[i0+len(width_str):i1])

def new_node_obj(name, at, style="mynode"):
    return r"""
\node["""+ str(style) +"""] ("""+ str(name) +""") at """+ str(at) +""" {};
"""

def get_node(nodes, idx):
    ld = list(nodes.items())
    return {ld[idx][0]:ld[idx][1]}

# layers definition
# =================
def to_input( pathfile, to='(-3,0,0)', width=8, height=8, name="temp"):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
"""

# Dense
def to_Dense(name, size=64, offset="(0,0,0)", to="(0,0,0)", width=2, height=2, depth=34, caption=" ", color="\ConvColor", opacity=.7):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +"""
    {Box={
        name="""   + name         +""",
        caption="""+ caption      +""",
        xlabel={{, }},
        zlabel=""" + str(size)    +r""",
        fill="""   + str(color)  +""",
        height=""" + str(height)  +""",
        width="""  + str(width)   +""",
        depth="""  + str(depth)   +""",
        opacity="""+ str(opacity) +""",
        }
    };
"""

# Conv
def to_Conv(name, s_filter=256, n_filter=64, size=32, offset="(0,0,0)", to="(0,0,0)", width=4, height=25, depth=40, caption=" ", color="\ConvColor", opacity=.7):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name="""    + name          +""",
        caption=""" + caption       +r""",
        xlabel={{"""+ '"' + str(n_filter) +"""@1x"""+ str(s_filter) +"""\", }},
        zlabel="""  + str(size)     +r""",
        fill="""    + str(color)    +""",
        height="""  + str(height)   +""",
        width="""   + str(width)    +""",
        depth="""   + str(depth)    +""",
        opacity=""" + str(opacity)  +""",
        }
    };
"""

# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu(name, s_filter=256, n_filter=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(n_filter[0]) +""", """+ str(n_filter[1]) +""" }},
        zlabel="""+ str(s_filter) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

# Pool
def to_Pool(name, s_pool=8, size=32, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, color="\PoolColor", opacity=.7, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""   + name           +""",
        caption="""+ caption        +r""",
        xlabel={{"1x"""+ str(s_pool) +"""\",}},
        zlabel=""" + str(size)      +r""",
        fill="""   + str(color)     +""",
        opacity="""+ str(opacity)   +""",
        height=""" + str(height)    +""",
        width="""  + str(width)     +""",
        depth="""  + str(depth)     +"""
        }
    };
"""

# unpool4, 
def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+ name +r""",
        caption="""+ caption +r""",
        fill=\UnpoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_ConvRes(name, s_filter=256, n_filter=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filter) + """, }},
        zlabel="""+ str(s_filter) +r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax(name, s_filter=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(s_filter) +""",
        fill=\SoftmaxColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# SoftMax
def to_SoftMax(name, s_filter=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" "):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        xlabel={{" ","dummy"}},
        zlabel="""+ str(s_filter) +""",
        fill=\SoftmaxColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_Sum(name, offset="(0,0,0)", to="(0,0,0)", radius=2.5, opacity=0.6):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Ball={
        name=""" + name +""",
        fill=\SumColor,
        opacity="""+ str(opacity) +""",
        radius="""+ str(radius) +""",
        logo=$+$
        }
    };
"""

def to_connection(of, to):
    return r"""
\draw [connection]  ("""+of+"""-east) -- node {\midarrow} ("""+to+"""-west);
"""

def to_connection_node(of, to):
    return r"""
\draw [connection]  ("""+of+"""-east) -- node {\mymidarrow} """+to+""";
"""

def to_connection_nodes(nodes):
    if len(nodes) <= 1:
        raise ValueError(f"`nodes` must contain more than one node. Now it has {len(nodes)}.")
    
    lines = r"""
\draw [connection] ("""+ nodes[0] +""")"""
    for node in nodes[1:]:
        lines = lines + """ -- node{\mymidarrow} (""" + node +""")"""
    
    return lines + """;
"""


def to_skip(of, to, pos=1.25):
    return r"""
\path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
\path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
\draw [copyconnection]  ("""+of+"""-northeast)  
-- node {\copymidarrow}("""+of+"""-top)
-- node {\copymidarrow}("""+to+"""-top)
-- node {\copymidarrow} ("""+to+"""-north);
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_generate(arch, pathname="file.tex", verbosity=0):
    with open(pathname, "w") as f: 
        for c in arch:
            if verbosity == 1:
                print(c)
            f.write(c)
