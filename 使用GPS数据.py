# 下载数据
"""
import urllib.request
import urllib.error
url = "http://git.io/vLbTv"
fileName = "./nmea.txt"
print(urllib.request.urlretrieve(url, fileName))
"""
from pynmea.streamer import NMEAStream

nmeaFile = open("nmea.txt")
nmea_stream = NMEAStream(nmeaFile)
print(nmea_stream)
next_data = nmea_stream.get_objects()
nmea_objects = []
while next_data:
    nmea_objects += next_data
    next_data = nmea_stream.get_objects()
# 解析NMEA流
# 遍历Python对象类型输出
for nmea_ob in nmea_objects:
    if hasattr(nmea_ob, "lat"):
        print(nmea_ob)
        print("Lat/Lon: ({}, {})".format(nmea_ob.lat, nmea_ob.lon))
