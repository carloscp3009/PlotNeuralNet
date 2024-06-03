
import os

def to_head( projectpath ):
    pathlayers = os.path.join( projectpath, 'layers/' ).replace('\\', '/')
    return r"""
\documentclass[border=0pt, multi, tikz]{standalone} 
\usepackage{import}
\subimport{"""+ pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{calc}
\usetikzlibrary{3d} %for including external image 
"""

def to_cor():
    return r"""
\def\InputColor{rgb:blue,2;green,1;black,0.3}
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,3;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}   
\def\SumColor{rgb:blue,5;green,15}
\def\ConcatColor{rgb:gray,5;white,15}
"""

def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""

# layers definition

# def to_source( pathfile, to='(-3,0,0)', width=8, height=8, name="temp" , straight=False):
#     if straight:
#         return r"""
#     \node[] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
#     """
#     return r"""
# \node[canvas is zy plane at x=0] (""" + name + """) at """+ to +""" {\includegraphics[width="""+ str(width)+"cm"+""",height="""+ str(height)+"cm"+"""]{"""+ pathfile +"""}};
# """
# def to_source(pathfile, to='(-3,0,0)', width=8, height=8, name="temp", straight=False, caption="", caption_size=30):
#     tikz_code = r"""
#     \node[{}] ({}) at {} {{
#         \begin{{tikzpicture}}
#             \node[anchor=south] (image) {{\includegraphics[width={}cm,height={}cm]{{{}}}}};
#             \node[below=of image] {{\fontsize{{{}}}{{1em}}\bfseries {}}};
#         \end{{tikzpicture}}
#     }};
#     """
#     if straight:
#         anchor = ""
#     else:
#         anchor = "canvas is zy plane at x=0"
        
#     return tikz_code.format(anchor, name, to, width, height, pathfile, caption_size, caption)
def to_text(text, to='(0,0,0)', name="textnode", caption_size=12):
    formatted_text = text.replace("\n", r"\\")
    tikz_code = r"""
    \node[{}] ({}) at {} {{\fontsize{{{}}}{{1em}}\selectfont\bfseries {}}};
    """
    return tikz_code.format("", name, to, caption_size, formatted_text)

def to_source(pathfile, to='(-3,0,0)', width=8, height=8, name="temp", straight=False, caption="", caption_size=20):
    tikz_code = r"""
    \node[{}] ({}) at {} {{
        \begin{{tikzpicture}}
            \node[anchor=south] (image) {{\includegraphics[width={}cm,height={}cm]{{{}}}}};
            \node[below=of image, align=center] {{\fontsize{{{}}}{{1em}}\selectfont\bfseries {} }};
        \end{{tikzpicture}}
    }};
    """
    if straight:
        anchor = ""
    else:
        anchor = "canvas is zy plane at x=0"
        
    return tikz_code.format(anchor, name, to, width, height, pathfile, caption_size, caption)



# Conv
def to_input( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\InputColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv
def to_Conv( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv
def to_Box( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " , color="", opacity=0.2):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill="""+ color +""",
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv
def to_ConeBox( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " , color="", opacity=0.2):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {SBox={
        name=""" + name +""",
        caption="""+ caption +r""",
        xlabel={{"""+ str(n_filer) +""", }},
        zlabel="""+ str(s_filer) +""",
        fill="""+ color +""",
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv,Conv,relu
def to_ConvRelu( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40, caption="" ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{"""+ str(n_filer) +""",  }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width) +"""},
        depth="""+ str(depth) +"""
        }
    };
"""

# Conv,Conv,relu
# Bottleneck
def to_ConvConvRelu( name, s_filer=256, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name +""",
        caption="""+ caption +""",
        xlabel={{ """+ str(f'{n_filer[1]}')+""", """+ str(" ") +""" }},
        zlabel="""+ str(s_filer) +""",
        fill=\ConvColor,
        bandfill=\ConvReluColor,
        height="""+ str(height) +""",
        width={ """+ str(width[0]) +""" , """+ str(width[1]) +""" },
        depth="""+ str(depth) +"""
        }
    };
"""

# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {Box={
        name="""+name+""",
        caption="""+ caption +r""",
        fill=\PoolColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
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



def to_ConvRes( name, s_filer=256, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" " ):
    return r"""
\pic[shift={ """+ offset +""" }] at """+ to +""" 
    {RightBandedBox={
        name="""+ name + """,
        caption="""+ caption + """,
        xlabel={{ """+ str(n_filer) + """, }},
        zlabel="""+ str(s_filer) +r""",
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
def to_ConvSoftMax( name, s_filer=40, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

# SoftMax
def to_SoftMax( name, s_filer=10, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" " ):
    return r"""
\pic[shift={"""+ offset +"""}] at """+ to +""" 
    {Box={
        name=""" + name +""",
        caption="""+ caption +""",
        xlabel={{" ","dummy"}},
        zlabel="""+ str(s_filer) +""",
        fill=\SoftmaxColor,
        opacity="""+ str(opacity) +""",
        height="""+ str(height) +""",
        width="""+ str(width) +""",
        depth="""+ str(depth) +"""
        }
    };
"""

def to_Sum( name, offset="(0,0,0)", to="(0,0,0)", radius=2.5, opacity=0.6):
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


def to_connection( of, to, of_side="east", to_side="west"):
    return r"""
\draw [connection]  ("""+of+"""-"""+of_side+""")    -- node {\midarrow} ("""+to+"""-"""+to_side+""");
"""

def to_skip( of, to, pos=1.25, up=False):
    if up:
        return r"""
    \path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
    \path ("""+ to +"""-north)  -- ("""+ to +"""-south)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-botton) ;
    \draw [copyconnection]  ("""+of+"""-northeast)  
    -- node {\copymidarrow}("""+of+"""-top)
    -- ++(2,0) 
    -- node {\copymidarrow}("""+to+"""-botton)
    -- node {\copymidarrow}("""+to+"""-south);
    """
    else:
        return r"""
    \path ("""+ of +"""-southeast) -- ("""+ of +"""-northeast) coordinate[pos="""+ str(pos) +"""] ("""+ of +"""-top) ;
    \path ("""+ to +"""-south)  -- ("""+ to +"""-north)  coordinate[pos="""+ str(pos) +"""] ("""+ to +"""-top) ;
    \draw [copyconnection]  ("""+of+"""-northeast)  
    -- node {\copymidarrow}("""+of+"""-top)
    -- node {\copymidarrow}("""+to+"""-top)
    -- node {\copymidarrow} ("""+to+"""-north);
    """

def to_lstm(to='10,10,10', offset="(10,0,0)"):
    return r"""
\draw[shift={"""+ offset +"""}, thick, -> ] ("""+to+"""-southeast) arc (0:320:0.7);
"""

def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""

def to_generate( arch, pathname="file.tex" ):
    with open(pathname, "w") as f: 
        for c in arch:
            print(c)
            f.write( c )
     


