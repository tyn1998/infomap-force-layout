import os
import argparse
from ogdf_python import *
from utils import green_print, get_org_files, ensure_dir
from classic_force_layouts import FM3, FME, FR, SM
from infomap_force_layouts import InfomapFM3, InfomapFME, InfomapFR, InfomapSM
from ftree import gen_ftree_file, parse_ftree_file, parse_ftree, build_network_from_ftree
from draw_graph import drawSVG
from save_layout import saveJSON

cppinclude("ogdf/fileformats/GraphIO.h")

parser = argparse.ArgumentParser(description='Layout GML files with OGDF.')
parser.add_argument('--input_dir', type=str, default='networks')
parser.add_argument('--output_dir', type=str, default='layouts')

args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

org_files = get_org_files(input_dir)
green_print(f'org_files: {org_files}')

for org, files in org_files.items():
    for file_name in files:
        input_file_path = os.path.join(input_dir, org, file_name)
        green_print(f'Processing {input_file_path}')

        org_output_dir = os.path.join(output_dir, org)
        ensure_dir(org_output_dir)

        G = ogdf.Graph()
        GA = ogdf.GraphAttributes(G, ogdf.GraphAttributes.all)
        ogdf.GraphIO.read(GA, G, input_file_path)

        ftree_path = os.path.join(org_output_dir, f"{file_name[:-4]}.ftree")
        max_depth = gen_ftree_file(G, GA, ftree_path)
        rows = parse_ftree_file(ftree_path)
        ftree = parse_ftree(rows)
        flow_network = build_network_from_ftree(ftree)

        layouts = {
            "FM3": FM3(G, GA),
            "FME": FME(G, GA),
            # "FR": FR(G, GA),
            "SM": SM(G, GA),
            "InfomapFM3": InfomapFM3(flow_network, max_depth),
            "InfomapFME": InfomapFME(flow_network, max_depth),
            # "InfomapFR": InfomapFR(flow_network, max_depth),
            "InfomapSM": InfomapSM(flow_network, max_depth),
        }

        for layout_name, [G, GA] in layouts.items():
            output_svg_path = os.path.join(org_output_dir, f"{file_name[:-4]}_{layout_name}.svg")
            drawSVG(G, GA, output_svg_path)

            output_json_path = os.path.join(org_output_dir, f"{file_name[:-4]}_{layout_name}.json")
            saveJSON(G, GA, output_json_path)

            print(f"Processed {input_file_path} and saved output to {output_svg_path} and {output_json_path}")
