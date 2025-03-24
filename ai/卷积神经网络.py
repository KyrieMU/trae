import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置随机种子
torch.manual_seed(42)
np.random.seed(42)

class SimpleCNN(nn.Module):
    """
    简单的卷积神经网络模型
    架构：
    输入(1x28x28) -> Conv1 -> ReLU -> MaxPool -> Conv2 -> ReLU -> MaxPool -> FC1 -> ReLU -> FC2
    """
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 第一个卷积层：1个输入通道，16个输出通道，5x5卷积核
        self.conv1 = nn.Conv2d(1, 16, kernel_size=5, padding=2)
        # 第二个卷积层：16个输入通道，32个输出通道，5x5卷积核
        self.conv2 = nn.Conv2d(16, 32, kernel_size=5, padding=2)
        # 最大池化层：2x2窗口
        self.pool = nn.MaxPool2d(2, 2)
        # 全连接层1：将特征图转换为类别概率
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        # 全连接层2：输出10个类别
        self.fc2 = nn.Linear(128, 10)
        # ReLU激活函数
        self.relu = nn.ReLU()

    def forward(self, x):
        # 第一个卷积块：卷积 -> ReLU -> 池化
        x = self.pool(self.relu(self.conv1(x)))  # 输出尺寸: 16x14x14
        # 第二个卷积块：卷积 -> ReLU -> 池化
        x = self.pool(self.relu(self.conv2(x)))  # 输出尺寸: 32x7x7
        # 将特征图展平
        x = x.view(-1, 32 * 7 * 7)
        # 全连接层
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def load_data():
    """加载MNIST数据集"""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    # 加载训练集和测试集
    train_dataset = torchvision.datasets.MNIST(
        root='./data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.MNIST(
        root='./data', train=False, download=True, transform=transform)

    # 创建数据加载器
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=64, shuffle=True)
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=1000, shuffle=False)

    return train_loader, test_loader

def train_model(model, train_loader, num_epochs=3):
    """训练CNN模型"""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 记录训练过程
    train_losses = []
    train_accs = []
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for i, (images, labels) in enumerate(train_loader):
            # 前向传播
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # 统计准确率
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            running_loss += loss.item()
            
        # 计算epoch的平均损失和准确率
        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100 * correct / total
        
        train_losses.append(epoch_loss)
        train_accs.append(epoch_acc)
        
        print(f'Epoch [{epoch+1}/{num_epochs}], '
              f'Loss: {epoch_loss:.4f}, '
              f'Accuracy: {epoch_acc:.2f}%')
    
    return train_losses, train_accs

def visualize_results(model, test_loader):
    """可视化模型结果"""
    # 获取一批测试数据
    dataiter = iter(test_loader)
    images, labels = next(dataiter)

    # 预测结果
    model.eval()
    with torch.no_grad():
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)

    # 显示一些预测结果
    plt.figure(figsize=(15, 5))
    for i in range(40):
        plt.subplot(8, 5, i+1)
        plt.imshow(images[i][0], cmap='gray')
        plt.title(f'预测: {predicted[i]}\n实际: {labels[i]}')
        plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_filters(model):
    """可视化第一层卷积核"""
    filters = model.conv1.weight.data.numpy()
    
    plt.figure(figsize=(10, 5))
    for i in range(16):
        plt.subplot(4, 4, i+1)
        plt.imshow(filters[i][0], cmap='gray')
        plt.axis('off')
    plt.suptitle('第一层卷积核可视化')
    plt.tight_layout()
    plt.show()

def main():
    print("=== 卷积神经网络演示 - MNIST手写数字识别 ===")
    
    # 加载数据
    print("\n1. 加载数据...")
    train_loader, test_loader = load_data()
    
    # 创建模型
    print("\n2. 创建CNN模型...")
    model = SimpleCNN()
    
    # 训练模型
    print("\n3. 开始训练...")
    train_losses, train_accs = train_model(model, train_loader)
    
    # 可视化结果
    print("\n4. 显示预测结果...")
    visualize_results(model, test_loader)
    
    # 可视化卷积核
    print("\n5. 显示卷积核...")
    visualize_filters(model)

if __name__ == "__main__":
    main()