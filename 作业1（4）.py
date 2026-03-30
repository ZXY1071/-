import heapq
from typing import List, Tuple, Optional, Dict, Any


class CampusNavigationSystem:
    """校园导航系统类"""

    def __init__(self):
        """初始化校园导航系统"""
        # 顶点列表：存储建筑名称
        self.vertices = []
        # 顶点到索引的映射
        self.vertex_to_index = {}
        # 邻接矩阵存储图的边权重（距离）
        self.adj_matrix = []
        # 建筑信息字典（可扩展存储更多信息）
        self.building_info = {}

    def add_building(self, name: str, info: str = "") -> bool:
        """添加建筑到图中

        Args:
            name: 建筑名称
            info: 建筑相关信息

        Returns:
            添加成功返回True，已存在返回False
        """
        if name in self.vertex_to_index:
            print(f"建筑 '{name}' 已存在!")
            return False

        # 添加新顶点
        self.vertices.append(name)
        self.vertex_to_index[name] = len(self.vertices) - 1
        self.building_info[name] = info

        # 扩展邻接矩阵
        n = len(self.vertices)
        if n == 1:
            # 第一个顶点
            self.adj_matrix = [[float('inf')]]
        else:
            # 扩展矩阵，新行新列初始化为无穷大
            for row in self.adj_matrix:
                row.append(float('inf'))
            new_row = [float('inf')] * n
            self.adj_matrix.append(new_row)

        # 对角线设为0（自己到自己的距离为0）
        self.adj_matrix[-1][-1] = 0

        print(f"建筑 '{name}' 添加成功!")
        return True

    def remove_building(self, name: str) -> bool:
        """从图中删除建筑

        Args:
            name: 要删除的建筑名称

        Returns:
            删除成功返回True，不存在返回False
        """
        if name not in self.vertex_to_index:
            print(f"建筑 '{name}' 不存在!")
            return False

        # 获取要删除的顶点索引
        idx = self.vertex_to_index[name]
        n = len(self.vertices)

        # 删除顶点
        self.vertices.pop(idx)
        del self.vertex_to_index[name]
        del self.building_info[name]

        # 更新顶点到索引的映射
        for i, vertex in enumerate(self.vertices):
            self.vertex_to_index[vertex] = i

        # 从邻接矩阵中删除对应的行和列
        # 删除行
        self.adj_matrix.pop(idx)
        # 删除列
        for row in self.adj_matrix:
            row.pop(idx)

        print(f"建筑 '{name}' 删除成功!")
        return True

    def add_road(self, building1: str, building2: str, distance: float, bidirectional: bool = True) -> bool:
        """添加道路（边）

        Args:
            building1: 建筑1名称
            building2: 建筑2名称
            distance: 距离
            bidirectional: 是否为双向道路

        Returns:
            添加成功返回True，失败返回False
        """
        if building1 not in self.vertex_to_index:
            print(f"建筑 '{building1}' 不存在!")
            return False

        if building2 not in self.vertex_to_index:
            print(f"建筑 '{building2}' 不存在!")
            return False

        idx1 = self.vertex_to_index[building1]
        idx2 = self.vertex_to_index[building2]

        if distance <= 0:
            print("距离必须大于0!")
            return False

        # 添加边
        self.adj_matrix[idx1][idx2] = distance
        if bidirectional:
            self.adj_matrix[idx2][idx1] = distance
            print(f"双向道路 '{building1}' ↔ '{building2}' 添加成功，距离: {distance}")
        else:
            print(f"单向道路 '{building1}' → '{building2}' 添加成功，距离: {distance}")

        return True

    def remove_road(self, building1: str, building2: str, bidirectional: bool = True) -> bool:
        """删除道路（边）

        Args:
            building1: 建筑1名称
            building2: 建筑2名称
            bidirectional: 是否为双向删除

        Returns:
            删除成功返回True，失败返回False
        """
        if building1 not in self.vertex_to_index:
            print(f"建筑 '{building1}' 不存在!")
            return False

        if building2 not in self.vertex_to_index:
            print(f"建筑 '{building2}' 不存在!")
            return False

        idx1 = self.vertex_to_index[building1]
        idx2 = self.vertex_to_index[building2]

        # 删除边
        if self.adj_matrix[idx1][idx2] == float('inf'):
            print(f"道路 '{building1}' 到 '{building2}' 不存在!")
            return False

        self.adj_matrix[idx1][idx2] = float('inf')
        if bidirectional:
            self.adj_matrix[idx2][idx1] = float('inf')
            print(f"双向道路 '{building1}' ↔ '{building2}' 删除成功")
        else:
            print(f"单向道路 '{building1}' → '{building2}' 删除成功")

        return True

    def dijkstra_shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """使用Dijkstra算法计算最短路径

        Args:
            start: 起点建筑名称
            end: 终点建筑名称

        Returns:
            (路径列表, 总距离) 如果路径存在
            ([], float('inf')) 如果路径不存在
        """
        if start not in self.vertex_to_index:
            print(f"起点建筑 '{start}' 不存在!")
            return [], float('inf')

        if end not in self.vertex_to_index:
            print(f"终点建筑 '{end}' 不存在!")
            return [], float('inf')

        start_idx = self.vertex_to_index[start]
        end_idx = self.vertex_to_index[end]
        n = len(self.vertices)

        # 初始化距离和前驱节点
        dist = [float('inf')] * n
        prev = [-1] * n
        visited = [False] * n

        dist[start_idx] = 0

        # 优先队列 (距离, 顶点索引)
        pq = [(0, start_idx)]

        while pq:
            current_dist, u = heapq.heappop(pq)

            if visited[u]:
                continue

            visited[u] = True

            # 如果找到终点，提前结束
            if u == end_idx:
                break

            # 遍历邻居
            for v in range(n):
                if not visited[v] and self.adj_matrix[u][v] != float('inf'):
                    new_dist = current_dist + self.adj_matrix[u][v]
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        prev[v] = u
                        heapq.heappush(pq, (new_dist, v))

        # 如果终点不可达
        if dist[end_idx] == float('inf'):
            print(f"从 '{start}' 到 '{end}' 没有可达路径!")
            return [], float('inf')

        # 重建路径
        path = []
        current = end_idx
        while current != -1:
            path.append(self.vertices[current])
            current = prev[current]

        path.reverse()

        return path, dist[end_idx]

    def floyd_all_pairs(self) -> List[List[float]]:
        """使用Floyd算法计算所有顶点对之间的最短距离

        Returns:
            距离矩阵
        """
        n = len(self.vertices)

        # 初始化距离矩阵
        dist = [row[:] for row in self.adj_matrix]

        # Floyd算法
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        return dist

    def bfs_traversal(self, start: str) -> List[str]:
        """广度优先遍历

        Args:
            start: 起始建筑名称

        Returns:
            遍历顺序列表
        """
        if start not in self.vertex_to_index:
            print(f"起始建筑 '{start}' 不存在!")
            return []

        start_idx = self.vertex_to_index[start]
        n = len(self.vertices)
        visited = [False] * n
        result = []

        # BFS队列
        queue = [start_idx]
        visited[start_idx] = True

        while queue:
            u = queue.pop(0)
            result.append(self.vertices[u])

            # 遍历邻居
            for v in range(n):
                if not visited[v] and self.adj_matrix[u][v] != float('inf'):
                    visited[v] = True
                    queue.append(v)

        return result

    def dfs_traversal(self, start: str) -> List[str]:
        """深度优先遍历

        Args:
            start: 起始建筑名称

        Returns:
            遍历顺序列表
        """
        if start not in self.vertex_to_index:
            print(f"起始建筑 '{start}' 不存在!")
            return []

        start_idx = self.vertex_to_index[start]
        n = len(self.vertices)
        visited = [False] * n
        result = []

        # 递归DFS辅助函数
        def dfs_util(u: int):
            visited[u] = True
            result.append(self.vertices[u])

            # 遍历邻居
            for v in range(n):
                if not visited[v] and self.adj_matrix[u][v] != float('inf'):
                    dfs_util(v)

        dfs_util(start_idx)
        return result

    def print_path_description(self, path: List[str], distance: float):
        """打印路径描述

        Args:
            path: 路径列表
            distance: 总距离
        """
        if not path:
            print("没有有效路径!")
            return

        print(f"路径描述: {' → '.join(path)}")
        print(f"总距离: {distance}")

        # 打印详细路径
        print("详细路线:")
        for i in range(len(path) - 1):
            start_idx = self.vertex_to_index[path[i]]
            end_idx = self.vertex_to_index[path[i + 1]]
            dist = self.adj_matrix[start_idx][end_idx]
            print(f"  {path[i]} → {path[i + 1]}: {dist}")

    def print_simple_map(self):
        """打印简易地图（邻接矩阵表示）"""
        n = len(self.vertices)

        print("\n简易校园地图 (邻接矩阵表示):")
        print("=" * 60)

        # 打印表头
        header = "建筑名称" + " " * 8
        for vertex in self.vertices:
            header += f"{vertex[:8]:8}"
        print(header)

        # 打印矩阵
        for i in range(n):
            row_str = f"{self.vertices[i]:15}"
            for j in range(n):
                if self.adj_matrix[i][j] == float('inf'):
                    row_str += "∞".center(8)
                else:
                    row_str += f"{self.adj_matrix[i][j]:8.1f}"
            print(row_str)

        print("=" * 60)

    def get_all_buildings(self) -> List[str]:
        """获取所有建筑列表"""
        return self.vertices.copy()

    def get_road_info(self, building1: str, building2: str) -> Optional[float]:
        """获取两个建筑之间的道路信息

        Args:
            building1: 建筑1名称
            building2: 建筑2名称

        Returns:
            距离，如果道路不存在返回None
        """
        if building1 not in self.vertex_to_index or building2 not in self.vertex_to_index:
            return None

        idx1 = self.vertex_to_index[building1]
        idx2 = self.