from __future__ import annotations

from figures import Rectangle, Ball
import pygame

CAPACITY = 1
MAX_DEPTH = 16


class QuadTree:

    def __init__(self, boundary: Rectangle, capacity: int = CAPACITY, depth: int = 0, max_depth: int = MAX_DEPTH):
        self.boundary = boundary
        self.depth = depth
        self.max_depth = max_depth
        self.capacity = capacity
        self.balls = []
        self.divided = False
        self.nw = self.ne = self.sw = self.se = None

    def subdivide(self):
        """
        Добавление 4 потомков к текущему узлу
        """
        b = self.boundary
        hw, hh = b.w * 0.5, b.h * 0.5

        d = self.depth + 1
        self.nw = QuadTree(Rectangle(b.x, b.y, hw, hh), self.capacity, d, self.max_depth)
        self.ne = QuadTree(Rectangle(b.x + hw, b.y, hw, hh), self.capacity, d, self.max_depth)
        self.sw = QuadTree(Rectangle(b.x, b.y + hh, hw, hh), self.capacity, d, self.max_depth)
        self.se = QuadTree(Rectangle(b.x + hw, b.y + hh, hw, hh), self.capacity, d, self.max_depth)

        self.divided = True

    def insert(self, ball: Ball):
        """
        Вставка элемента класса Ball в QuadTree
        """
        if not self.boundary.contains_ball(ball):
            return False

        if len(self.balls) < self.capacity or self.depth >= self.max_depth:
            self.balls.append(ball)
            return True

        if not self.divided:
            self.subdivide()

        for child in (self.nw, self.ne, self.sw, self.se):
            if child.insert(ball):
                return True

    def query(self, rect: Rectangle, out: list):
        """
        Получение списка элементов класса Ball в rect
        """
        if not self.boundary.intersects(rect):
            return

        for ball in self.balls:
            if rect.contains_ball(ball):
                out.append(ball)

        if self.divided:
            self.nw.query(rect, out)
            self.ne.query(rect, out)
            self.sw.query(rect, out)
            self.se.query(rect, out)

    def draw(self, surf, color: Any = (60, 90, 130)):
        """
        Раскрашивание границ текущего узла
        """
        b = self.boundary
        pygame.draw.rect(surf, color, (b.x, b.y, b.w, b.h), 1)
        if self.divided:
            self.nw.draw(surf, color)
            self.ne.draw(surf, color)
            self.sw.draw(surf, color)
            self.se.draw(surf, color)
