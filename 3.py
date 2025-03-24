import random
import numpy as np
import matplotlib.pyplot as plt

def simulate_one_game():
    total_score = 0
    while True:
        # 随机取一个球（1-5）
        ball = random.randint(1, 5)
        
        # 如果取到5号球，加5分并结束
        if ball == 5:
            total_score += 5
            break
        # 否则加上对应的分数继续
        else:
            total_score += ball
    
    return total_score

# 模拟大量次数求期望
def calculate_expected_value(num_simulations=1000000):
    total = 0
    for _ in range(num_simulations):
        total += simulate_one_game()
    
    return total / num_simulations

# 计算并打印结果
expected_value = calculate_expected_value()
print(f"X的数学期望约为: {expected_value:.2f}")

# 计算前20个k值的概率（实际上k可以到无穷，但概率会变得很小）
k_values = np.arange(0, 20)
probabilities = (2**k_values)/(3**(k_values+1))

# 绘制概率分布图
plt.figure(figsize=(10, 6))
plt.bar(k_values, probabilities, alpha=0.6)
plt.title('概率分布 P(X=k) = 2^k/3^(k+1)')
plt.xlabel('k')
plt.ylabel('概率')
plt.grid(True, alpha=0.3)

# 计算期望
# E(X) = Σ(k * P(X=k))
expectation = sum(k * prob for k, prob in zip(k_values, probabilities))

# 计算方差
# Var(X) = E(X^2) - (E(X))^2
expectation_squared = sum(k**2 * prob for k, prob in zip(k_values, probabilities))
variance = expectation_squared - expectation**2

print(f"期望 E(X) ≈ {expectation:.4f}")
print(f"方差 Var(X) ≈ {variance:.4f}")

plt.show()


def generate_gaussian_process(n_points=1000, t_max=10):
    # 生成时间点
    t = np.linspace(0, t_max, n_points)
    
    # 构建协方差矩阵
    cov_matrix = np.zeros((n_points, n_points))
    for i in range(n_points):
        for j in range(n_points):
            cov_matrix[i,j] = 1 + t[i]*t[j]
    
    # 生成多元正态分布样本
    sample = np.random.multivariate_normal(np.zeros(n_points), cov_matrix)
    
    # 绘制样本曲线
    plt.figure(figsize=(12, 6))
    plt.plot(t, sample)
    plt.title('高斯随机过程样本曲线')
    plt.xlabel('t')
    plt.ylabel('X(t)')
    plt.grid(True)
    plt.show()
    
    return t, sample

# 生成并显示多条样本曲线
plt.figure(figsize=(12, 6))
for _ in range(5):
    t, sample = generate_gaussian_process()
    plt.plot(t, sample, alpha=0.7)

plt.title('多条高斯随机过程样本曲线')
plt.xlabel('t')
plt.ylabel('X(t)')
plt.grid(True)
plt.show()