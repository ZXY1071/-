# -*- coding: utf-8 -*-
import sys

# 打印所有参数
print("脚本文件名：", sys.argv[0])
print("传入参数：", sys.argv[1:])
print("参数个数：", len(sys.argv)-1)

# 下面再放你的原来代码
# ...
import heapq
from typing import Dict, List, Tuple, Optional, Set
import sys


class BUPTNavigationSystem:
    def __init__(self):
        """
        初始化北京邮电大学西土城路校区导航系统
        使用邻接表存储图结构：{地点: [(相邻地点, 距离), ...]}
        """
        self.graph: Dict[str, List[Tuple[str, float]]] = {}
        self.locations: Set[str] = set()
        self.location_types: Dict[str, str] = {}  # 地点类型：教学、宿舍、生活、运动、校门等
        self.initialize_bupt_campus()

    def initialize_bupt_campus(self):
        """初始化北邮西土城路校区数据"""
        print("正在初始化北京邮电大学西土城路校区导航系统...")

        # 根据地图信息添加地点（按区域分类）
        # 教学区
        teaching_buildings = [
            ("主楼", "教学楼"),
            ("教一楼", "教学楼"),
            ("教二楼", "教学楼"),
            ("教三楼", "教学楼"),
            ("教四楼", "教学楼"),
            ("教九楼", "教学楼"),
            ("经管楼", "教学楼"),
            ("国际学院楼", "教学楼"),
            ("北通大楼", "教学楼"),
        ]

        # 宿舍区
        dormitory_buildings = [
            ("学一公寓", "宿舍"),
            ("学二公寓", "宿舍"),
            ("学三公寓", "宿舍"),
            ("学五公寓", "宿舍"),
            ("学六公寓", "宿舍"),
            ("学九公寓", "宿舍"),
            ("学十公寓", "宿舍"),
            ("学十一公寓", "宿舍"),
            ("留学生公寓", "宿舍"),
        ]

        # 生活服务区
        service_buildings = [
            ("食堂", "生活服务"),
            ("学生食堂", "生活服务"),
            ("综合服务楼", "生活服务"),
            ("学生活动中心", "生活服务"),
            ("快递站", "生活服务"),
            ("邮局", "生活服务"),
            ("校医院", "生活服务"),
            ("北邮江锦江酒店", "生活服务"),
            ("员工宿舍", "生活服务"),
            ("运输中心", "生活服务"),
        ]

        # 运动区
        sports_facilities = [
            ("体育场", "运动设施"),
            ("篮球场", "运动设施"),
            ("体育馆", "运动设施"),
        ]

        # 校门和出入口
        gates = [
            ("北门", "校门"),
            ("南门", "校门"),
            ("西门", "校门"),
            ("中门", "校门"),
            ("北三门", "校门"),
            ("东北门", "校门"),
        ]

        # 其他地点
        other_locations = [
            ("北京邮电大学附属中学", "其他"),
            ("蓟门桥", "周边"),
            ("明光桥", "周边"),
            ("明光桥北站", "周边"),
        ]

        # 添加所有地点到图中
        all_locations = (teaching_buildings + dormitory_buildings +
                         service_buildings + sports_facilities +
                         gates + other_locations)

        for location, loc_type in all_locations:
            self.graph[location] = []
            self.locations.add(location)
            self.location_types[location] = loc_type

        print(f"已添加 {len(self.locations)} 个校园地点")

        # 根据地图添加道路连接（距离为估算值，单位：米）
        self.add_campus_roads()

        print("北邮校园导航系统初始化完成！")

    def add_campus_roads(self):
        """根据北邮校园地图添加道路连接"""
        # 核心道路连接（基于地图的相对位置估算距离）
        roads = [
            # 教学区内部连接
            ("主楼", "教一楼", 80),
            ("教一楼", "教二楼", 60),
            ("教二楼", "教三楼", 60),
            ("教三楼", "教四楼", 70),
            ("教四楼", "北通大楼", 50),
            ("北通大楼", "国际学院楼", 120),
            ("国际学院楼", "经管楼", 150),
            ("经管楼", "教九楼", 100),

            # 宿舍区连接
            ("学一公寓", "学二公寓", 40),
            ("学二公寓", "学三公寓", 40),
            ("学三公寓", "学五公寓", 60),
            ("学五公寓", "学六公寓", 70),
            ("学六公寓", "学九公寓", 90),
            ("学九公寓", "学十公寓", 50),
            ("学十公寓", "学十一公寓", 50),
            ("留学生公寓", "学五公寓", 80),

            # 生活服务区连接
            ("食堂", "学生食堂", 30),
            ("食堂", "综合服务楼", 60),
            ("综合服务楼", "学生活动中心", 40),
            ("学生活动中心", "快递站", 70),
            ("快递站", "邮局", 50),
            ("邮局", "校医院", 100),
            ("校医院", "北邮江锦江酒店", 120),
            ("北邮江锦江酒店", "员工宿舍", 80),
            ("员工宿舍", "运输中心", 90),

            # 运动区连接
            ("体育场", "篮球场", 50),
            ("篮球场", "体育馆", 60),

            # 校门连接
            ("北门", "快递站", 30),
            ("北门", "经管楼", 100),
            ("西门", "北通大楼", 40),
            ("西门", "明光桥", 200),
            ("南门", "教二楼", 50),
            ("南门", "北京邮电大学附属中学", 150),
            ("中门", "校医院", 30),
            ("中门", "邮局", 40),
            ("北三门", "邮局", 30),
            ("东北门", "食堂", 60),

            # 跨区域连接
            ("教四楼", "学一公寓", 120),
            ("教九楼", "学九公寓", 80),
            ("经管楼", "学六公寓", 60),
            ("学生活动中心", "学十公寓", 70),
            ("综合服务楼", "学十一公寓", 60),
            ("食堂", "学五公寓", 90),
            ("体育场", "南门", 110),
            ("篮球场", "教二楼", 130),

            # 周边连接
            ("西门", "明光桥北站", 150),
            ("北门", "蓟门桥", 200),
            ("蓟门桥", "明光桥", 500),
        ]

        # 添加所有道路
        for road in roads:
            building1, building2, distance = road
            if building1 in self.graph and building2 in self.graph:
                self.graph[building1].append((building2, distance))
                self.graph[building2].append((building1, distance))

        print(f"已添加 {len(roads)} 条校园道路")

    def add_location(self, name: str, loc_type: str = "其他") -> bool:
        """添加地点"""
        if name in self.graph:
            print(f"地点 '{name}' 已存在!")
            return False
        self.graph[name] = []
        self.locations.add(name)
        self.location_types[name] = loc_type
        print(f"成功添加地点: {name} ({loc_type})")
        return True

    def remove_location(self, name: str) -> bool:
        """删除地点"""
        if name not in self.graph:
            print(f"地点 '{name}' 不存在!")
            return False

        # 删除该地点
        del self.graph[name]
        self.locations.remove(name)
        if name in self.location_types:
            del self.location_types[name]

        # 删除其他地点指向该地点的边
        for location in self.graph:
            self.graph[location] = [
                (neighbor, dist) for neighbor, dist in self.graph[location]
                if neighbor != name
            ]

        print(f"成功删除地点: {name}")
        return True

    def add_road(self, location1: str, location2: str, distance: float) -> bool:
        """添加道路（双向边）"""
        if location1 not in self.graph or location2 not in self.graph:
            print("错误: 地点不存在!")
            return False

        # 检查道路是否已存在
        for neighbor, _ in self.graph[location1]:
            if neighbor == location2:
                print(f"道路 {location1} - {location2} 已存在!")
                return False

        # 添加双向边
        self.graph[location1].append((location2, distance))
        self.graph[location2].append((location1, distance))

        print(f"成功添加道路: {location1} <-- {distance}米 --> {location2}")
        return True

    def remove_road(self, location1: str, location2: str) -> bool:
        """删除道路"""
        if location1 not in self.graph or location2 not in self.graph:
            print("错误: 地点不存在!")
            return False

        # 删除双向边
        original_len1 = len(self.graph[location1])
        original_len2 = len(self.graph[location2])

        self.graph[location1] = [
            (neighbor, dist) for neighbor, dist in self.graph[location1]
            if neighbor != location2
        ]
        self.graph[location2] = [
            (neighbor, dist) for neighbor, dist in self.graph[location2]
            if neighbor != location1
        ]

        if len(self.graph[location1]) < original_len1 and len(self.graph[location2]) < original_len2:
            print(f"成功删除道路: {location1} -- {location2}")
            return True
        else:
            print(f"错误: {location1} 和 {location2} 之间没有道路!")
            return False

    def dijkstra_shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """
        使用Dijkstra算法查找最短路径
        返回: (路径列表, 总距离)
        """
        if start not in self.graph or end not in self.graph:
            print(f"错误: 起点 '{start}' 或终点 '{end}' 不存在!")
            return [], float('inf')

        # 初始化距离和前驱节点
        distances = {location: float('inf') for location in self.graph}
        predecessors = {location: None for location in self.graph}
        distances[start] = 0

        # 使用优先队列
        pq = [(0, start)]

        while pq:
            current_dist, current_location = heapq.heappop(pq)

            # 如果已经找到到当前节点的更短路径，跳过
            if current_dist > distances[current_location]:
                continue

            # 到达目标节点
            if current_location == end:
                break

            # 遍历邻居
            for neighbor, weight in self.graph[current_location]:
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_location
                    heapq.heappush(pq, (distance, neighbor))

        # 如果无法到达目标节点
        if distances[end] == float('inf'):
            return [], float('inf')

        # 重构路径
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return path, distances[end]

    def find_nearest_facility(self, start: str, facility_type: str) -> Tuple[str, List[str], float]:
        """
        查找最近的特定类型设施
        facility_type: "教学楼", "宿舍", "生活服务", "运动设施", "食堂", "校门"
        """
        if start not in self.graph:
            print(f"错误: 起点 '{start}' 不存在!")
            return "", [], float('inf')

        # 筛选目标类型的地点
        target_locations = [
            loc for loc in self.locations
            if self.location_types.get(loc) == facility_type and loc != start
        ]

        if not target_locations:
            print(f"没有找到类型为 '{facility_type}' 的设施!")
            return "", [], float('inf')

        # 查找最近的目标
        nearest_location = ""
        shortest_path = []
        min_distance = float('inf')

        for target in target_locations:
            path, distance = self.dijkstra_shortest_path(start, target)
            if path and distance < min_distance:
                min_distance = distance
                shortest_path = path
                nearest_location = target

        return nearest_location, shortest_path, min_distance

    def bfs_traversal(self, start: str) -> List[str]:
        """广度优先遍历"""
        if start not in self.graph:
            print(f"错误: 起点 '{start}' 不存在!")
            return []

        visited = set()
        result = []
        queue = [start]

        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                result.append(current)

                # 按字母顺序添加邻居
                neighbors = sorted([neighbor for neighbor, _ in self.graph[current]])
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    def dfs_traversal(self, start: str) -> List[str]:
        """深度优先遍历"""
        if start not in self.graph:
            print(f"错误: 起点 '{start}' 不存在!")
            return []

        visited = set()
        result = []

        def dfs(location: str):
            visited.add(location)
            result.append(location)

            # 按字母顺序遍历邻居
            neighbors = sorted([neighbor for neighbor, _ in self.graph[location]])
            for neighbor in neighbors:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(start)
        return result

    def get_location_type(self, location: str) -> str:
        """获取地点类型"""
        return self.location_types.get(location, "未知")

    def get_locations_by_type(self, loc_type: str) -> List[str]:
        """按类型筛选地点"""
        return sorted([loc for loc in self.locations if self.location_types.get(loc) == loc_type])

    def print_path_description(self, path: List[str], distance: float) -> str:
        """生成路径文字描述"""
        if not path:
            return "无法到达目标地点!"

        description = f"路径规划: {' -> '.join(path)}\n"
        description += f"总距离: {distance:.2f} 米 (约 {distance / 80:.1f} 分钟步行)\n\n"
        description += "详细路线:\n"

        total_time = 0
        for i in range(len(path) - 1):
            # 查找两地点间的实际距离
            for neighbor, dist in self.graph[path[i]]:
                if neighbor == path[i + 1]:
                    walk_time = dist / 80  # 按步行速度80米/分钟计算
                    total_time += walk_time
                    location_type = self.get_location_type(path[i])
                    description += f"{i + 1}. 从 {path[i]} ({location_type}) 到 {path[i + 1]}, 距离: {dist:.0f}米, 步行约{walk_time:.1f}分钟\n"
                    break

        description += f"\n总计: {len(path) - 1}段路程，总步行时间约{total_time:.1f}分钟\n"
        return description

    def print_campus_map(self) -> str:
        """生成北邮校园简易地图"""
        if not self.graph:
            return "校园地图为空!"

        map_str = "=" * 70 + "\n"
        map_str += "北京邮电大学西土城路校区导航地图\n"
        map_str += "=" * 70 + "\n"

        # 按类型分组显示地点
        location_types = ["教学楼", "宿舍", "生活服务", "运动设施", "校门", "周边", "其他"]

        for loc_type in location_types:
            locations_of_type = self.get_locations_by_type(loc_type)
            if locations_of_type:
                map_str += f"\n[{loc_type}]:\n"
                for location in locations_of_type:
                    # 获取连接信息
                    connections = []
                    for neighbor, dist in self.graph[location]:
                        connections.append(f"{neighbor}({dist:.0f}m)")

                    if connections:
                        map_str += f"  {location:15} → 连接: {', '.join(connections[:3])}"
                        if len(connections) > 3:
                            map_str += f" 等{len(connections)}处"
                        map_str += "\n"
                    else:
                        map_str += f"  {location:15} → (暂无连接)\n"

        # 统计信息
        map_str += "\n" + "=" * 70 + "\n"
        map_str += f"校园统计: {len(self.locations)}个地点，{sum(len(neighbors) for neighbors in self.graph.values()) // 2}条道路\n"
        map_str += "=" * 70

        return map_str

    def display_locations_by_type(self) -> None:
        """按类型显示所有地点"""
        if not self.locations:
            print("校园中暂无地点!")
            return

        print("=" * 60)
        print("北邮校园地点分类列表")
        print("=" * 60)

        for loc_type in ["教学楼", "宿舍", "生活服务", "运动设施", "校门", "周边", "其他"]:
            locations = self.get_locations_by_type(loc_type)
            if locations:
                print(f"\n【{loc_type}】 ({len(locations)}个):")
                for i, location in enumerate(locations, 1):
                    connections = len(self.graph[location])
                    print(f"  {i:2d}. {location:15} (连接{connections}处)")

        print("\n" + "=" * 60)


def demo_bupt_navigation():
    """演示北邮校园导航系统"""
    print("=" * 70)
    print("北京邮电大学西土城路校区导航系统")
    print("=" * 70)

    # 创建北邮导航系统实例
    bupt = BUPTNavigationSystem()

    # 1. 显示校园地图
    print("\n1. 北邮校园地图:")
    print(bupt.print_campus_map())

    # 2. 按类型显示地点
    bupt.display_locations_by_type()

    # 3. 典型路径查询示例
    print("\n2. 典型路径查询示例:")

    # 示例1: 宿舍到教学楼
    print("\n【示例1】从宿舍到教学楼的最短路径:")
    start1 = "学六公寓"
    end1 = "教四楼"
    path1, dist1 = bupt.dijkstra_shortest_path(start1, end1)
    if path1:
        print(f"查询: {start1} → {end1}")
        print(bupt.print_path_description(path1, dist1))
    else:
        print(f"无法从 {start1} 到达 {end1}!")

    # 示例2: 食堂到快递站
    print("\n【示例2】从食堂到快递站的最短路径:")
    start2 = "食堂"
    end2 = "快递站"
    path2, dist2 = bupt.dijkstra_shortest_path(start2, end2)
    if path2:
        print(f"查询: {start2} → {end2}")
        print(bupt.print_path_description(path2, dist2))
    else:
        print(f"无法从 {start2} 到达 {end2}!")

    # 示例3: 西门到南门
    print("\n【示例3】从西门到南门的最短路径:")
    start3 = "西门"
    end3 = "南门"
    path3, dist3 = bupt.dijkstra_shortest_path(start3, end3)
    if path3:
        print(f"查询: {start3} → {end3}")
        print(bupt.print_path_description(path3, dist3))
    else:
        print(f"无法从 {start3} 到达 {end3}!")

    # 4. 查找最近设施
    print("\n3. 查找最近设施功能:")

    # 查找最近的教学楼
    print("\n【查找最近的教学楼】")
    start = "学十公寓"
    facility_type = "教学楼"
    nearest, path, dist = bupt.find_nearest_facility(start, facility_type)
    if nearest:
        print(f"从 {start} 出发，最近的{facility_type}是: {nearest}")
        print(f"路径: {' -> '.join(path)}")
        print(f"距离: {dist:.0f}米")
    else:
        print(f"没有找到从 {start} 出发的最近{facility_type}!")

    # 查找最近的食堂
    print("\n【查找最近的食堂】")
    start = "教四楼"
    facility_type = "生活服务"
    nearest, path, dist = bupt.find_nearest_facility(start, facility_type)
    if nearest:
        print(f"从 {start} 出发，最近的生活服务设施是: {nearest}")
        print(f"路径: {' -> '.join(path)}")
        print(f"距离: {dist:.0f}米")
    else:
        print(f"没有找到从 {start} 出发的最近{facility_type}!")

    # 5. 图的遍历
    print("\n4. 校园地点遍历演示:")

    # BFS遍历
    print("\n【广度优先遍历】从主楼出发:")
    bfs_result = bupt.bfs_traversal("主楼")
    print(f"遍历了 {len(bfs_result)} 个地点: {' -> '.join(bfs_result[:10])}...")

    # DFS遍历
    print("\n【深度优先遍历】从主楼出发:")
    dfs_result = bupt.dfs_traversal("主楼")
    print(f"遍历了 {len(dfs_result)} 个地点: {' -> '.join(dfs_result[:10])}...")

    # 6. 动态修改校园结构演示
    print("\n5. 动态修改校园结构演示:")

    # 添加新地点（根据地图可能缺少的地点）
    print("\n【添加新地点】")
    bupt.add_location("图书馆", "教学楼")
    bupt.add_location("游泳馆", "运动设施")
    bupt.add_road("图书馆", "主楼", 80)
    bupt.add_road("游泳馆", "体育场", 60)

    # 查询新路径
    print("\n【查询到新地点的路径】")
    start4 = "图书馆"
    end4 = "游泳馆"
    path4, dist4 = bupt.dijkstra_shortest_path(start4, end4)
    if path4:
        print(f"查询: {start4} → {end4}")
        print(bupt.print_path_description(path4, dist4))
    else:
        print(f"无法从 {start4} 到达 {end4}!")

    # 7. 完整校园地图
    print("\n6. 完整校园地图（更新后）:")
    print(bupt.print_campus_map())

    print("\n" + "=" * 70)
    print("北邮校园导航系统演示结束！")
    print("=" * 70)


def interactive_bupt_mode():
    """北邮校园交互式导航模式"""
    bupt = BUPTNavigationSystem()

    while True:
        print("\n" + "=" * 70)
        print("北京邮电大学西土城路校区导航系统 - 交互模式")
        print("=" * 70)
        print("1. 显示校园地图")
        print("2. 按类型显示所有地点")
        print("3. 查询最短路径")
        print("4. 查找最近设施")
        print("5. 添加新地点")
        print("6. 添加新道路")
        print("7. 删除地点")
        print("8. 删除道路")
        print("9. 广度优先遍历")
        print("10. 深度优先遍历")
        print("0. 退出系统")
        print("=" * 70)

        choice = input("请选择操作 (0-10): ").strip()

        if choice == "0":
            print("感谢使用北邮校园导航系统!")
            break

        elif choice == "1":
            print("\n" + bupt.print_campus_map())

        elif choice == "2":
            bupt.display_locations_by_type()

        elif choice == "3":
            print("\n可用的地点:")
            locations = sorted(list(bupt.locations))
            for i, loc in enumerate(locations, 1):
                print(f"{i:3d}. {loc:15} ({bupt.get_location_type(loc)})")

            start = input("\n请输入起点: ").strip()
            end = input("请输入终点: ").strip()

            if start not in bupt.locations or end not in bupt.locations:
                print("错误: 输入的地点不存在，请检查拼写!")
            else:
                path, dist = bupt.dijkstra_shortest_path(start, end)
                if path:
                    print("\n" + "=" * 60)
                    print(f"路径规划: {start} → {end}")
                    print("=" * 60)
                    print(bupt.print_path_description(path, dist))
                else:
                    print(f"\n无法从 {start} 到达 {end}!")

        elif choice == "4":
            print("\n可查找的设施类型: 教学楼, 宿舍, 生活服务, 运动设施, 校门")
            start = input("请输入当前位置: ").strip()
            facility_type = input("请输入要查找的设施类型: ").strip()

            if start not in bupt.locations:
                print("错误: 起点不存在!")
            else:
                nearest, path, dist = bupt.find_nearest_facility(start, facility_type)
                if nearest:
                    print("\n" + "=" * 60)
                    print(f"最近{facility_type}查找结果")
                    print("=" * 60)
                    print(f"当前位置: {start}")
                    print(f"最近{facility_type}: {nearest}")
                    print(f"距离: {dist:.0f}米 (约{dist / 80:.1f}分钟步行)")
                    print(f"路径: {' -> '.join(path)}")
                else:
                    print(f"没有找到从 {start} 出发的最近{facility_type}!")

        elif choice == "5":
            name = input("请输入新地点名称: ").strip()
            print("可选的类型: 教学楼, 宿舍, 生活服务, 运动设施, 校门, 周边, 其他")
            loc_type = input("请输入地点类型: ").strip()
            bupt.add_location(name, loc_type)

        elif choice == "6":
            print("\n当前所有地点:")
            locations = sorted(list(bupt.locations))
            for i, loc in enumerate(locations, 1):
                if i % 5 == 0 or i == len(locations):
                    print(f"{i:3d}. {loc:15}")
                else:
                    print(f"{i:3d}. {loc:15}", end="  ")

            location1 = input("\n请输入第一个地点: ").strip()
            location2 = input("请输入第二个地点: ").strip()
            try:
                distance = float(input("请输入距离(米): ").strip())
                bupt.add_road(location1, location2, distance)
            except ValueError:
                print("错误: 距离必须是数字!")

        elif choice == "7":
            name = input("请输入要删除的地点名称: ").strip()
            bupt.remove_location(name)

        elif choice == "8":
            location1 = input("请输入第一个地点: ").strip()
            location2 = input("请输入第二个地点: ").strip()
            bupt.remove_road(location1, location2)

        elif choice == "9":
            start = input("请输入起始地点: ").strip()
            if start in bupt.locations:
                result = bupt.bfs_traversal(start)
                if result:
                    print(f"\n广度优先遍历结果 (共{len(result)}个地点):")
                    for i, loc in enumerate(result, 1):
                        print(f"{i:3d}. {loc:15} ({bupt.get_location_type(loc)})")
                else:
                    print("错误: 无法遍历!")
            else:
                print("错误: 地点不存在!")

        elif choice == "10":
            start = input("请输入起始地点: ").strip()
            if start in bupt.locations:
                result = bupt.dfs_traversal(start)
                if result:
                    print(f"\n深度优先遍历结果 (共{len(result)}个地点):")
                    for i, loc in enumerate(result, 1):
                        print(f"{i:3d}. {loc:15} ({bupt.get_location_type(loc)})")
                else:
                    print("错误: 无法遍历!")
            else:
                print("错误: 地点不存在!")

        else:
            print("无效选择，请重新输入!")

        input("\n按回车键继续...")


def main_menu():
    """主菜单"""
    print("=" * 70)
    print("北京邮电大学西土城路校区导航系统")
    print("北邮人团队 2025.08 出品")
    print("=" * 70)
    print("\n基于北邮西土城路校区真实地图构建")
    print("包含教学楼、宿舍、生活服务设施等完整校园地点")
    print("\n请选择运行模式:")
    print("1. 完整功能演示 (推荐首次使用)")
    print("2. 交互导航模式 (自定义查询)")
    print("3. 退出系统")

    while True:
        choice = input("\n请选择模式 (1-3): ").strip()

        if choice == "1":
            demo_bupt_navigation()
            input("\n演示结束，按回车键返回主菜单...")
            return True
        elif choice == "2":
            interactive_bupt_mode()
            input("\n交互模式结束，按回车键返回主菜单...")
            return True
        elif choice == "3":
            print("感谢使用北邮校园导航系统，再见！")
            return False
        else:
            print("无效选择，请重新输入!")


if __name__ == "__main__":
    # 显示欢迎信息
    print("=" * 70)
    print("欢迎使用北京邮电大学西土城路校区导航系统")
    print("=" * 70)
    print("系统特点:")
    print("1. 基于真实北邮校园地图构建")
    print("2. 包含教学楼、宿舍、食堂、运动场等完整设施")
    print("3. 支持最短路径查询和最近设施查找")
    print("4. 支持校园地图的动态修改")
    print("=" * 70)

    # 运行主菜单
    while main_menu():
        pass