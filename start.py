import pygame
import random
class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width = 500
        self.height = 500
        self.snake_size = [10,10]
        self.food_size = [10,10]
        self.font = pygame.font.SysFont(None, 30)
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((self.width, self.height))

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)

        self.snake_position = [0,0]
        self.snake_direction = 'right'
        self.food_position = [0,0]
        self.score = 0
        self.snake_length = 2
        self.snake_body = []
    def reset(self):
        self.window.fill(self.black)
        self.score = 0
        self.snake_length = 3
        self.snake_position = [250,250]
        self.food_position = [random.randint(1, (self.width/10) - 1) * 10,random.randint(1, (self.height/10) - 1) * 10]
        self.snake_direction = 'right'
        self.snake_body = []
    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.snake_direction != "right":
                    self.snake_direction = "left"
                elif event.key == pygame.K_RIGHT and self.snake_direction != "left":
                    self.snake_direction = "right"
                elif event.key == pygame.K_UP and self.snake_direction != "down":
                    self.snake_direction = "up"
                elif event.key == pygame.K_DOWN and self.snake_direction != "up":
                    self.snake_direction = "down"
    def draw(self):
        if self.snake_length > 0:
            pygame.draw.rect(self.window,self.white,[self.snake_position[0], self.snake_position[1], self.snake_size[0], self.snake_size[1]])
            self.snake_length -= 1
            self.snake_body += [list(self.snake_position)]
        else:
            pygame.draw.rect(self.window,self.black,[self.snake_body[0][0], self.snake_body[0][1], self.snake_size[0], self.snake_size[1]])
            self.snake_body.pop(0)  # remove the oldest element from the list
            pygame.draw.rect(self.window,self.white,[self.snake_position[0], self.snake_position[1], self.snake_size[0], self.snake_size[1]])
            self.snake_body += [list(self.snake_position)]

        if self.snake_position == self.food_position:
            self.score += 1
            self.snake_length += 1
            self.food_position = [random.randint(1, (self.width/10) - 1) * 10,random.randint(1, (self.height/10) - 1) * 10]
        pygame.draw.rect(self.window,self.red,[self.food_position[0], self.food_position[1], self.food_size[0], self.food_size[1]])
        pygame.display.update()
    def update(self):
        if self.snake_direction == 'right':
            self.snake_position[0] += 10
        if self.snake_direction == 'left':
            self.snake_position[0] -= 10
        if self.snake_direction == 'up':
            self.snake_position[1] -= 10
        if self.snake_direction == 'down':
            self.snake_position[1] += 10

        if self.snake_position[0] == self.width or self.snake_position[1] == self.height:
            self.lose()
        if self.snake_position[0] == -10 or self.snake_position[1] == -10:
            self.lose()
        if self.snake_position in self.snake_body:
            self.lose()
    def lose(self):
        lose_text = self.font.render(f"SCORE : {self.score}",True,self.white)
        self.window.blit(lose_text,(10,10))
        #pygame.quit()
        #quit()
        self.reset()
    def start(self):
        self.reset()
        while True:
            self.inputs()
            self.update()
            self.draw()
            self.clock.tick(5)
game = SnakeGame()
game.start()