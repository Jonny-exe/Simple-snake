#!/usr/bin/python3
import pygame
import random

HEIGHT = 10
WIDTH = 11
SIZE = 50
LIGHT_GREEN = (164, 213, 98)
DARK_GREEN = (157,207,90)
APPLE_GREEN = (12, 194, 67)
BLUE = (51, 118, 228)
RED = (244, 75, 39)

APPLES_COUNT = 5


class Snake():
  def __init__(self):
    self.body = [(0, int(HEIGHT/2)), (1, int(HEIGHT/2)), (2, int(HEIGHT/2)), (3, int(HEIGHT/2))]
    self.length = len(self.body)
    self.head = self.body[self.length - 1]
    self.tail = self.body[0]
    self.position = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for i in self.body:
      self.position[i[1]][i[0]] = 1
    
  def move(self, direction: tuple, grow=False):
    if not grow:
      del self.body[0]
      self.position[self.tail[1]][self.tail[0]] = 0
    new_position = (self.head[0] + direction[0], self.head[1] + direction[1])
    self.body.append(new_position)

    self.head = new_position
    print("HEAD: ", self.head)
    self.tail = self.body[0]

    self.position[self.head[1]][self.head[0]] = 1

class Apples():
  def __init__(self):
    self.count = 0
    self.position = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

  def remove_apple(self, pos):
    self.count -= 1
    print(self.position[pos[1]][pos[0]])
    self.position[pos[1]][pos[0]] = 0
    print(self.position[pos[1]][pos[0]])

  def add_apple(self, snake):
    self.count += 1
    pos = [0, 0]
    while 1:
      idx = 0
      while idx < 2:
        pos[idx] = random.randint(0, WIDTH - 1 if idx == 0 else HEIGHT - 1) 
        idx += 1

      #print(pos)
      #print(self.position[pos[1]][pos[0]], snake.position[pos[1]][pos[0]])
      if self.position[pos[1]][pos[0]] == 0 and snake.position[pos[1]][pos[0]] == 0:
        break

    print("set")
    self.position[pos[1]][pos[0]] = 1

    return pos[0], pos[1]



class Game():
  def __init__(self):
    self.snake = Snake()
    pygame.init()
    self.screen = pygame.display.set_mode([700, 700])
    apples = Apples()

    running = True
    self.draw_board()
    self.draw_snake(self.snake.body)
    mov = (+1, 0)
    while running:
      print("-------------")
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
              mov = (-1, 0)
            elif event.key == pygame.K_RIGHT:
              mov = (+1, 0)
            elif event.key == pygame.K_DOWN:
              mov = (0, +1)
            elif event.key == pygame.K_UP:
              mov = (0, -1)
      new_pos = (self.snake.head[0] + mov[0], self.snake.head[1] + mov[1])
      print("NEW_POS", new_pos)
      if (new_pos[0] >= WIDTH) or (new_pos[1] >= HEIGHT) or (new_pos[0] < 0) or (new_pos[1] < 0):
        break

      if self.snake.position[new_pos[1]][new_pos[0]] == 1:
        break
      grow = False
      if apples.position[new_pos[1]][new_pos[0]] == 1:
        grow = True
        apples.remove_apple(new_pos)
      else:
        self.remove_snake_tail()
      self.snake.move(mov, grow)
      self.add_snake_head()

      if apples.count < APPLES_COUNT:
        print("COUNT: ", apples.count)
        print("POSITION: ", apples.position)
        new_apple_pos = apples.add_apple(self.snake)
        self.draw_apple(new_apple_pos)


      pygame.display.flip()
      pygame.time.wait(120)

    # Done! Time to quit.
    pygame.quit()

  def remove_snake_tail(self):
    self.draw_board_cell(self.snake.tail)
  
  def add_snake_head(self):
    x, y = self.snake.head 
    pygame.draw.rect(self.screen, BLUE, (x*SIZE,y*SIZE, SIZE,SIZE))

  def draw_board_cell(self, pos):
    x, y = pos
    pygame.draw.rect(self.screen, DARK_GREEN if (x + y * WIDTH) % 2 == 0 else LIGHT_GREEN, (x*SIZE,y*SIZE, SIZE,SIZE))

  def draw_board(self):
    turn = 0
    for y in range(HEIGHT):
      for x in range(WIDTH):
        pygame.draw.rect(self.screen, DARK_GREEN if turn % 2 == 0 else LIGHT_GREEN, (x*SIZE,y*SIZE, SIZE,SIZE))
        turn += 1

  def draw_snake(self, snake: list):
    for pos in snake:
      x, y = pos
      pygame.draw.rect(self.screen, BLUE, (x*SIZE+5,y*SIZE+5, SIZE-10,SIZE-10))

  def draw_apple(self, pos):
    x, y = pos
    #pygame.draw.circle(self.screen, RED, (x*SIZE+SIZE/2,y*SIZE+SIZE/2), SIZE-SIZE/2-4)
    #pygame.draw.rect(self.screen, APPLE_GREEN, (x*SIZE+25,y*SIZE, SIZE-30,SIZE-40))
    appleImg = pygame.image.load('apple.png')
    appleImg = pygame.transform.scale(appleImg, (SIZE, SIZE))

    self.screen.blit(appleImg, (x*SIZE,y*SIZE))


Game()
