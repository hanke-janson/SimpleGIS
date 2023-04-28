import struct

# 以二进制模式打开shp文件
f = open("./shp/poly.shp", "rb")
# 定位到文件头的第36个字节
f.seek(36)
# 读取8字节为单位的双精度数值(用字母d表示)，并使用结构体模块采用的小端序解析数值(用<操作符表示)
print(struct.unpack("<d", f.read(8)))
print(struct.unpack("<d", f.read(8)))
print(struct.unpack("<d", f.read(8)))
print(struct.unpack("<d", f.read(8)))
print(struct.unpack("<dd", f.read(16)))
print(struct.unpack("<dddd", f.read(32)))
