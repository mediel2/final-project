import pygame
from copy import deepcopy
from random import choice, randrange

pygame.init()

w, h = 10, 20
size = 40
FPS = 60

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

figures = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
           [(0, 0), (0, -1), (0, 1), (-1, 0)],
           [(0, -1), (-1, -1), (-1, 0), (0, 0)],
           [(0, 0), (-1, 0), (0, 1), (-1, -1)],
           [(0, 0), (0, -1), (0, 1), (1, -1)],
           [(-1, 0), (-1, 1), (0, 0), (0, -1)],
           [(0, 0), (0, -1), (0, 1), (-1, -1)]]

rear = [[0 for i in range(w)] for j in range(h)]

start = 0
speed = 15
speed_fall = 2000

sc = pygame.display.set_mode((400, 800))
pygame.display.set_caption('Тетрис')
pygame.display.set_icon(pygame.image.load('Logo.bmp'))
clock = pygame.time.Clock

net = [pygame.Rect(x * size, y * size, size, size) for x in range(w) for y in range(h)]
figeres_ig = [[pygame.Rect(x + 5, y + 1, 1, 1) for x, y in pos] for pos in figures]
figure_rect = pygame.Rect(0, 0, size - 1, size - 1)
figure = deepcopy(choice(figeres_ig))

figure_color = lambda: (randrange(0 , 255), randrange(0 , 255), randrange(0 , 255))
color = figure_color()

def borders():
    if figure[i].x < 0 or figure[i].x > w - 1:
        return False
    elif figure[i].y > h - 1 or rear[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    move = 0
    x = 0
    spin = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move = -1
            elif event.key == pygame.K_RIGHT:
                move = +1
            elif event.key == pygame.K_DOWN:
                speed_fall = 150
            elif event.key == pygame.K_UP:
                spin = True

    figure_1 = deepcopy(figure)
    for i in range(4):
        figure[i].x += move
        if not borders():
            figure = deepcopy(figure_1)
            break
        sc.fill(Black)

    start += speed
    if start > speed_fall:
        start = 0
        figure_1 = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not borders():
                for i in range(4):
                    rear[figure_1[i].y][figure_1[i].x] = color
                color = figure_color()
                figure = deepcopy(choice(figeres_ig))
                speed_fall = 2000
                break
            sc.fill(Black)

    center = figure[0]
    figure_1 = deepcopy(figure)
    if spin:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not borders():
                figure = deepcopy(figure_1)
                break
            sc.fill(Black)

    cleean_line = h - 1
    for j in range(h - 1, -1, -1):
        clean = 0
        for i in range(w):
            if rear[j][i]:
                clean += 1
            rear[cleean_line][i] = rear[j][i]
        if clean < w:
            cleean_line -= 1

    for i in range(4):
        figure_rect.x = figure[i].x * size
        figure_rect.y = figure[i].y * size
        pygame.draw.rect(sc, color, figure_rect)

    for y, z in enumerate(rear):
        for x, col in enumerate(z):
            if col:
                figure_rect.x, figure_rect.y = x * size, y * size
                pygame.draw.rect(sc, col, figure_rect)

    [pygame.draw.rect(sc, (100, 100, 100), i, 1) for i in net]
    pygame.display.flip()
