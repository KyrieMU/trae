import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 定义颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
# 在游戏窗口设置部分添加最小速度限制
GAME_SPEED = 10  # 初始速度
MIN_SPEED = 5    # 最小速度限制
MAX_SPEED = 25   # 最大速度限制
SPEED_CHANGE = 1 # 手动调整时的速度变化量
MAX_SPEED = 25   # 添加最大速度限制
SPEED_INCREMENT = 0.5  # 每吃一个食物增加的速度

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')
clock = pygame.time.Clock()

# 在颜色定义后添加图片加载
try:
    # 加载贴图（请确保图片文件存在）
    snake_head = pygame.image.load('e:\\Desktop\\szu.png')
    snake_body = pygame.image.load('e:\\Desktop\\szu.png')
    food_img = pygame.image.load('e:\\Desktop\\szu1.png')
  
    # 调整图片大小为BLOCK_SIZE
    snake_head = pygame.transform.scale(snake_head, (BLOCK_SIZE, BLOCK_SIZE))
    snake_body = pygame.transform.scale(snake_body, (BLOCK_SIZE, BLOCK_SIZE))
    food_img = pygame.transform.scale(food_img, (BLOCK_SIZE, BLOCK_SIZE))
except:
    # 如果加载失败，使用默认的矩形显示
    snake_head = None
    snake_body = None
    food_img = None

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = GAME_SPEED  # 添加速度属性

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.speed = GAME_SPEED  # 重置速度

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x*BLOCK_SIZE)) % WINDOW_WIDTH, (cur[1] + (y*BLOCK_SIZE)) % WINDOW_HEIGHT)
        if new in self.positions[3:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            if snake_head is not None and snake_body is not None:
                if i == 0:  # 蛇头
                    # 根据方向旋转蛇头
                    angle = 0
                    if self.direction == UP:
                        angle = 0
                    elif self.direction == DOWN:
                        angle = 180
                    elif self.direction == LEFT:
                        angle = 90
                    elif self.direction == RIGHT:
                        angle = 270
                    rotated_head = pygame.transform.rotate(snake_head, angle)
                    surface.blit(rotated_head, (p[0], p[1]))
                else:  # 蛇身
                    surface.blit(snake_body, (p[0], p[1]))
            else:
                # 如果没有贴图，使用原来的矩形显示
                pygame.draw.rect(surface, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)

    def draw(self, surface):
        if food_img is not None:
            surface.blit(food_img, (self.position[0], self.position[1]))
        else:
            pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 在颜色定义部分添加新的颜色
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# 添加新的按钮类
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.original_color = color
        self.hover_color = LIGHT_GRAY
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.hover_color
            else:
                self.color = self.original_color
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# 添加设置菜单函数
def settings_menu():
    speed = GAME_SPEED
    running = True
    
    speed_text = pygame.font.Font(None, 36).render("speed:", True, WHITE)
    
    while running:
        screen.fill(BLACK)
        
        # 显示当前速度
        current_speed = pygame.font.Font(None, 36).render(f"{speed}", True, WHITE)
        screen.blit(speed_text, (250, 250))
        screen.blit(current_speed, (400, 250))
        
        # 创建速度调整按钮
        speed_up = Button(450, 245, 30, 30, "+", WHITE)
        speed_down = Button(350, 245, 30, 30, "-", WHITE)
        back_button = Button(300, 400, 200, 50, "back", WHITE)
        
        for button in [speed_up, speed_down, back_button]:
            button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if speed_up.handle_event(event):
                # 确保speed是数字类型
                speed = min(float(speed) + 1, float(MAX_SPEED))
            if speed_down.handle_event(event):
                speed = max(speed - 1, 5)
            if back_button.handle_event(event):
                return speed
        
        pygame.display.update()
        clock.tick(60)

# 修改main函数
def main():
    global GAME_SPEED
    
    # 定义方向
    global UP, DOWN, LEFT, RIGHT
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    # 创建菜单按钮
    start_button = Button(300, 200, 200, 50, "start", WHITE)
    settings_button = Button(300, 300, 200, 50, "setting", WHITE)
    quit_button = Button(300, 400, 200, 50, "quit", WHITE)
    
    in_menu = True
    while in_menu:
        screen.fill(BLACK)
        
        # 绘制标题
        title = pygame.font.Font(None, 74).render("JJJJ", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH/2, 100))
        screen.blit(title, title_rect)
        
        # 绘制按钮
        for button in [start_button, settings_button, quit_button]:
            button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if start_button.handle_event(event):
                game_loop()  # 开始游戏
            if settings_button.handle_event(event):
                GAME_SPEED = settings_menu()  # 打开设置菜单
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(60)

# 添加游戏主循环函数
def game_loop():
    snake = Snake()
    food = Food()
    font = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == pygame.K_ESCAPE:  # 添加返回菜单功能
                    return
        
        # 更新蛇的位置
        if not snake.update():
            snake.reset()
            food.randomize_position()

        # 检查是否吃到食物
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            # 增加速度，但不超过最大速度
            snake.speed = min(snake.speed + SPEED_INCREMENT, MAX_SPEED)
            food.randomize_position()

        # 绘制游戏界面
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        
        # 显示分数
        # 在分数显示后添加速度显示
        score_text = font.render(f'point: {snake.score}', True, WHITE)
        speed_text = font.render(f'speed: {snake.speed:.1f}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 50))

        pygame.display.update()
        clock.tick(snake.speed)  # 使用蛇的当前速度

if __name__ == '__main__':
    main()