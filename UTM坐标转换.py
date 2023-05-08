import utm

y = 479747.0453210057
x = 5377685.825323031
zone = 32
band = 'U'
# UTM投影坐标转经纬度坐标
to_latlon_result = utm.to_latlon(y, x, zone, band)
print(to_latlon_result)
# 经纬度坐标转UTM投影坐标
from_latlon_result = utm.from_latlon(48.551944002183426, 8.725555999988195)
print(from_latlon_result)
