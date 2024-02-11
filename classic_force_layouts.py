from ogdf_python import *
import random

cppinclude("ogdf/energybased/FMMMLayout.h")
cppinclude("ogdf/energybased/FastMultipoleEmbedder.h")
cppinclude("ogdf/energybased/SpringEmbedderFRExact.h")
cppinclude("ogdf/energybased/StressMinimization.h")


def FM3(G, GA, use_initial_layout=False):
    GA_copy = ogdf.GraphAttributes(GA)
    layout = ogdf.FMMMLayout()
    layout.call(GA_copy)
    return G, GA_copy


def FME(G, GA, use_initial_layout=False):
    GA_copy = ogdf.GraphAttributes(GA)
    layout = ogdf.FastMultipoleEmbedder()
    if use_initial_layout:
        layout.setRandomize(False)
    layout.call(GA_copy)
    return G, GA_copy


def FRE(G, GA, use_initial_layout=False):
    GA_copy = ogdf.GraphAttributes(GA)
    for v in G.nodes:
        GA_copy.x[v] = random.uniform(-5, 5)
        GA_copy.y[v] = random.uniform(-5, 5)
    layout = ogdf.SpringEmbedderFRExact()
    layout.call(GA_copy)
    return G, GA_copy


def SM(G, GA, use_initial_layout=False):
    GA_copy = ogdf.GraphAttributes(GA)
    layout = ogdf.StressMinimization()
    if use_initial_layout:
        layout.hasInitialLayout(True)
    layout.call(GA_copy)
    return G, GA_copy
