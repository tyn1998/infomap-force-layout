from infomap import Infomap


def gen_ftree_file(G, GA, output_ftree_path):
    im = Infomap(ftree=True)
    for e in G.edges:
        u = e.source().index()
        v = e.target().index()
        weight = GA.doubleWeight(e)
        im.add_link(u, v, weight)
    im.run()
    im.write_flow_tree(output_ftree_path)


def parse_ftree_file(file_path, opts=None):
    default_opts = {
        "delimiter": " ",
        "quotechar": "\"",
        "skip_blank_lines": True,
    }
    if opts:
        default_opts.update(opts)

    try:
        data = []
        with open(file_path, "r") as file:
            for line in file:
                if not line.startswith(default_opts.get("comments", "#")):
                    data.append(line.strip().split(default_opts["delimiter"]))
        return data
    except Exception as e:
        raise Exception(f"Error parsing file: {e}")


# transformed by GPT4 with the below JS counterpart
# https://github.com/mapequation/network-navigator/blob/master/src/io/ftree.js
# Example input
# [
#     ["*Modules", 4],  # optional section
#     ["1", 0.5, "ModuleName 1", 0.4],
#     # ...
#     ["*Nodes", 10],  # optional header
#     ["1:1:1", 0.0564732, "Name 1", 29],
#     ["1:1:2", 0.0066206, "Name 2", 286],
#     ["1:1:3", 0.0025120, "Name 3", 146],
#     ["1:1:4", 0.0024595, "Name 4", 155],
#     # ...
#     ["*Links", "directed"],
#     ["*Links", "root", 0, 0, 68, 208],
#     [2, 1, 0.000107451],
#     [1, 2, 0.0000830222],
#     [3, 1, 0.00000900902],
#     # ...
# ]

# Example output structure
# {
#     "data": {
#         "tree": [
#             { "path", "flow", "name", "stateNode?", "node" },
#             # ...
#         ],
#         "links": [
#             {
#                 "path",
#                 "name",  # optional
#                 "enterFlow",
#                 "exitFlow",
#                 "numEdges",
#                 "numChildren",
#                 "links": [
#                     { "source", "target", "flow" },
#                     # ...
#                 ],
#             },
#             # ...
#         ],
#     },
#     "errors": [],
#     "meta": {
#         "directed",
#     },
# }
def parse_ftree(rows):
    result = {
        "data": {
            "tree": [],
            "links": []
        },
        "errors": [],
        "meta": {
            "directed": True
        }
    }

    modules = {}
    tree = result["data"]["tree"]
    links = result["data"]["links"]

    i = 0

    # Parse modules section
    modules_header = "*Modules"
    nodes_header = ["*Nodes", "*Tree"]
    if modules_header in rows[i][0]:
        # Consume modules header
        i += 1

        for row in rows[i:]:
            if row[0] in nodes_header:
                i += 1
                break

            if len(row) != 4:
                result["errors"].append(f"Malformed ftree data: expected 4 fields, found {len(row)} when parsing modules.")
                continue

            modules[row[0]] = {
                "path": row[0],
                "flow": row[1],
                "name": row[2],
                "exitFlow": row[3]
            }

            i += 1

    # Parse tree section
    for row in rows[i:]:
        if "*Links" in row[0]:
            break

        if len(row) < 4 or len(row) > 6:
            result["errors"].append(f"Malformed ftree data: expected 4 to 6 fields, found {len(row)} when parsing tree.")
            continue

        node = {
            "path": row[0],
            "flow": row[1],
            "name": row[2],
            "node": row[-1]
        }

        if len(row) == 5:
            node["stateNode"] = row[3]

        tree.append(node)

        i += 1

    if not tree:
        result["errors"].append("No tree data found!")

    # Get link type
    if i < len(rows) and "directed" in rows[i][1]:
        result["meta"]["directed"] = rows[i][1] == "directed"
        i += 1

    link = {"links": []}

    # Parse links section
    is_old_format = False
    for row in rows[i:]:
        if row[0].startswith("*Links"):
            if len(row) < 6:
                if len(row) == 5:
                    if not is_old_format:
                        print('Detected old ftree format (missing enterFlow on modules). Use Infomap v1.0+ for the latest format.')
                    is_old_format = True
                else:
                    result["errors"].append(f"Malformed ftree link header: expected 6 fields, found {len(row)} when parsing links header.")
                    continue

            enter_flow_offset = -1 if len(row) == 5 else 0

            link = {
                "path": row[1],
                "enterFlow": row[2],
                "exitFlow": row[3 + enter_flow_offset],
                "numEdges": row[4 + enter_flow_offset],
                "numChildren": row[5 + enter_flow_offset],
                "links": []
            }

            mod = modules.get(link["path"])
            if mod:
                link["name"] = mod["name"]

            links.append(link)
        else:
            if len(row) != 3:
                result["errors"].append(f"Malformed ftree link data: expected 3 fields, found {len(row)} when parsing links.")
                continue

            link["links"].append({
                "source": row[0],
                "target": row[1],
                "flow": row[2]
            })

        i += 1

    if not links:
        result["errors"].append("No link data found!")

    return result
