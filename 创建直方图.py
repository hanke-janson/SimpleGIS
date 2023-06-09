from osgeo import gdal_array
import turtle as t
import operator
from functools import reduce


# 根据图片中获得的RGB频率最大值自动缩放y轴的取值范围
# 从技术上来说，y轴表示的最大频率是图片中的像素值，即使表达该图片的颜色只有一种也是如此

# 计算直方图
def histogram(a, bins=None):
    if bins is None:
        bins = list(range(0, 256))
    fa = a.flat
    n = gdal_array.numpy.searchsorted(gdal_array.numpy.sort(fa), bins)
    n = gdal_array.numpy.concatenate([n, [len(fa)]])
    hist = n[1:] - n[:-1]
    return hist


# 绘制直方图
def draw_histogram(hist, scale=True):
    t.color("black")
    axes = ((-355, -200), (355, -200), (-355, -200), (-355, 250))
    t.up()
    for p in axes:
        t.goto(p)
        t.down()
    t.up()
    t.goto(0, -250)
    t.write("VALUE", font=("Arial, ", 12, "bold"))
    t.up()
    t.goto(-400, 280)
    t.write("FREQUENCY", font=("Arial, ", 12, "bold"))
    x = -355
    y = -200
    t.up()
    for i in range(1, 11):
        x = x + 65
        t.goto(x, y)
        t.down()
        t.goto(x, y - 10)
        t.up()
        t.goto(x, y - 25)
        t.write("{}".format((i * 25)), align="center")
    x = -355
    y = -200
    t.up()
    pixels = sum(hist[0])
    if scale:
        max = 0
        for h in hist:
            hmax = h.max()
            if hmax > max:
                max = hmax
        pixels = max
    label = int(pixels / 10)
    for i in range(1, 11):
        y = y + 45
        t.goto(x, y)
        t.down()
        t.goto(x - 10, y)
        t.up()
        t.goto(x - 15, y - 6)
        t.write("{}".format((i * label)), align="right")
    x_ratio = 709.0 / 256
    y_ratio = 450.0 / pixels
    colors = ["red", "green", "blue"]
    for j in range(len(hist)):
        h = hist[j]
        x = -354
        y = -199
        t.up()
        t.goto(x, y)
        t.down()
        t.color(colors[j])
    for i in range(256):
        x = i * x_ratio
        y = h[i] * y_ratio
        x = x - (709 / 2)
        y = y + -199
        t.goto((x, y))


def stretch(a):
    # 在gdal_array上传的图像数组中执行直方图均衡化操作
    hist = histogram(a)
    lut = []
    for b in range(0, len(hist), 256):
        # 步长尺寸
        step = reduce(operator.add, hist[b:b + 256]) / 255
        # 创建均衡的查找表
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + hist[i + b]
    gdal_array.numpy.take(lut, a, out=a)
    return a


# 直方图展示
def show_histograms(img):
    histograms = []
    arr = gdal_array.LoadFile(img)
    for b in arr:
        histograms.append(histogram(b))
        draw_histogram(histograms)
        # 获取的结果是以图片尺寸的绝对比例显示的
        # draw_histogram(histograms, scale=False)
        t.pen(shown=False)
        t.done


# 直方图均衡化生成tiff
def stretch_histograms(src):
    arr = gdal_array.LoadFile(src)
    stretched = stretch(arr)
    output = gdal_array.SaveArray(arr, "stretched.tif", format="GTiff", prototype=src)
    output = None


if __name__ == '__main__':
    img = "stretched.tif"
    # 直方图展示
    show_histograms(img)
    # 直方图均衡化生成tiff
    # stretch_histograms(img)
