"""
待补充代码：对搜索过的格子染色
"""

import matplotlib.pyplot as plt
import copy
from typing import List, Any, Tuple
from heapq import *
import time


def visualize_maze_with_path(maze, path, title: str):
    # figure=plt.figure(figsize=(len(maze[0]), len(maze)))  # 设置图形大小
    plt.imshow(
        maze, cmap="Accent", interpolation=None, vmin=0, vmax=6
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

    plt.title(title)
    # input()
    plt.pause(0.1)


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
        figure = plt.figure(figsize=(len(self.maze[0]), len(self.maze)))  # 设置图形大小

    def __str__(self) -> str:
        res = ""
        for row in self.maze_original:
            for col in row:
                res += str(col) + " "
            res += "\n"
        return res

    def run(self, type: str):
        plt.close()
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
        elif type == "dijikstra_wall":
            self.dijikstra_wall()

    def visualize(self, title: str):
        print(self.path)
        for a in self.maze:
            print(a)
        visualize_maze_with_path(self.maze, self.path, title)

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
                # and self.maze_original[nx][ny] != 3
            ):
                res.append((nx, ny))
        return res

    def dfs(self, now: tuple, post: tuple, path: List = []):
        self.maze[now[0]][now[1]] = (
            self.maze[now[0]][now[1]] + 1 if self.maze[now[0]][now[1]] != 0 else 4
        )
        self.visualize(title="DFS")
        # print(path+[now])
        if len(self.path)!=0 and len(path)>len(self.path):
            self.maze[now[0]][now[1]] = (
                self.maze[now[0]][now[1]] - 1 if self.maze[now[0]][now[1]] != 4 else 0
            )
            return
        if now == (self.n - 1, self.m - 1):
            if len(path + [now]) < len(self.path) or len(self.path) == 0:
                self.path = path + [now]
            return
        next_list = self.next(now)
        for next in next_list:
            if next in path or self.maze[next[0]][next[1]]!=0:
                continue
            self.dfs(next, now, path + [now])
        self.maze[now[0]][now[1]] = (
            self.maze[now[0]][now[1]] - 1 if self.maze[now[0]][now[1]] != 4 else 0
        )
        return

    def bfs(self):
        pq = []
        heappush(pq, State(self.Manhattan((0, 0)), 0, [(0, 0)]))
        self.maze[0][0] = 2
        while len(pq) != 0:
            self.visualize(title="BFS")
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

    def L2(self,pos:tuple):
        x,y=pos
        return (self.n-1-x)**2 + (self.n-1-y)**2

    def dijikstra(self):
        pq = []
        heappush(pq, State(0, 0, [(0, 0)]))
        self.maze[0][0] = 2
        while len(pq) != 0:
            self.visualize(title="DIJIKSTRA")
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
    
    def dijikstra_wall(self):
        pq = []
        heappush(pq, State(0, 0, [(0, 0)]))
        self.maze[0][0] = 2
        while len(pq) != 0:
            self.visualize(title="DIJIKSTRA_WALL")
            state: State = heappop(pq)
            nowx, nowy = state.path[-1]
            # print(nowx, nowy)
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
                # if self.maze[nx][ny] != 0:
                #     continue
                # if (nx,ny) in state.path:
                #     continue
                if self.maze[nx][ny]==3:
                    tx=2*nx-nowx
                    ty=2*ny-nowy
                    if (tx<0 or tx>=self.n or ty<0 or ty>=self.m) or self.maze[tx][ty]!=0:
                        continue
                    self.maze[tx][ty]=1
                    heappush(
                        pq,
                        State(
                            state.step+7,
                            state.step+1,
                            state.path+[(tx,ty)]
                        )
                    )
                if self.maze[nx][ny] != 0:
                    continue
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
            self.visualize(title="A*")
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
                        # self.L2((nx, ny)) + state.step + 1,
                        state.step + 1,
                        state.path + [(nx, ny)],
                    ),
                )


if __name__ == "__main__":
    plt.ion()

    maze = Maze()
    print(maze)

    # maze.run("dfs")
    # maze.visualize(title="DFS")

    # maze.run("dijikstra_wall")
    # maze.visualize(title="dijikstra_wall")
    # input()

    # maze.run("bfs")
    # maze.visualize(title="BFS")
    # input()
    # maze.run("dijikstra")
    # maze.visualize(title="DIJIKSTRA")
    # input()
    maze.run("A_star")
    maze.visualize(title="A*")
    input()
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
0 0 1 0 0 0 1 1 0
0 1 1 0 1 0 0 0 0
0 0 1 0 0 0 1 1 0
0 0 0 0 0 0 1 0 0
1 0 1 1 1 0 1 0 1
0 0 0 0 1 0 0 1 0
0 0 1 0 0 1 0 0 0
"""
