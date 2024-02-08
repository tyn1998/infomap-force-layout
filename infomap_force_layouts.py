from ogdf_python import *
from infomap import Infomap

cppinclude("ogdf/energybased/FMMMLayout.h")
cppinclude("ogdf/energybased/FastMultipoleEmbedder.h")
cppinclude("ogdf/energybased/SpringEmbedderFRExact.h")


def gen_layout_wrapper(layout_class):
    def layout_wrapper(G, GA):
        GA_copy = ogdf.GraphAttributes(GA)
        return GA_copy
    return layout_wrapper


InfomapFM3 = gen_layout_wrapper(ogdf.FMMMLayout)
InfomapFME = gen_layout_wrapper(ogdf.FastMultipoleEmbedder)
InfomapFR = gen_layout_wrapper(ogdf.SpringEmbedderFRExact)
