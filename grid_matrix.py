import copy
import numpy as np


class Grid(object):
    def __init__(self, x=None, y=None, types=0, value=0.0):
        self.x = x
        self.y = y
        self.type = types  # 类别值
        self.value = value  # 该格子的价值
        self.strategy = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.greedy_strategy = self.strategy
        self.motive_strategy = self.strategy


class GridMatrix(object):

    def __init__(self, n_width, n_height):
        self.grids = None
        self.n_height = n_height
        self.n_width = n_width
        self.init()
        self.gamma = 0.8
        self.epsilon = 0.1
        self.flag = 0

    def init(self):
        self.grids = []
        for y in range(self.n_height):
            for x in range(self.n_width):
                if x == 0 or y == 0 or x == self.n_width - 1 or y == self.n_height - 1:
                    self.grids.append(Grid(x, y, 2))
                else:
                    self.grids.append(Grid(x, y, 0))

    def print_grids(self):
        val = np.zeros((self.n_height, self.n_width))
        for y in range(self.n_height):
            for x in range(self.n_width):
                val[self.n_height - 1 - y][x] = (round(self.grids[x + y * self.n_width].value))
        print(val)
        print("end==========================")

    def set_type(self, x, y, types):
        grid = self.get_grid(x + 1, y + 1)
        grid.type = types

    def get_grid(self, x, y):
        index = x + y * self.n_width
        return self.grids[index]

    def get_reward(self, grid, action):
        next_x = grid.x + action[0]
        next_y = grid.y + action[1]
        next_grid = self.get_grid(next_x, next_y)
        if next_grid.type in [0, 2]:
            return -1
        elif next_grid.type == 1:
            return 5
        elif next_grid.type == 4:
            return -5
        elif next_grid.type == 5:
            if self.flag:
                return -1
            else:
                return 20

    def get_value(self, grid, action):
        next_x = grid.x + action[0]
        next_y = grid.y + action[1]
        next_grid = self.get_grid(next_x, next_y)
        if next_grid.type == 2:
            return grid.value
        else:
            return next_grid.value

    def get_type(self, x, y):
        grid = self.get_grid(x, y)
        return grid.type

    def update_flag(self, flag):
        self.flag = flag

    def update_value(self, strategy_type):
        new_grids = []
        for grid in self.grids:
            new_grid = copy.deepcopy(grid)
            if grid.type in [1, 2, 3, 4]:
                new_grids.append(new_grid)
                continue
            value_new = 0
            if strategy_type == "greedy":
                strategy = grid.greedy_strategy
            else:
                strategy = grid.motive_strategy
            for action in grid.strategy:
                n = len(grid.strategy)
                m = len(strategy)
                if action in strategy:
                    p = (1 - self.epsilon) / m + self.epsilon / n
                else:
                    p = self.epsilon / n
                value_new += p * (self.get_reward(grid, action) + self.gamma * self.get_value(grid, action))
            new_grid.value = value_new
            new_grids.append(new_grid)
        self.grids = new_grids

    def init_strategy(self):
        for grid in self.grids:
            if grid.type == 0:
                for s in grid.strategy:
                    if self.get_type(grid.x + s[0], grid.y + s[1]) == 3:
                        grid.strategy.remove(s)

    def update_strategy(self, is_motive):
        for grid in self.grids:
            if grid.type != 0:
                continue
            val = []
            # 考虑每步的即时收益，以及下一个状态的值函数
            maximum = round(self.get_reward(grid, grid.strategy[0]) + self.gamma * self.get_value(grid, grid.strategy[0]))
            for action in grid.strategy:
                temp = round(self.get_reward(grid, action) + self.gamma * self.get_value(grid, action))
                if temp == maximum:
                    val.append(action)
                elif temp > maximum:
                    maximum = temp
                    val.clear()
                    val.append(action)
            if is_motive:
                grid.motive_strategy = val
            else:
                grid.greedy_strategy = val
