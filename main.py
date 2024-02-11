import os
import re
import argparse
import subprocess
import pandas as pd
from ogdf_python import *
from utils import green_print, get_org_files, ensure_dir
from classic_force_layouts import FM3, FME, FRE, SM
from infomap_force_layouts import InfomapFM3, InfomapFME, InfomapFRE, InfomapSM, InfomapML
from ftree import gen_ftree_file, parse_ftree_file, parse_ftree, build_network_from_ftree
from draw_graph import drawSVG
from save_layout import saveJSON

cppinclude("ogdf/fileformats/GraphIO.h")

parser = argparse.ArgumentParser(description='Layout GML files with OGDF.')
parser.add_argument('--input_dir', type=str, default='networks')
parser.add_argument('--output_dir', type=str, default='layouts')
parser.add_argument('--glam_path', type=str, default='', help='Path to the precompiled glam executable')

args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir
glam_path = args.glam_path

org_files = get_org_files(input_dir)
green_print(f'org_files: {org_files}')

for org, files in org_files.items():
    all_layouts_results = {}  # 存储所有布局结果的字典

    for file_name in files:
        input_file_path = os.path.join(input_dir, org, file_name)
        green_print(f'Processing {input_file_path}')

        org_output_dir = os.path.join(output_dir, org)
        ensure_dir(org_output_dir)

        G = ogdf.Graph()
        GA = ogdf.GraphAttributes(G, ogdf.GraphAttributes.all)
        ogdf.GraphIO.read(GA, G, input_file_path)

        ftree_path = os.path.join(org_output_dir, f"{file_name[:-4]}.ftree")
        gen_ftree_file(G, GA, ftree_path)
        rows = parse_ftree_file(ftree_path)
        ftree = parse_ftree(rows)
        flow_network = build_network_from_ftree(ftree)

        layouts = {
            "FM3": FM3(G, GA),
            "FME": FME(G, GA),
            "FRE": FRE(G, GA),
            "SM": SM(G, GA),
            # "InfomapFM3": InfomapFM3(G, GA, flow_network),
            # "InfomapFME": InfomapFME(G, GA, flow_network),
            # "InfomapFRE": InfomapFRE(G, GA, flow_network),
            # "InfomapSM": InfomapSM(G, GA, flow_network),
            "InfomapML": InfomapML(G, GA, flow_network),
        }

        for layout_name, [G, GA] in layouts.items():
            output_svg_path = os.path.join(org_output_dir, f"{file_name[:-4]}_{layout_name}.svg")
            drawSVG(G, GA, output_svg_path)

            output_json_path = os.path.join(org_output_dir, f"{file_name[:-4]}_{layout_name}.json")
            saveJSON(G, GA, output_json_path)

            metrics = ['crosslessness', 'min_angle', 'shape_gabriel']
            results = {"layout_method": layout_name}
            for metric in metrics:
                cmd = f'{glam_path} {output_json_path} -m {metric}'
                process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                output = process.stdout
                match = re.search(rf"{metric}=([0-9.]+)", output)
                if match:
                    value = match.group(1)
                else:
                    value = "未找到"
                results[metric] = float(value) if value != "未找到" else None
            results['average'] = sum([v for v in results.values() if isinstance(v, float)]) / len([v for v in results.values() if isinstance(v, float)])
            all_layouts_results[layout_name] = results

            print(f"Processed {input_file_path} and saved output to {output_svg_path} and {output_json_path}")

        # 创建存储所有布局算法结果的 DataFrame 并保存到 CSV 文件
        results_df = pd.DataFrame(all_layouts_results.values())
        csv_path = os.path.join(org_output_dir, f"{file_name[:-4]}_metrics.csv")
        results_df.to_csv(csv_path, index=False)
        print(f"All layouts results saved to {csv_path}")
