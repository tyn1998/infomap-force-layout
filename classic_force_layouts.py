from ogdf_python import *

cppinclude("ogdf/energybased/FMMMLayout.h")
cppinclude("ogdf/energybased/FastMultipoleEmbedder.h")
cppinclude("ogdf/energybased/SpringEmbedderFRExact.h")


def gen_layout_wrapper(layout_class):
    def layout_wrapper(GA):
        GA_copy = ogdf.GraphAttributes(GA)
        layout = layout_class()
        layout.call(GA_copy)
        return GA_copy

    return layout_wrapper


FM3 = gen_layout_wrapper(ogdf.FMMMLayout)
FME = gen_layout_wrapper(ogdf.FastMultipoleEmbedder)
FR = gen_layout_wrapper(ogdf.SpringEmbedderFRExact)
