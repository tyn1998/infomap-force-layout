import os
import argparse  # 导入argparse模块
from ogdf_python import *

cppinclude("ogdf/fileformats/GraphIO.h")
cppinclude("ogdf/energybased/FMMMLayout.h")
cppinclude("ogdf/energybased/FastMultipoleEmbedder.h")
cppinclude("ogdf/energybased/MultilevelLayout.h")
cppinclude("ogdf/energybased/SpringEmbedderGridVariant.h")
cppinclude("ogdf/energybased/SpringEmbedderKK.h")


def green_print(text):
    print(f"\033[92m{text}\033[0m")


def get_org_files(events_dir):
    org_files = {}
    for org in os.listdir(events_dir):
        org_path = os.path.join(events_dir, org)
        if os.path.isdir(org_path):
            files = []
            for file_name in os.listdir(org_path):
                if file_name.endswith('.gml') and not file_name.startswith('.'):
                    files.append(file_name)
            org_files[org] = files
    return org_files


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


# 设置argparse
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

        # 确保输出目录存在
        org_output_dir = os.path.join(output_dir, org)
        ensure_dir(org_output_dir)

        # 创建图形对象和属性对象
        G = ogdf.Graph()
        GA = ogdf.GraphAttributes(G, ogdf.GraphAttributes.all)

        # 读取GML文件
        ogdf.GraphIO.read(GA, G, input_file_path)

        # 选择布局算法并进行配置
        layout = ogdf.FMMMLayout()  # 示例：使用FMMM布局算法

        # 运行布局算法
        layout.call(GA)

        # TODO: 写入布局后的GML文件

        # 对节点和边进行遍历，设置属性
        for v in G.nodes:
            GA.width[v] = 2
            GA.height[v] = 2
            GA.fillColor[v] = ogdf.Color(0, 0, 0)
            GA.shape[v] = ogdf.Shape.Ellipse
            GA.label[v] = ""

        for e in G.edges:
            GA.strokeColor[e] = ogdf.Color(0, 0, 0)
            GA.strokeWidth[e] = 0.1
            GA.label[e] = ""

        output_svg_path = os.path.join(org_output_dir, f"{file_name[:-4]}.svg")
        # 输出处理后的图形
        ogdf.GraphIO.drawSVG(GA, output_svg_path)

        print(f"Processed {input_file_path} and saved output to {output_svg_path}")
