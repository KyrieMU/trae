import pygame
import random
import math

# 初始化pygame
pygame.init()

# 屏幕设置
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("太空射击")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 玩家设置
player_size = 30
player_x = screen_width // 2
player_y = screen_height - 2 * player_size
player_speed = 5
player_health = 100

# 子弹设置
bullets = []
bullet_speed = 7
bullet_size = 5
bullet_cooldown = 20
bullet_timer = 0

# 敌人设置
enemies = []
enemy_size = 30
enemy_speed = 2
enemy_spawn_rate = 60
enemy_timer = 0

# 陨石设置
asteroids = []
asteroid_sizes = [15, 25, 35]
asteroid_speeds = [1, 2, 3]
asteroid_spawn_rate = 30
asteroid_timer = 0

# 分数
score = 0
font = pygame.font.SysFont(None, 36)

# 游戏循环
running = True
clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.polygon(screen, BLUE, [
        (x, y - player_size),
        (x - player_size, y + player_size),
        (x, y + player_size // 2),
        (x + player_size, y + player_size)
    ])

def draw_health_bar(health):
    bar_width = 200
    bar_height = 20
    fill_width = (health / 100) * bar_width
    outline_rect = pygame.Rect(10, 10, bar_width, bar_height)
    fill_rect = pygame.Rect(10, 10, fill_width, bar_height)
    pygame.draw.rect(screen, RED, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

def spawn_enemy():
    enemy_x = random.randint(enemy_size, screen_width - enemy_size)
    enemy_y = -enemy_size
    enemies.append([enemy_x, enemy_y])

def spawn_asteroid():
    size_index = random.randint(0, len(asteroid_sizes) - 1)
    size = asteroid_sizes[size_index]
    speed = asteroid_speeds[size_index]
    asteroid_x = random.randint(size, screen_width - size)
    asteroid_y = -size
    asteroids.append([asteroid_x, asteroid_y, size, speed])

def check_collision(x1, y1, size1, x2, y2, size2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < (size1 + size2)

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_timer <= 0:
                bullets.append([player_x, player_y - player_size // 2])
                bullet_timer = bullet_cooldown

    # 获取按键状态
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > player_size:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed

    # 更新子弹
    if bullet_timer > 0:
        bullet_timer -= 1
    
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # 生成敌人
    enemy_timer += 1
    if enemy_timer >= enemy_spawn_rate:
        spawn_enemy()
        enemy_timer = 0

    # 更新敌人
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        
        # 检查敌人是否被子弹击中
        for bullet in bullets[:]:
            if check_collision(enemy[0], enemy[1], enemy_size, bullet[0], bullet[1], bullet_size):
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 10
                break
        
        # 检查敌人是否与玩家碰撞
        if check_collision(enemy[0], enemy[1], enemy_size, player_x, player_y, player_size):
            if enemy in enemies:
                enemies.remove(enemy)
            player_health -= 20
        
        # 移除超出屏幕的敌人
        if enemy[1] > screen_height + enemy_size:
            if enemy in enemies:
                enemies.remove(enemy)

    # 生成陨石
    asteroid_timer += 1
    if asteroid_timer >= asteroid_spawn_rate:
        spawn_asteroid()
        asteroid_timer = 0

    # 更新陨石
    for asteroid in asteroids[:]:
        asteroid[1] += asteroid[3]  # 使用陨石的速度
        
        # 检查陨石是否被子弹击中
        for bullet in bullets[:]:
            if check_collision(asteroid[0], asteroid[1], asteroid[2], bullet[0], bullet[1], bullet_size):
                if bullet in bullets:
                    bullets.remove(bullet)
                if asteroid in asteroids:
                    asteroids.remove(asteroid)
                score += 5
                break
        
        # 检查陨石是否与玩家碰撞
        if check_collision(asteroid[0], asteroid[1], asteroid[2], player_x, player_y, player_size):
            if asteroid in asteroids:
                asteroids.remove(asteroid)
            player_health -= 10
        
        # 移除超出屏幕的陨石
        if asteroid[1] > screen_height + asteroid[2]:
            if asteroid in asteroids:
                asteroids.remove(asteroid)

    # 检查游戏结束
    if player_health <= 0:
        running = False

    # 绘制
    screen.fill(BLACK)
    
    # 绘制子弹
    for bullet in bullets:
        pygame.draw.circle(screen, RED, (bullet[0], bullet[1]), bullet_size)
    
    # 绘制敌人
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0] - enemy_size // 2, enemy[1] - enemy_size // 2, enemy_size, enemy_size))
    
    # 绘制陨石
    for asteroid in asteroids:
        pygame.draw.circle(screen, WHITE, (asteroid[0], asteroid[1]), asteroid[2])
    
    # 绘制玩家
    draw_player(player_x, player_y)
    
    # 绘制生命值
    draw_health_bar(player_health)
    
    # 绘制分数
    score_text = font.render(f"分数: {score}", True, WHITE)
    screen.blit(score_text, (screen_width - 150, 10))
    
    pygame.display.flip()
    clock.tick(60)

# 游戏结束显示
game_over_font = pygame.font.SysFont(None, 72)
game_over_text = game_over_font.render("游戏结束", True, RED)
screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 36))
final_score_text = font.render(f"最终分数: {score}", True, WHITE)
screen.blit(final_score_text, (screen_width // 2 - 100, screen_height // 2 + 36))
pygame.display.flip()

# 等待几秒后退出
pygame.time.wait(3000)
pygame.quit()