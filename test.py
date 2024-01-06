import timeit
import math
import heapq
import pygame
from contextlib import contextmanager
import Constants


def time_seq_loops():
    def hi():
        for i in range(200):
            math.factorial(150)

    def bye():
        for i in range(300):
            math.factorial(150)


    def both():
        for i in range(200):
            math.factorial(150)
        for i in range(300):
            math.factorial(150)

    def f1():
        for i in range(4000):
            hi()
            bye()


    def f2():
        for i in range(4000):
            hi()
        for i in range(4000):
            bye()


    def f3():
        for i in range(4000):
            both()


    t = timeit.timeit("f1()", globals={"f1": f1}, number=1)
    print(t)

    t = timeit.timeit("f2()", globals={"f2": f2}, number=1)
    print(t)

    t = timeit.timeit("f3()", globals={"f3": f3}, number=1)
    print(t)


def heaptest():
    x = []
    heapq.heappush(x, (1,"hi"))
    heapq.heappush(x, (2, "hii"))
    heapq.heappush(x, (3, "hiii"))
    heapq.heappush(x, (4, "hiiii"))
    print(heapq.heappop(x))
    print(heapq.heappop(x))
    print(heapq.heappop(x))
    print(heapq.heappop(x))
    print(heapq.heappop(x))


@contextmanager
def drawer():
    screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)
    screen.fill((255, 255, 255))

    yield screen

    pygame.display.update()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.clear()
    pygame.event.wait()


def mask_test():
    with drawer() as screen:
        shad = pygame.image.load("./assets/images/ball shadow.png").convert_alpha()
        ball = pygame.image.load("./assets/images/balloon.png").convert_alpha()

        sqr = pygame.Surface((100, 100)).convert_alpha()
        sqr.fill((0, 255, 0))

        m = pygame.mask.from_surface(ball)
        print(m)
        m.to_surface(sqr, dest=(20, 20))

        screen.blit(shad, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        screen.blit(ball, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        screen.blit(sqr, (300, 300))


def opacity_test():
    with drawer() as screen:
        sqr = pygame.Surface((100, 100)).convert_alpha()
        sqr.fill((0, 255, 0))
        sqr2 = pygame.Surface((100, 100)).convert_alpha()
        sqr2.fill((0, 255, 0))
        sqr.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_SUB)
        screen.blit(sqr, (300, 300))
        screen.blit(sqr2, (100, 100))


def spritesheet_parser():
    screen = pygame.display.set_mode((500, 500))
    sheet = pygame.image.load("./assets/images/explosion.png").convert_alpha()
    frames = Constants.spritesheet2frames(sheet, (9, 9), 10)

    running = True
    i = 0

    while running:
        screen.fill((255, 255, 255))

        screen.blit(frames[(i // 5) % len(frames)], (100, 100))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        pygame.display.update()
        i += 1


def generator_test():
    def get():
        for i in range(10):
            yield i

    for i in get():
        print(i)


class A:
    def __init__(self):
        pass


class B(A):
    def __init__(self):
        super().__init__()


def inheritance_test():
    print(isinstance(B(), A))
    print(B == A)


if __name__ == "__main__":
    generator_test()
