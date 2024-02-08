import os
import subprocess
from ogdf_python import *

cppinclude("ogdf/fileformats/GraphIO.h")


def drawSVG(G, GA, output_svg_path):
    for v in G.nodes:
        GA.width[v] = 2
        GA.height[v] = 2
        GA.fillColor[v] = ogdf.Color(0, 0, 0)
        GA.shape[v] = ogdf.Shape.Ellipse
        GA.label[v] = ""

    for e in G.edges:
        GA.strokeColor[e] = ogdf.Color(0, 0, 0)
        GA.strokeWidth[e] = 0.1
        GA.label[e] = ""

    ogdf.GraphIO.drawSVG(GA, output_svg_path)
