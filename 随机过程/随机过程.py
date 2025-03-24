import numpy as np
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def drunk_walk(n_steps, n_drunks, p=0.5, step_size=1):
    """
    模拟醉汉随机游走
    n_steps: 步数
    n_drunks: 醉汉数量
    p: 向前走的概率
    step_size: 步长
    """
    # 初始化位置矩阵
    positions = np.zeros((n_drunks, n_steps))
    
    # 生成随机步骤
    for i in range(1, n_steps):
        # 生成随机数决定方向
        random_steps = np.where(np.random.random(n_drunks) < p, step_size, -step_size)
        positions[:, i] = positions[:, i-1] + random_steps
    
    return positions

# 模拟参数
n_steps = 100    # 总步数
n_drunks = 1000      # 醉汉数量
p = 0.5           # 向前走的概率
step_size = 1     # 步长

# 生成随机游走数据
positions = drunk_walk(n_steps, n_drunks, p, step_size)

# 创建图形
plt.figure(figsize=(15, 6))

# 绘制随机游走轨迹
plt.subplot(121)
time = np.arange(n_steps)
for i in range(n_drunks):
    plt.plot(time, positions[i], label=f'醉汉 {i+1}')
plt.title('醉汉随机游走轨迹')
plt.xlabel('时间步数')
plt.ylabel('位置')
plt.legend()
plt.grid(True)

# 绘制最终位置分布直方图
plt.subplot(122)
plt.hist(positions[:, -1], bins=20, density=True, alpha=0.7)
plt.title('最终位置分布')
plt.xlabel('位置')
plt.ylabel('频率密度')
plt.grid(True)

plt.tight_layout()
plt.show()

# 计算统计特性
print("\n随机游走统计特性：")
print(f"理论均值（期望位置）：{n_steps * (2*p-1) * step_size:.2f}")
print(f"实际均值（平均位置）：{np.mean(positions[:, -1]):.2f}")
print(f"理论标准差：{np.sqrt(4*p*(1-p)*n_steps) * step_size:.2f}")
print(f"实际标准差：{np.std(positions[:, -1]):.2f}")
print(f"最远距离：{np.max(np.abs(positions[:, -1])):.2f}")
