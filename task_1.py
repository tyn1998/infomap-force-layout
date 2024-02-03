# uncomment if you didn't install OGDF globally:
# %env OGDF_BUILD_DIR=~/ogdf/build-debug
from ogdf_python import *

cppinclude("ogdf/fileformats/GraphIO.h")
cppinclude("ogdf/energybased/FMMMLayout.h")
cppinclude("ogdf/energybased/FastMultipoleEmbedder.h")
cppinclude("ogdf/energybased/MultilevelLayout.h")
cppinclude("ogdf/energybased/SpringEmbedderGridVariant.h")
cppinclude("ogdf/energybased/SpringEmbedderKK.h")

# 创建一个图形对象
G = ogdf.Graph()

# 创建一个图形属性对象，可用于存储布局等信息
GA = ogdf.GraphAttributes(G, ogdf.GraphAttributes.all)

# 读取GML文件
ogdf.GraphIO.read(GA, G, "input/xlab_ra.gml")

# 创建FMMMLayout对象
# layout = ogdf.FastMultipoleEmbedder()
layout = ogdf.FMMMLayout()
# layout = ogdf.MultilevelLayout()
# layout = ogdf.SpringEmbedderGridVariant()
# layout = ogdf.SpringEmbedderKK()  # 只能用于连通图


# 设置FMMMLayout的参数（例如：温度、最大迭代次数等）
# layout.unitEdgeLength(100.0)  # 设置单位边长
# layout.setTemperature(1.0)     # 设置初始温度
# layout.setCoolingFactor(0.8)  # 设置冷却因子
# layout.setMaxIter(500)        # 设置最大迭代次数

# 运行布局算法
layout.call(GA)

# 遍历所有节点，改变大小和颜色，隐藏标签
for v in G.nodes:
    GA.width[v] = 2  # 设置节点宽度
    GA.height[v] = 2  # 设置节点高度
    GA.fillColor[v] = ogdf.Color(0, 0, 0)  # 设置节点填充颜色
    GA.shape[v] = ogdf.Shape.Ellipse  # 设置节点形状为椭圆
    GA.label[v] = ""  # 隐藏标签
    # GA.x[v] = 1.1  # 可以修改坐标

# 遍历所有边，改变颜色
for e in G.edges:
    # GA.strokeColor[e] = ogdf.Color(178, 178, 178)  # 设置边颜色
    GA.strokeColor[e] = ogdf.Color(0, 0, 0)  # 设置边颜色
    GA.strokeWidth[e] = 0.1  # 设置节点宽度
    GA.label[e] = ""  # 隐藏边的标签

ogdf.GraphIO.drawSVG(GA, "output.svg")
ogdf.GraphIO.write(GA, "output.dot")
