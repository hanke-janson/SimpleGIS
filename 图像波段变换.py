# 下载数据
"""
import urllib.request
import urllib.error
url = "http://git.io/vqs41"
fileName = "./FalseColor.zip"
print(urllib.request.urlretrieve(url, fileName))
"""
from osgeo import gdal_array

# 原图像名称
src = "FalseColor.tif"
# 将原图像加载到数组中
arr = gdal_array.LoadFile(src)
print(arr)
# 为了获得一张自然色彩的图片，交换波段1和波段2的位置
# 使用Numpy库的高级分片功能对波段进行重新排列
# 调用原图片
# 波段索引 0 1 2
output = gdal_array.SaveArray(arr[[1, 0, 2], :], "swap.tif", format="GTiff", prototype=src)
# 取消输出避免在某些平台上损坏文件
output = None
