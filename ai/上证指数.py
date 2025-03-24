# ... 前面的数据处理代码保持不变 ...
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import baostock as bs
import matplotlib


# 设置随机种子以确保结果可重现
torch.manual_seed(42)

# 登陆 Baostock
lg = bs.login()

# 获取上证指数数据
# 修改数据获取部分
rs = bs.query_history_k_data_plus("sh.000001",
    "date,close,volume",  # 添加成交量数据
    start_date='2023-01-01', 
    end_date='2025-03-14',
    frequency="d",
    adjustflag="3")

# 将数据转换为 DataFrame
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
df = pd.DataFrame(data_list, columns=['date', 'close', 'volume'])

# 退出系统
bs.logout()

# 将数据处理成需要的格式
prices = df['close'].astype('float').values.reshape(-1, 1)

# 数据归一化
scaler = MinMaxScaler()
prices_normalized = scaler.fit_transform(prices)

# 准备训练数据
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])  # 输入序列：每10天的数据
        y.append(data[i + seq_length])      # 目标值：第11天的数据
    return torch.FloatTensor(X), torch.FloatTensor(y)

sequence_length = 10  # 使用过去10天的数据预测下一天
X, y = create_sequences(prices_normalized, sequence_length)

# 划分训练集和测试集
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 定义新的神经网络模型
class HybridStockPredictor(nn.Module):
    def __init__(self):
        super(HybridStockPredictor, self).__init__()
        
        # 1D CNN层用于提取局部特征
        self.conv1 = nn.Conv1d(1, 32, kernel_size=3)
        self.conv2 = nn.Conv1d(32, 32, kernel_size=3)
        self.dropout1 = nn.Dropout(0.2)
        
        # GRU层用于处理时序依赖
        self.gru = nn.GRU(32, 64, num_layers=2, batch_first=True, dropout=0.2)
        
        # 注意力机制
        self.attention = nn.MultiheadAttention(64, num_heads=4, batch_first=True)
        
        # 全连接层
        self.fc1 = nn.Linear(64, 32)
        self.dropout2 = nn.Dropout(0.2)
        self.fc2 = nn.Linear(32, 1)
        
        # 激活函数
        self.relu = nn.ReLU()
        
    def forward(self, x):
        # 调整输入维度 [batch, seq_len, features] -> [batch, features, seq_len]
        x = x.transpose(1, 2)
        
        # CNN特征提取
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.dropout1(x)
        
        # 调整维度用于GRU [batch, features, seq_len] -> [batch, seq_len, features]
        x = x.transpose(1, 2)
        
        # GRU处理
        gru_out, _ = self.gru(x)
        
        # 注意力机制
        attn_out, _ = self.attention(gru_out, gru_out, gru_out)
        
        # 取最后一个时间步
        x = attn_out[:, -1, :]
        
        # 全连接层
        x = self.relu(self.fc1(x))
        x = self.dropout2(x)
        x = self.fc2(x)
        
        return x

# 创建新模型实例
model = HybridStockPredictor()

# 定义损失函数
criterion = nn.MSELoss()

# 修改优化器和学习率调度器
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=20, verbose=True)

# 修改训练循环
epochs = 100  # 增加训练轮数
batch_size = 32  # 添加批处理
train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

losses = []
best_loss = float('inf')

for epoch in range(epochs):
    model.train()
    epoch_losses = []
    
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        
        # 梯度裁剪，防止梯度爆炸
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        epoch_losses.append(loss.item())
    
    avg_loss = np.mean(epoch_losses)
    losses.append(avg_loss)
    
    # 学习率调整
    scheduler.step(avg_loss)
    
    # 保存最佳模型
    if avg_loss < best_loss:
        best_loss = avg_loss
        torch.save(model.state_dict(), 'best_model.pth')
    
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}')

# 加载最佳模型
model.load_state_dict(torch.load('best_model.pth'))

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 评估模型
model.eval()
with torch.no_grad():
    train_pred = model(X_train)
    test_pred = model(X_test)
    
    # 反归一化预测结果
    train_pred = scaler.inverse_transform(train_pred.numpy())
    test_pred = scaler.inverse_transform(test_pred.numpy())
    y_train_orig = scaler.inverse_transform(y_train.numpy())
    y_test_orig = scaler.inverse_transform(y_test.numpy())

# 绘制结果
plt.figure(figsize=(15, 5))

# 绘制损失曲线
plt.subplot(131)
plt.plot(losses)
plt.title('训练损失')
plt.xlabel('迭代次数')
plt.ylabel('损失值')

# 绘制预测结果对比
plt.subplot(132)
plt.plot(y_train_orig, label='训练集实际值')
plt.plot(train_pred, label='训练集预测值')
plt.plot(range(len(y_train_orig), len(y_train_orig) + len(y_test_orig)), 
         y_test_orig, label='测试集实际值')
plt.plot(range(len(y_train_orig), len(y_train_orig) + len(test_pred)), 
         test_pred, label='测试集预测值')
plt.title('股票价格预测')
plt.xlabel('时间')
plt.ylabel('价格')
plt.legend()

# 计算并绘制预测准确率
plt.subplot(133)
train_accuracy = 1 - np.mean(np.abs(train_pred - y_train_orig) / y_train_orig)
test_accuracy = 1 - np.mean(np.abs(test_pred - y_test_orig) / y_test_orig)

plt.bar(['训练集', '测试集'], [train_accuracy, test_accuracy])
plt.title('预测准确率')
plt.ylabel('准确率')

plt.tight_layout()
plt.show()

# 打印评估指标
print(f'训练集准确率: {train_accuracy:.2%}')
print(f'测试集准确率: {test_accuracy:.2%}')


# 添加向前预测功能
def predict_future(model, last_sequence, n_days=30):
    model.eval()
    future_predictions = []
    current_sequence = last_sequence.clone()
    
    for _ in range(n_days):
        # 预测下一天
        with torch.no_grad():
            next_pred = model(current_sequence.unsqueeze(0))
        
        # 添加预测值到序列
        future_predictions.append(next_pred.item())
        # 更新序列（移除最早的一天，添加预测的一天）
        current_sequence = torch.cat((current_sequence[1:], next_pred))
    
    # 反归一化预测结果
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
    return future_predictions

# 获取最后一个序列用于预测
last_sequence = X[-1]

# 预测未来30天
future_pred = predict_future(model, last_sequence, n_days=30)

# 获取最后的日期
last_date = pd.to_datetime(df['date'].iloc[-1])
future_dates = pd.date_range(start=last_date, periods=31)[1:]

# 打印预测结果
print("\n未来30天预测：")
for date, pred in zip(future_dates, future_pred):
    print(f"{date.strftime('%Y-%m-%d')}: {pred[0]:.2f}")

# 绘制包含未来预测的图表
plt.figure(figsize=(12, 6))
# 绘制最近30天的历史数据和未来30天的预测
historical_dates = pd.to_datetime(df['date'].values[-30:])
plt.plot(historical_dates, prices[-30:], label='历史数据', marker='o')
plt.plot(future_dates, future_pred, 'r--', label='预测数据', marker='*')
plt.title('未来30天股价预测')
plt.xlabel('日期')
plt.ylabel('价格')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()  # 自动调整日期标签
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()