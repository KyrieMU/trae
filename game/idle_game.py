import pygame
import sys
from pygame import font

pygame.init()
font.init()

# 窗口设置
# 在颜色定义后添加窗口相关设置
# 初始窗口大小
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
# 最小窗口大小
MIN_WIDTH = 400
MIN_HEIGHT = 500

# 创建可调整大小的窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('挂机')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GRAY = (128, 128, 128)
BLUE = (100, 149, 237)
GREEN = (50, 205, 50)

# 字体设置
try:
    # 使用 Segoe UI Emoji 字体，这是 Windows 系统自带的支持 emoji 的字体
    font_small = pygame.font.SysFont('segoe ui emoji', 18)
    font_large = pygame.font.SysFont('segoe ui emoji', 22)
except:
    # 如果没有 Segoe UI Emoji，使用文字替代
    font_small = pygame.font.SysFont('microsoft yahei', 18)
    font_large = pygame.font.SysFont('microsoft yahei', 22)

class IdleGame:
    def __init__(self):
        self.coins = 0
        self.click_power = 1
        self.auto_miners = 0
        self.auto_miner_cost = 10
        self.auto_miner_power = 0.1
        self.click_upgrade_cost = 20
        self.miner_upgrade_cost = 50
        self.last_time = pygame.time.get_ticks()
        self.paused = False
        # 添加新的高级道具属性
        self.super_miner = 0
        self.super_miner_cost = 1000
        self.super_miner_power = 1.0
        self.multiplier = 1
        self.multiplier_cost = 2000
        # 添加状态面板位置属性
        self.panel_x = 10
        self.panel_y = 10
        self.dragging_panel = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def buy_super_miner(self):
        if not self.paused and self.coins >= self.super_miner_cost:
            self.coins -= self.super_miner_cost
            self.super_miner += 1
            self.super_miner_cost = int(self.super_miner_cost * 2)

    def upgrade_multiplier(self):
        if not self.paused and self.coins >= self.multiplier_cost:
            self.coins -= self.multiplier_cost
            self.multiplier *= 1.5
            self.multiplier_cost = int(self.multiplier_cost * 2.5)

    def click(self):
        if not self.paused:
            self.coins += self.click_power

    def buy_auto_miner(self):
        if not self.paused and self.coins >= self.auto_miner_cost:
            self.coins -= self.auto_miner_cost
            self.auto_miners += 1
            self.auto_miner_cost = int(self.auto_miner_cost * 1.5)

    def upgrade_click(self):
        if not self.paused and self.coins >= self.click_upgrade_cost:
            self.coins -= self.click_upgrade_cost
            self.click_power *= 1.5
            self.click_upgrade_cost = int(self.click_upgrade_cost * 2)

    def upgrade_miner(self):
        if not self.paused and self.coins >= self.miner_upgrade_cost:
            self.coins -= self.miner_upgrade_cost
            self.auto_miner_power *= 1.5
            self.miner_upgrade_cost = int(self.miner_upgrade_cost * 2)

    def update(self):
        if not self.paused:
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.last_time) / 1000.0
            # 修改收入计算，加入新的收入来源
            basic_income = self.auto_miners * self.auto_miner_power
            super_income = self.super_miner * self.super_miner_power
            total_income = (basic_income + super_income) * self.multiplier
            self.coins += total_income * dt
            self.last_time = current_time

    # 添加窗口状态属性
    def __init__(self):
        self.coins = 0
        self.click_power = 1
        self.auto_miners = 0
        self.auto_miner_cost = 10
        self.auto_miner_power = 0.1
        self.click_upgrade_cost = 20
        self.miner_upgrade_cost = 50
        self.last_time = pygame.time.get_ticks()
        self.paused = False
        # 添加新的高级道具属性
        self.super_miner = 0
        self.super_miner_cost = 1000
        self.super_miner_power = 1.0
        self.multiplier = 1
        self.multiplier_cost = 2000
        # 添加状态面板位置属性
        self.panel_x = 10
        self.panel_y = 10
        self.dragging_panel = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def buy_super_miner(self):
        if not self.paused and self.coins >= self.super_miner_cost:
            self.coins -= self.super_miner_cost
            self.super_miner += 1
            self.super_miner_cost = int(self.super_miner_cost * 2)

    def upgrade_multiplier(self):
        if not self.paused and self.coins >= self.multiplier_cost:
            self.coins -= self.multiplier_cost
            self.multiplier *= 1.5
            self.multiplier_cost = int(self.multiplier_cost * 2.5)

    def click(self):
        if not self.paused:
            self.coins += self.click_power

    def buy_auto_miner(self):
        if not self.paused and self.coins >= self.auto_miner_cost:
            self.coins -= self.auto_miner_cost
            self.auto_miners += 1
            self.auto_miner_cost = int(self.auto_miner_cost * 1.5)

    def upgrade_click(self):
        if not self.paused and self.coins >= self.click_upgrade_cost:
            self.coins -= self.click_upgrade_cost
            self.click_power *= 1.5
            self.click_upgrade_cost = int(self.click_upgrade_cost * 2)

    def upgrade_miner(self):
        if not self.paused and self.coins >= self.miner_upgrade_cost:
            self.coins -= self.miner_upgrade_cost
            self.auto_miner_power *= 1.5
            self.miner_upgrade_cost = int(self.miner_upgrade_cost * 2)

    def update(self):
        if not self.paused:
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.last_time) / 1000.0
            # 修改收入计算，加入新的收入来源
            basic_income = self.auto_miners * self.auto_miner_power
            super_income = self.super_miner * self.super_miner_power
            total_income = (basic_income + super_income) * self.multiplier
            self.coins += total_income * dt
            self.last_time = current_time

    # 添加窗口调整方法
    def handle_resize(self, width, height):
        self.window_width = max(width, MIN_WIDTH)
        self.window_height = max(height, MIN_HEIGHT)
        if not self.is_fullscreen:
            pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
            
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # 保存当前窗口大小
            self.window_width = screen.get_width()
            self.window_height = screen.get_height()
            # 切换到全屏
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            # 恢复窗口模式
            pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

def main():
    game = IdleGame()
    clock = pygame.time.Clock()

    # 定义按钮区域
    # 主按钮 - 点击获取金币
    click_button = pygame.Rect(50, 30, 300, 120)
    pause_button = pygame.Rect(WINDOW_WIDTH - 45, 10, 35, 35)
    
    # 基础功能按钮
    basic_buttons = [
        {"rect": pygame.Rect(50, 170, 300, 60), "color": BLUE, "action": game.buy_auto_miner, 
         "icon": "BUY MINER", "cost": lambda g: f"${g.auto_miner_cost}", "unlock": 0},
        {"rect": pygame.Rect(50, 240, 145, 50), "color": GREEN, "action": game.upgrade_click, 
         "icon": "POWER UP", "cost": lambda g: f"${g.click_upgrade_cost}", "unlock": 0},
        {"rect": pygame.Rect(205, 240, 145, 50), "color": GOLD, "action": game.upgrade_miner, 
         "icon": "BOOST", "cost": lambda g: f"${g.miner_upgrade_cost}", "unlock": 0},
    ]
    
    # 高级功能按钮
    advanced_buttons = [
        {"rect": pygame.Rect(50, 310, 300, 60), "color": BLUE, "action": game.buy_super_miner,
         "icon": "SUPER MINER", "cost": lambda g: f"${g.super_miner_cost}", "unlock": 1000},
        {"rect": pygame.Rect(50, 380, 300, 60), "color": GOLD, "action": game.upgrade_multiplier,
         "icon": "MULTIPLIER", "cost": lambda g: f"${g.multiplier_cost}", "unlock": 2000},
    ]
    
    # 合并所有按钮用于事件处理
    buttons = basic_buttons + advanced_buttons

    # 在绘制功能按钮部分修改
    for btn in buttons:
        # 检查是否解锁
        if game.coins >= btn["unlock"]:
            pygame.draw.rect(screen, btn["color"] if not game.paused else GRAY, btn["rect"], border_radius=5)
            btn_text = font_small.render(btn["icon"], True, BLACK)
            screen.blit(btn_text, (btn["rect"].centerx - btn_text.get_width()//2,
                                 btn["rect"].centery - btn_text.get_height()//2 - 10))
            cost_text = font_small.render(btn["cost"](game), True, BLACK)
            screen.blit(cost_text, (btn["rect"].centerx - cost_text.get_width()//2,
                                 btn["rect"].centery + cost_text.get_height()//2))
        else:
            # 显示未解锁状态
            pygame.draw.rect(screen, GRAY, btn["rect"], border_radius=5)
            unlock_text = font_small.render(f"解锁需要: ${btn['unlock']}", True, BLACK)
            screen.blit(unlock_text, (btn["rect"].centerx - unlock_text.get_width()//2,
                                   btn["rect"].centery - unlock_text.get_height()//2))

    # 显示状态部分添加新内容
    income_text = font_small.render(f'INCOME/s: {(game.auto_miners * game.auto_miner_power + game.super_miner * game.super_miner_power) * game.multiplier:.1f}', True, BLACK)
    multi_text = font_small.render(f'MULTI: x{game.multiplier:.1f}', True, BLACK)
    screen.blit(multi_text, (10, 390))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 检查是否点击状态面板
                status_panel = pygame.Rect(game.panel_x, game.panel_y, WINDOW_WIDTH - 65, 100)
                if status_panel.collidepoint(mouse_pos):
                    game.dragging_panel = True
                    game.drag_offset_x = mouse_pos[0] - game.panel_x
                    game.drag_offset_y = mouse_pos[1] - game.panel_y
                if click_button.collidepoint(mouse_pos):
                    game.click()
                elif pause_button.collidepoint(mouse_pos):  # 检测暂停按钮点击
                    game.paused = not game.paused
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        btn["action"]()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    game.paused = not game.paused

        game.update()

        # 绘制界面
        screen.fill(WHITE)

        # 绘制主点击按钮
        pygame.draw.rect(screen, GOLD if not game.paused else GRAY, click_button, border_radius=10)
        click_text = font_large.render('💰', True, BLACK)
        screen.blit(click_text, (click_button.centerx - click_text.get_width()//2, 
                                click_button.centery - click_text.get_height()//2))

        # 绘制功能按钮
        for btn in buttons:
            # 检查是否解锁
            if game.coins >= btn["unlock"]:
                # 绘制按钮背景
                pygame.draw.rect(screen, btn["color"] if not game.paused else GRAY, btn["rect"], border_radius=8)
                # 绘制按钮内部边框效果
                inner_rect = btn["rect"].inflate(-4, -4)
                pygame.draw.rect(screen, WHITE, inner_rect, border_radius=6, width=1)
                
                # 绘制按钮名称
                btn_text = font_large.render(btn["icon"], True, WHITE)
                screen.blit(btn_text, (btn["rect"].centerx - btn_text.get_width()//2,
                                     btn["rect"].centery - btn_text.get_height()//2 - 8))
                # 绘制价格
                cost_text = font_small.render(btn["cost"](game), True, WHITE)
                screen.blit(cost_text, (btn["rect"].centerx - cost_text.get_width()//2,
                                     btn["rect"].centery + cost_text.get_height()//2))
            else:
                # 未解锁状态显示
                pygame.draw.rect(screen, GRAY, btn["rect"], border_radius=8)
                pygame.draw.rect(screen, WHITE, btn["rect"].inflate(-4, -4), border_radius=6, width=1)
                unlock_text = font_small.render(f"UNLOCK: ${btn['unlock']}", True, WHITE)
                screen.blit(unlock_text, (btn["rect"].centerx - unlock_text.get_width()//2,
                                       btn["rect"].centery - unlock_text.get_height()//2))

        # 显示状态面板
        # 创建一个状态面板区域，放置在窗口底部
        panel_width = WINDOW_WIDTH - 20  # 左右各留10像素边距
        panel_height = 100
        game.panel_x = 10  # 固定在左边10像素处
        game.panel_y = WINDOW_HEIGHT - panel_height - 10  # 固定在底部，留10像素边距
        status_panel = pygame.Rect(game.panel_x, game.panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (240, 240, 240), status_panel, border_radius=5)
        pygame.draw.rect(screen, GRAY, status_panel, border_radius=5, width=1)

        # 在面板内显示各种状态
        coins_text = font_large.render(f'COINS: {int(game.coins)}', True, BLACK)
        miners_text = font_small.render(f'MINERS: {game.auto_miners}', True, BLACK)
        power_text = font_small.render(f'POWER: x{game.click_power:.1f}', True, BLACK)
        income_text = font_small.render(f'INCOME/s: {(game.auto_miners * game.auto_miner_power + game.super_miner * game.super_miner_power) * game.multiplier:.1f}', True, BLACK)
        multi_text = font_small.render(f'MULTI: x{game.multiplier:.1f}', True, BLACK)

        # 调整文本位置，使用面板的实际位置
        screen.blit(coins_text, (game.panel_x + 10, game.panel_y + 10))
        screen.blit(miners_text, (game.panel_x + 10, game.panel_y + 35))
        screen.blit(power_text, (game.panel_x + 10, game.panel_y + 55))
        screen.blit(income_text, (game.panel_x + status_panel.width//2, game.panel_y + 35))
        screen.blit(multi_text, (game.panel_x + status_panel.width//2, game.panel_y + 55))

        if game.paused:
            pause_text = font_large.render('⏸', True, BLACK)
            screen.blit(pause_text, (WINDOW_WIDTH - 30, 10))

        # 绘制暂停按钮
        pygame.draw.rect(screen, GRAY if game.paused else GREEN, pause_button, border_radius=5)
        pause_icon = "PAUSE" if not game.paused else "PLAY"
        pause_text = font_large.render(pause_icon, True, BLACK)
        screen.blit(pause_text, (pause_button.centerx - pause_text.get_width()//2,
                               pause_button.centery - pause_text.get_height()//2))

        pygame.display.flip()
        clock.tick(60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                game.dragging_panel = False
            elif event.type == pygame.MOUSEMOTION:
                if game.dragging_panel:
                    mouse_pos = pygame.mouse.get_pos()
                    game.panel_x = mouse_pos[0] - game.drag_offset_x
                    game.panel_y = mouse_pos[1] - game.drag_offset_y
                    # 确保面板不会移出屏幕
                    game.panel_x = max(0, min(game.panel_x, WINDOW_WIDTH - (WINDOW_WIDTH - 65)))
                    game.panel_y = max(0, min(game.panel_y, WINDOW_HEIGHT - 100))

        if game.paused:
            pause_text = font_large.render('⏸', True, BLACK)
            screen.blit(pause_text, (WINDOW_WIDTH - 30, 10))

        # 绘制暂停按钮
        pygame.draw.rect(screen, GRAY if game.paused else GREEN, pause_button, border_radius=5)
        pause_icon = "PAUSE" if not game.paused else "PLAY"
        pause_text = font_large.render(pause_icon, True, BLACK)
        screen.blit(pause_text, (pause_button.centerx - pause_text.get_width()//2,
                               pause_button.centery - pause_text.get_height()//2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()