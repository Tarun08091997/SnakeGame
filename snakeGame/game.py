"""
This section handles the logic for the snake's movement and growth in the game. 
We have two lists: `self.snake` for storing the coordinates of the snake's body segments, 
and `self.snake_rect` for storing the corresponding rectangle objects used for collision detection.

To remove the collision part we can simply generate each fruit and snake on the multiple part of Block.
i.e., x = n * Block, y = m * Block using `self.generateFruit()` and ensuring positions align with grid blocks.

When the snake moves, a new head segment is added at the front of these lists based on the 
current direction of movement set by `self.moveSnake()`. At the same time, if the snake hasn't eaten food 
(`self.updateScore()` returns False, indicating fruit not being eaten), we remove the last segment using `pop()`. 
This effectively shifts the snake forward without increasing its length.

By keeping both `self.snake` and `self.snake_rect` lists in sync (adding and removing elements 
at the same time), we ensure that the visual representation of the snake and its collision 
boundaries are always accurate. The flow is simple: 
1. Update the head position using `self.updateHead()`
2. Add it to the lists
3. Remove the tail using `self.snake.pop()` and `self.snake_rect.pop()` if `self.updateScore()` is False.
4. Continuously check for collisions using `self.checkCollision()` 
5. Generate new fruits as needed with `self.generateFruit()` 

These functions work together to maintain smooth movement and gameplay mechanics.
"""


import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
Point = namedtuple('Point','x,y')
class Direction(Enum):
    RIGHT = Point(1,0)
    LEFT = Point(-1,0)
    UP = Point(0,-1)
    DOWN = Point(0,1)


FPS = 30
OUTER_BLOCK_COLOR = (0,0,255)
INNER_BLOCK_COLOR = (255,0,0)
BLOCK = 20
BORDER_WIDTH = BLOCK//10

INNER_BLOCK = BLOCK-2*BORDER_WIDTH

class SnakeGame:
    def __init__(self,w=1000,h=600):
        self.w = w
        self.h = h

        # Screen
        self.sc = pygame.display.set_mode((w,h))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()

        # game States
        self.direction = Direction.RIGHT
        self.score = 0
        self.fruit = None
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK,self.head.y),
                      Point(self.head.x-2*BLOCK,self.head.y)]
        
        self.snake_rect = []
        for pt in self.snake:
            self.snake_rect.append(pygame.Rect(pt.x,pt.y,BLOCK,BLOCK))
        
        
    
    def createFruit(self):
        x = random.randint(0,self.w - BLOCK)
        y = random.randint(0,self.h - BLOCK)
        rect = pygame.Rect(x,y,BLOCK,BLOCK)
        while rect.collidelist(self.snake_rect) != -1:
            x = random.randint(0,self.w - BLOCK)
            y = random.randint(0,self.h - BLOCK)
            rect = pygame.Rect(x,y,BLOCK,BLOCK)
        
        self.fruit = Point(x,y)
        self.fruit_rect = rect
        pygame.draw.rect(self.sc,INNER_BLOCK_COLOR,(self.fruit.x,self.fruit.y,BLOCK,BLOCK))
    
    def drawSnake(self):
        # print(self.snake)
        for pt in self.snake:
            #outer Rect
            pygame.draw.rect(self.sc,OUTER_BLOCK_COLOR,(pt.x,pt.y,BLOCK,BLOCK))
            # inner rect
            pygame.draw.rect(self.sc,INNER_BLOCK_COLOR,(pt.x+BORDER_WIDTH,pt.y+BORDER_WIDTH,INNER_BLOCK,INNER_BLOCK))
    
    def drawFruit(self):
        pygame.draw.rect(self.sc,INNER_BLOCK_COLOR,(self.fruit.x,self.fruit.y,BLOCK,BLOCK))

    def draw_score(self):
        text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Arial", 30)
        score_text = self.font.render(f"Score: {self.score}", True, text_color)
        score_rect = score_text.get_rect(center=(self.w // 2, 20))
        self.sc.blit(score_text, score_rect)
    
    def move(self):
        head = self.snake[0]
        x = game.direction.value.x * BLOCK + head.x
        y = game.direction.value.y * BLOCK + head.y

        self.snake.insert(0,Point(x,y))
        self.snake_rect.insert(0,pygame.Rect(x,y,BLOCK,BLOCK))

        # delete tail if fruit was not eaten => update score is false
        if not self.updateScore():
            self.snake.pop()
            self.snake_rect.pop()
        

    def isGameOver(self):
        head = self.snake[0]
        if self.snake_rect[0].collidelist(self.snake_rect[1:]) != -1 or (not 0 <= head.x <= self.w-BLOCK) or (not 0 <= head.y <= self.h-BLOCK):
            return True
        return False

    def updateScore(self):
        if self.fruit:
            # if snake head collide with fruit
            if self.fruit_rect.colliderect(self.snake_rect[0]):
                self.fruit = None
                self.score += 1
                print(self.score)
                # increase snake length
                return True
        return False

    def playStep(self):
        self.sc.fill((0,0,0))
        game.clock.tick(FPS)

        # 2. Move
        self.move()
        # 3. Check for game will run
        if(self.isGameOver()):
            return False
        
        
        # 5. Update UI
        self.drawSnake()
        if not self.fruit:
            self.createFruit()
        else:
            self.drawFruit()
        self.draw_score()
        pygame.display.update()

        # return False if not game over
        return True
        pass





if __name__ == "__main__":
    game = SnakeGame()


    running = True
    while(running):
        running = game.playStep()
        
        
        
        # 1. controls
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                
                if event.key == pygame.K_UP and game.direction != Direction.DOWN:
                    game.direction = Direction.UP
                
                elif event.key == pygame.K_DOWN and game.direction != Direction.UP:
                    game.direction = Direction.DOWN
                
                if event.key == pygame.K_LEFT and game.direction != Direction.RIGHT:
                    game.direction = Direction.LEFT
                
                elif event.key == pygame.K_RIGHT and game.direction != Direction.LEFT:
                    game.direction = Direction.RIGHT


                
                    
            
            if event.type == pygame.QUIT:
                runnig = False
                pygame.quit()
                