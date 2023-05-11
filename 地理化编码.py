import geocoder

# 查看geocoder有哪些接口
print(dir(geocoder))
# 默认使用谷歌地图作为其引擎
g = geocoder.google("Ottawa")
print(g.geojson)
print(g.wkt)

from geopy.geocoders import Nominatim

g = Nominatim()
location = g.geocode("Ottawa")
rev = g.reverse("{}, {}".format(location.latitude, location.longitude))
print(rev)
print(location.raw)
