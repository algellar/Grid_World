import gym
import random
import time
from grid_matrix import GridMatrix
from gym.envs.classic_control import rendering


class GridWorldEnv(gym.Env):
    def __init__(self, n_width, n_height, u_size, start):
        self.n_width = n_width + 2  # 格子世界宽度（以格子数计）
        self.n_height = n_height + 2  # 高度
        self.u_size = u_size  # 当前格子绘制尺寸
        self.width = u_size * self.n_width  # 场景宽度
        self.height = u_size * self.n_height  # 场景长度
        self.grids = GridMatrix(n_width=self.n_width, n_height=self.n_height)

        self.ends = []  # 终止格子坐标
        self.wall = []
        self.bound = []
        self.trap = []
        self.motive = []
        self.start = (start[0] + 1, start[1] + 1)  # 起始格子坐标
        self.state = self.start
        self.types = []  # 特殊种类的格子
        self.viewer = None  # 图形接口对象
        self.agent = None
        self.agent_trans = None
        self.motive_agent = None

    def step(self, strategy):
        num = len(strategy)
        rand = random.randint(0, num - 1)
        action = strategy[rand]
        next_x = self.state[0] + action[0]
        next_y = self.state[1] + action[1]
        next_grid = self.grids.get_grid(next_x, next_y)
        if next_grid.type in [0, 1, 4, 5]:
            self.state = (next_x, next_y)
            if next_grid.type == 1:
                return 1
            elif next_grid.type == 4:
                return 4
            elif next_grid.type == 5:
                return 5
        return 0

    def perform(self):
        self.grids.init_strategy()
        updated = 0
        print("updated:", updated)
        self.grids.print_grids()
        # for _ in range(10):
        #     self.grids.update_value(strategy_type="greedy")
        # self.grids.print_grids()
        # self.grids.update_strategy(is_motive=0)
        steps = 0
        for _ in range(20):
            while True:
                steps += 1
                self.render()
                time.sleep(0.2)
                cur_grid = self.grids.get_grid(self.state[0], self.state[1])
                rand = random.random()
                if rand > self.grids.epsilon:
                    if self.grids.flag == 0:
                        strategy = cur_grid.greedy_strategy
                    else:
                        strategy = cur_grid.motive_strategy
                else:
                    strategy = cur_grid.strategy
                state = self.step(strategy)
                if state == 1:
                    print("steps:", steps)
                    steps = 0
                    self.render()
                    break
                elif state == 4:
                    self.render()
                    self.state = self.start
                elif state == 5:
                    if not self.grids.flag:
                        self.grids.update_flag(flag=1)
                        self.motive_agent.set_color(0.9, 0.9, 0.9)
                        for _ in range(9):
                            self.grids.update_value(strategy_type="motive")
                        self.grids.print_grids()
                        self.grids.update_strategy(is_motive=1)
            self.state = self.start
            self.grids.update_flag(0)
            self.motive_agent.set_color(0.5, 0.2, 0.7)
            self.grids.epsilon = 1 / (10 * (updated + 1))
            for _ in range(9):
                self.grids.update_value(strategy_type="greedy")
            updated += 1
            print("updated:", updated)
            self.grids.print_grids()
            self.grids.update_strategy(is_motive=0)

    def refresh_setting(self):
        """用户在使用该类创建格子世界后可能会修改格子世界某些格子类型或奖励值
        的设置，修改设置后通过调用该方法使得设置生效。
        """
        self.types = self.ends + self.wall + self.bound + self.trap + self.motive
        for x, y, t in self.types:
            self.grids.set_type(x, y, t)

    def render_grid(self, x, y):
        u_size = self.u_size
        m = 2  # 格子之间的间隙尺寸
        v = [(x * u_size + m, y * u_size + m),
             ((x + 1) * u_size - m, y * u_size + m),
             ((x + 1) * u_size - m, (y + 1) * u_size - m),
             (x * u_size + m, (y + 1) * u_size - m)]
        rect = rendering.FilledPolygon(v)
        r = self.grids.get_type(x, y)
        if r == 1:
            rect.set_color(0.75, 0.92, 0.93)
        elif r == 2:
            rect.set_color(0.3, 0.3, 0.3)
        elif r == 3:
            rect.set_color(1.0, 1.0, 1.0)
        elif r == 4:
            rect.set_color(1.0, 0.0, 0.0)
        elif r == 5:
            rect.set_color(0.5, 0.2, 0.7)
            self.motive_agent = rect
        else:
            rect.set_color(0.9, 0.9, 0.9)
        self.viewer.add_geom(rect)

    # 图形化界面
    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        # 初始化整个屏幕具备的元素。
        u_size = self.u_size
        if self.viewer is None:
            self.viewer = rendering.Viewer(self.width, self.height)
            # 绘制格子
            for y in range(self.n_height):
                for x in range(self.n_width):
                    self.render_grid(x, y)
            # 绘制个体
            self.agent = rendering.make_circle(u_size / 2.5)
            self.agent.set_color(1.0, 1.0, 0)
            self.viewer.add_geom(self.agent)
            self.agent_trans = rendering.Transform()
            self.agent.add_attr(self.agent_trans)
            # 更新个体位置
        self.agent_trans.set_translation((self.state[0] + 0.5) * u_size, (self.state[1] + 0.5) * u_size)
        return self.viewer.render(return_rgb_array=mode == 'rgb_array')


if __name__ == "__main__":
    print(233)
