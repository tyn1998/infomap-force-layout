import random
from ogdf_python import *
from classic_force_layouts import FM3, FME, FRE, SM

cppinclude("ogdf/energybased/MultilevelLayout.h")


def layout_G1(flow_network, classic_force_layout):
    G1 = ogdf.Graph()
    GA1 = ogdf.GraphAttributes(G1, ogdf.GraphAttributes.all)

    for node in flow_network['children']:
        new_node = G1.newNode()
        GA1.label[new_node] = node['name']
        GA1.weight[new_node] = len(node['children'])

    for link in flow_network['links']:
        # flow_network 中 id 是从 1 开始的
        source = G1.nodes[int(link['source']) - 1]
        target = G1.nodes[int(link['target']) - 1]
        new_edge = G1.newEdge(source, target)
        GA1.doubleWeight[new_edge] = link['flow']

    G1, GA1_copy = classic_force_layout(G1, GA1)

    return G1, GA1_copy


def layout_G0(G, GA, flow_network, G1, GA1, classic_force_layout):
    G0 = G
    GA0 = ogdf.GraphAttributes(GA)

    positions = {}
    for v in G1.nodes:
        id = v.index()
        for node in flow_network['children'][id]['children']:
            # TODO: 把更深层的节点也拎出来放到一起，不然超出2层的节点会漏掉
            positions[node['name']] = {
                "x": GA1.x(v),
                "y": GA1.y(v),
            }

    for v in G0.nodes:
        label = GA0.label[v].decode('utf-8')
        if label in positions:
            # x y 都加上一个很小的随机数
            GA0.x[v] = positions[label]['x'] + random.uniform(-1, 1)
            GA0.y[v] = positions[label]['y'] + random.uniform(-1, 1)

    G0, GA0_copy = classic_force_layout(G0, GA0, use_initial_layout=True)

    return G0, GA0_copy


def InfomapFM3(G, GA, flow_network):
    G1, GA1_copy = layout_G1(flow_network, FM3)
    G0, GA0_copy = layout_G0(G, GA, flow_network, G1, GA1_copy, FM3)
    return G0, GA0_copy


def InfomapFME(G, GA, flow_network):
    G1, GA1_copy = layout_G1(flow_network, FME)
    G0, GA0_copy = layout_G0(G, GA, flow_network, G1, GA1_copy, FME)
    return G0, GA0_copy


def InfomapFRE(G, GA, flow_network):
    G1, GA1_copy = layout_G1(flow_network, FRE)
    G0, GA0_copy = layout_G0(G, GA, flow_network, G1, GA1_copy, FRE)
    return G0, GA0_copy


def InfomapSM(G, GA, flow_network):
    G1, GA1_copy = layout_G1(flow_network, SM)
    G0, GA0_copy = layout_G0(G, GA, flow_network, G1, GA1_copy, SM)
    return G0, GA0_copy


def InfomapML(G, GA, flow_network):
    GA_copy = ogdf.GraphAttributes(GA)
    layout = ogdf.MultilevelLayout()
    layout.call(GA_copy)

    return G, GA_copy