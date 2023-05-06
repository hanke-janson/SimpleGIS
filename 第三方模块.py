# PyPI无法提供下载的模块通常会提供与之相关的安装文件链接，可以下载这些python第三方模块的源码到当前的工作目录或者python的site-packages目录，手动进行安装。
# 当导入一个模块时，python编译器会自动搜索上述两个文件路径，如果将模块放在了当前工作目录下，那么这个模块只有当在该目录下启动python环境时才会被系统识别
# site-packages目录是专门用来存放第三方模块的
"""
import sys

print(sys.path)
"""

# GDAL 安装
# Windows下
# 检查python版本，下载与之对应的gdal发行包，通过pip进行本地手动安装 pip install C:\Users\admin\Downloads\GDAL-3.4.2-cp37-cp37m-win_amd64.whl
# Ubuntu下
# sudo apt install gdal-bin    sudo apt install python-gdal
import time

"""
from osgeo import gdal

print(gdal.__version__)
"""

# python 网络库
# 数据通常以zip压缩格式进行发布

# urllib模块：通过一个URL访问任意文件

# 下载一个压缩过的Shapefile文件

"""
import urllib.request
import urllib.error
url = "https://github.com/GeospatialPython/Learn/raw/master/hancock.zip"
fileName = "./hancock.zip"
print(urllib.request.urlretrieve(url, fileName))
"""

# 访问在线csv文件
"""
url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv"
earthquakes = urllib.request.urlopen(url)
print(earthquakes.readline())
for record in earthquakes:
    print(record)
"""

# FTP模块

"""
import ftplib

server = "ftp.ngdc.noaa.gov"
dir = "hazards/DART/20070815_peru"
fileName = "21415_from_20070727_08_55_15_tides.txt"
# 不设置用户名密码，即用匿名用户访问公共服务器
ftp = ftplib.FTP(server)
print(ftp.login())
print(ftp.cwd(dir))
out = open(fileName, "wb")
print(ftp.retrbinary("RETR" + fileName, out.write))
out.close()
dart = open(fileName)
for line in dart:
    if "LAT," in line:
        print(line)
        break
"""

# ZIP和TAR文件 TAR格式不包含压缩算法，只是提供了可选的gzip压缩项    zipfile tarfile 模块

# 解压文件
"""
import zipfile

zip = open("./hancock.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""

# 压缩文件

"""
import tarfile

tar = tarfile.open("hancock.tar.gz", "w:gz")
tar.add("hancock.shp")
tar.add("hancock.dbf")
tar.add("hancock.shx")
tar.close()
"""
# 解压文件
"""
tar = tarfile.open("hancock.tar.gz", "r:gz")
tar.extractall()
tar.close()
"""

# 不下载到本地，直接读取网络上的zip文件内容
"""
import urllib.request
import urllib.error
import zipfile
import io
import struct

url = "https://github.com/GeospatialPython/Learn/raw/master/hancock.zip"
cloudShape = urllib.request.urlopen(url)
memoryShape = io.BytesIO(cloudShape.read())
zipShape = zipfile.ZipFile(memoryShape)
cloudShp = zipShape.read("hancock.shp")
print(struct.unpack("<dddd", cloudShp[36:68]))
"""

# 标记、标签解析器

# minidom模块(纯python实现)：可以将xml源当作字符串进行处理，适合处理小于20MB的中小型XML文档，若超过此大小，程序效率会变慢
"""
# 下载数据
import urllib.request
import urllib.error
url = "https://github.com/GeospatialPython/Learn/raw/master/time-stamp-point.kml"
fileName = "./time-stamp-point.kml"
print(urllib.request.urlretrieve(url, fileName))
"""
# 从文件中读取数据并创建一个minidom解析器对象，获取文件中位置标记的一组列表
"""
from xml.dom import minidom

kml = minidom.parse("./time-stamp-point.kml")
Placemarks = kml.getElementsByTagName("Placemark")
# print(len(Placemarks))
# print(Placemarks[0])
# 查看具体内容 toxml()会将Placemarks标签包含的内容作为字符串对象输出
# print(Placemarks[0].toxml())
# toprettyxml()会增加格式缩进
# print(Placemarks[0].toprettyxml())
# 根据标签名称进一步获取坐标信息
coordinates = Placemarks[0].getElementsByTagName("coordinates")
# 访问该节点下的第一个子节点
point = coordinates[0].firstChild.data
# x, y, z = point.split(",")
# x = float(x)
# y = float(y)
# z = float(z)
# 使用List操作处理
x, y, z = [float(c) for c in point.split(",")]
print(x, y, z)

"""
# 元素树(多语言实现版本) 从python2.5起用ElementTree   cElementTree更快，但系统不一定支持
"""
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
# ElementTree不能自动处理命名空间，需要手动声明它或者将其通过字符解析函数从元素根节点标签名中提取出来
tree = ET.ElementTree(file="./time-stamp-point.kml")
# 手动定义KML的命名空间
ns = "{http://www.opengis.net/kml/2.2}"
# 使用XPath表达式和find()方法查找第一个位置标记元素
placemark = tree.find(".//%sPlacemark" % ns)
coordinates = placemark.find("./{}Point/{}coordinates".format(ns, ns))
print(coordinates.text)
"""

# 构建xml
"""

# 定义根节点
root = ET.Element("kml")
# 指定命名空间
root.attrib["xmlns"] = "http://www.opengis.net/kml/2.2"
# 添加一系列子节点
placemark = ET.SubElement(root, "Placemark")
office = ET.SubElement(placemark, "name")
office.text = "Office"
point = ET.SubElement(placemark, "point")
coordinates = ET.SubElement(point, "coordinates")
coordinates.text = "-122.087461,37.422069,37.422069"
# 将这些元素封装成一个ElementTree对象
tree = ET.ElementTree(root)
# 声明XML文件编码格式，另存为placemark.kml文件
tree.write("placemark.kml", xml_declaration=True, encoding="utf-8", method="xml")
"""
# BeautifulSoup4：主要用于可靠的处理那些格式错误的XML文件
# pip install beautifulsoup4
"""
# 下载数据
import urllib.request
import urllib.error
url = "https://github.com/GeospatialPython/Learn/raw/master/broken_data.gpx"
fileName = "./broken_data.gpx"
print(urllib.request.urlretrieve(url, fileName))
"""

"""
from bs4 import BeautifulSoup

gpx = open("./broken_data.gpx")
soup = BeautifulSoup(gpx.read(), features="xml")
# 可能报错 Couldn't find a tree builder with the features you requested: xml. Do you need to install a parser library?
# 因为BeautifulSoup4依赖于lxml 所以需要安装  pip install lxml
# print(soup.tagStack)
# print(soup.trkpt)
# tracks = soup.find_all("trkpt")
# print(len(tracks))
# 将修复的文件写入磁盘，并且格式化
fixed = open("fixed_data.gpx", "w")
fixed.write(soup.prettify())
fixed.close()
"""

# WKT 文本
# 例：描述多边形 —— POLYGON((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2, 1 2,1 1))
# Shapely库：是GEOS提供的一套充满Python风格的接口，需要pip下载，或使用whl本地安装
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade  shapely pip指定清华源下载最新版包
"""
import shapely.wkt

wktPoly = "POLYGON((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2, 1 2,1 1))"
poly = shapely.wkt.loads(wktPoly)
# 计算多边形面积
# print(poly.area)
# 通过wkt属性，将该对象转为原先的WKT形式
# print(poly.wkt)
# 同样，也可以处理wkb数据,WKB数据主要用于将WKT格式的字符串以二进制对象的形式存储在数据库中
from shapely.geometry import Point
from shapely.wkb import dumps, loads

s = dumps(Point(1, 2), hex=True)
print(s)
ss = loads(s, hex=True)
print(ss)
"""
# 下载数据
"""
import urllib.request
import urllib.error
url = "https://github.com/GeospatialPython/Learn/raw/master/polygon.zip"
fileName = "./polygon.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile
import os

zip = open("./polygon.zip", "rb")
zipShape = zipfile.ZipFile(zip)
os.mkdir("polygon")
for fileName in zipShape.namelist():
    if fileName.endswith("/"):
        continue
    if fileName.startswith("__"):
        continue
    print(fileName)
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
# 读取shp文件，获取其第一个图层，将其转为WKT格式
"""
from osgeo import ogr

shape = ogr.Open("./polygon/polygon.shp")
layer = shape.GetLayer()
feature = layer.GetNextFeature()
geom = feature.GetGeometryRef()
# ExportToWkt()只能处理要素对象
wkt = geom.ExportToWkt()
print(wkt)
# 重新将wkt导入ogr，获取它的多边形边框
poly = ogr.CreateGeometryFromWkt(wkt)
print(poly.GetEnvelope())
"""
# JSON库

"""
geojson_demo = {
    "type": "Feature",
    "id": "OpenLayers.Feature.Vector_314",
    "properties": {},
    "geometry": {
        "type": "Point",
        "coordinates":
            [
                97.03125,
                39.7265625
            ]
    },
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    }
}
"""

jsdata = """
{"type":"Feature","id":"OpenLayers.Feature.Vector_314","properties":{},"geometry":{"type":"Point","coordinates":[97.03125,39.7265625]},"crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:OGC:1.3:CRS84"}}}
"""
# 将这个geojson转换成python代码  eval()不安全

# point = eval(jsdata)
# print(point["geometry"])

# 使用json模块以正确的方式将字符串转为Python代码
"""
import json

pydata = json.loads(jsdata)
jsondata = json.dumps(pydata)
print(pydata)
print(jsondata)
"""
# geojson模块 需安装 pip install geojson
"""
import geojson

# 创建点 构建geojson
p = geojson.Point((-92, 37))
geojs = geojson.dumps(p)
print(geojs)
# geojson模块结合shapely模块
from shapely.geometry import shape
point = shape(p)
print(point.wkt)
"""
# OGR 通用矢量库
# 下载数据
"""
import urllib.request
import urllib.error
url = "https://github.com/GeospatialPython/Learn/raw/master/point.zip"
fileName = "./point.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile

zip = open("./point.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
# 查看x,y,及属性表第一个字段的信息
"""
from osgeo import ogr

shp = ogr.Open("./point.shp")
layer = shp.GetLayer()
for feature in layer:
    geometry = feature.GetGeometryRef()
    print(geometry.GetX(), geometry.GetY(), feature.GetField("FIRST_FLD"))
"""

# PyShp 需要安装 pip install pyshp 主要用于读写Shapefile文件，不支持任何几何操作，只调用Python标准库
"""
import shapefile

shp = shapefile.Reader("point.shp")
for feature in shp.shapeRecords():
    point = feature.shape.points[0]
    rec = feature.record[0]
    print(point[0], point[1], rec)
"""
# dbfpy3 专门用于处理dbf文件 目前只能通过github.com托管服务获取 pip install https://github.com/GeospatialPython/dbfpy3/archive/master.zip
# dbf文件包含Shapefile文件的属性和字段信息。OGR和PyShp只提供了对dbf文件基本操作的支持
# 下载数据 这个数据包含美国人口普查局提供的600多行dbf记录
"""
import urllib.request
import urllib.error
url = "https://github.com/GeospatialPython/Learn/raw/master/GIS_CensusTract.zip"
fileName = "./GIS_CensusTract.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile

zip = open("./GIS_CensusTract.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
# 对dbf文件进行操作
"""
from dbfpy3 import dbf

# 打开dbf文件获取第一条记录
db = dbf.Dbf("GIS_CensusTract_poly.dbf")
rec = db[0]
field = rec["POPULAT10"]
# 1760
print(field)
# 给人口字段POPULAT10值加1
rec["POPULAT10"] = field + 1
rec.store()
# 删除变量引用
del rec
print(db[0]["POPULAT10"]) 
"""

# Shapely在WKT文本导入导出时用到过，但是其主要用途是通用几何库
"""
from shapely import wkt, geometry

# 定义一个简单的WKT多边形
wktPoly = "POLYGON((0 0,4 0,4 4,0 4,0 0))"
poly = wkt.loads(wktPoly)
# 面积
print(poly.area)
# 通过5个任意单位对多边形进行缓冲区分析
buf = poly.buffer(5.0)
print(buf.area)
# 在该多边形和其缓冲区之间执行差异分析操作
print(buf.difference(poly).area)
"""

# Fiona模块为OGR库的数据访问功能提供了一套简洁的Python API 默认输出格式为GeoJSON 需安装 pip install Fiona

"""
import fiona
# 用于格式化输出
import pprint

f = fiona.open("./GIS_CensusTract_poly.shp")
# 驱动
print(f.driver)
# 坐标系
print(f.crs)
# 数据边框
print(f.bounds)
# geojson格式化输出
print(pprint.pprint(f.schema))
# 要素总数
print(len(list(f)))
# 以Geojson格式输出其中的一条记录
print(pprint.pprint(f[0]))
"""

# GDAL 处理栅格数据的主流地理空间库
# 下载数据
"""
import urllib.request
import urllib.error
url = "https://github.com/GeospatialPython/Learn/raw/master/SatImage.zip"
fileName = "./SatImage.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile

zip = open("./SatImage.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
"""
from osgeo import gdal
raster = gdal.Open("./SatImage.tif")
# 波段数
print(raster.RasterCount)
# 像素行数
print(raster.RasterXSize)
# 像素列数
print(raster.RasterYSize)
"""
# NumPy 专为Python和科学计算设计的一款高效、多维Python数组处理工具
# NumPy库可以和GDAL、Shapely、Python影像库(the Python Imaging Library, PIL)以及其他领域的Python科学计算库交换数据
"""
from osgeo import gdal_array

srcArray = gdal_array.LoadFile("./SatImage.tif")
print(len(srcArray))
band1 = srcArray[0]
band2 = srcArray[1]
band3 = srcArray[2]
# 将第一个波段保存为jpg图片
gdal_array.SaveArray(band1, "band1.jpg", format="JPEG")
gdal_array.SaveArray(band2, "band2.jpg", format="JPEG")
gdal_array.SaveArray(band3, "band3.jpg", format="JPEG")
"""
# PIL库 原本是用来处理遥感影像的，在python中一般用于图像编辑，对于Python3来说，可以使用PIL库的升级版本Pillow 通过pip安装 pip install Pillow
"""
try:
    import Image
    import ImageDraw
except:
    from PIL import Image
    from PIL import ImageDraw
import shapefile

r = shapefile.Reader("hancock.shp")
# 获取shp数据的边框经纬度值 r.bbox
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 400
iheight = 600
xratio = iwidth / xdist
yratio = iheight / ydist
pixels = []
# 获取所有的经纬度 r.shapes()[0].points
# 经纬度转屏幕坐标
for x, y in r.shapes()[0].points:
    px = int(iwidth - ((r.bbox[2] - x) * xratio))
    py = int((r.bbox[3] - y) * yratio)
    pixels.append((px, py))
img = Image.new("RGB", (iwidth, iheight), "white")
draw = ImageDraw.Draw(img)
draw.polygon(pixels, fill="rgb(198, 204, 189)", outline="rgb(203, 196, 190)", width=1)
img.save("hancock.png")
"""
# PNGCanvas "轻量级PIL" pip install pngcanvas
"""
import shapefile
import pngcanvas

r = shapefile.Reader("hancock.shp")
xdist = r.bbox[2] - r.bbox[0]
ydist = r.bbox[3] - r.bbox[1]
iwidth = 400
iheight = 600
xratio = iwidth / xdist
yratio = iheight / ydist
pixels = []
for x, y in r.shapes()[0].points:
    px = int(iwidth - ((r.bbox[2]) - x) * xratio)
    py = int((r.bbox[3] - y) * yratio)
    pixels.append([px, py])
c = pngcanvas.PNGCanvas(iwidth, iheight)
c.polyline(pixels)
f = open("hancock_pngcvs.png", "wb")
f.write(c.dump())
f.close()
"""

# Pandas 是一款高性能的Python数据分析库 可以处理海量数据表格(类似数据库)、有序化/无序化、标签化矩阵以及无标记的统计数据
# GeoPandas 是由Shapely、Fiona、PyProj、matplotlib、Descartes以及其他必需的库一同构建的Pandas的地理空间扩展，还需要特定的数据库提供支持，如PostGIS
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade geopandas
"""
import geopandas
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade matplotlib
import matplotlib.pyplot as plt
# 打开shp文件，转储为Geojson格式后绘制一张地图
gdf = geopandas.GeoDataFrame
census = gdf.from_file("GIS_CensusTract_poly.shp")
print(census)
census.plot()
plt.show()
"""
# PyMySQL  pip install pymysql
# mysql空间功能不足之处在于采用的是平面几何和矩形边框而非立体几何形状
"""
import pymysql

# 创建数据库
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='mysql')
# 获取游标对象
cur = conn.cursor()
cur.execute("DROP DATABASE IF EXISTS spatial_db")
cur.execute("CREATE DATABASE spatial_db")
cur.close()
conn.close()
# 数据库操作
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='spatial_db')
cur = conn.cursor()
cur.execute("create table places(id int not null auto_increment primary key, "
            "name varchar(50) not null, "
            "location Geometry not null)")
cur.execute("insert into places(name, location) values('NEW ORLEANS', ST_GeomFromText('POINT(30.03 90.03)'))")
cur.execute("insert into places(name, location) values('MEMPHIS', ST_GeomFromText('POINT(35.05 90.00)'))")
conn.commit()
cur.execute("select ST_AsText(location) from places")
# 列表生成式
p1, p2 = [p[0] for p in cur.fetchall()]
print(p1)
print(p2)
cur.execute("set @p1 = ST_GeomFromText('{}')".format(p1))
cur.execute("set @p2 = ST_GeomFromText('{}')".format(p2))
cur.execute("select ST_Distance(@p1, @p2)")
d = float(cur.fetchone()[0])
print("{:.2f} miles from New Orleans to Memphis".format(d * 70))
cur.close()
conn.close()
"""
# PyFPDF 是一种轻量级的创建包括地图 等PDF文件的解决方案
# PDF格式是一种非常流行的标准，也常常用来发布地图  Python 3.7+ support    pip install fpdf2
# 该模块使用了一种单元格的概念来对页面上的元素进行布局
# 导入之前的png地图后，将其转换为pdf文件创建简单地图
"""
import fpdf

# PDF对象构造器  图片，毫米为单位，A4页面大小
pdf = fpdf.FPDF("p", "mm", "A4")
# 创建一个新页面
pdf.add_page()
# 设置字体样式 arial, bold, size 20
pdf.set_font("Arial", "B", 20)
# 单元格布局样式 160 * 25mm, 标题, 无边框 居中
pdf.cell(160, 25, 'Hancock County Boundary', border=0, align="C")
# 按指定尺寸写入图片
pdf.image("hancock.png", 25, 50, 110, 160)
# 文件保存 文件名，F=文件类型
pdf.output("map.pdf", 'F')
"""
# Spectral Python, SPY是Python光谱功能包，是一款专门处理遥感应用的高级功能包 使用数据来自官网示例
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade spectral
"""
from spectral import *

img = open_image("92AV3C.lan")
# img 是一个BilFile对象 是SpyFile的子类
# print(img.__class__)
# 因为高光谱影像通常很大，当SpyFile对象被创建时，只读取元数据，影像数据只有在通过SpyFile方法请求时才会被读取
print(img)
# 加载影像
# SPY根据需要读取数据还不缓存
# 返回一个ImageArray对象 NOTE: 在调用 load() 方法前，一定要考虑返回的ImageArray对象会消耗的内存大小，谨防内存溢出。
arr = img.load()
print(arr.info())
# numpy memmap接口 返回一个numpy memmap对象
# 作为加载整景高光谱影像到内存的替代方法，这是一种稍微有点慢但内存使用效率更高的访问影像数据，既可以用来读取数据，也可以将数据写入影像文件
# numpy_arr = img.open_memmap()
# print(numpy_arr)
"""
# 显示图像
"""
from spectral import *
img = open_image('92AV3C.lan')
view = imshow(img, (29, 19, 9))
# save_rgb('rgb.jpg', img, [29, 19, 9])
"""
# 类图显示
"""
from spectral import *

img = open_image('92AV3C.lan')
gt = open_image('92AV3GT.GIS').read_band(0)
# save_rgb('gt.jpg', gt, colors=spy_colors)
view = imshow(img, (30, 20, 10), classes=gt)
view.set_display_mode('overlay')
view.class_alpha = 0.5
"""
# 光谱绘制
"""
from spectral import *
import spectral.io.aviris as aviris
img = open_image('92AV3C.lan')
img.bands = aviris.read_aviris_bands('92AV3C.spc')
"""
