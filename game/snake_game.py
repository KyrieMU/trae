import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 设置游戏窗口和颜色
WINDOW_SIZE = 400
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('小摸鱼')

class Snake:
    def __init__(self):
        self.body = [(GRID_COUNT//2, GRID_COUNT//2)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        self.grow = False

    def check_collision(self):
        head = self.body[0]
        return (head in self.body[1:] or 
                head[0] < 0 or head[0] >= GRID_COUNT or 
                head[1] < 0 or head[1] >= GRID_COUNT)

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
    score = 0
    game_speed = 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                if event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                if event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                if event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        snake.move()
        
        # 检查是否吃到食物
        if snake.body[0] == food:
            snake.grow = True
            score += 1
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))
            while food in snake.body:
                food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))

        # 检查碰撞
        if snake.check_collision():
            snake = Snake()
            score = 0
            food = (random.randint(0, GRID_COUNT-1), random.randint(0, GRID_COUNT-1))

        # 绘制游戏画面
        screen.fill(BLACK)
        
        # 绘制蛇
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, 
                           (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, 
                            GRID_SIZE-1, GRID_SIZE-1))
        
        # 绘制食物
        pygame.draw.rect(screen, RED,
                        (food[0]*GRID_SIZE, food[1]*GRID_SIZE,
                         GRID_SIZE-1, GRID_SIZE-1))

        pygame.display.flip()
        clock.tick(game_speed)

if __name__ == '__main__':
    main()