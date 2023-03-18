"""
帮我写一个贪吃蛇游戏
"""
import pygame
import random
import time

# 初始化pygame
pygame.init()

# 设置窗口大小
screen = pygame.display.set_mode((600, 400))

# 设置窗口标题
pygame.display.set_caption("贪吃蛇")

# 设置窗口背景颜色
screen.fill((255, 255, 255))

# 设置蛇的初始位置
snake = [(200, 200), (210, 200), (220, 200)]

# 设置蛇的颜色
snake_color = (255, 0, 0)

# 设置蛇的初始方向
direction = "left"

# 设置食物的初始位置
food = (random.randint(0, 590), random.randint(0, 390))

# 设置食物的颜色
food_color = (0, 255, 0)

# 设置游戏的初始分数
score = 0

# 设置游戏的初始速度
speed = 0.1

# 设置游戏的初始状态
game_over = False

# 设置游戏的初始等级
level = 1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 400))
        self.snake = [(200, 200), (210, 200), (220, 200)]
        self.snake_color = (255, 0, 0)
        self.direction = "left"
        self.food = (random.randint(0, 590), random.randint(0, 390))
        self.food_color = (0, 255, 0)
        self.score = 0
        self.speed = 0.1
        self.game_over = False
        self.level = 1

    def run(self):
        while True:
            # 设置窗口背景颜色
            self.screen.fill((255, 255, 255))

            # 设置蛇的移动方向
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "down":
                        self.direction = "up"
                    elif event.key == pygame.K_DOWN and self.direction != "up":
                        self.direction = "down"
                    elif event.key == pygame.K_LEFT and self.direction != "right":
                        self.direction = "left"
                    elif event.key == pygame.K_RIGHT and self.direction != "left":
                        self.direction = "right"

            # 设置蛇的移动
            if self.direction == "up":
                new_head = (self.snake[0][0], self.snake[0][1] - 10)
            elif self.direction == "down":
                new_head = (self.snake[0][0], self.snake[0][1] + 10)
            elif self.direction == "left":
                new_head = (self.snake[0][0] - 10, self.snake[0][1])
            elif self.direction == "right":
                new_head = (self.snake[0][0] + 10, self.snake[0][1])

            # 设置蛇的吃食物
            if new_head == self.food:
                self.snake.insert(0, new_head)
                self.food = (random.randint(0, 590), random.randint(0, 390))
                self.score += 1
                if self.score % 5 == 0:
                    self.speed -= 0.01
                    self.level += 1
            else:
                self.snake.insert(0, new_head)
                self.snake.pop()

            # 设置蛇的死亡
            if new_head[0] < 0 or new_head[0] > 590 or new_head[1] < 0 or new_head[1] > 390:
                self.game_over = True
            if new_head in self.snake[1:]:
                self.game_over = True

            # 设置蛇的显示
            for x, y in self.snake:
                pygame.draw.rect(self.screen, self.snake_color, pygame.Rect(x, y, 10, 10))

            # 设置食物的显示
            pygame.draw.rect(self.screen, self.food_color, pygame.Rect(self.food[0], self.food[1], 10, 10))
            
            # 设置游戏的分数
            font = pygame.font.SysFont("arial", 20)
            score_text = font.render("Score: " + str(self.score), True, (0, 0, 0))
            self.screen.blit(score_text, (10, 10))

            # 设置游戏的等级
            level_text = font.render("Level: " + str(self.level), True, (0, 0, 0))

            # 设置游戏的速度
            speed_text = font.render("Speed: " + str(self.speed), True, (0, 0, 0))

            # 设置游戏的结束
            if self.game_over:
                game_over_text = font.render("Game Over", True, (0, 0, 0))
                self.screen.blit(game_over_text, (250, 200))
                self.screen.blit(score_text, (250, 230))
                self.screen.blit(level_text, (250, 260))
                self.screen.blit(speed_text, (250, 290))

            # 更新窗口
            pygame.display.update()

            # 设置游戏的速度
            time.sleep(self.speed)

if __name__ == "__main__":
    game = Game()
    game.run()


# 代码解析
# 1.导入pygame模块
# 2.初始化pygame
# 3.设置窗口大小
# 4.设置窗口标题
# 5.设置窗口背景颜色
# 6.设置蛇的初始位置
