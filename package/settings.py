""" Создание окна настроек """


from __future__ import annotations

import pygame


def input_screen():
    """
    Создание и запуск окна настроек

    return: (n, rmin, rmax, w, h, vmin, vmax) или None, если окно закрыто.
    """
    screen_width, screen_height = 480, 470
    s = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Настройки")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    labels = ["Шаров",
              "Мин. радиус", "Макс. радиус",
              "Ширина области", "Высота области",
              "Мин. скорость", "Макс. скорость"]
    texts = ["60", "10", "25", "1000", "800", "80", "220"]
    rects = [pygame.Rect(190, 25 + i * 50, 265, 30) for i in range(7)]
    button = pygame.Rect(140, 410, 200, 36)
    active = 0
    error = ""

    def validate():

        try:

            n = int(texts[0].strip())
            rmin = int(texts[1].strip())
            rmax = int(texts[2].strip())
            w = int(texts[3].strip())
            h = int(texts[4].strip())
            vmin = int(texts[5].strip())
            vmax = int(texts[6].strip())

        except Exception:

            return None, "Все поля должны содержать целые числа"

        if n < 1:
            return None, "Шаров >= 1"

        if rmin < 1 or rmax < rmin:
            return None, "Нужно 1 <= min <= max"

        if w < 100 or h < 100:
            return None, "Область минимум 100x100"

        if rmax * 2 >= min(w, h):
            return None, "Слишком большой радиус"

        if vmin < 0 or vmax < vmin:
            return None, "Нужно 0 <= min <= max"

        return (n, rmin, rmax, w, h, vmin, vmax), ""

    while True:

        mp = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return None

                if event.key == pygame.K_RETURN:

                    params, error = validate()

                    if params:
                        return params

                elif event.key == pygame.K_BACKSPACE:

                    texts[active] = texts[active][:-1]

                elif event.key == pygame.K_TAB:

                    active = (active + 1) % len(texts)

                elif event.unicode and event.unicode.isdigit():

                    texts[active] += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:

                hit = False
                for i, r in enumerate(rects):

                    if r.collidepoint(event.pos):
                        active = i
                        hit = True
                        break

                if not hit and button.collidepoint(event.pos):

                    params, error = validate()
                    if params:
                        return params

        s.fill((30, 30, 45))
        for i, (lbl, r) in enumerate(zip(labels, rects)):
            s.blit(font.render(lbl + ":", True, (200, 200, 210)), (15, r.y + 5))
            pygame.draw.rect(s, (40, 40, 55), r)
            pygame.draw.rect(s, (120, 180, 255) if i == active else (80, 80, 110), r, 2)
            s.blit(font.render(texts[i], True, (240, 240, 240)), (r.x + 6, r.y + 5))

        pygame.draw.rect(s, (90, 150, 230) if button.collidepoint(mp) else (60, 110, 180), button)
        bt = font.render("Запустить", True, (255, 255, 255))
        s.blit(bt, (button.x + (button.w - bt.get_width()) // 2,
                    button.y + (button.h - bt.get_height()) // 2))

        if error:
            s.blit(font.render(error, True, (255, 120, 120)), (15, 385))

        pygame.display.flip()
        clock.tick(60)
