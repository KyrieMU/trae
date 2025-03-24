import random
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class Card:
    """扑克牌类"""
    def __init__(self, suit, value):
        self.suit = suit    # 花色
        self.value = value  # 点数
    
    def __str__(self):
        suits = {'Hearts': '♥', 'Diamonds': '♦', 'Spades': '♠', 'Clubs': '♣'}
        values = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        card_value = values.get(self.value, str(self.value))
        return f"{suits[self.suit]}{card_value}"

class Deck:
    """牌组类"""
    def __init__(self):
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        for suit in suits:
            for value in range(1, 14):
                self.cards.append(Card(suit, value))
        random.shuffle(self.cards)
    
    def draw(self):
        """抽一张牌"""
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Hand:
    """手牌类"""
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        """添加一张牌"""
        self.cards.append(card)
    
    def get_value(self):
        """计算手牌总点数"""
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.value == 1:  # A
                aces += 1
            elif card.value > 10:  # J, Q, K
                value += 10
            else:
                value += card.value
        
        # 处理A的点数（1或11）
        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        
        return value
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)

# 在Card, Deck, Hand类之后添加Player类
class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.hand = Hand()
        self.chips = chips
        self.current_bet = 0
        self.status = 'waiting'  # waiting, playing, stand, bust

# 修改Game类
class Game:
    def __init__(self, num_players=3):
        self.deck = Deck()
        self.dealer_hand = Hand()
        self.players = []
        self.current_player = 0
        
        # 创建默认玩家
        for i in range(num_players):
            self.players.append(Player(f"玩家{i+1}"))
    
    def initial_deal(self):
        """初始发牌"""
        self.deck = Deck()  # 每轮使用新牌组
        self.dealer_hand = Hand()
        for player in self.players:
            player.hand = Hand()
        
        # 每个玩家发两张牌
        for _ in range(2):
            for player in self.players:
                player.hand.add_card(self.deck.draw())
            self.dealer_hand.add_card(self.deck.draw())

# 修改BlackjackGUI类
class BlackjackGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("21点多人游戏")
        self.window.geometry("1000x800")
        self.window.configure(bg="#2c3e50")
        self.game = Game(3)
        self.setup_gui()

    def setup_gui(self):
        # 删除旧的筹码显示代码
        # 原错误代码位置：self.chips_label = tk.Label(...self.game.player_chips)
        
        # 创建标题
        title_label = tk.Label(self.window, text="21点多人游戏", 
                             font=("黑体", 24), bg="#2c3e50", fg="white")
        title_label.pack(pady=20)
        
        # 删除旧的单人游戏相关代码
        # 直接使用之前定义的多人游戏界面代码
        # 创建玩家信息区域
        self.players_frame = tk.Frame(self.window, bg="#2c3e50")
        self.players_frame.pack(pady=10)
        
        self.player_frames = []
        self.player_labels = []
        self.bet_entries = []
        self.player_cards_labels = []
        
        # 为每个玩家创建显示区域
        for i, player in enumerate(self.game.players):
            frame = tk.Frame(self.players_frame, bg="#2c3e50")
            frame.pack(pady=5)
            
            # 玩家信息标签
            label = tk.Label(frame, text=f"{player.name} 筹码: {player.chips}", 
                           font=("黑体", 12), bg="#2c3e50", fg="white")
            label.pack(side=tk.LEFT, padx=5)
            
            # 下注输入框
            bet_entry = tk.Entry(frame, width=8, font=("黑体", 12))
            bet_entry.pack(side=tk.LEFT, padx=5)
            
            # 手牌显示
            cards_label = tk.Label(frame, text="手牌: ", font=("黑体", 12),
                                 bg="#2c3e50", fg="white")
            cards_label.pack(side=tk.LEFT, padx=5)
            
            self.player_frames.append(frame)
            self.player_labels.append(label)
            self.bet_entries.append(bet_entry)
            self.player_cards_labels.append(cards_label)
        
        # 庄家区域
        self.dealer_frame = tk.Frame(self.window, bg="#2c3e50")
        self.dealer_frame.pack(pady=20)
        self.dealer_label = tk.Label(self.dealer_frame, text="庄家手牌: ",
                                   font=("黑体", 12), bg="#2c3e50", fg="white")
        self.dealer_label.pack()
        
        # 修改按钮区域（取消注释按钮创建）
        self.button_frame = tk.Frame(self.window, bg="#2c3e50")
        self.button_frame.pack(pady=20)
        self.create_buttons()  # 取消注释这行
    
    def create_buttons(self):
        """创建游戏控制按钮"""
        button_style = {"font": ("黑体", 12), "width": 10, "height": 2}
        
        self.deal_button = tk.Button(self.button_frame, text="发牌", command=self.start_round, **button_style)
        self.hit_button = tk.Button(self.button_frame, text="要牌", command=self.hit, state=tk.DISABLED, **button_style)
        self.stand_button = tk.Button(self.button_frame, text="停牌", command=self.stand, state=tk.DISABLED, **button_style)
        
        self.deal_button.pack(side=tk.LEFT, padx=10)
        self.hit_button.pack(side=tk.LEFT, padx=10)
        self.stand_button.pack(side=tk.LEFT, padx=10)
    
    # 添加缺失的 run 方法
    def run(self):
        """运行游戏"""
        self.window.mainloop()
    
    def start_round(self):
        """开始新一轮"""
        # 检查所有玩家的下注
        for i, player in enumerate(self.game.players):
            try:
                bet = int(self.bet_entries[i].get())
                if bet < 10 or bet > player.chips:
                    messagebox.showerror("错误", f"{player.name}的下注无效！")
                    return
                player.current_bet = bet
                player.status = 'playing'
            except ValueError:
                messagebox.showerror("错误", f"{player.name}请输入有效下注！")
                return
        
        self.game.initial_deal()
        self.game.current_player = 0
        self.update_display()
        self.update_buttons()
    
    def hit(self):
        """当前玩家要牌"""
        current_player = self.game.players[self.game.current_player]
        current_player.hand.add_card(self.game.deck.draw())
        
        if current_player.hand.get_value() > 21:
            current_player.status = 'bust'
            self.next_player()
        
        self.update_display()
        self.update_buttons()
    
    def stand(self):
        """当前玩家停牌"""
        self.game.players[self.game.current_player].status = 'stand'
        self.next_player()
        self.update_display()
        self.update_buttons()
    
    def next_player(self):
        """切换到下一个玩家"""
        self.game.current_player += 1
        if self.game.current_player >= len(self.game.players):
            self.dealer_play()
    
    def dealer_play(self):
        """庄家回合"""
        while self.game.dealer_hand.get_value() < 17:
            self.game.dealer_hand.add_card(self.game.deck.draw())
        self.end_round()
    
    def update_display(self):
        """更新显示"""
        # 更新玩家信息
        for i, player in enumerate(self.game.players):
            self.player_labels[i].config(
                text=f"{player.name} 筹码: {player.chips} 状态: {player.status}")
            self.player_cards_labels[i].config(
                text=f"手牌: {player.hand} (点数: {player.hand.get_value()})")
        
        # 更新庄家信息
        if self.game.current_player >= len(self.game.players):
            dealer_text = f"庄家手牌: {self.game.dealer_hand} (点数: {self.game.dealer_hand.get_value()})"
        else:
            dealer_text = f"庄家手牌: {self.game.dealer_hand.cards[0]} **"
        self.dealer_label.config(text=dealer_text)
    
    def update_buttons(self):
        """更新按钮状态"""
        if self.game.current_player >= len(self.game.players):
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.deal_button.config(state=tk.NORMAL)
        else:
            current_player = self.game.players[self.game.current_player]
            if current_player.status == 'playing':
                self.hit_button.config(state=tk.NORMAL)
                self.stand_button.config(state=tk.NORMAL)
            else:
                self.hit_button.config(state=tk.DISABLED)
                self.stand_button.config(state=tk.DISABLED)

    # 添加缺失的 end_round 方法
    def end_round(self):
        """结算回合结果"""
        dealer_value = self.game.dealer_hand.get_value()
        for player in self.game.players:
            player_value = player.hand.get_value()
            
            if player_value > 21:
                result = -player.current_bet
            elif dealer_value > 21 or player_value > dealer_value:
                result = player.current_bet
            elif dealer_value > player_value:
                result = -player.current_bet
            else:
                result = 0
                
            player.chips += result
            messagebox.showinfo("结算", f"{player.name} 筹码变化: {result:+d}")

        # 重置游戏状态
        for player in self.game.players:
            player.status = 'waiting'
        self.update_buttons()

# 在文件最后添加主程序入口
if __name__ == "__main__":
    gui = BlackjackGUI()
    gui.run()