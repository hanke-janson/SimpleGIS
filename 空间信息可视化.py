# 点密度计算
"""
import random
import pngcanvas
import shapefile


# 判断一个点是否在多边形内部
def point_in_poly(x, y, poly):
    global xints
    poly_length = len(poly)
    # 判断点是否是顶点
    if (x, y) in poly:
        print("(", x, " ", y, ")", "是多边形的顶点")
        return True
    # 判断点是否在边框上
    for i in range(poly_length):
        p1 = None
        p2 = None
        if i == 0:
            p1 = poly[0]
            p2 = poly[1]
        else:
            p1 = poly[i - 1]
            p2 = poly[i]
        if p1[1] == p2[1] and p1[1] == y and min(p1[0], p2[0]) < x < max(p1[0], p1[0]):
            print("(", x, " ", y, ")", "在多边形的边框上")
            return True
    # 判断点是否在多边形内部
    inside = False
    plx, ply = poly[0]
    for i in range(poly_length + 1):
        p2x, p2y = poly[i % poly_length]
        if y > min(ply, p2y):
            if y <= max(ply, p2y):
                if x <= max(plx, p2x):
                    if ply != p2y:
                        xints = (y - ply) * (p2x - plx) / (p2y - ply) + plx
                    if plx == p2x or x <= xints:
                        inside = not inside
        plx, ply = p2x, p2y
    if inside:
        print("(", x, " ", y, ")", "在多边形的内部")
        return True
    print("(", x, " ", y, ")", "在多边形的外部")
    return inside


def world2screen(bbox, w, h, x, y):
    # 地理左边转换为屏幕坐标
    minx, miny, maxx, maxy = bbox
    xdist = maxx - minx
    ydist = maxy - miny
    xratio = w / xdist
    yratio = h / ydist
    px = int(w - ((maxx - x) * xratio))
    py = int((maxy - y) * yratio)
    return px, py


if __name__ == '__main__':
    # 打开人口普查矢量文件
    inShp = shapefile.Reader(r"GIS_CensusTract_poly")

    # 设置输出图片尺寸
    iwidth = 600
    iheight = 400
    print("============ 1、读取属性 ====================")
    # 获取人口记录索引
    pop_index = None
    dots = []
    for i, f in enumerate(inShp.fields):
        # 找到人口字段的索引
        if f[0] == "POPULAT11":
            # 声明删除标记
            pop_index = i - 1

    # 计算点密度并绘制相关点，生成的所有点都存储在dots中，利用point_in_poly函数来判断是否在要素内
    for sr in inShp.shapeRecords():
        population = sr.record[pop_index]
        # 点密度比例，一个点代表100人
        density = population / 100
        print("点密度比例：", density)
        found = 0
        # 绘制随机点，直到密度达到指定比率
        while found < int(density):
            minx, miny, maxx, maxy = sr.shape.bbox
            # 生成随机点
            x = random.uniform(minx, maxx)
            y = random.uniform(miny, maxy)
            # 判断随机点是否在要素内，在就添加到dots中
            if point_in_poly(x, y, sr.shape.points):
                dots.append((x, y))
                found += 1
    # 为输出png图片做准备，设置长和宽
    c = pngcanvas.PNGCanvas(iwidth, iheight)
    # 绘制红色的点
    c.color = (255, 0, 0, 0xff)
    for d in dots:
        x, y = world2screen(inShp.bbox, iwidth, iheight, *d)
        c.filled_rectangle(x - 1, y - 1, x + 1, y + 1)
    print("============ 2、读取图形 ====================")
    # 绘制人口普查区域
    c.color = (0, 0, 0, 0xff)
    for s in inShp.iterShapes():
        pixels = []
        for p in s.points:
            pixel = world2screen(inShp.bbox, iwidth, iheight, *p)
            pixels.append(pixel)
        c.polyline(pixels)

    # 保存图片
    with open(r"DotDensity1.png", "wb") as img:
        img.write(c.dump())
"""
# 等值区域图
# 根据人口普查区域每平方公里的人口得出密度比率，然后根据比例配置相应的颜色，颜色越深的区域密度越大，反之亦然
"""
import math
import shapefile

try:
    import Image
    import ImageDraw
except:
    from PIL import Image, ImageDraw


def world2screen(bbox, w, h, x, y):
    # 地理坐标转换为屏幕坐标
    # bbox 外接矩形范围
    # w 宽度 h 高度
    # x，y 坐标
    minx, miny, maxx, maxy = bbox
    xdist = maxx - minx
    ydist = maxy - miny
    xratio = w / xdist
    yratio = h / ydist
    px = int(w - ((maxx - x) * xratio))
    py = int((maxy - y) * yratio)
    return px, py


if __name__ == '__main__':
    # 打开shapefile文件
    inputShp = shapefile.Reader(r"GIS_CensusTract_poly")
    # 定义输出图片的大小
    iwidth = 600
    iheight = 400
    # 初始化PIL库的Image对象
    img = Image.new("RGB", (iwidth, iheight), (255, 255, 255))
    # PIL库的Draw模块用于填充多边形
    draw = ImageDraw.Draw(img)
    # 设置人口和面积索引
    pop_index = None
    area_index = None
    # 获取人口普查区阴影
    # print(inputShp.fields)
    for i, f in enumerate(inputShp.fields):
        # print(i,f)
        if f[0] == "POPULAT11":
            pop_index = i - 1
        elif f[0] == "AREASQKM":
            area_index = i - 1
    # 绘制多边形
    for sr in inputShp.shapeRecords():
        # 计算密度
        density = sr.record[pop_index] / sr.record[area_index]
        print(density)
        # 计算权重 根据权重来配置人口相关的颜色深度
        weight = min(math.sqrt(density / 80.0), 1.0) * 50
        R = int(205 - weight)
        G = int(215 - weight)
        B = int(245 - weight)
        print(R, G, B)
        pixels = []
        for x, y in sr.shape.points:
            # 地理坐标转换为屏幕坐标
            (px, py) = world2screen(inputShp.bbox, iwidth, iheight, x, y)
            pixels.append((px, py))
        # 绘制
        draw.polygon(pixels, outline=(255, 55, 255), fill=(R, G, B))
    img.save(r"choropleth1.png")
"""
