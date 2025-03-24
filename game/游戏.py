import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.font_manager import FontProperties

# 尝试加载中文字体
try:
    # 尝试使用系统中可能存在的中文字体
    font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf")
except:
    # 如果找不到指定字体，使用系统默认字体
    font = FontProperties()

# 赌场游戏及其庄家优势数据
games = [
    "百家乐(庄)", "百家乐(闲)", "21点(基本策略)", "21点(普通玩家)", 
    "美式轮盘", "欧式轮盘", "老虎机", "骰宝", 
    "德州扑克(赌场抽水)", "加勒比扑克", "牌九", "三卡扑克"
]

house_edges = [
    1.06, 1.24, 0.5, 2.0, 
    5.26, 2.7, 10.0, 2.78, 
    5.0, 5.22, 1.5, 3.37
]

# 游戏模拟函数
def simulate_games(num_simulations=10000):
    player_win_rates = []
    
    for edge in house_edges:
        # 玩家胜率 = 100% - 庄家优势
        player_win_rate = (100 - edge) / 100
        wins = 0
        
        # 模拟游戏
        for _ in range(num_simulations):
            # 生成0-1之间的随机数，如果小于玩家胜率则视为玩家获胜
            if random.random() < player_win_rate:
                wins += 1
        
        # 计算实际胜率
        actual_win_rate = (wins / num_simulations) * 100
        player_win_rates.append(actual_win_rate)
    
    return player_win_rates

# 运行模拟
print("正在模拟游戏，请稍候...")
player_win_rates = simulate_games(100000)

# 创建图表1：庄家优势
plt.figure(figsize=(12, 8))
bars = plt.barh(games, house_edges, color='skyblue')
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width}%', 
             va='center', fontproperties=font)
plt.title('赌场经典游戏庄家优势比较', fontproperties=font, fontsize=16)
plt.xlabel('庄家优势 (%)', fontproperties=font, fontsize=12)
plt.ylabel('游戏', fontproperties=font, fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.xticks(fontproperties=font)
plt.yticks(fontproperties=font)
plt.savefig('e:\\Desktop\\1\\赌场游戏庄家优势.png', dpi=300, bbox_inches='tight')
plt.show()

# 创建图表2：玩家胜率
plt.figure(figsize=(12, 8))
bars = plt.barh(games, player_win_rates, color='lightgreen')
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
             va='center', fontproperties=font)
plt.title('赌场经典游戏玩家胜率模拟结果', fontproperties=font, fontsize=16)
plt.xlabel('玩家胜率 (%)', fontproperties=font, fontsize=12)
plt.ylabel('游戏', fontproperties=font, fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.xticks(fontproperties=font)
plt.yticks(fontproperties=font)
plt.savefig('e:\\Desktop\\1\\赌场游戏玩家胜率.png', dpi=300, bbox_inches='tight')
plt.show()

# 创建图表3：对比图
plt.figure(figsize=(14, 10))
x = np.arange(len(games))
width = 0.35

plt.barh([i + width/2 for i in x], house_edges, width, label='庄家优势', color='skyblue')
plt.barh([i - width/2 for i in x], player_win_rates, width, label='玩家胜率', color='lightgreen')

plt.yticks(x, games, fontproperties=font)
plt.xlabel('百分比 (%)', fontproperties=font, fontsize=12)
plt.title('赌场游戏庄家优势与玩家胜率对比', fontproperties=font, fontsize=16)
plt.legend(prop=font)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('e:\\Desktop\\1\\赌场游戏对比.png', dpi=300, bbox_inches='tight')
plt.show()

print("模拟完成！图表已生成并保存到桌面。")
print(f"模拟次数: 100,000")
print("玩家理论胜率 vs 模拟胜率:")
for i, game in enumerate(games):
    theoretical = 100 - house_edges[i]
    simulated = player_win_rates[i]
    print(f"{game}: 理论 {theoretical:.2f}% vs 模拟 {simulated:.2f}%")