from math import atan2, cos, sin, degrees

# 判断杰克逊(lon1, lat1)位于比洛克西(lon2, lat2)的什么方位
lon1 = -90.21
lat1 = 32.31
lon2 = -88.95
lat2 = 30.43

angle = atan2(cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1), sin(lon2 - lon1) * cos(lat2))
bearing = (degrees(angle) + 360) % 360
print(bearing)
# 正北方向为0度，顺时针转bearing度
# 308.7992752836875  杰克逊位于比洛克西的西北方向
