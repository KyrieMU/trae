import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 模拟参数
n_particles = 50      # 粒子数量
n_steps = 1000      # 时间步数
dt = 0.01           # 时间步长
sigma = 0.1         # 扩散系数

# 生成一维布朗运动
def brownian_motion_1d():
    # 初始位置都在原点
    positions = np.zeros((n_particles, n_steps))
    
    # 模拟运动
    for i in range(1, n_steps):
        # 随机位移，服从正态分布
        dx = np.random.normal(0, sigma * np.sqrt(dt), n_particles)
        positions[:, i] = positions[:, i-1] + dx
    
    return positions

# 生成二维布朗运动
def brownian_motion_2d():
    # 初始位置都在原点
    positions_x = np.zeros((n_particles, n_steps))
    positions_y = np.zeros((n_particles, n_steps))
    
    # 模拟运动
    for i in range(1, n_steps):
        # x和y方向的随机位移
        dx = np.random.normal(0, sigma * np.sqrt(dt), n_particles)
        dy = np.random.normal(0, sigma * np.sqrt(dt), n_particles)
        positions_x[:, i] = positions_x[:, i-1] + dx
        positions_y[:, i] = positions_y[:, i-1] + dy
    
    return positions_x, positions_y

# 生成数据
positions_1d = brownian_motion_1d()
positions_2d_x, positions_2d_y = brownian_motion_2d()

# 创建图形
plt.figure(figsize=(15, 5))

# 绘制一维布朗运动
plt.subplot(121)
time = np.arange(n_steps) * dt
for i in range(n_particles):
    plt.plot(time, positions_1d[i], label=f'粒子 {i+1}')
plt.title('一维布朗运动')
plt.xlabel('时间')
plt.ylabel('位置')
plt.legend()
plt.grid(True)

# 绘制二维布朗运动
plt.subplot(122)
for i in range(n_particles):
    plt.plot(positions_2d_x[i], positions_2d_y[i], label=f'粒子 {i+1}')
plt.title('二维布朗运动')
plt.xlabel('X位置')
plt.ylabel('Y位置')
plt.legend()
plt.grid(True)

# 保持横纵比相等
plt.axis('equal')
plt.tight_layout()
plt.show()

# 计算和打印一些统计特性
print("\n布朗运动的统计特性：")
print(f"一维运动最终位置的均值：{np.mean(positions_1d[:, -1]):.4f}")
print(f"一维运动最终位置的标准差：{np.std(positions_1d[:, -1]):.4f}")
print(f"二维运动最终位置的平均距离：{np.mean(np.sqrt(positions_2d_x[:, -1]**2 + positions_2d_y[:, -1]**2)):.4f}")