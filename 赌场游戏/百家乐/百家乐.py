import random
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class Baccarat:
    def __init__(self):
        self.deck = []
        self.player_cards = []
        self.banker_cards = []
        self.create_deck(8)  # 使用8副牌
        self.shuffle_deck()
        self.player_score = 0
        self.banker_score = 0
        self.balance = 1000  # 初始余额
        self.game_history = []  # 记录游戏历史
        
    def create_deck(self, num_decks):
        """创建指定副数的牌组"""
        suits = ['♥', '♦', '♣', '♠']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for _ in range(num_decks):
            for suit in suits:
                for rank in ranks:
                    self.deck.append((rank, suit))
    
    def shuffle_deck(self):
        """洗牌"""
        random.shuffle(self.deck)
        
    def draw_card(self):
        """抽取一张牌"""
        if len(self.deck) < 10:  # 牌不够时重新洗牌
            self.create_deck(8)
            self.shuffle_deck()
        return self.deck.pop()
    
    def calculate_points(self, cards):
        """计算牌的点数"""
        points = 0
        for card in cards:
            rank = card[0]
            if rank in ['10', 'J', 'Q', 'K']:
                value = 0
            elif rank == 'A':
                value = 1
            else:
                value = int(rank)
            points += value
        return points % 10  # 取个位数
    
    def need_third_card_player(self):
        """判断闲家是否需要补第三张牌"""
        return self.player_score <= 5
    
    def need_third_card_banker(self, player_third_card=None):
        """判断庄家是否需要补第三张牌"""
        if self.banker_score <= 2:
            return True
        elif self.banker_score == 3:
            return player_third_card is None or player_third_card[0] != '8'
        elif self.banker_score == 4:
            return player_third_card is not None and player_third_card[0] in ['2', '3', '4', '5', '6', '7']
        elif self.banker_score == 5:
            return player_third_card is not None and player_third_card[0] in ['4', '5', '6', '7']
        elif self.banker_score == 6:
            return player_third_card is not None and player_third_card[0] in ['6', '7']
        return False
    
    def display_cards(self, cards):
        """显示牌"""
        return ' '.join([f"{card[0]}{card[1]}" for card in cards])
    
    def play_round(self, bet_on, bet_amount, verbose=True):
        """进行一局游戏"""
        if bet_amount > self.balance:
            if verbose:
                print(f"余额不足！当前余额: {self.balance}")
            return False
        
        self.balance -= bet_amount
        self.player_cards = []
        self.banker_cards = []
        
        # 发牌
        if verbose:
            print("\n开始发牌...")
            time.sleep(0.5)
        
        # 闲家第一张牌
        self.player_cards.append(self.draw_card())
        if verbose:
            print(f"闲家第一张牌: {self.player_cards[-1][0]}{self.player_cards[-1][1]}")
            time.sleep(0.2)
        
        # 庄家第一张牌
        self.banker_cards.append(self.draw_card())
        if verbose:
            print(f"庄家第一张牌: {self.banker_cards[-1][0]}{self.banker_cards[-1][1]}")
            time.sleep(0.2)
        
        # 闲家第二张牌
        self.player_cards.append(self.draw_card())
        if verbose:
            print(f"闲家第二张牌: {self.player_cards[-1][0]}{self.player_cards[-1][1]}")
            time.sleep(0.2)
        
        # 庄家第二张牌
        self.banker_cards.append(self.draw_card())
        if verbose:
            print(f"庄家第二张牌: {self.banker_cards[-1][0]}{self.banker_cards[-1][1]}")
            time.sleep(0.2)
        
        # 计算初始点数
        self.player_score = self.calculate_points(self.player_cards)
        self.banker_score = self.calculate_points(self.banker_cards)
        
        if verbose:
            print(f"\n闲家前两张牌: {self.display_cards(self.player_cards)} = {self.player_score}点")
            print(f"庄家前两张牌: {self.display_cards(self.banker_cards)} = {self.banker_score}点")
        
        # 检查天生赢家（Natural）
        natural = False
        if self.player_score >= 8 or self.banker_score >= 8:
            if verbose:
                print("出现天生赢家（Natural），无需补牌！")
            natural = True
        else:
            # 闲家补牌
            player_third_card = None
            if self.need_third_card_player():
                player_third_card = self.draw_card()
                self.player_cards.append(player_third_card)
                self.player_score = self.calculate_points(self.player_cards)
                if verbose:
                    print(f"\n闲家补第三张牌: {player_third_card[0]}{player_third_card[1]}")
                    print(f"闲家三张牌: {self.display_cards(self.player_cards)} = {self.player_score}点")
                    time.sleep(0.2)
            elif verbose:
                print("\n闲家不补牌")
            
            # 庄家补牌
            if self.need_third_card_banker(player_third_card):
                self.banker_cards.append(self.draw_card())
                self.banker_score = self.calculate_points(self.banker_cards)
                if verbose:
                    print(f"庄家补第三张牌: {self.banker_cards[-1][0]}{self.banker_cards[-1][1]}")
                    print(f"庄家三张牌: {self.display_cards(self.banker_cards)} = {self.banker_score}点")
            elif verbose:
                print("庄家不补牌")
        
        # 显示最终结果
        if verbose:
            print("\n=== 最终结果 ===")
            print(f"闲家: {self.display_cards(self.player_cards)} = {self.player_score}点")
            print(f"庄家: {self.display_cards(self.banker_cards)} = {self.banker_score}点")
        
        # 判断胜负
        result = ""
        win_amount = -bet_amount  # 默认输掉投注金额
        
        if self.player_score > self.banker_score:
            result = "闲家胜"
            if bet_on == "闲":
                win_amount = bet_amount  # 赢得等同于投注金额的筹码
                self.balance += bet_amount * 2  # 返还本金和赢得的筹码
                if verbose:
                    print(f"恭喜！你赢了 {win_amount} 筹码")
            elif verbose:
                print(f"很遗憾，你输了 {bet_amount} 筹码")
        elif self.banker_score > self.player_score:
            result = "庄家胜"
            if bet_on == "庄":
                win_amount = bet_amount * 0.95  # 赢得投注金额的95%（扣除5%佣金）
                self.balance += bet_amount * 1.95  # 返还本金和赢得的筹码（扣除佣金）
                if verbose:
                    print(f"恭喜！你赢了 {win_amount} 筹码（已扣除5%佣金）")
            elif verbose:
                print(f"很遗憾，你输了 {bet_amount} 筹码")
        else:
            result = "和局"
            if bet_on == "和":
                win_amount = bet_amount * 8  # 赢得投注金额的8倍
                self.balance += bet_amount * 9  # 返还本金和赢得的筹码
                if verbose:
                    print(f"恭喜！和局赔率8:1，你赢了 {win_amount} 筹码")
            else:
                win_amount = 0  # 和局退还本金
                self.balance += bet_amount  # 和局退还本金
                if verbose:
                    print("和局，退还本金")
        
        if verbose:
            print(f"结果: {result}")
            print(f"当前余额: {self.balance}")
        
        # 记录游戏历史
        self.game_history.append({
            'bet_on': bet_on,
            'bet_amount': bet_amount,
            'result': result,
            'win_amount': win_amount,
            'player_score': self.player_score,
            'banker_score': self.banker_score,
            'natural': natural,
            'balance': self.balance
        })
        
        return True
        
    def display_rules(self):
        """显示游戏规则"""
        print("\n=== 百家乐游戏规则 ===")
        print("1. 游戏目标：预测庄家或闲家哪一方的牌点数更接近9点")
        print("2. 牌面点数：A为1点，2-9按面值计算，10/J/Q/K为0点")
        print("3. 计算方式：两张或三张牌的总点数取个位数（如：7+8=15，计为5点）")
        print("4. 补牌规则：")
        print("   - 闲家点数为0-5时必须补牌，6-7点不补牌")
        print("   - 庄家补牌规则较复杂，根据自身点数和闲家第三张牌决定")
        print("5. 赔率：")
        print("   - 押庄赢：1:1（扣除5%佣金）")
        print("   - 押闲赢：1:1")
        print("   - 押和局：8:1")
        print("6. 天生赢家：任一方前两张牌达到8或9点，则为天生赢家，无需补牌")
    
    def simulate_strategy(self, strategy, num_rounds=1000, bet_amount=10):
        """模拟不同策略的结果"""
        original_balance = self.balance
        self.balance = 1000  # 重置余额
        self.game_history = []  # 重置游戏历史
        
        print(f"\n=== 模拟策略: {strategy} ===")
        print(f"初始余额: {self.balance}")
        print(f"模拟局数: {num_rounds}")
        print(f"每局投注: {bet_amount}")
        
        balances = [self.balance]  # 记录每局后的余额变化
        
        # 连续输赢记录
        current_streak = 0
        max_win_streak = 0
        max_lose_streak = 0
        
        # 策略变量
        last_result = None
        
        for i in range(num_rounds):
            if self.balance < bet_amount:
                print(f"余额不足，无法继续。停止于第 {i} 局")
                break
                
            # 根据不同策略决定投注
            if strategy == "始终押庄":
                bet_on = "庄"
                current_bet = bet_amount
            elif strategy == "始终押闲":
                bet_on = "闲"
                current_bet = bet_amount
            elif strategy == "始终押和":
                bet_on = "和"
                current_bet = bet_amount
            elif strategy == "交替押注":
                bet_on = "庄" if i % 2 == 0 else "闲"
                current_bet = bet_amount
            elif strategy == "跟上把赢家":
                if last_result is None or last_result == "和局":
                    bet_on = "庄"  # 默认押庄
                else:
                    bet_on = "庄" if last_result == "庄家胜" else "闲"
                current_bet = bet_amount
            elif strategy == "反上把赢家":
                if last_result is None or last_result == "和局":
                    bet_on = "庄"  # 默认押庄
                else:
                    bet_on = "闲" if last_result == "庄家胜" else "庄"
                current_bet = bet_amount
            elif strategy == "Martin格尔":
                # Martin格尔策略：输了就翻倍投注
                current_bet = bet_amount * (2 ** abs(min(0, current_streak)))
                current_bet = min(current_bet, self.balance)  # 确保不超过余额
                bet_on = "庄"
            else:
                bet_on = random.choice(["庄", "闲"])  # 随机策略
                current_bet = bet_amount
            
            # 进行游戏
            self.play_round(bet_on, current_bet, verbose=False)
            balances.append(self.balance)
            
            # 更新连续输赢记录
            last_game = self.game_history[-1]
            if last_game['win_amount'] > 0:
                current_streak = max(0, current_streak + 1)
                max_win_streak = max(max_win_streak, current_streak)
            else:
                current_streak = min(0, current_streak - 1)
                max_lose_streak = max(max_lose_streak, abs(current_streak))
            
            last_result = last_game['result']
        
        # 计算统计数据
        final_balance = self.balance
        profit = final_balance - 1000
        win_count = sum(1 for game in self.game_history if game['win_amount'] > 0)
        lose_count = sum(1 for game in self.game_history if game['win_amount'] < 0)
        tie_count = sum(1 for game in self.game_history if game['win_amount'] == 0)
        win_rate = win_count / len(self.game_history) if self.game_history else 0
        
        # 输出统计结果
        print(f"\n=== {strategy} 策略统计 ===")
        print(f"总局数: {len(self.game_history)}")
        print(f"胜局数: {win_count} ({win_rate:.2%})")
        print(f"负局数: {lose_count} ({lose_count/len(self.game_history):.2%})")
        print(f"和局数: {tie_count} ({tie_count/len(self.game_history):.2%})")
        print(f"最大连胜: {max_win_streak}")
        print(f"最大连败: {max_lose_streak}")
        print(f"最终余额: {final_balance}")
        print(f"总盈亏: {profit} ({profit/1000:.2%})")
        
        # 绘制余额变化图
        plt.figure(figsize=(10, 6))
        plt.plot(balances, linewidth=2)
        plt.axhline(y=1000, color='r', linestyle='--', alpha=0.7)
        plt.title(f"{strategy}策略 - 余额变化", fontsize=15)
        plt.xlabel("游戏局数", fontsize=12)
        plt.ylabel("余额", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.savefig(f"e:\\Desktop\\1\\{strategy}_余额变化.png", dpi=300, bbox_inches='tight')
        
        # 恢复原始余额
        self.balance = original_balance
        
        return {
            'strategy': strategy,
            'rounds': len(self.game_history),
            'win_rate': win_rate,
            'profit': profit,
            'profit_rate': profit/1000,
            'max_win_streak': max_win_streak,
            'max_lose_streak': max_lose_streak,
            'balances': balances
        }
    
    def compare_strategies(self, num_rounds=1000, bet_amount=10):
        """比较不同策略的效果"""
        strategies = [
            "始终押庄", 
            "始终押闲", 
            "始终押和", 
            "交替押注", 
            "跟上把赢家", 
            "反上把赢家", 
            "Martin格尔"
        ]
        
        results = []
        for strategy in strategies:
            print(f"\n开始模拟 {strategy} 策略...")
            result = self.simulate_strategy(strategy, num_rounds, bet_amount)
            results.append(result)
        
        # 绘制策略比较图
        self.plot_strategy_comparison(results)
        
        return results
    
    def plot_strategy_comparison(self, results):
        """绘制策略比较图表"""
        # 1. 盈利率比较
        plt.figure(figsize=(12, 6))
        strategies = [r['strategy'] for r in results]
        profits = [r['profit_rate'] * 100 for r in results]
        
        colors = ['#3498db' if p >= 0 else '#e74c3c' for p in profits]
        plt.bar(strategies, profits, color=colors)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.title("不同策略盈利率比较", fontsize=15)
        plt.ylabel("盈利率(%)", fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        for i, p in enumerate(profits):
            plt.text(i, p + (1 if p >= 0 else -1), f"{p:.1f}%", ha='center')
        plt.savefig("e:\\Desktop\\1\\策略盈利率比较.png", dpi=300, bbox_inches='tight')
        
        # 2. 胜率比较
        plt.figure(figsize=(12, 6))
        win_rates = [r['win_rate'] * 100 for r in results]
        plt.bar(strategies, win_rates, color='#2ecc71')
        plt.title("不同策略胜率比较", fontsize=15)
        plt.ylabel("胜率(%)", fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        for i, w in enumerate(win_rates):
            plt.text(i, w + 0.5, f"{w:.1f}%", ha='center')
        plt.savefig("e:\\Desktop\\1\\策略胜率比较.png", dpi=300, bbox_inches='tight')
        
        # 3. 余额变化趋势比较
        plt.figure(figsize=(12, 8))
        for r in results:
            plt.plot(r['balances'], label=r['strategy'], linewidth=2)
        plt.axhline(y=1000, color='r', linestyle='--', alpha=0.5, label='初始余额')
        plt.title("不同策略余额变化趋势比较", fontsize=15)
        plt.xlabel("游戏局数", fontsize=12)
        plt.ylabel("余额", fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.savefig("e:\\Desktop\\1\\策略余额趋势比较.png", dpi=300, bbox_inches='tight')
        
        # 4. 连胜连败比较
        plt.figure(figsize=(12, 6))
        max_win_streaks = [r['max_win_streak'] for r in results]
        max_lose_streaks = [r['max_lose_streak'] for r in results]
        
        x = np.arange(len(strategies))
        width = 0.35
        
        plt.bar(x - width/2, max_win_streaks, width, label='最大连胜', color='#3498db')
        plt.bar(x + width/2, max_lose_streaks, width, label='最大连败', color='#e74c3c')
        
        plt.title("不同策略连胜连败比较", fontsize=15)
        plt.xticks(x, strategies)
        plt.ylabel("局数", fontsize=12)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        for i, v in enumerate(max_win_streaks):
            plt.text(i - width/2, v + 0.3, str(v), ha='center')
        for i, v in enumerate(max_lose_streaks):
            plt.text(i + width/2, v + 0.3, str(v), ha='center')
            
        plt.savefig("e:\\Desktop\\1\\策略连胜连败比较.png", dpi=300, bbox_inches='tight')
    
    def analyze_game_patterns(self):
        """分析游戏模式和规律"""
        if not self.game_history:
            print("没有游戏历史记录可供分析")
            return
        
        # 统计庄闲和出现频率
        results = [game['result'] for game in self.game_history]
        banker_wins = results.count("庄家胜")
        player_wins = results.count("闲家胜")
        ties = results.count("和局")
        
        total_games = len(results)
        banker_rate = banker_wins / total_games
        player_rate = player_wins / total_games
        tie_rate = ties / total_games
        
        # 统计天生赢家出现频率
        naturals = sum(1 for game in self.game_history if game['natural'])
        natural_rate = naturals / total_games
        
        # 统计点数分布
        player_scores = [game['player_score'] for game in self.game_history]
        banker_scores = [game['banker_score'] for game in self.game_history]
        
        # 绘制结果分布饼图
        plt.figure(figsize=(10, 8))
        plt.pie([banker_wins, player_wins, ties], 
                labels=['庄家胜', '闲家胜', '和局'],
                autopct='%1.1f%%',
                colors=['#3498db', '#e74c3c', '#2ecc71'],
                startangle=90,
                explode=(0.05, 0.05, 0.1))
        plt.title('百家乐游戏结果分布', fontsize=15)
        plt.savefig("e:\\Desktop\\1\\游戏结果分布.png", dpi=300, bbox_inches='tight')
        
        # 绘制点数分布柱状图
        plt.figure(figsize=(12, 6))
        
        # 创建点数频率统计
        score_counts_player = [player_scores.count(i) for i in range(10)]
        score_counts_banker = [banker_scores.count(i) for i in range(10)]
        
        x = np.arange(10)
        width = 0.35
        
        plt.bar(x - width/2, score_counts_player, width, label='闲家点数', color='#3498db')
        plt.bar(x + width/2, score_counts_banker, width, label='庄家点数', color='#e74c3c')
        
        plt.title('庄闲点数分布', fontsize=15)
        plt.xlabel('点数', fontsize=12)
        plt.ylabel('频率', fontsize=12)
        plt.xticks(x)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.savefig("e:\\Desktop\\1\\点数分布.png", dpi=300, bbox_inches='tight')
        
        # 输出统计结果
        print("\n=== 游戏模式分析 ===")
        print(f"总局数: {total_games}")
        print(f"庄家胜率: {banker_rate:.2%}")
        print(f"闲家胜率: {player_rate:.2%}")
        print(f"和局概率: {tie_rate:.2%}")
        print(f"天生赢家出现率: {natural_rate:.2%}")
        
        # 分析连续出现的模式
        self.analyze_consecutive_patterns(results)
        
    def analyze_consecutive_patterns(self, results):
        """分析连续出现的模式"""
        # 统计连续出现的庄、闲
        max_consecutive_banker = 0
        max_consecutive_player = 0
        current_consecutive_banker = 0
        current_consecutive_player = 0
        
        for result in results:
            if result == "庄家胜":
                current_consecutive_banker += 1
                current_consecutive_player = 0
                max_consecutive_banker = max(max_consecutive_banker, current_consecutive_banker)
            elif result == "闲家胜":
                current_consecutive_player += 1
                current_consecutive_banker = 0
                max_consecutive_player = max(max_consecutive_player, current_consecutive_player)
            else:  # 和局
                continue
        
        print(f"最大连续庄: {max_consecutive_banker}")
        print(f"最大连续闲: {max_consecutive_player}")
        
        # 分析常见模式
        pattern_length = 3  # 分析3连模式
        patterns = {}
        
        for i in range(len(results) - pattern_length + 1):
            pattern = tuple(results[i:i+pattern_length])
            if pattern in patterns:
                patterns[pattern] += 1
            else:
                patterns[pattern] = 1
        
        # 输出最常见的模式
        print("\n最常见的游戏模式:")
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        for i, (pattern, count) in enumerate(sorted_patterns[:5]):
            pattern_str = " -> ".join(pattern)
            print(f"{i+1}. {pattern_str}: 出现{count}次 ({count/len(results):.2%})")
    
    def simulate_single_strategy_menu(self):
        """单一策略模拟菜单"""
        print("\n=== 单一策略模拟 ===")
        print("可选策略:")
        print("1. 始终押庄")
        print("2. 始终押闲")
        print("3. 始终押和")
        print("4. 交替押注")
        print("5. 跟上把赢家")
        print("6. 反上把赢家")
        print("7. Martin格尔")
        
        choice = input("请选择策略(1-7): ")
        strategies = ["始终押庄", "始终押闲", "始终押和", "交替押注", "跟上把赢家", "反上把赢家", "Martin格尔"]
        
        try:
            strategy_index = int(choice) - 1
            if 0 <= strategy_index < len(strategies):
                rounds = int(input("请输入模拟局数: "))
                bet = int(input("请输入每局投注金额: "))
                self.simulate_strategy(strategies[strategy_index], rounds, bet)
            else:
                print("无效选择")
        except ValueError:
            print("请输入有效数字")
    
    def play_game_menu(self):
        """游戏菜单"""
        while True:
            print("\n=== 百家乐游戏 ===")
            print(f"当前余额: {self.balance}")
            print("1. 开始游戏")
            print("2. 充值")
            print("3. 返回主菜单")
            
            choice = input("请选择: ")
            
            if choice == "1":
                while True:
                    print("\n=== 投注选项 ===")
                    print("1. 押庄")
                    print("2. 押闲")
                    print("3. 押和")
                    print("4. 返回")
                    
                    bet_choice = input("请选择投注选项: ")
                    
                    if bet_choice in ["1", "2", "3"]:
                        bet_options = {"1": "庄", "2": "闲", "3": "和"}
                        bet_on = bet_options[bet_choice]
                        
                        try:
                            bet_amount = int(input(f"请输入投注金额（当前余额: {self.balance}）: "))
                            if bet_amount <= 0:
                                print("投注金额必须大于0")
                                continue
                            
                            # 进行游戏
                            self.play_round(bet_on, bet_amount)
                        except ValueError:
                            print("请输入有效数字")
                    elif bet_choice == "4":
                        break
                    else:
                        print("无效选择")
            elif choice == "2":
                try:
                    amount = int(input("请输入充值金额: "))
                    if amount > 0:
                        self.balance += amount
                        print(f"充值成功！当前余额: {self.balance}")
                    else:
                        print("充值金额必须大于0")
                except ValueError:
                    print("请输入有效数字")
            elif choice == "3":
                break
            else:
                print("无效选择")
    
    def main_menu(self):
        """主菜单"""
        while True:
            print("\n=== 百家乐游戏与分析系统 ===")
            print("1. 开始游戏")
            print("2. 查看游戏规则")
            print("3. 模拟单一策略")
            print("4. 比较多种策略")
            print("5. 分析游戏模式")
            print("6. 退出")
            
            choice = input("请选择: ")
            
            if choice == "1":
                self.play_game_menu()
            elif choice == "2":
                self.display_rules()
            elif choice == "3":
                self.simulate_single_strategy_menu()
            elif choice == "4":
                rounds = int(input("请输入模拟局数(建议1000-5000): "))
                bet = int(input("请输入每局投注金额: "))
                self.compare_strategies(rounds, bet)
                print("策略比较完成，图表已保存到桌面")
            elif choice == "5":
                if not self.game_history:
                    print("没有游戏历史记录，请先进行游戏或模拟")
                    continue
                self.analyze_game_patterns()
            elif choice == "6":
                print("感谢使用，再见！")
                break
            else:
                print("无效选择，请重新输入")

# 主程序入口
if __name__ == "__main__":
    print("欢迎使用百家乐游戏与策略分析系统！")
    print("本系统可以模拟百家乐游戏，并分析不同投注策略的效果")
    
    game = Baccarat()
    game.main_menu()