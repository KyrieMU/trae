import numpy as np
import matplotlib.pyplot as plt
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def generate_poisson_process(lambda_rate, T, num_samples=5):
    """
    生成泊松过程的样本函数
    lambda_rate: 强度（到达率）
    T: 观察时间长度
    num_samples: 样本函数数量
    """
    plt.figure(figsize=(12, 6))
    
    for sample in range(num_samples):
        # 生成指数分布的时间间隔
        times = []
        current_time = 0
        while current_time <= T:
            # 生成下一个事件的时间间隔（指数分布）
            interval = np.random.exponential(1/lambda_rate)
            current_time += interval
            if current_time <= T:
                times.append(current_time)
        
        # 构建阶梯函数
        t_points = [0] + times
        counts = np.arange(len(t_points))
        
        # 绘制阶梯图
        plt.step(t_points, counts, where='post', label=f'样本 {sample+1}')
    
    plt.title(f'泊松过程样本函数 (λ={lambda_rate}人/分钟)')
    plt.xlabel('时间 (分钟)')
    plt.ylabel('到达人数')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, T)
    plt.show()

# 设置参数
lambda_rate = 2  # 强度为2人/分钟
T = 5           # 观察5分钟

# 生成并显示样本函数
generate_poisson_process(lambda_rate, T)

# 显示理论特性
print(f"期望值 E[N(t)] = λt = {lambda_rate}t")
print(f"方差 Var[N(t)] = λt = {lambda_rate}t")