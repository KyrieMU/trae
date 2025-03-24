import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
import seaborn as sns
from tqdm import tqdm

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 添加以下代码以确保中文显示
import matplotlib as mpl
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi', 'FangSong', 'SimSun', 'Arial Unicode MS']
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

class BaccaratGame:
    def __init__(self, num_decks=8):
        self.num_decks = num_decks
        self.reset_shoe()
        
    def reset_shoe(self):
        # 初始化牌靴 (8副牌)
        cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4 * self.num_decks
        random.shuffle(cards)
        self.shoe = cards
        
    def get_card_value(self, card):
        if card in ['10', 'J', 'Q', 'K']:
            return 0
        elif card == 'A':
            return 1
        else:
            return int(card)
    
    def calculate_points(self, cards):
        total = sum(self.get_card_value(card) for card in cards)
        return total % 10  # 取个位数
    
    def draw_card(self):
        if len(self.shoe) < 52:  # 当牌靴中牌数少于一副牌时，重新洗牌
            self.reset_shoe()
        return self.shoe.pop()
    
    def should_player_draw(self, player_points):
        return player_points <= 5
    
    def should_banker_draw(self, banker_points, player_third_card=None):
        if banker_points >= 7:
            return False
        if banker_points <= 2:
            return True
        
        if player_third_card is None:  # 闲家没有补第三张牌
            return banker_points <= 5
        
        # 庄家补牌规则
        if banker_points == 3:
            return player_third_card != '8'
        elif banker_points == 4:
            return player_third_card in ['2', '3', '4', '5', '6', '7']
        elif banker_points == 5:
            return player_third_card in ['4', '5', '6', '7']
        elif banker_points == 6:
            return player_third_card in ['6', '7']
        
        return False
    
    def play_hand(self):
        # 发牌
        player_cards = [self.draw_card(), self.draw_card()]
        banker_cards = [self.draw_card(), self.draw_card()]
        
        player_points = self.calculate_points(player_cards)
        banker_points = self.calculate_points(banker_cards)
        
        # 检查自然赢家 (Natural)
        if player_points >= 8 or banker_points >= 8:
            return self.determine_winner(player_points, banker_points)
        
        # 闲家补牌
        player_third_card = None
        if self.should_player_draw(player_points):
            player_third_card = self.draw_card()
            player_cards.append(player_third_card)
            player_points = self.calculate_points(player_cards)
        
        # 庄家补牌
        if self.should_banker_draw(banker_points, player_third_card):
            banker_cards.append(self.draw_card())
            banker_points = self.calculate_points(banker_cards)
        
        return self.determine_winner(player_points, banker_points)
    
    def determine_winner(self, player_points, banker_points):
        if player_points > banker_points:
            return "player", player_points, banker_points
        elif banker_points > player_points:
            return "banker", player_points, banker_points
        else:
            return "tie", player_points, banker_points

class BaccaratSimulator:
    def __init__(self, initial_balance=100000, bet_unit= 200 ):
        self.game = BaccaratGame()
        self.initial_balance = initial_balance
        self.bet_unit = bet_unit
        
    def simulate_strategy(self, strategy, num_hands=1000):
        balance = self.initial_balance
        balance_history = [balance]
        win_count = {"player": 0, "banker": 0, "tie": 0}
        
        for _ in range(num_hands):
            if balance <= 0:
                break
                
            # 根据策略决定投注
            bet_on, bet_amount = strategy(balance, self.bet_unit, win_count)
            bet_amount = min(bet_amount, balance)  # 确保投注金额不超过余额
            
            # 玩一手百家乐
            winner, player_points, banker_points = self.game.play_hand()
            win_count[winner] += 1
            
            # 计算赢/输
            if winner == bet_on:
                if winner == "banker":
                    # 庄家抽水5%
                    balance += bet_amount * 0.95
                elif winner == "player":
                    balance += bet_amount
                elif winner == "tie":
                    balance += bet_amount * 8  # 和局赔率8:1
            elif winner == "tie" and bet_on != "tie":
                # 押注庄/闲，结果是和，退回本金
                pass
            else:
                balance -= bet_amount
                
            balance_history.append(int(balance))
            
        return {
            "final_balance": balance,
            "balance_history": balance_history,
            "win_count": win_count,
            "num_hands_played": min(num_hands, len(balance_history) - 1)
        }

# 定义不同的投注策略
def always_player(balance, bet_unit, win_count):
    """始终押注闲家"""
    return "player", bet_unit

def always_banker(balance, bet_unit, win_count):
    """始终押注庄家"""
    return "banker", bet_unit

def alternate_player_banker(balance, bet_unit, win_count):
    """交替押注庄家和闲家"""
    total_hands = sum(win_count.values())
    return "player" if total_hands % 2 == 0 else "banker", bet_unit

def follow_banker_streak(balance, bet_unit, win_count):
    """见庄跟庄策略"""
    # 获取最近的结果
    total_hands = sum(win_count.values())
    if total_hands == 0 or win_count["banker"] == 0:
        return "player", bet_unit
    
    banker_ratio = win_count["banker"] / total_hands
    if banker_ratio > 0.5:
        return "banker", bet_unit
    else:
        return "player", bet_unit

def martingale_player(balance, bet_unit, win_count):
    """Martin格尔策略 - 押注闲家"""
    # 简化版Martin格尔：输了就加倍，赢了就回到基本投注
    total_hands = sum(win_count.values())
    if total_hands == 0:
        return "player", bet_unit
    
    # 检查上一手是否输了
    if win_count["banker"] + win_count["tie"] > 0:
        last_bet = bet_unit * (2 ** (win_count["banker"] % 5))  # 限制最大加倍次数为5
        return "player", min(last_bet, balance // 2)  # 确保不会一次性押上所有筹码
    else:
        return "player", bet_unit

# 运行模拟
def run_simulations(num_simulations=5, num_hands=10000):
    strategies = {
        "始终押注闲家": always_player,
        "始终押注庄家": always_banker,
        "交替押注": alternate_player_banker,
        "见庄跟庄": follow_banker_streak,
        "Martin格尔(闲)": martingale_player
    }
    
    results = {}
    
    for strategy_name, strategy_func in strategies.items():
        strategy_results = []
        
        for _ in tqdm(range(num_simulations), desc=f"模拟 {strategy_name}"):
            simulator = BaccaratSimulator()
            result = simulator.simulate_strategy(strategy_func, num_hands)
            strategy_results.append(result)
            
        results[strategy_name] = strategy_results
        
    return results

# 可视化结果
def visualize_results(results, num_hands):
    # 设置更美观的风格
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 确保中文显示正确
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi', 'FangSong', 'SimSun', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 1. 最终余额比较 - 使用小提琴图替代箱线图，更能显示分布特性
    plt.figure(figsize=(14, 8))
    final_balances = {}
    
    for strategy, strategy_results in results.items():
        final_balances[strategy] = [result["final_balance"] for result in strategy_results]
    
    df_balances = pd.DataFrame(final_balances)
    
    # 使用小提琴图展示分布
    sns.violinplot(data=df_balances, palette="Set3")
    plt.title('不同策略的最终余额分布', fontsize=18, fontweight='bold')
    plt.ylabel('最终余额', fontsize=16)
    plt.xlabel('投注策略', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig('e:\\Desktop\\1\\百家乐1\\最终余额分布.png', dpi=300, bbox_inches='tight')
    
    # 2. 余额变化曲线 - 增加平均线和置信区间
    plt.figure(figsize=(16, 10))
    
    # 使用更丰富的颜色方案
    colors = plt.cm.tab10(np.linspace(0, 1, len(results)))
    
    for (strategy, strategy_results), color in zip(results.items(), colors):
        # 计算所有模拟的平均余额变化
        all_histories = [result["balance_history"] for result in strategy_results]
        # 找到最短的历史记录长度
        min_length = min(len(history) for history in all_histories)
        # 截断所有历史记录到相同长度
        truncated_histories = [history[:min_length] for history in all_histories]
        # 计算平均值和标准差
        mean_balance = np.mean(truncated_histories, axis=0)
        #std_balance = np.std(truncated_histories, axis=0)
        
        # 绘制平均线
        x = np.arange(len(mean_balance))
        plt.plot(x, mean_balance, label=strategy, color=color, linewidth=2.5)
        # 添加置信区间
        #plt.fill_between(x, mean_balance-std_balance, mean_balance+std_balance, 
                         #alpha=0.2, color=color)
    
    plt.title('不同策略的余额变化趋势 (不含置信区间)', fontsize=18, fontweight='bold')
    plt.xlabel('游戏局数', fontsize=16)
    plt.ylabel('余额', fontsize=16)
    plt.legend(fontsize=14, loc='best', frameon=True, facecolor='white', edgecolor='gray')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('e:\\Desktop\\1\\百家乐1\\余额变化趋势.png', dpi=300, bbox_inches='tight')
    
    # 3. 胜率分析 - 使用更美观的堆叠条形图
    plt.figure(figsize=(16, 10))
    win_rates = {}
    
    for strategy, strategy_results in results.items():
        # 计算平均胜率
        player_wins = sum(result["win_count"]["player"] for result in strategy_results)
        banker_wins = sum(result["win_count"]["banker"] for result in strategy_results)
        tie_wins = sum(result["win_count"]["tie"] for result in strategy_results)
        total_hands = player_wins + banker_wins + tie_wins
        
        win_rates[strategy] = {
            "闲家胜率": player_wins / total_hands * 100,
            "庄家胜率": banker_wins / total_hands * 100,
            "和局概率": tie_wins / total_hands * 100
        }
    
    df_win_rates = pd.DataFrame(win_rates).T
    
    # 使用堆叠条形图
    ax = df_win_rates.plot(kind='bar', stacked=True, figsize=(16, 10), 
                          colormap='viridis', width=0.7)
    
    # 在每个条形上添加百分比标签
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%', fontsize=12)
    
    plt.title('各投注选项的胜率分析', fontsize=18, fontweight='bold')
    plt.xlabel('投注策略', fontsize=16)
    plt.ylabel('胜率 (%)', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=14, title='结果类型', title_fontsize=14)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig('e:\\Desktop\\1\\百家乐1\\胜率分析.png', dpi=300, bbox_inches='tight')
    
    # 4. 策略收益率比较 - 使用水平条形图并添加误差线
    plt.figure(figsize=(14, 10))
    roi_data = {}
    roi_std = {}
    
    for strategy, strategy_results in results.items():
        roi_values = [(result["final_balance"] - 100000) / 100000 * 100 for result in strategy_results]
        roi_data[strategy] = np.mean(roi_values)
        roi_std[strategy] = np.std(roi_values)
    
    # 按收益率排序
    sorted_strategies = sorted(roi_data.keys(), key=lambda x: roi_data[x])
    sorted_roi = [roi_data[s] for s in sorted_strategies]
    sorted_std = [roi_std[s] for s in sorted_strategies]
    
    # 创建水平条形图
    bars = plt.barh(sorted_strategies, sorted_roi, xerr=sorted_std, 
                   color=plt.cm.RdYlGn(np.linspace(0, 1, len(sorted_strategies))),
                   alpha=0.8, capsize=5)
    
    # 在条形上添加数值标签
    for i, bar in enumerate(bars):
        width = bar.get_width()
        label_x_pos = width + 0.5 if width >= 0 else width - 3
        plt.text(label_x_pos, bar.get_y() + bar.get_height()/2, 
                f'{sorted_roi[i]:.2f}%', va='center', fontsize=12,
                fontweight='bold')
    
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.7)
    plt.title('不同策略的平均收益率 (含标准差)', fontsize=18, fontweight='bold')
    plt.xlabel('收益率 (%)', fontsize=16)
    plt.ylabel('投注策略', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('e:\\Desktop\\1\\百家乐1\\平均收益率.png', dpi=300, bbox_inches='tight')
    
    # 5. 策略风险-收益分析 (散点图)
    plt.figure(figsize=(14, 10))
    
    # 计算每种策略的风险(标准差)和收益(平均收益率)
    risk_reward = {}
    for strategy, strategy_results in results.items():
        roi_values = [(result["final_balance"] - 100000) / 100000 * 100 for result in strategy_results]
        risk_reward[strategy] = {
            'risk': np.std(roi_values),
            'reward': np.mean(roi_values),
            'win_rate': np.mean([result["win_count"]["player"] + result["win_count"]["banker"] for result in strategy_results]) / 
                       np.mean([result["num_hands_played"] for result in strategy_results]) * 100
        }
    
    # 转换为DataFrame
    df_risk_reward = pd.DataFrame.from_dict(risk_reward, orient='index')
    
    # 绘制散点图，点大小表示胜率
    plt.figure(figsize=(14, 10))
    scatter = plt.scatter(df_risk_reward['risk'], df_risk_reward['reward'], 
                         s=df_risk_reward['win_rate']*10, # 点大小与胜率成正比
                         c=df_risk_reward['reward'], # 颜色与收益率相关
                         cmap='RdYlGn', alpha=0.7)
    
    # 添加策略标签
    for strategy in risk_reward:
        plt.annotate(strategy, 
                    (df_risk_reward.loc[strategy, 'risk'], df_risk_reward.loc[strategy, 'reward']),
                    fontsize=12, fontweight='bold',
                    xytext=(5, 5), textcoords='offset points')
    
    # 添加颜色条
    cbar = plt.colorbar(scatter)
    cbar.set_label('收益率 (%)', fontsize=14)
    
    # 添加参考线
    plt.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
    plt.axvline(x=0, color='gray', linestyle='--', alpha=0.7)
    
    plt.title('策略风险-收益分析 (点大小表示胜率)', fontsize=18, fontweight='bold')
    plt.xlabel('风险 (收益率标准差)', fontsize=16)
    plt.ylabel('收益率 (%)', fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('e:\\Desktop\\1\\百家乐1\\风险收益分析.png', dpi=300, bbox_inches='tight')
    
    # 6. 策略表现热力图
    plt.figure(figsize=(16, 12))
    
    # 准备热力图数据
    heatmap_data = []
    for strategy, strategy_results in results.items():
        avg_final_balance = np.mean([result["final_balance"] for result in strategy_results])
        roi = (avg_final_balance - 100000) / 100000 * 100
        std_dev = np.std([result["final_balance"] for result in strategy_results])
        
        # 计算平均每局收益
        avg_profit_per_hand = roi / num_hands
        
        # 计算破产概率 (余额低于初始余额的10%)
        bankruptcy_prob = sum(1 for result in strategy_results if result["final_balance"] < 10000) / len(strategy_results) * 100
        
        # 计算最大回撤
        max_drawdowns = []
        for result in strategy_results:
            balance_history = result["balance_history"]
            max_drawdown = 0
            peak = balance_history[0]
            
            for balance in balance_history:
                if balance > peak:
                    peak = balance
                drawdown = (peak - balance) / peak * 100
                max_drawdown = max(max_drawdown, drawdown)
            
            max_drawdowns.append(max_drawdown)
        
        avg_max_drawdown = np.mean(max_drawdowns)
        
        heatmap_data.append({
            '策略': strategy,
            '平均最终余额': avg_final_balance,
            '收益率(%)': roi,
            '标准差': std_dev,
            '每局平均收益(%)': avg_profit_per_hand,
            '破产概率(%)': bankruptcy_prob,
            '平均最大回撤(%)': avg_max_drawdown
        })
    
    df_heatmap = pd.DataFrame(heatmap_data)
    df_heatmap.set_index('策略', inplace=True)
    
    # 选择要显示的指标
    #metrics = ['收益率(%)', '标准差', '每局平均收益(%)', '破产概率(%)', '平均最大回撤(%)']
    metrics = ['收益率(%)', '每局平均收益(%)', '破产概率(%)', '平均最大回撤(%)']
    # 创建热力图
    sns.heatmap(df_heatmap[metrics], annot=True, fmt='.2f', cmap='RdYlGn_r', 
               linewidths=0.5, cbar_kws={'label': '数值大小'})
    
    plt.title('策略综合表现评估', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('e:\\Desktop\\1\\百家乐1\\策略综合评估.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    # 设置模拟参数
    num_simulations = 50  # 每个策略模拟的次数
    num_hands = 1000     # 每次模拟的游戏局数
    
    print("开始百家乐策略模拟分析...")
    results = run_simulations(num_simulations, num_hands)
    print("模拟完成，正在生成可视化结果...")
    visualize_results(results, num_hands)
    print("分析完成！可视化结果已保存到文件夹中。")