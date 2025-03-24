# 导入必要的库
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

# 设置随机种子，确保结果可复现
torch.manual_seed(1)
np.random.seed(1)

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class SimpleNeuralNetwork(nn.Module):
    """
    简单的深度神经网络模型
    架构：输入层(2) -> 隐藏层1(10) -> 隐藏层2(8) -> 输出层(1)
    """
    def __init__(self):
        super(SimpleNeuralNetwork, self).__init__()
        # 定义网络层
        self.layer1 = nn.Linear(2, 10)    # 第一层：2个输入特征，10个神经元
        self.layer2 = nn.Linear(10, 8)    # 第二层：10个输入，8个神经元
        self.layer3 = nn.Linear(8, 1)     # 输出层：8个输入，1个输出
        self.relu = nn.ReLU()             # ReLU激活函数
        self.sigmoid = nn.Sigmoid()        # Sigmoid激活函数

    def forward(self, x):
        """正向传播过程"""
        x = self.relu(self.layer1(x))     # 第一层后接ReLU激活函数
        x = self.relu(self.layer2(x))     # 第二层后接ReLU激活函数
        x = self.sigmoid(self.layer3(x))  # 输出层后接Sigmoid激活函数
        return x

def generate_spiral_data(samples_per_class=100, classes=2):
    """生成螺旋形状的数据集用于分类问题演示"""
    X = np.zeros((samples_per_class*classes, 2))
    y = np.zeros(samples_per_class*classes)
    
    for class_idx in range(classes):
        ix = range(samples_per_class*class_idx, samples_per_class*(class_idx+1))
        r = np.linspace(0.0, 1, samples_per_class)
        t = np.linspace(class_idx*4, (class_idx+1)*4, samples_per_class) + np.random.randn(samples_per_class)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_idx
    
    return torch.FloatTensor(X), torch.FloatTensor(y)

def train_model():
    """训练神经网络模型"""
    # 生成训练数据
    X, y = generate_spiral_data()
    
    # 创建模型实例
    model = SimpleNeuralNetwork()
    criterion = nn.BCELoss()              # 二元交叉熵损失函数
    optimizer = optim.Adam(model.parameters(), lr=0.01)  # Adam优化器
    
    # 训练过程
    epochs = 1000
    losses = []
    
    for epoch in range(epochs):
        # ===== 正向传播 =====
        outputs = model(X)                # 前向计算
        loss = criterion(outputs, y.view(-1, 1))  # 计算损失
        
        # ===== 反向传播 =====
        optimizer.zero_grad()             # 清零梯度
        loss.backward()                   # 计算梯度
        optimizer.step()                  # 更新参数
        
        losses.append(loss.item())
        
        if (epoch + 1) % 100 == 0:
            print(f'训练轮次: [{epoch+1}/{epochs}], 损失: {loss.item():.4f}')
    
    return model, losses, X, y

def visualize_results(model, losses, X, y):
    """可视化训练结果"""
    plt.figure(figsize=(15, 5))
    
    # 绘制损失曲线
    plt.subplot(1, 2, 1)
    plt.plot(losses)
    plt.title('训练损失曲线')
    plt.xlabel('训练轮次')
    plt.ylabel('损失值')
    
    # 绘制决策边界
    plt.subplot(1, 2, 2)
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                        np.linspace(y_min, y_max, 100))
    
    # 对网格点进行预测
    grid = torch.FloatTensor(np.c_[xx.ravel(), yy.ravel()])
    with torch.no_grad():
        Z = model(grid)
    Z = Z.numpy().reshape(xx.shape)
    
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8)
    plt.title('神经网络分类结果')
    plt.xlabel('特征1')
    plt.ylabel('特征2')
    plt.colorbar()
    
    plt.tight_layout()
    plt.show()

def main():
    """主函数"""
    print("=== 深度神经网络演示 - 非线性分类问题 ===")
    print("\n1. 开始训练模型...")
    model, losses, X, y = train_model()
    
    print("\n2. 训练完成，显示结果...")
    visualize_results(model, losses, X, y)
    
    print("\n3. 模型结构：")
    print(model)

if __name__ == "__main__":
    main()


'''
这个教学示例包含以下几个主要部分：

1. 网络结构 ：
   
   - 使用了一个三层神经网络（两个隐藏层）
   - 采用ReLU和Sigmoid激活函数
   - 展示了层与层之间的连接方式
2. 正向传播 ：
   
   - 数据从输入层开始，依次通过各个隐藏层
   - 每一层都包含线性变换和非线性激活
   - 最终得到分类预测结果
3. 反向传播 ：
   
   - 使用二元交叉熵作为损失函数
   - 通过自动求导计算梯度
   - 使用Adam优化器更新网络参数
4. 可视化功能 ：
   
   - 展示训练过程中损失值的变化
   - 可视化模型学习到的决策边界
   - 展示数据分布和分类结果
这个示例使用螺旋形数据集来演示神经网络处理非线性分类问题的能力，通过可视化帮助理解神经网络的学习过程和效果。
'''