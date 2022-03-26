import random
from math import floor

import pygame as pg

pg.font.init()


def redraw_screen(surface):
    pg.display.update()
    surface.fill((255, 255, 255))


class CardPair:
    def __init__(self, image, pos, size, m, columns, o_set):
        self.size = size
        self.position1 = [o_set[0] - columns + (size[0] + m[0]) * pos[0][0],
                          o_set[1] + (size[1] + m[1]) * pos[0][1]]
        self.position2 = [o_set[0] - columns + (size[0] + m[0]) * pos[1][0],
                          o_set[1] + (size[1] + m[1]) * pos[1][1]]
        self.image = image
        self.chosen1 = 0
        self.chosen2 = 0

    def choose(self, m_pos):
        if self.position1[0] < m_pos[0] < self.position1[0] + self.size[0] and self.position1[1] < m_pos[1] < \
                self.position1[1] + self.size[1]:
            self.chosen1 = 1
        if self.position2[0] < m_pos[0] < self.position2[0] + self.size[0] and self.position2[1] < m_pos[1] < \
                self.position2[1] + self.size[1]:
            self.chosen2 = 1

    def draw_matching(self, default, screen):
        if self.chosen1:
            screen.blit(self.image, self.position1)
        else:
            screen.blit(default, self.position1)
        if self.chosen2:
            screen.blit(self.image, self.position2)
        else:
            screen.blit(default, self.position2)


class MatchingScreen:
    def __init__(self, lvl, images, screen):
        self.rows = 4
        self.columns = 2 * lvl + 1
        self.image_list = images
        self.card_set = []
        self.screen = screen

    def generate_pairs(self, size, m, o_set):
        key_list = random.sample([a + 1 for a in range(self.rows * self.columns)], self.rows * self.columns)
        key_list = [(key_list[2 * a], key_list[(2 * a) + 1]) for a in range(int(self.rows * self.columns / 2))]
        image_cards = {image: ((floor((key_list[a][0] - 1) / self.columns), (key_list[a][0] - 1) % self.columns),
                               (floor((key_list[a][1] - 1) / self.columns), (key_list[a][1] - 1) % self.columns))
                       for a, image in enumerate(self.image_list)}
        self.card_set = [CardPair(card, image_cards[card], size, m, self.columns, o_set) for card in image_cards]
        return self.card_set

    def draw_cards(self, m_pos, chosen_cards):
        if chosen_cards < 2:
            for pair in self.card_set:
                pair.choose(m_pos)
        for pair in self.card_set:
            pair.draw_matching(self.image_list[-1], self.screen)
        redraw_screen(self.screen)

    def complete(self):
        count = 0
        for a in self.card_set:
            if a.chosen1 + a.chosen2 == 2:
                return 2, 1, 1
            else:
                count += a.chosen1 + a.chosen2
        return count, 1, 0

    def reset(self):
        for m, a in enumerate(self.card_set):
            if a.chosen1 + a.chosen2 == 2:
                self.card_set.pop(m)
            a.chosen1 = 0
            a.chosen2 = 0


def run(level, X, Y, image_list, size, margins, matches, delay, surface):
    clock = pg.time.Clock()
    offset = [(X - (margins[0] + size[0]) * 4) / 2, (Y - (margins[1] + size[1]) * (2 * level + 1)) / 2]
    g = MatchingScreen(1, image_list, surface)
    pairs = g.generate_pairs(size, margins, offset)
    word = pg.font.SysFont('Comic Sans MS', 20)
    time = 0
    correct_matches = 0
    f = [0]
    close_time = pg.time.get_ticks()
    while matches or close_time + delay[0] > pg.time.get_ticks():
        if not pairs:
            pairs = g.generate_pairs(size, margins, offset)
        mouse_pos = [0, 0]
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = list(pg.mouse.get_pos())
        g.draw_cards(mouse_pos, f[0])
        f = g.complete()
        if f[0] == 2:
            if not time:
                time = pg.time.get_ticks()
            if pg.time.get_ticks() > time + delay[1]:
                correct_matches += f[2]
                matches -= f[1]
                g.reset()
                time = 0
                if not matches:
                    close_time = pg.time.get_ticks()
        text = word.render("Energy: " + str(matches), True, (255, 0, 0))
        surface.blit(text, (20, 10))
        clock.tick(60)

# X = 800
# Y = 600
# size = (80, 120)
# margins = (20, 30)
# surface = pg.display.set_mode((X, Y))
# image_1 = pg.image.load(r"C:\Users\massi\IdeaProjects\Grade_12\Testing_Folder\image_1.jpg").convert_alpha()
# image_1 = pg.transform.scale(image_1, size)
# image_2 = pg.image.load(r"C:\Users\massi\IdeaProjects\Grade_12\Testing_Folder\image_2.jpg").convert_alpha()
# image_2 = pg.transform.scale(image_2, size)
# image_3 = pg.image.load(r"C:\Users\massi\IdeaProjects\Grade_12\Testing_Folder\image_3.jpg").convert_alpha()
# image_3 = pg.transform.scale(image_3, size)
# image_4 = pg.image.load(r"C:\Users\massi\IdeaProjects\Grade_12\Testing_Folder\image_4.jpg").convert_alpha()
# image_4 = pg.transform.scale(image_4, size)
# image_5 = pg.image.load(r"C:\Users\massi\IdeaProjects\Grade_12\Testing_Folder\image_5.jpg").convert_alpha()
# image_5 = pg.transform.scale(image_5, size)
# image_6 = pg.image.load(r"C:\Users\massi\IdeaProjects\Grade_12\Testing_Folder\image_6.jpg").convert_alpha()
# image_6 = pg.transform.scale(image_6, size)
# image_list = [image_1, image_2, image_3, image_4, image_5, image_6]
# run(1, X, Y, image_list, size, margins, 3, (1000, 500), surface)
