# 导入必要的库
import numpy as np  # 导入NumPy用于数值计算
import matplotlib.pyplot as plt  # 导入Matplotlib用于数据可视化
from sklearn.linear_model import LinearRegression, LogisticRegression  # 导入sklearn中的线性回归和逻辑回归模型
from sklearn.datasets import make_regression, make_classification  # 导入数据生成工具

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 1. 线性回归模型
def linear_regression_tutorial():
    """
    线性回归模型教学示例
    原理：通过最小化预测值与实际值之间的均方误差来找到最佳的线性关系
    公式：y = wx + b，其中w为权重（斜率），b为偏置（截距）
    应用：房价预测、销售预测等连续值预测问题
    """
    # 生成示例数据：100个样本，1个特征，噪声水平为10
    X, y = make_regression(n_samples=100, n_features=1, noise=10, random_state=42)
    
    # 创建线性回归模型实例并训练
    model = LinearRegression()
    model.fit(X, y)  # 使用训练数据拟合模型
    
    # 使用训练好的模型进行预测
    y_pred = model.predict(X)
    
    # 数据可视化
    plt.figure(figsize=(10, 6))  # 设置图形大小
    plt.scatter(X, y, color='blue', label='实际数据点')  # 绘制散点图
    plt.plot(X, y_pred, color='red', label='拟合直线')  # 绘制预测线
    plt.title('线性回归示例 - 数据拟合效果')
    plt.xlabel('输入特征 X')
    plt.ylabel('目标变量 y')
    plt.legend()
    plt.show()
    
    # 输出模型参数
    print(f"模型斜率(w): {model.coef_[0]:.2f}")  # 打印权重系数
    print(f"模型截距(b): {model.intercept_:.2f}")  # 打印偏置项

# 2. 逻辑回归模型
def logistic_regression_tutorial():
    """
    逻辑回归模型教学示例
    原理：通过sigmoid函数将线性模型的输出转换为概率，用于分类问题
    公式：P(y=1|x) = 1 / (1 + e^(-wx-b))
    应用：垃圾邮件分类、疾病诊断等二分类问题
    """
    # 生成二分类示例数据：100个样本，2个特征
    X, y = make_classification(n_samples=100, n_features=2, n_redundant=0, 
                             n_informative=2, random_state=42)
    
    # 创建逻辑回归模型实例并训练
    model = LogisticRegression()
    model.fit(X, y)  # 使用训练数据拟合模型
    
    # 创建网格点用于可视化决策边界
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))
    
    # 对网格点进行预测
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # 可视化决策边界和数据点
    plt.figure(figsize=(10, 6))
    plt.contourf(xx, yy, Z, alpha=0.4)  # 绘制决策边界
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)  # 绘制数据点
    plt.title('逻辑回归分类示例 - 决策边界可视化')
    plt.xlabel('特征1 (X1)')
    plt.ylabel('特征2 (X2)')
    plt.show()

# 主程序入口
if __name__ == "__main__":
    print("=== 线性回归模型演示 - 连续值预测 ===")
    linear_regression_tutorial()
    
    print("\n=== 逻辑回归模型演示 - 二分类问题 ===")
    logistic_regression_tutorial()