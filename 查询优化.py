# 点包容性公式
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
        print("(", x, " ", y, ")", "是多边形的内部")
        return True
    print("(", x, " ", y, ")", "是多边形的外部")
    return inside


# 验证point_in_poly(x, y, poly)
"""
# 判断点是否在某个区域内
# 判断一个点是否包含在某区域
myPolygon = [(-70.593016, -33.416032), (-70.589604, -33.415370),
             (-70.589046, -33.417340), (-70.592351, -33.417949),
             (-70.593016, -33.416032)]
# 测试位置点1
lon = -70.592000
lat = -33.416000
print(point_in_poly(lon, lat, myPolygon))
# 测试位置点2
lon = -70.593016
lat = -33.416032
print(point_in_poly(lon, lat, myPolygon))
# 测试位置点3
lon = -73.593016
lat = -33.416032
print(point_in_poly(lon, lat, myPolygon))
"""
# 下载数据
"""
import urllib.request
import urllib.error

url = "https://github.com/GeospatialPython/Learn/raw/master/roads.zip"
fileName = "./roads.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 使用简单的边框将一个复杂的要素集子级化
"""
import shapefile

# 读取数据
r = shapefile.Reader(r"roadtrl020")
# 创建一个w文件，用于写入在选择区内的r数据
with shapefile.Writer(r"Puerto_Rico_Roads", r.shapeType) as w:
    # 字段
    w.fields = list(r.fields)
    # 定义选择区域的范围
    xmin = -67.5
    xmax = -65.0
    ymin = 17.8
    ymax = 18.6
    # 循环读取r文件的记录
    for road in r.iterShapeRecords():
        # 定义shape
        geom = road.shape
        # 定义记录
        rec = road.record
        # 得到每条记录的外包矩形范围
        sxmin, symin, sxmax, symax = geom.bbox
        # 判断是否在所选的范围内
        if sxmin < xmin:
            continue
        elif sxmax > xmax:
            continue
        elif symin < ymin:
            continue
        elif symax > ymax:
            continue
        # 在范围内的线被添加到新的图层中
        w.line([geom.points])
        w.record(*list(rec))
"""
# 下载数据
"""
import urllib.request
import urllib.error

url = "http://git.io/vLbU9"
fileName = "./MS_UrbanAnC10.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 使用属性表获取矢量数据子集
# 通过记录表中的城市人口密度来进行筛选，选择城市人口密度小于5000的要素
"""
import shapefile

# 读取矢量文件
r = shapefile.Reader(r"MS_UrbanAnC10.shp")
with shapefile.Writer(r"MS_UrbanAnC10_subset.shp", r.shapeType) as w:
    w.fields = list(r.fields)
    selection = []
    # 打印第一条记录
    # print(r.record())
    # 打印所有记录
    print(r.records())
    # 注意enumerate的用法，
    for rec in enumerate(r.records()):
        # 查询城区中人口密度小于5000的区域
        if rec[1][15] < 5000:
            # print(rec[0])
            # print(rec[1])
            # print(rec[1][15])
            selection.append(rec)
    for rec in selection:
        # 添加形状
        w.poly([r.shape(rec[0]).points])
        # 添加记录
        w.record(*list(rec[1]))
"""
# 使用fiona库实现这个案例，该库可以方便的调用OGR库
"""
import fiona

with fiona.open(r"MS_UrbanAnC10.shp") as sf:
    # 将使用嵌套语句适当缩减打开和关闭文件代码的数量。
    filtered = filter(lambda f: f["properties"]["POP"] < 5000, sf)
    # shapefile文件格式驱动
    drv = sf.driver
    # 参考坐标系
    crs = sf.crs
    # Dbf架构
    schema = sf.schema
    # 定义子集文件名
    subset = r"MS_UrbanAnC10_FionaSubset.shp"
    with fiona.open(subset, "w", driver=drv, crs=crs, schema=schema) as w:
        for rec in filtered:
            w.write(rec)
"""
