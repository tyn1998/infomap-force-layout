from ogdf_python import *

cppinclude("ogdf/energybased/FMMMLayout.h")
cppinclude("ogdf/energybased/FastMultipoleEmbedder.h")
cppinclude("ogdf/energybased/SpringEmbedderFRExact.h")
cppinclude("ogdf/energybased/StressMinimization.h")


def gen_layout_wrapper(layout_method):
    def layout_wrapper(flow_network, max_depth):
        # TODO: Implement Infomap force-directed layout
        # 1. Create a new graph with the same nodes and edges as the original graph
        # 2. Create a new graph attributes object for the new graph
        # 3. Create a new force-directed layout object
        # 4. Run the force-directed layout
        # 5. Return the new graph attributes object
        L = max_depth - 1
        G_L = ogdf.Graph()
        GA_L = ogdf.GraphAttributes(G_L, ogdf.GraphAttributes.all)

        for node in flow_network['children']:
            new_node = G_L.newNode()
            GA_L.label[new_node] = node['name']
            GA_L.weight[new_node] = len(node['children'])

        for link in flow_network['links']:
            # flow_network 中 id 是从 1 开始的
            source = G_L.nodes[int(link['source']) - 1]
            target = G_L.nodes[int(link['target']) - 1]
            new_edge = G_L.newEdge(source, target)
            GA_L.doubleWeight[new_edge] = link['flow']

        layout = layout_method()
        layout.call(GA_L)
        return G_L, GA_L

    return layout_wrapper


InfomapFM3 = gen_layout_wrapper(ogdf.FMMMLayout)
InfomapFME = gen_layout_wrapper(ogdf.FastMultipoleEmbedder)
InfomapFR = gen_layout_wrapper(ogdf.SpringEmbedderFRExact)
InfomapSM = gen_layout_wrapper(ogdf.StressMinimization)
