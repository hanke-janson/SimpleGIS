import turtle as t

# 名称，坐标，人口数索引
NAME = 0
POINTS = 1
POP = 2
# 州
state = ["COLORADO", [[-109, 37], [-109, 41], [-102, 41], [-102, 37]], 5187582]
# 城市列表
cities = []
cities.append(["DENVER", [-104.98, 39.74], 634265])
cities.append(["BOULDER", [-105.27, 40.02], 98889])
cities.append(["DENVER", [-107.88, 37.28], 17069])
# 地图尺寸
map_width = 400
map_height = 300
# 经纬度范围
minx = 180
maxx = -180
miny = 90
maxy = -90
# 匹配地图和绘图版尺寸
for x, y in state[POINTS]:
    if x < minx:
        minx = x
    elif x > maxx:
        maxx = x
    if y < miny:
        miny = y
    elif y > maxy:
        maxy = y
# 计算州和绘图板之间的缩放比例
dist_x = maxx - minx
dist_y = maxy - miny
x_ratio = map_width / dist_x
y_ratio = map_height / dist_y


# 用于将经纬度转换为屏幕坐标
def convert(point):
    lon = point[0]
    lat = point[1]
    x = map_width - ((maxx - lon) * x_ratio)
    y = map_height - ((maxy - lat) * y_ratio)
    # turtle的坐标原点在画板中心
    x = x - (map_width / 2)
    y = y - (map_height / 2)
    return [x, y]


# 绘制州
t.up()
first_pixel = None
for point in state[POINTS]:
    pixel = convert(point)
    if not first_pixel:
        first_pixel = pixel
    t.goto(pixel)
    t.down()
t.goto(first_pixel)
t.up()
t.goto([0, 0])
t.write(state[NAME], align="center", font=("Arial", 16, "bold"))

# 绘制城市
for city in cities:
    pixel = convert(city[POINTS])
    t.up()
    t.goto(pixel)
    # 绘制城市位置
    t.dot(10)
    # 标记城市
    t.write(city[NAME] + ", Pop.:" + str(city[POP]), align="left")
    # GIS属性查询
    # 哪个城市的人口最多？
    biggest_city = max(cities, key=lambda city: city[POP])
    t.goto(0, -200)
    t.write("人口最多的城市是：" + biggest_city[NAME])
    # 哪个城市离西部最远？
    western_city = min(cities, key=lambda city: city[POINTS])
    t.goto(0, -220)
    t.write("离西部最远的城市是：" + western_city[NAME])
# 隐藏画笔
t.pen(shown=False)
# 运行代码后不关闭窗口
t.done()
