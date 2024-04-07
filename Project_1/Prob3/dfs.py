"""
待补充代码：对搜索过的格子染色
"""

import matplotlib.pyplot as plt
import copy
from typing import List, Any, Tuple
from heapq import *


def visualize_maze_with_path(maze, path):
    plt.figure(figsize=(len(maze[0]), len(maze)))  # 设置图形大小
    plt.imshow(
        maze, cmap="Greys", interpolation="nearest", vmin=0, vmax=3
    )  # 使用灰度色图，并关闭插值

    # 绘制路径
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, marker="o", markersize=8, color="red", linewidth=3)

    # 设置坐标轴刻度和边框
    plt.xticks(range(len(maze[0])))
    plt.yticks(range(len(maze)))
    plt.gca().set_xticks([x - 0.5 for x in range(1, len(maze[0]))], minor=True)
    plt.gca().set_yticks([y - 0.5 for y in range(1, len(maze))], minor=True)
    plt.grid(which="minor", color="black", linestyle="-", linewidth=2)

    plt.axis("on")  # 显示坐标轴
    plt.show()


class State:
    def __init__(self, cost: int, step: int, path: List[int]) -> None:
        self.cost = cost
        self.step = step
        self.path = copy.deepcopy(path)

    def __lt__(self, other):
        return (
            self.cost < other.cost
            if self.cost != other.cost
            else self.step < other.step
        )


class Maze:
    def __init__(self) -> None:
        self.n, self.m = map(int, input().strip().split())
        self.maze_original = (
            []
        )  # 0代表没有搜索过，3代表障碍物，2代表已经搜索过,1代表准备准备搜索
        for i in range(self.n):
            a = list(map(lambda x: int(x) * 3, input().strip().split()))
            self.maze_original.append(a)
        self.maze = copy.deepcopy(self.maze_original)
        self.path = []

    def __str__(self) -> str:
        res = ""
        for row in self.maze_original:
            for col in row:
                res += str(col) + " "
            res += "\n"
        return res

    def run(self, type: str):
        self.path = []
        self.maze = copy.deepcopy(self.maze_original)
        if type == "dfs":
            self.dfs((0, 0), (-1, -1), [])
        elif type == "bfs":
            self.bfs()
        elif type == "dijikstra":
            self.dijikstra()
        elif type == "A_star":
            self.A_star()

    def visualize(self):
        print(self.path)
        for a in self.maze:
            print(a)
        visualize_maze_with_path(self.maze, self.path)

    def next(self, pos: tuple) -> list[tuple]:
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        res = []
        for i in range(4):
            nx = pos[0] + dx[i]
            ny = pos[1] + dy[i]
            if (
                0 <= nx
                and nx <= self.n - 1
                and 0 <= ny
                and ny <= self.m - 1
                and self.maze_original[nx][ny] != 3
            ):
                res.append((nx, ny))
        return res

    def dfs(self, now: tuple, post: tuple, path: List = []):
        self.maze[now[0]][now[1]] = 2
        # print(path+[now])
        if now == (self.n - 1, self.m - 1):
            if len(path + [now]) < len(self.path) or len(self.path) == 0:
                self.path = path + [now]
            return
        next_list = self.next(now)
        for next in next_list:
            if next in path:
                continue
            self.dfs(next, now, path + [now])
        return

    def bfs(self):
        pq = []
        heappush(pq, State(self.Manhattan((0, 0)), 0, [(0, 0)]))
        self.maze[0][0] = 2
        while len(pq) != 0:
            state: State = heappop(pq)
            nowx, nowy = state.path[-1]
            # print(nowx, nowy)
            self.maze[nowx][nowy] = 2
            if nowx == self.n - 1 and nowy == self.m - 1:
                self.path = state.path
                return
            next_list = self.next((nowx, nowy))
            for nx, ny in next_list:
                if self.maze[nx][ny] != 0:
                    continue
                # if (nx,ny) in state.path:
                #     continue
                self.maze[nx][ny] = 1
                heappush(
                    pq,
                    State(
                        state.step + 1,
                        state.step + 1,
                        state.path + [(nx, ny)],
                    ),
                )

    def Manhattan(self, pos: tuple):
        x, y = pos
        return abs(self.n - 1 - x) + abs(self.m - 1 - y)

    def dijikstra(self):
        pq = []
        heappush(pq, State(0, 0, [(0, 0)]))
        self.maze[0][0] = 2
        while len(pq) != 0:
            state: State = heappop(pq)
            nowx, nowy = state.path[-1]
            print(nowx, nowy)
            self.maze[nowx][nowy] = 2
            if (
                nowx == self.n - 1
                and nowy == self.m - 1
                # and (len(state.path) < len(self.path) or len(self.path) == 0)
            ):
                self.path = state.path
                return
            next_list = self.next((nowx, nowy))
            for nx, ny in next_list:
                if self.maze[nx][ny] != 0:
                    continue
                # if (nx,ny) in state.path:
                #     continue
                self.maze[nx][ny] = 1
                heappush(
                    pq,
                    State(
                        state.step + 1,
                        state.step + 1,
                        state.path + [(nx, ny)],
                    ),
                )

    def A_star(self):
        pq = []
        heappush(pq, State(self.Manhattan((0, 0)), 0, [(0, 0)]))
        self.maze[0][0] = 2
        while len(pq) != 0:
            state: State = heappop(pq)
            nowx, nowy = state.path[-1]
            print(nowx, nowy)
            self.maze[nowx][nowy] = 2
            if nowx == self.n - 1 and nowy == self.m - 1:
                self.path = state.path
                return
            next_list = self.next((nowx, nowy))
            for nx, ny in next_list:
                if self.maze[nx][ny] != 0:
                    continue
                # if (nx,ny) in state.path:
                #     continue
                self.maze[nx][ny] = 1
                heappush(
                    pq,
                    State(
                        self.Manhattan((nx, ny)) + state.step + 1,
                        state.step + 1,
                        state.path + [(nx, ny)],
                    ),
                )


if __name__ == "__main__":
    maze = Maze()
    print(maze)

    # maze.run("dfs")
    # maze.visualize()

    maze.run("bfs")
    maze.visualize()

    maze.run("dijikstra")
    maze.visualize()

    maze.run("A_star")
    maze.visualize()
"""
5 5
0 1 0 0 0
0 1 0 1 0
0 0 0 0 0
0 1 1 1 0
0 0 0 1 0

5 5
0 1 0 0 0
0 1 0 1 0
0 0 0 1 0
0 1 0 1 0
0 0 0 1 0

9 9
0 0 0 0 0 0 0 0 0 
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0

9 9
0 0 0 0 0 0 0 0 0 
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 0 0 0 1 0 0
0 0 1 1 1 1 1 0 0
0 0 1 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
"""
