import json


def saveJSON(G, GA, output_json_path):
    nodes = [{"x": GA.x(v), "y": GA.y(v)} for v in G.nodes]
    links = [{"source": e.source().index(), "target": e.target().index()} for e in G.edges]
    graph_data = {"nodes": nodes, "links": links}
    with open(output_json_path, 'w') as f:
        json.dump(graph_data, f, indent=4)
