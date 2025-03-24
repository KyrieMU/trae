import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import baostock as bs
import matplotlib
matplotlib.use('TkAgg')
plt.ioff()  # 禁用交互模式

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

# 定义神经网络模型
class StockPredictor(nn.Module):
    def __init__(self):
        super(StockPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=64, num_layers=2, batch_first=True)
        self.fc = nn.Linear(64, 1)
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_time_step = lstm_out[:, -1, :]
        predictions = self.fc(last_time_step)
        return predictions

# 创建模型实例
model = StockPredictor()

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练模型
epochs = 200
losses = []

for epoch in range(epochs):
    model.train()
    # 前向传播
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    
    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # 记录损失
    losses.append(loss.item())
    
    # 每10轮打印一次损失
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

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

# 计算交易信号和收益率（只做多，带止损）
# 修改交易策略函数
def calculate_returns(predictions, actual_prices, volumes, 
                     stop_loss_pct=0.03,    # 止损比例
                     take_profit_pct=1,   # 止盈比例
                     max_holding_days=5,    # 最大持仓天数
                     transaction_cost=0.001): # 交易成本
    positions = np.zeros(len(predictions))
    returns = np.zeros(len(predictions))
    in_position = False
    entry_price = 0
    holding_days = 0
    volume_ma = np.convolve(volumes, np.ones(5)/5, mode='valid')  # 5日成交量均线
    
    # 根据预测值生成交易信号
    for i in range(5, len(predictions)):  # 从第5天开始，确保有足够数据计算均线
        # 如果持仓中
        if in_position:
            holding_days += 1
            current_return = (actual_prices[i] - entry_price) / entry_price
            
            # 检查止损、止盈或持仓时间限制
            if (current_return < -stop_loss_pct or  # 止损
                current_return > take_profit_pct or  # 止盈
                holding_days >= max_holding_days):   # 持仓时间限制
                positions[i] = 0
                in_position = False
                holding_days = 0
                # 计算平仓收益（考虑交易成本）
                returns[i] = current_return - transaction_cost
                continue
            
        # 生成交易信号（只做多）
        if not in_position:
            # 检查成交量条件：当前成交量大于5日均线
            volume_condition = volumes[i] > volume_ma[i-5]
            
            if predictions[i] > actual_prices[i-1] and volume_condition:
                positions[i] = 1  # 做多
                in_position = True
                entry_price = actual_prices[i]
                holding_days = 0
                returns[i] = -transaction_cost  # 考虑开仓交易成本
        
        elif in_position:
            positions[i] = 1  # 保持持仓
            # 计算当日收益率
            price_change = (actual_prices[i] - actual_prices[i-1]) / actual_prices[i-1]
            returns[i] = price_change
    
    return positions, returns

# 修改计算收益率的调用
volumes = df['volume'].astype('float').values
_, train_returns = calculate_returns(train_pred, y_train_orig, volumes[:len(train_pred)])
_, test_returns = calculate_returns(test_pred, y_test_orig, volumes[len(train_pred):])

# 计算累计收益率
train_cumulative_returns = np.cumprod(1 + train_returns) - 1
test_cumulative_returns = np.cumprod(1 + test_returns) - 1

# 计算年化收益率（假设每年250个交易日）
train_annual_return = (1 + train_cumulative_returns[-1]) ** (250 / len(train_returns)) - 1
test_annual_return = (1 + test_cumulative_returns[-1]) ** (250 / len(test_returns)) - 1

print(f'训练集年化收益率: {train_annual_return:.2%}')
print(f'测试集年化收益率: {test_annual_return:.2%}')

# 绘制结果
plt.figure(figsize=(15, 6))
plt.subplot(1, 3, 1)
plt.plot(losses)
plt.title('训练损失')
plt.xlabel('迭代次数')
plt.ylabel('损失')

plt.subplot(1, 3, 2)
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

plt.subplot(1, 3, 3)
plt.plot(train_cumulative_returns, label='训练集累计收益')
plt.plot(range(len(train_cumulative_returns), 
         len(train_cumulative_returns) + len(test_cumulative_returns)), 
         test_cumulative_returns, label='测试集累计收益')
plt.title('累计收益率')
plt.xlabel('交易日')
plt.ylabel('收益率')
plt.legend()

plt.tight_layout()
plt.show()


# 添加向前预测功能
def predict_future(model, last_sequence, n_days=50):
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

# 预测未来5天
future_pred = predict_future(model, last_sequence, n_days=50)

# 获取最后的日期
last_date = pd.to_datetime(df['date'].iloc[-1])
future_dates = pd.date_range(start=last_date, periods=51)[1:]  # 修改为51以匹配50天预测

# 打印预测结果
print("\n未来50天预测：")  # 修改为50天
for date, pred in zip(future_dates, future_pred):
    print(f"{date.strftime('%Y-%m-%d')}: {pred[0]:.2f}")

# 绘制包含未来预测的图表
plt.figure(figsize=(12, 6))
# 转换日期格式
historical_dates = pd.to_datetime(df['date'].values[-30:])
plt.plot(historical_dates, prices[-30:], label='历史数据', marker='o')
plt.plot(future_dates[:50], future_pred, 'r--', label='预测数据', marker='*')  # 确保使用所有50天的预测数据
plt.title('未来50天股价预测')  # 更新标题
plt.xlabel('日期')
plt.ylabel('价格')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()  # 自动调整日期标签
plt.legend()
plt.grid(True)  # 添加网格
plt.tight_layout()
plt.show()

# 在绘图之前添加数据检查
print("历史数据点数:", len(prices[-30:]))
print("预测数据点数:", len(future_pred))
print("最后30天的价格:", prices[-30:])
print("预测价格:", future_pred)
