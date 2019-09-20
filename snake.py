import pygame
import random


class Fruit(object):
    position = 0, 0

    def __init__(self, cell_count):
        self.cell_count = cell_count
        # self.generate_next()

    def generate_next(self):
        x = random.randint(0, self.cell_count-2)
        y = random.randint(0, self.cell_count-2)
        self.position = x, y
        return self.position


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.body.append((0, 0))
        self.body.append((1, 0))
        self.head = (2, 0)
        self.body.append(self.head)
        self.dir_x = 1
        self.dir_y = 0
        self.lenght = 3

    def eat(self):
        self.lenght += 1
        self.body.append((-1, -1))

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                elif keys[pygame.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                elif keys[pygame.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                elif keys[pygame.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1

        self.head = (self.head[0]+self.dir_x, self.head[1]+self.dir_y)
        for i in range(self.lenght - 1):
            self.body[i] = self.body[i+1]
        self.body[self.lenght-1] = self.head


def draw_grid(w, rows, surface):
    cell_length = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + cell_length
        y = y + cell_length
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def draw_rect(surface, postion, color=(255, 0, 0)):
    rect_side = width // rows
    x = postion[0]
    y = postion[1]
    pygame.draw.rect(surface, color, (x*rect_side, y *
                                      rect_side, rect_side, rect_side))


def redraw_window(surface, fruit,  snake):
    surface.fill((0, 0, 0))
    draw_grid(width, rows, surface)
    draw_snake(snake, surface)
    draw_fruit(fruit, surface)
    pygame.display.update()


def draw_fruit(fruit: Fruit, surface):
    draw_rect(surface, fruit.position, (0, 255, 0))


def draw_snake(snake, surface):
    for b in snake.body:
        draw_rect(surface, b)


def game_over(snake: Snake, rows):
    return body_collision(snake) or boundaries_collision(snake, rows)


def body_collision(snake: Snake):
    return snake.head in snake.body[:-1]


def boundaries_collision(snake: Snake, rows):
    return snake.head[0] >= rows or snake.head[1] >= rows or snake.head[0] < 0 or snake.head[1] < 0


if __name__ == "__main__":
    global width, rows
    width = 600
    rows = 15
    window = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (10, 10))
    fruit = Fruit(rows)
    clock = pygame.time.Clock()
    while True:
        pygame.time.delay(90)
        clock.tick(10)
        if game_over(snake, rows):
            break
        if snake.head == fruit.position:
            snake.eat()
            pos = fruit.generate_next()
        snake.move()

        redraw_window(window, fruit, snake)
