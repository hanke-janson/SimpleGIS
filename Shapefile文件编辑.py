# 下载数据
"""
import urllib.request
import urllib.error

url = "http://git.io/vLbU4"
fileName = "./MSCities_Geo_Pts.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile
zip = open("./MSCities_Geo_Pts.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    print(fileName)
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
# 这里因为处理的数据至少包括.shp和.dbf等多种文件类型，所以不包含文件的扩展名的基础文件名才能满足实际需求
# 注意:建议使用扩展名，PyShp库会自动忽略并只使用不带扩展的文件名
# 如果基础文件名中带有"."例如"shapefile.version.1.2.",PyShp库会尝试将".2."作为该文件的扩展名，这样将会导致无法打开此shapefile文件
# 所以如果基础文件名中含有"."，最好使用文件扩展名
import shapefile

print("======== Shapefile文件访问 ========")
"""
shapefile_data = shapefile.Reader("MSCities_Geo_Pts")
# Shapefile文件元数据信息
print(shapefile_data)
# 可以获取一些相关的地理空间信息
# 边框信息存放在bbox属性中，返回一个包含最小值x,最小值y,最大值x,最大值y的list对象
print("Shapefile文件的边框:", shapefile_data.bbox)
# 1代表点，3代表线，5代表多边形
print("Shapefile文件的几何形状类型：", shapefile_data.shapeType)
# 每条记录都有相关的dbf记录信息
print("Shapefile文件的记录总数：", shapefile_data.numRecords)
print("Shapefile文件的编码：", shapefile_data.encoding)
print("Shapefile文件的encodingErrors：", shapefile_data.encodingErrors)
print("Shapefile文件的字段属性：", shapefile_data.fields)
print("Shapefile文件的mbox：", shapefile_data.mbox)
print("Shapefile文件的numShapes：", shapefile_data.numShapes)
print("Shapefile文件的名称：", shapefile_data.shapeName)
print("Shapefile文件的shpLength：", shapefile_data.shpLength)
print("Shapefile文件的shp对象：", shapefile_data.shp)
print("Shapefile文件的shx对象：", shapefile_data.shx)
print("Shapefile文件的dbf文件对象：", shapefile_data.dbf)
"""

print("======== Shapefile文件属性读取 ========")
"""
for data in shapefile_data.fields:
    print(data)
print("==================")
"""
# 单纯获取字段名而不包括其他元数据信息，可以使用列表推导式
"""
[print(item[0]) for item in shapefile_data.fields[1:]]
print("==================")
print("shapefile_data.record(2)结果:", shapefile_data.record(2))
"""
# 字段名和实际数据记录是分开存储的,
# 获取其中的记录值，必须使用它的索引值获取它，
# 每条记录对应的城市名的索引值是4
"""
print("shapefile_data.record(2)[4]结果:", shapefile_data.record(2)[4])
"""
# 推荐使用字段名来访问
# 方法一: 通过获取字段名的索引位置来将字段名和值对应起来
"""
NAME10 = [item[0] for item in shapefile_data.fields[1:]].index("NAME10")
print(shapefile_data.record(2)[NAME10])
"""
# 方法二: 通过Python内置的zip方法将字段名和数据记录关联起来
# 该方法是通过两个或者多个List合并为一个元组List实现的，然后遍历List，根据名字取值
"""
fieldNames = [item[0] for item in shapefile_data.fields[1:]]
rec = shapefile_data.record(2)
zipList = list(zip(fieldNames, rec))
for data in zipList:
    if data[0] == "NAME10":
        print(data[1])
"""
# 方法三: enumerate方法 它会返回包含记录索引的一个元组
"""
for rec in enumerate(shapefile_data.records()[:4]):
    print(rec[0] + 1, ": ", rec[1])
"""
# 方法四: 如果处理一些非常大的Shapefile文件，PyShp库的迭代器方法能够高效地访问数据。
# 默认的records()方法会一次性将所有记录读入内存中，对于小型的dbf文件来说还好，但对于包含几千条记录的dbf文件来说，就会变得非常难以管理。
# 在使用records()方法的同时，可以使用iterRecords()对其进行替代。该方法不会一次性读取所有数据，而是根据需要读取一定数量的数据。
"""
counter = 0
for rec in shapefile_data.iterRecords():
    print(rec)
    counter += 1
print(counter)
"""

print("======== Shapefile文件几何图形读取 ========")
"""
# 根据头文件信息可以确定该文件是一个点Shapefile文件，因此每一条记录都包含一个点
geom = shapefile_data.shape(297)
print(geom.points)
"""
print("======== Shapefile文件修改 ========")
# 下载数据
"""
import urllib.request
import urllib.error

url = "http://git.io/vLd8Y"
fileName = "./NYC_MUSEUMS_GEO.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile
zip = open("./NYC_MUSEUMS_GEO.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    print(fileName)
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
import utm

# 重投影
"""
r = shapefile.Reader(r"NYC_MUSEUMS_GEO.shp")
w = shapefile.Writer(r"NYC_MUSEUMS_UTM.shp", shapeType=r.shapeType)
w.fields = list(r.fields[1:])
for rec in r.iterShapeRecords():
    # print(rec.record[0])
    # 逐条添加数
    # 注意*list(rec.record)和list(rec.record)的区别：
    w.record(*list(rec.record))
# 投影转换
for shape in r.iterShapes():
    lon, lat = shape.points[0]
    # 投影转换，设置坐标
    y, x, zone, band = utm.from_latlon(lat, lon)
    w.point(x, y)
# 此外，不需要像重投影示例中那样写入一个PRJ投影文件。
# 有一种简便的方法可以创建一个PRJ文件，
# 那就是通过EPSG代码访问SpatialReference.org网站来实现。
# 从前面的示例中的时区变量可以知道，之前使用的UTM18区的EPSG代码是26918
# 生成投影文件
import urllib.request

prj = urllib.request.urlopen("http://spatialreference.org/ref/epsg/26918/esriwkt/")
with open(r"NYC_MUSEUMS_UTM.prj", "w") as f:
    f.write(str(prj.read()))
"""
# 给shapefile文件添加要素
# 下载数据
"""
import urllib.request
import urllib.error

url = "http://git.io/vLdlA"
fileName = "./ep202009_5day_026.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile
zip = open("./ep202009_5day_026.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    print(fileName)
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
"""
file_name = r"ep202009.026_5day_pgn.shp"
r = shapefile.Reader(file_name)
# 拷贝shapefile文件到 写入对象中
w = shapefile.Writer(r"test2.shp", r.shapeType)
# 复制现有的字段
w.fields = list(r.fields)
# 复制现有的记录
for rec in r.records():
    w.record(*list(rec))
# 复制现有的矩形
for s in r.shapes():
    w._shapeparts(parts=[s.points], shapeType=s.shapeType)
# 添加一个矩形
w.poly([[[-104, 24], [-104, 25], [-103, 25], [-103, 24], [-104, 24]]])
# 添加一个新的数据
w.record("STANLEY", "TD", "091022/1500", "27", "21", "48", "ep")
"""
# 添加字段
"""
filename1 = r"NYC_MUSEUMS_GEO.shp"
r = shapefile.Reader(filename1)
filename2 = r"NYC_MUSEUMS_GEO_2.shp"
with shapefile.Writer(filename2, r.shapeType) as w:
    # 复制原有的字段
    w.fields = list(r.fields[1:])
    # 添加新字段，添加一个最大长度为8、小数精度为5位的浮点型字段
    w.field("LAT", "F", 8, 5)
    w.field("LON", "F", 8, 5)
    for i in range(r.numRecords):
        lon, lat = r.shape(i).points[0]
        # 设置点的坐标
        w.point(lon, lat)
        # 逐条记录添加，并添加坐标
        w.record(*list(r.record(i)), lat, lon)
"""
print("======== Shapefile文件合并 ========")
# 下载数据
# 这是一组某城市分布于4个不同方位（西北，东北，西南，东南）的建筑物轮廓分布图，文件是根据方位命名的
"""
import urllib.request
import urllib.error

url = "http://git.io/vLbUE"
fileName = "./tiled_footprints.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile
zip = open("./tiled_footprints.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    print(fileName)
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
import glob

# 使用PyShp模块合并shapefile文件
"""
# 读取相同字符footprints_*.shp的矢量文件
filename = glob.glob(r"footprints_*.shp")
w = shapefile.Writer(r"merge.shp")
r = None
for f in filename:
    r = shapefile.Reader(f)
    # 写入字段
    if not w.fields:
        w.fields = list(r.fields)
    # 写入记录
    for rec in r.records():
        w.record(*list(rec))
    # 写入形状
    for shp in r.shapes():
        w._shapeparts(parts=[shp.points], shapeType=shp.shapeType)
"""
# 使用dbfpy3模块合并shapefile文件
"""
from dbfpy3 import dbf

shp_files = glob.glob("footprints_*.shp")
w = shapefile.Writer(shp="merged.shp", shx="merged.shx")
# 只遍历shapefile文件，，不打开dbf文件是为了避免产生任何文件解析错误
for f in shp_files:
    print("Shp: {}".format(f))
    r = shapefile.Reader(f)
    # 复制几何图形
    for s in r.shapes():
        # w._shapeparts(parts=[s.points], shapeType=s.shapeType)
        w.poly([s.points])
    r.close()
w.close()

# 现在使用dbfPy并合并dbf文件
dbf_files = glob.glob("footprints_*.dbf")
# 将第一个dbf文件作为临时模板
template = dbf_files.pop(0)
print('dbf模板文件: ', template)
merged_dbf_name = "merged.dbf"
# 拷贝实体dbf模板文件到合并后的新文件中
merged_dbf = open(merged_dbf_name, "wb")
temp = open(template, "rb")
merged_dbf.write(temp.read())
merged_dbf.close()
temp.close()
# Todo 不清楚下面哪句话处理的有问题，最后的的结果，属性表的字段名消失了
# 现在从剩下的dbf文件中读取所有记录并在新合并的dbf文件中建立对应的记录
db = dbf.Dbf(merged_dbf_name)
for f in dbf_files:
    print("Dbf: {}".format(f))
    dba = dbf.Dbf(f)
    for rec in dba:
        db_rec = db.newRecord()
        for k, v in list(rec.asDict().items()):
            # print(k, v)
            db_rec[k] = v
        db_rec.store()
db.close()
"""
print("======== Shapefile文件分割 ========")
# 根据区域对建筑物分布图进行过滤并将导出大约100平方米的建筑物分布图到一个新的Shapefile文件中
"""
# 读取矢量面文件
r = shapefile.Reader(r"footprints_se")
# 创建新的矢量面对象
with shapefile.Writer(r"footprints_sp100", r.shapeType) as w:
    # 将字段复制给w
    w.fields = list(r.fields)
    # 遍历r记录
    for sr in r.shapeRecords():
        utmPoints = []
        for p in sr.shape.points:
            x, y, band, zone = utm.from_latlon(p[1], p[0])
            utmPoints.append([x, y])
            # print(utmPoints)
        # 计算每个矢量面的坐标
        area = abs(shapefile.signed_area(utmPoints))
        # print(area)
        if area <= 100:
            w.poly([sr.shape.points])
            w.record(*list(sr.record))
# 结果验证
r = shapefile.Reader(r"footprints_se")
subset = shapefile.Reader(r"footprints_sp100")
print("总数：", r.numRecords)
print("子集：", subset.numRecords)
"""
