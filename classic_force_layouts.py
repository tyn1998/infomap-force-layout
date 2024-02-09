from ogdf_python import *

cppinclude("ogdf/energybased/FMMMLayout.h")
cppinclude("ogdf/energybased/FastMultipoleEmbedder.h")
cppinclude("ogdf/energybased/SpringEmbedderFRExact.h")
cppinclude("ogdf/energybased/StressMinimization.h")


def gen_layout_wrapper(layout_method):
    def layout_wrapper(G, GA):
        GA_copy = ogdf.GraphAttributes(GA)
        layout = layout_method()
        layout.call(GA_copy)
        return G, GA_copy

    return layout_wrapper


FM3 = gen_layout_wrapper(ogdf.FMMMLayout)
FME = gen_layout_wrapper(ogdf.FastMultipoleEmbedder)
FR = gen_layout_wrapper(ogdf.SpringEmbedderFRExact)
SM = gen_layout_wrapper(ogdf.StressMinimization)
