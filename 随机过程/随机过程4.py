import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子以保证结果可重复
np.random.seed(50)

# 生成时间点
t = np.linspace(0, 5, 1000)

# 模拟抛硬币
coin = np.random.choice(['正面', '反面'])

# 根据硬币结果生成样本函数
if coin == '正面':
    xt = np.cos(np.pi * t)
else:
    xt = 2 * t

# 绘制样本函数
plt.figure(figsize=(10, 6))
plt.plot(t, xt, label=f'硬币结果: {coin}')
plt.title('随机过程样本函数')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)
plt.legend()
plt.show()

print(f"硬币投掷结果: {coin}")