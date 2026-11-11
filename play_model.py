from __future__ import annotations

import math
import random
import pygame

from settings import input_screen
from figures import Ball, Rectangle
from quadtree import QuadTree

WIDTH, HEIGHT = 1000, 800
FPS = 60


def find_collisions(balls: list, width: int, height: int):
    """
    Поиск коллизий
    """
    if not balls:
        return [], None

    qt = QuadTree(Rectangle(0, 0, width, height))
    rmax = 0.0
    for ball in balls:
        qt.insert(ball)
        if ball.r > rmax:
            rmax = ball.r

    pairs = []
    for ball in balls:
        search_r = ball.r + rmax
        # область поиска вокруг ball — квадрат со стороной 2d
        query_rect = Rectangle(ball.x - search_r, ball.y - search_r, 2.0 * search_r, 2.0 * search_r)
        found = []
        qt.query(query_rect, found)

        for founded_ball in found:
            # Каждая пара проверяется один раз. Если убрать эту проверку, мячи будут проверяться дважды
            if founded_ball.id <= ball.id:
                continue
            dx = founded_ball.x - ball.x
            dy = founded_ball.y - ball.y
            rsum = ball.r + founded_ball.r
            dsq = dx * dx + dy * dy
            if 0.0 < dsq < rsum * rsum:
                dist = math.sqrt(dsq)
                pairs.append((ball, founded_ball, dx / dist, dy / dist, dist))

    return pairs, qt


def resolve_pair(a: Ball, b: Ball, nx: float | int, ny: float | int, dist: float | int):
    """
    Разрешение коллизий (изменений траектории, скорости, коррекция позиции столкнувшихся объектов)
    """
    m1, m2 = a.mass, b.mass
    inv1, inv2 = 1.0 / m1, 1.0 / m2
    total_inv = inv1 + inv2

    # позиционная коррекция (чтобы не было случая, когда один шар полностью перекрыл другой)
    overlap = (a.r + b.r) - dist
    a.x -= nx * overlap * (inv1 / total_inv)
    a.y -= ny * overlap * (inv1 / total_inv)
    b.x += nx * overlap * (inv2 / total_inv)
    b.y += ny * overlap * (inv2 / total_inv)

    rvx = b.vx - a.vx
    rvy = b.vy - a.vy
    vn = rvx * nx + rvy * ny
    if vn > 0:
        return

    j = -2.0 * vn / total_inv
    a.vx -= j * inv1 * nx
    a.vy -= j * inv1 * ny
    b.vx += j * inv2 * nx
    b.vy += j * inv2 * ny


def wall_collisions(balls: list, width: int, height: int):
    """
    Проверка и разрешение коллизий между экземпляром класса Ball и границами области
    """
    for ball in balls:
        if ball.x - ball.r < 0:
            ball.x = ball.r
            ball.vx = abs(ball.vx)
        elif ball.x + ball.r > width:
            ball.x = width - ball.r
            ball.vx = -abs(ball.vx)
        if ball.y - ball.r < 0:
            ball.y = ball.r
            ball.vy = abs(ball.vy)
        elif ball.y + ball.r > height:
            ball.y = height - ball.r
            ball.vy = -abs(ball.vy)


def start_model():
    """
    Инициализация модели, запуск главного окна приложения, создание экземпляров класса Ball
    """
    pygame.init()

    params = input_screen()
    if params is None:
        pygame.quit()
        raise SystemExit
    n_balls, r_min, r_max, WIDTH, HEIGHT, v_min, v_max = params

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('QuadTree collisions')
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 22)

    balls = []
    for _ in range(n_balls):
        r = random.randint(r_min, r_max)

        x = random.uniform(r, WIDTH - r)
        y = random.uniform(r, HEIGHT - r)

        speed = random.uniform(v_min, v_max)
        ang = random.uniform(0, 2 * math.pi)
        balls.append(Ball(x, y, speed * math.cos(ang), speed * math.sin(ang), r))

    running = True
    dt = 1.0 / FPS

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        for ball in balls:
            ball.x += ball.vx * dt
            ball.y += ball.vy * dt

        wall_collisions(balls, WIDTH, HEIGHT)

        pairs, qt = find_collisions(balls, WIDTH, HEIGHT)
        last_qt = qt
        for (ball, b, nx, ny, dist) in pairs:
            resolve_pair(ball, b, nx, ny, dist)

        wall_collisions(balls, WIDTH, HEIGHT)

        screen.fill((15, 15, 25))
        if last_qt is not None:
            last_qt.draw(screen)

        for b in balls:
            pygame.draw.circle(screen, b.color, (int(b.x), int(b.y)), int(b.r))
            pygame.draw.circle(screen, (0, 0, 0), (int(b.x), int(b.y)), int(b.r), 1)

        info = font.render(
            f"Balls: {len(balls)}  ESC: quit",
            True, (200, 200, 200)
        )

        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
