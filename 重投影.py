# 下载数据
"""
import urllib.request
import urllib.error

url = "http://git.io/vLbT4"
fileName = "./NYC_MUSEUMS_LAMBERT.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
# 解压数据
"""
import zipfile
zip = open("./NYC_MUSEUMS_LAMBERT.zip", "rb")
zipShape = zipfile.ZipFile(zip)
for fileName in zipShape.namelist():
    if fileName.startswith("_"):
        continue
    print(fileName)
    out = open(fileName, "wb")
    out.write(zipShape.read(fileName))
    out.close()
"""
from osgeo import ogr
from osgeo import osr
import os
# Python标准库的shutil库主要用于拷贝dbf文件（是shell utilities的缩写）
import shutil

# 定义文件路径，包括原始文件和重投影后的文件
srcName = "NYC_MUSEUMS_LAMBERT.shp"
tgtName = "NYC_MUSEUMS_GEO.shp"
# 定义坐标系统
tgt_spatRef = osr.SpatialReference()
tgt_spatRef.ImportFromEPSG(4326)
print(tgt_spatRef)
# 我国常用坐标系的对应编码
# spatialReference.importFromEPSG(4326)WGS84
# spatialReference.importFromEPSG(4214)BeiJing54
# spatialReference.importFromEPSG(4610)XIAN80
# spatialReference.importFromEPSG(4490)CGCS2000
# 获取矢量文件
driver = ogr.GetDriverByName("ESRI Shapefile")
# 其中update为0是只读，为1是可写
src = driver.Open(srcName, 0)
srcLyr = src.GetLayer()
src_spatRef = srcLyr.GetSpatialRef()
print(src_spatRef)
# 如果文件存在则删除
if os.path.exists(tgtName):
    driver.DeleteDataSource(tgtName)
# 创建新文件
tgt = driver.CreateDataSource(tgtName)
lyrName = os.path.splitext(tgtName)[0]
# 使用WKB格式声明几何图形
# wkt(OGC well-known text)和wkb(OGC well-known binary)是OGC制定的空间数据的组织规范，
# wkt是以文本形式描述，wkb是以二进制形式描述
# 使用wkt和wkb能够很好到和其他系统进行数据交换，目前大部分支持空间数据存储的数据库构造空间数据都采用这两种方式。
# 创建矢量（图层名称，几何类型wkbPoint为点类型）
tgtLyr = tgt.CreateLayer(lyrName, geom_type=ogr.wkbPoint)
featDef = srcLyr.GetLayerDefn()
# 投影转换  将原坐标New York 3104转成WGS 84
trans = osr.CoordinateTransformation(src_spatRef, tgt_spatRef)
srcFeat = srcLyr.GetNextFeature()
while srcFeat:
    # 获取点信息
    geom = srcFeat.GetGeometryRef()
    geom.Transform(trans)
    feature = ogr.Feature(featDef)
    feature.SetGeometry(geom)
    tgtLyr.CreateFeature(feature)
    # 关闭数据源
    feature.Destroy()
    srcFeat.Destroy()
    srcFeat = srcLyr.GetNextFeature()
src.Destroy()
tgt.Destroy()
# 导出投影文件 将几何图形转换为Esri的WKT格式
tgt_spatRef.MorphToESRI()
prj = open(lyrName + ".prj", "w")
prj.write(tgt_spatRef.ExportToWkt())
prj.close()
# dfb属性文件不会变化，所以直接把属性文件拷贝过来
srcDbf = os.path.splitext(srcName)[0] + ".dbf"
tgtDbf = lyrName + ".dbf"
shutil.copyfile(srcDbf, tgtDbf)
