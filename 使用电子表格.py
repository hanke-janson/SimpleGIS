# 下载数据
"""
import urllib.request
import urllib.error

url = "https://github.com/GeospatialPython/Learn/raw/master/NYC_MUSEUMS_GEO.xls"
fileName = "./NYC_MUSEUMS_GEO.xls"
print(urllib.request.urlretrieve(url, fileName))
"""
import xlrd
import shapefile

# 打开电子表格
xls = xlrd.open_workbook(r"NYC_MUSEUMS_GEO.xls")
sheet = xls.sheet_by_index(0)
# 创建一个shapefile文件写者对象
with shapefile.Writer(r"NYC_MUSEUMS_GEO_toShp", shapefile.POINT) as w:
    # column是列，row是行
    # 获取电子表格的第一行作为dbf文件的表头
    for i in range(sheet.ncols):
        print(sheet.cell(0, i))
        # cell(行号，列号)
        w.field(str(sheet.cell(0, i)), "C", 40)
    # 循环遍历电子表格每一行，将属性拷贝到dbf文件中
    for i in range(1, sheet.nrows):
        values = []
        for j in range(sheet.ncols):
            values.append(sheet.cell(i, j).value)
        w.record(*values)
        # 从最后两列获取经纬度信息，并创建点
        w.point(float(values[-2]), float(values[-1]))
