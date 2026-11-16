"""Модуль хранит классы - фигуры (шар и прямоугольник)"""

from __future__ import annotations

import math
import random


class Ball:
    """
    Класс шар используется как основной объект за которым мы наблюдаем
    """
    _next_id = 0

    def __init__(self, x: float | int, y: float | int, vx: float | int, vy: float | int, r: float | int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.mass = math.pi * r * r
        self.id = Ball._next_id
        Ball._next_id += 1

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Rectangle:
    """
    Класс прямоугольник, используется как объект, с помощью которого определяются коллизии
    """
    __slots__ = ("x", "y", "w", "h")

    def __init__(self, x: float | int, y: float | int, w: float | int, h: float | int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains_point(self, px: float | int, py: float | int):
        """
        Проверка, что 2D точка находится в границах текущего прямоугольника
        """
        return self.x <= px < self.x + self.w and self.y <= py < self.y + self.h

    def contains_ball(self, ball: Ball):
        """
        Проверка, что элемент класса Ball находится в границах текущего прямоугольника
        """
        return self.contains_point(ball.x, ball.y)

    def intersects(self, other: Rectangle):
        """
        Проверка, находится ли other в текущем прямоугольнике
        """
        return not (other.x >= self.x + self.w
                    or other.y >= self.y + self.h
                    or other.x + other.w <= self.x
                    or other.y + other.h <= self.y)
