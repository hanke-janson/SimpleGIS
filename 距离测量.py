import math

print("=====勾股定理=====")
# 杰克逊(x1, y1)  比洛克西(x2, y2) 计算两点距离
# 这里点的坐标是横轴墨卡托投影后的坐标，单位为m，x轴的位置时根据该州最西部的中央子午线定义的，y轴时根据NAD83水平基准定义的
x1 = 456456.23
y1 = 1279721.064
x2 = 576628.34
y2 = 1071740.33
x_dist = x2 - x1
y_dist = y2 - y1
dist_sq = x_dist ** 2 + y_dist ** 2
distance = math.sqrt(dist_sq)
# 计算结果准确，因为采用的投影方法在测量密西西比州的距离和面积时已经使用笛卡尔坐标优化过了
print("通过投影后的坐标得出的距离：%f km" % (distance / 1000))

# 还可以通过十进制度数进行距离测量，为了使用角度进行测量，必须先将角度转换为弧度
x1 = -90.21
y1 = 32.31
x2 = -88.95
y2 = 30.43
x_dist = math.radians(x2 - x1)
y_dist = math.radians(y2 - y1)
dist_sq = x_dist ** 2 + y_dist ** 2
dist_rad = math.sqrt(dist_sq)
#  6371.125146 km 地球半径
distance = dist_rad * 6371.125146
# 这个结果比第一次的结果多了大约11km，因此，选择不同的测量方法和地球模型获得的结果可能存在很大差异
print("通过经纬度坐标得出的距离：%f km" % distance)

print("=====半正失公式=====")
x1 = -90.212452861859035
y1 = 32.316272202663704
x2 = -88.952170968942525
y2 = 30.438559624660321
x_dist = math.radians(x2 - x1)
y_dist = math.radians(y2 - y1)
y1_rad = math.radians(y1)
y2_rad = math.radians(y2)
h = ((1 - math.cos(y_dist)) / 2) + math.cos(y1_rad) * math.cos(y2_rad) * ((1 - math.cos(x_dist)) / 2)
distance = 2 * 6371.125146 * math.asin(math.sqrt(h))
# 与勾股定理投影结果之间误差小于0.5km
print("通过经纬度坐标得出的距离：%f km" % distance)

print("=====Vincenty公式=====")
# 使用Vincenty公式计算NAD83椭球体模型中两点之间的距离
x1 = -90.212452861859035
y1 = 32.316272202663704
x2 = -88.952170968942525
y2 = 30.438559624660321
# NAD83椭球体参数
# 椭球体半长轴的长度（赤道处的半径）
a = 6378137
# 椭球体的扁平率
f = 1 / 298.257222101
# 半短轴
b = abs((1 - f) * a)
# 两点经度差
L = math.radians(x2 - x1)
# 减少的纬度（辅助球体上的纬度）
U1 = math.atan((1 - f) * math.tan(math.radians(y1)))
U2 = math.atan((1 - f) * math.tan(math.radians(y2)))
# 辅助球面上各点的经度差
lam = L

sinU1 = math.sin(U1)
cosU1 = math.cos(U1)
sinU2 = math.sin(U2)
cosU2 = math.cos(U2)

for i in range(100):
    sinLam = math.sin(lam)
    cosLam = math.cos(lam)
    sinSigma = math.sqrt((cosU2 * sinLam) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLam) ** 2)
    if (sinSigma == 0):
        # 重合点
        distance = 0
        break
    cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLam
    sigma = math.atan2(sinSigma, cosSigma)
    sinAlpha = cosU1 * cosU2 * sinLam / sinSigma
    cosSqAlpha = 1 - sinAlpha ** 2
    cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha

    if math.isnan(cos2SigmaM):
        # 赤道线
        cos2SigmaM = 0
    C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
    LP = lam
    lam = L + (1 - C) * f * sinAlpha * (
            sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM * cos2SigmaM)))
    if not abs(lam - LP) > 1e-12:
        break
uSq = cosSqAlpha * (a ** 2 - b ** 2) / b ** 2
A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (
        cosSigma * (-1 + 2 * cos2SigmaM * cos2SigmaM) - B / 6 * cos2SigmaM * (-3 + 4 * sinSigma * sinSigma) * (
        -3 + 4 * cos2SigmaM * cos2SigmaM)))
s = b * A * (sigma - deltaSigma)
distance = s
print("使用Vincenty公式计算NAD83椭球体模型中两点得出的距离：%f km" % (distance / 1000))
