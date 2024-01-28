from gridworld_env import *

env = GridWorldEnv(n_width=9, n_height=8, u_size=40, start=(0, 7))
env.ends = [(5, 3, 1)]
env.wall = [(4, 4, 2), (4, 3, 2), (5, 4, 2), (6, 2, 2)]
env.bound = [(1, 2, 3), (2, 2, 3), (1, 3, 3), (2, 3, 3), (1, 4, 3), (2, 4, 3)]
env.trap = [(4, 2, 4), (6, 5, 4)]
env.motive = [(8, 4, 5)]
# env.motive = [(1, 7, 5)]
env.refresh_setting()
env.perform()
# env.render()

env.close()
input("press any key to continue...")

