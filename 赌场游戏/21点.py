import random
import numpy as np
from collections import defaultdict

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f"{self.value}{self.suit}"
    
    def get_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11  # A的值会在Hand类中动态调整
        else:
            return int(self.value)

class Deck:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.reset()
    
    def reset(self):
        suits = ['♠', '♥', '♦', '♣']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = []
        for _ in range(self.num_decks):
            for suit in suits:
                for value in values:
                    self.cards.append(Card(suit, value))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) <= self.num_decks * 52 * 0.25:  # 当牌少于25%时洗牌
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self, bet=1):
        self.cards = []
        self.bet = bet
        self.is_split = False
        self.is_doubled = False
        self.is_blackjack = False
        self.is_surrender = False
    
    def add_card(self, card):
        self.cards.append(card)
        if len(self.cards) == 2 and self.get_value() == 21:
            self.is_blackjack = True
        return self
    
    def get_value(self):
        value = sum(card.get_value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.value == 'A')
        
        # 如果有A且总点数超过21，则将A视为1点
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        
        return value
    
    def is_soft(self):
        """判断是否为软手牌（含有作为11点的A）"""
        value = sum(card.get_value() for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.value == 'A')
        
        # 检查是否有A被计为11点
        return num_aces > 0 and value <= 21 and value - 10 * num_aces < 11
    
    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].get_value() == self.cards[1].get_value()
    
    def __str__(self):
        return " ".join(str(card) for card in self.cards) + f" ({self.get_value()})"

class Player:
    def __init__(self, strategy, initial_money=1000):
        self.hands = []
        self.strategy = strategy
        self.money = initial_money
        self.initial_money = initial_money
        self.bet_size = 1
    
    def place_bet(self):
        self.hands = [Hand(self.bet_size)]
        self.money -= self.bet_size
        return self.hands[0]
    
    def make_decision(self, hand, dealer_up_card):
        if hand.is_blackjack:
            return "S"  # 如果是黑杰克，自动停牌
        
        return self.strategy(hand, dealer_up_card)
    
    def double_down(self, hand_index):
        """双倍下注"""
        if len(self.hands[hand_index].cards) != 2:
            return False
        
        self.money -= self.hands[hand_index].bet
        self.hands[hand_index].bet *= 2
        self.hands[hand_index].is_doubled = True
        return True
    
    def split(self, hand_index, deck):
        """分牌"""
        hand = self.hands[hand_index]
        if not hand.can_split():
            return False
        
        # 从原手牌中取出第二张牌
        card = hand.cards.pop()
        
        # 创建新手牌并添加第二张牌
        new_hand = Hand(hand.bet)
        new_hand.add_card(card)
        new_hand.is_split = True
        
        # 为两手牌各发一张新牌
        hand.add_card(deck.deal())
        new_hand.add_card(deck.deal())
        
        # 扣除新的赌注
        self.money -= hand.bet
        
        # 将新手牌添加到玩家的手牌列表中
        self.hands.insert(hand_index + 1, new_hand)
        
        return True
    
    def surrender(self, hand_index):
        """投降"""
        if len(self.hands[hand_index].cards) != 2:
            return False
        
        self.hands[hand_index].is_surrender = True
        self.money += self.hands[hand_index].bet / 2  # 返还一半赌注
        return True

class Dealer:
    def __init__(self):
        self.hand = Hand()
    
    def show_card(self):
        """返回庄家的明牌"""
        return self.hand.cards[0]
    
    def play(self, deck):
        """庄家按规则要牌直到17点或以上"""
        while self.hand.get_value() < 17:
            self.hand.add_card(deck.deal())

class Game:
    def __init__(self, player, num_decks=6):
        self.deck = Deck(num_decks)
        self.player = player
        self.dealer = Dealer()
        self.num_hands = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
    
    def play_round(self):
        # 初始化
        self.dealer.hand = Hand()
        self.player.place_bet()
        
        # 发牌
        for _ in range(2):
            self.player.hands[0].add_card(self.deck.deal())
            self.dealer.hand.add_card(self.deck.deal())
        
        dealer_up_card = self.dealer.show_card()
        
        # 玩家回合
        hand_index = 0
        while hand_index < len(self.player.hands):
            hand = self.player.hands[hand_index]
            
            # 如果是黑杰克，直接进入下一手牌
            if hand.is_blackjack:
                hand_index += 1
                continue
            
            # 玩家决策
            while True:
                decision = self.player.make_decision(hand, dealer_up_card)
                
                if decision == "H":  # 要牌
                    hand.add_card(self.deck.deal())
                    if hand.get_value() >= 21:  # 爆牌或21点，停止要牌
                        break
                
                elif decision == "S":  # 停牌
                    break
                
                elif decision == "D":  # 双倍下注
                    if self.player.double_down(hand_index):
                        hand.add_card(self.deck.deal())
                        break
                    else:
                        decision = "H"  # 如果不能双倍下注，默认要牌
                
                elif decision == "P":  # 分牌
                    if self.player.split(hand_index, self.deck):
                        continue  # 分牌后继续处理当前手牌
                    else:
                        decision = "H"  # 如果不能分牌，默认要牌
                
                elif decision == "R":  # 投降
                    if self.player.surrender(hand_index):
                        break
                    else:
                        decision = "H"  # 如果不能投降，默认要牌
            
            hand_index += 1
        
        # 庄家回合
        player_all_busted = all(hand.get_value() > 21 or hand.is_surrender for hand in self.player.hands)
        if not player_all_busted:
            self.dealer.play(self.deck)
        
        # 结算
        dealer_value = self.dealer.hand.get_value()
        dealer_blackjack = self.dealer.hand.is_blackjack
        
        for hand in self.player.hands:
            self.num_hands += 1
            
            if hand.is_surrender:
                self.losses += 1
                continue
            
            player_value = hand.get_value()
            
            if player_value > 21:  # 玩家爆牌
                self.losses += 1
            elif hand.is_blackjack and not dealer_blackjack:  # 玩家黑杰克，庄家非黑杰克
                self.wins += 1
                self.blackjacks += 1
                self.player.money += hand.bet * 2.5  # 赔付1.5倍
            elif dealer_value > 21:  # 庄家爆牌
                self.wins += 1
                self.player.money += hand.bet * 2  # 赔付1倍
            elif dealer_blackjack and not hand.is_blackjack:  # 庄家黑杰克，玩家非黑杰克
                self.losses += 1
            elif player_value > dealer_value:  # 玩家点数大于庄家
                self.wins += 1
                self.player.money += hand.bet * 2  # 赔付1倍
            elif player_value < dealer_value:  # 玩家点数小于庄家
                self.losses += 1
            else:  # 平局
                self.pushes += 1
                self.player.money += hand.bet  # 返还赌注
    
    def simulate(self, num_rounds=1000):
        for _ in range(num_rounds):
            self.play_round()
        
        win_rate = self.wins / self.num_hands * 100
        profit = self.player.money - self.player.initial_money
        
        return {
            "胜率": win_rate,
            "盈利": profit,
            "黑杰克次数": self.blackjacks,
            "胜场": self.wins,
            "负场": self.losses,
            "平局": self.pushes,
            "总手数": self.num_hands
        }

# 策略定义
def basic_strategy(hand, dealer_up_card):
    """基本策略"""
    dealer_value = dealer_up_card.get_value()
    player_value = hand.get_value()
    
    # 可以分牌的情况
    if hand.can_split():
        card_value = hand.cards[0].get_value()
        # A和8总是分牌
        if card_value == 11 or card_value == 8:
            return "P"
        # 9分牌，除非庄家是7、10或A
        elif card_value == 9 and dealer_value not in [7, 10, 11]:
            return "P"
        # 2和3分牌，如果庄家是2-7
        elif (card_value == 2 or card_value == 3) and 2 <= dealer_value <= 7:
            return "P"
        # 6分牌，如果庄家是2-6
        elif card_value == 6 and 2 <= dealer_value <= 6:
            return "P"
        # 7分牌，如果庄家是2-7
        elif card_value == 7 and 2 <= dealer_value <= 7:
            return "P"
        # 4分牌，如果庄家是5-6
        elif card_value == 4 and 5 <= dealer_value <= 6:
            return "P"
    
    # 软手牌（含有作为11点的A）
    if hand.is_soft():
        # A,8或更高 => 停牌
        if player_value >= 19:
            return "S"
        # A,7 => 庄家2-8时停牌，否则要牌
        elif player_value == 18:
            if 2 <= dealer_value <= 8:
                return "S"
            else:
                return "H"
        # A,6 => 庄家3-6时双倍，否则要牌
        elif player_value == 17:
            if 3 <= dealer_value <= 6:
                return "D" if len(hand.cards) == 2 else "H"
            else:
                return "H"
        # A,4-5 => 庄家4-6时双倍，否则要牌
        elif 15 <= player_value <= 16:
            if 4 <= dealer_value <= 6:
                return "D" if len(hand.cards) == 2 else "H"
            else:
                return "H"
        # A,2-3 => 庄家5-6时双倍，否则要牌
        elif 13 <= player_value <= 14:
            if 5 <= dealer_value <= 6:
                return "D" if len(hand.cards) == 2 else "H"
            else:
                return "H"
        else:
            return "H"
    
    # 硬手牌
    # 17+ => 停牌
    if player_value >= 17:
        return "S"
    # 13-16 => 庄家2-6时停牌，否则要牌
    elif 13 <= player_value <= 16:
        if 2 <= dealer_value <= 6:
            return "S"
        else:
            return "H"
    # 12 => 庄家4-6时停牌，否则要牌
    elif player_value == 12:
        if 4 <= dealer_value <= 6:
            return "S"
        else:
            return "H"
    # 11 => 双倍
    elif player_value == 11:
        return "D" if len(hand.cards) == 2 else "H"
    # 10 => 庄家2-9时双倍，否则要牌
    elif player_value == 10:
        if 2 <= dealer_value <= 9:
            return "D" if len(hand.cards) == 2 else "H"
        else:
            return "H"
    # 9 => 庄家3-6时双倍，否则要牌
    elif player_value == 9:
        if 3 <= dealer_value <= 6:
            return "D" if len(hand.cards) == 2 else "H"
        else:
            return "H"
    # 8及以下 => 要牌
    else:
        return "H"

def conservative_strategy(hand, dealer_up_card):
    """保守策略：17点以上停牌，否则要牌"""
    player_value = hand.get_value()
    if player_value >= 17:
        return "S"
    else:
        return "H"

def aggressive_strategy(hand, dealer_up_card):
    """激进策略：只有在20点以上才停牌"""
    player_value = hand.get_value()
    if player_value >= 20:
        return "S"
    else:
        return "H"

def mimic_dealer_strategy(hand, dealer_up_card):
    """模仿庄家策略：17点以上停牌，否则要牌，不分牌，不双倍"""
    player_value = hand.get_value()
    if player_value >= 17:
        return "S"
    else:
        return "H"

def never_bust_strategy(hand, dealer_up_card):
    """永不爆牌策略：12点以上停牌"""
    player_value = hand.get_value()
    if player_value >= 12:
        return "S"
    else:
        return "H"

# 添加新的高级策略

def card_counting_strategy(hand, dealer_up_card):
    """计牌策略：基于高低法(Hi-Lo)的策略
    
    这个策略模拟了玩家根据牌局中已出现的牌来调整决策的过程
    当剩余牌堆中大牌比例高时，玩家会更激进
    当剩余牌堆中小牌比例高时，玩家会更保守
    """
    # 获取基本信息
    dealer_value = dealer_up_card.get_value()
    player_value = hand.get_value()
    
    # 模拟计牌系统中的"真数"(True Count)
    # 在实际游戏中，这个值应该是通过跟踪已出现的牌计算得出
    # 这里我们简化为随机生成一个-3到+3之间的值
    true_count = random.uniform(-3, 3)
    
    # 根据"真数"调整策略
    if true_count >= 2:  # 剩余牌堆中大牌比例高，更激进
        # 可以分牌的情况
        if hand.can_split():
            card_value = hand.cards[0].get_value()
            # 更多情况下选择分牌
            if card_value in [9, 8, 7, 6, 2, 3]:
                return "P"
        
        # 更激进的停牌点
        if player_value >= 16:
            return "S"
        # 更多情况下选择双倍下注
        elif player_value in [9, 10, 11] and len(hand.cards) == 2:
            return "D"
        else:
            return "H"
    
    elif true_count <= -2:  # 剩余牌堆中小牌比例高，更保守
        # 提高停牌点
        if player_value >= 13 and dealer_value < 7:
            return "S"
        elif player_value >= 17:
            return "S"
        # 减少双倍下注
        elif player_value == 11 and dealer_value < 10 and len(hand.cards) == 2:
            return "D"
        else:
            return "H"
    
    else:  # 中性牌局，使用基本策略
        return basic_strategy(hand, dealer_up_card)

def kelly_criterion_strategy(hand, dealer_up_card):
    """凯利公式策略：根据预期收益调整决策
    
    凯利公式用于确定最优下注比例，这里我们用它来影响决策
    当预期收益高时，策略更激进；当预期收益低时，策略更保守
    """
    dealer_value = dealer_up_card.get_value()
    player_value = hand.get_value()
    
    # 计算预期胜率(简化模型)
    win_probability = 0.5  # 基础胜率
    
    # 根据玩家点数调整胜率
    if player_value <= 11:  # 不可能爆牌
        win_probability += 0.1
    elif player_value <= 16:  # 可能爆牌
        win_probability -= 0.1
    elif player_value <= 20:  # 较好的牌
        win_probability += 0.15
    elif player_value == 21:  # 21点
        win_probability += 0.3
    
    # 根据庄家明牌调整胜率
    if 2 <= dealer_value <= 6:  # 庄家弱牌
        win_probability += 0.1
    elif 7 <= dealer_value <= 9:  # 庄家中性牌
        win_probability += 0.0
    else:  # 庄家强牌
        win_probability -= 0.1
    
    # 根据凯利公式计算的最优策略
    if win_probability > 0.6:  # 高胜率情况
        # 分牌情况
        if hand.can_split():
            card_value = hand.cards[0].get_value()
            if card_value in [11, 8, 9, 7]:
                return "P"
        
        # 双倍下注情况
        if 9 <= player_value <= 11 and len(hand.cards) == 2:
            return "D"
        
        # 停牌情况
        if player_value >= 17 or (player_value >= 13 and dealer_value <= 6):
            return "S"
        else:
            return "H"
    
    elif win_probability < 0.4:  # 低胜率情况
        # 考虑投降
        if len(hand.cards) == 2 and 15 <= player_value <= 16 and dealer_value >= 9:
            return "R"
        
        # 保守停牌
        if player_value >= 17:
            return "S"
        else:
            return "H"
    
    else:  # 中等胜率，使用基本策略
        return basic_strategy(hand, dealer_up_card)

def team_play_strategy(hand, dealer_up_card):
    """团队合作策略：模拟多人协作的策略
    
    在实际团队打法中，不同角色有不同任务：
    - 计牌员：专注计算真数
    - 下注员：根据信号调整下注
    - 玩牌员：执行基本策略
    
    这里我们模拟团队配合下的决策过程
    """
    dealer_value = dealer_up_card.get_value()
    player_value = hand.get_value()
    
    # 模拟团队信号系统
    # 随机生成一个信号：-1(不利牌局)，0(中性牌局)，1(有利牌局)
    team_signal = random.choice([-1, 0, 1])
    
    if team_signal == 1:  # 有利牌局，激进策略
        # 更多情况下分牌
        if hand.can_split():
            card_value = hand.cards[0].get_value()
            if card_value in [11, 8, 9, 7, 6, 2, 3]:
                return "P"
        
        # 更多情况下双倍下注
        if 9 <= player_value <= 11 and len(hand.cards) == 2:
            return "D"
        elif player_value == 8 and 2 <= dealer_value <= 6 and len(hand.cards) == 2:
            return "D"
        
        # 调整停牌点
        if player_value >= 16:
            return "S"
        elif 12 <= player_value <= 15 and 2 <= dealer_value <= 6:
            return "S"
        else:
            return "H"
    
    elif team_signal == -1:  # 不利牌局，保守策略
        # 考虑投降
        if len(hand.cards) == 2 and 15 <= player_value <= 16:
            return "R"
        
        # 提高停牌点
        if player_value >= 17:
            return "S"
        else:
            return "H"
    
    else:  # 中性牌局，使用基本策略
        return basic_strategy(hand, dealer_up_card)

# 添加可视化功能
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def visualize_results(results):
    """可视化模拟结果"""
    # 设置中文字体
    try:
        # 尝试使用系统中的中文字体
        font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf")
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    except:
        font = FontProperties()
    
    # 准备数据
    strategies = list(results.keys())
    win_rates = [results[s]['胜率'] for s in strategies]
    profits = [results[s]['盈利'] for s in strategies]
    blackjacks = [results[s]['黑杰克次数'] for s in strategies]
    
    # 创建图表
    plt.figure(figsize=(15, 12))
    
    # 胜率图表
    plt.subplot(3, 1, 1)
    bars = plt.bar(strategies, win_rates, color='skyblue')
    plt.title('不同策略的胜率比较', fontsize=15)
    plt.ylabel('胜率 (%)')
    plt.ylim(0, max(win_rates) * 1.2)
    plt.xticks(fontproperties=font)  # 确保X轴标签使用中文字体
    
    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{height:.2f}%', ha='center', va='bottom')
    
    # 盈利图表
    plt.subplot(3, 1, 2)
    bars = plt.bar(strategies, profits, color='lightgreen')
    plt.title('不同策略的盈利比较', fontsize=15)
    plt.ylabel('盈利 (单位)')
    plt.ylim(min(min(profits) * 1.2, 0), max(max(profits) * 1.2, 0))
    plt.xticks(fontproperties=font)  # 确保X轴标签使用中文字体
    
    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1 if height >= 0 else height - 10,
                 f'{height:.2f}', ha='center', va='bottom' if height >= 0 else 'top')
    
    # 黑杰克次数图表
    plt.subplot(3, 1, 3)
    bars = plt.bar(strategies, blackjacks, color='salmon')
    plt.title('不同策略的黑杰克次数比较', fontsize=15)
    plt.ylabel('黑杰克次数')
    plt.ylim(0, max(blackjacks) * 1.2)
    plt.xticks(fontproperties=font)  # 确保X轴标签使用中文字体
    
    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{height}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(r'e:\Desktop\1\21点策略比较.png', dpi=300)
    plt.show()

# 主函数
def main():
    strategies = {
        "基本策略": basic_strategy,
        "保守策略": conservative_strategy,
        "激进策略": aggressive_strategy,
        "模仿庄家": mimic_dealer_strategy,
        "永不爆牌": never_bust_strategy,
        "计牌策略": card_counting_strategy,
        "凯利公式": kelly_criterion_strategy,
        "团队合作": team_play_strategy
    }
    
    results = {}
    
    for name, strategy in strategies.items():
        print(f"模拟 {name} 中...")
        player = Player(strategy)
        game = Game(player)
        result = game.simulate(10000)
        results[name] = result
    
    # 打印结果
    print("\n===== 模拟结果 =====")
    print(f"{'策略名称':<10} {'胜率':<8} {'盈利':<8} {'黑杰克次数':<10} {'胜场':<6} {'负场':<6} {'平局':<6}")
    print("-" * 60)
    
    for name, result in results.items():
        print(f"{name:<10} {result['胜率']:.2f}% {result['盈利']:<8.2f} {result['黑杰克次数']:<10} {result['胜场']:<6} {result['负场']:<6} {result['平局']:<6}")
    
    # 可视化结果
    visualize_results(results)

if __name__ == "__main__":
    main()