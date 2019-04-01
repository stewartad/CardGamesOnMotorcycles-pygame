import pygame
from pygame import sprite as sprite

import constants as c


class CardSprite(sprite.Sprite):
    def __init__(self, card_obj, x, y):
        super(CardSprite, self).__init__()
        self.card = card_obj
        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.rect = pygame.Rect(x, y, c.CARD_WIDTH, c.CARD_HEIGHT)

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)

    def update(self):
        self.image.fill(c.WHITE)
        name_font = pygame.font.SysFont(c.F_TIMES, 14)
        stat_font = pygame.font.SysFont(c.F_TIMES, 12)

        card_name = name_font.render(self.card.name, True, c.BLACK)
        card_image = pygame.image.load('resources/{:0>3d}.png'.format(self.card.id))
        card_image = pygame.transform.scale(card_image, (c.IMG_WIDTH, c.IMG_HEIGHT))
        card_atk = stat_font.render(str(self.card.attack), True, c.BLACK)
        card_def = stat_font.render(str(self.card.defense), True, c.BLACK)

        self.image.blit(card_name, c.NAME_CORNER)
        self.image.blit(card_image, c.IMG_CORNER)
        if self.card.card_type == 'MONSTER':
            self.image.blit(card_atk, c.ATK_CORNER)
            self.image.blit(card_def, c.DEF_CORNER)


class SmallCardSprite(sprite.Sprite):
    def __init__(self, card_obj, x=0, y=0):
        super(SmallCardSprite, self).__init__()
        self.card = card_obj
        self.name = self.card.name
        self.image = pygame.Surface([c.S_CARD_WIDTH, c.S_CARD_HEIGHT])
        self.rect = pygame.Rect(x, y, c.S_CARD_WIDTH, c.S_CARD_HEIGHT)

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)

    def update(self):
        self.image.fill(c.WHITE)
        name_font = pygame.font.SysFont(c.F_TIMES, 12)

        card_name = name_font.render(self.card.name, True, c.BLACK)
        card_image = pygame.image.load('resources/{:0>3d}.png'.format(self.card.id))
        card_image = pygame.transform.scale(card_image, (c.S_IMG_WIDTH, c.S_IMG_HEIGHT))

        self.image.blit(card_name, c.S_NAME_CORNER)
        self.image.blit(card_image, c.S_IMG_CORNER)


class Button(sprite.Sprite):
    def __init__(self, text, x, y):
        super(Button, self).__init__()
        self.text = text
        self.image = pygame.Surface([c.BUTTON_W, c.BUTTON_H])
        self.rect = pygame.Rect(x, y, c.BUTTON_W, c.BUTTON_H)

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)

    def update(self):
        self.image.fill(c.BUTTON_COLOR)
        name_font = pygame.font.SysFont(c.F_TIMES, 14)
        button_text = name_font.render(self.text, True, c.BLACK)
        size = name_font.size(self.text)
        center = ((self.rect.width - size[0]) / 2, (self.rect.height - size[1]) /2)

        self.image.blit(button_text, center)


class Cursor(sprite.Sprite):
    def __init__(self, x, y):
        super(Cursor, self).__init__()
        self.image = pygame.Surface((10, 10))
        self.rect = pygame.Rect(x, y, 10, 10)


class Block(sprite.Sprite):
    def __init__(self, color, x, y, w, h):
        super(Block, self).__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)


class FieldSlot(sprite.GroupSingle):
    def __init__(self, x, y):
        super(FieldSlot, self).__init__()
        self.x = x
        self.y = y
        # self.image = pygame.Surface((c.FIELD_ZONE_W, c.FIELD_ZONE_H))
        self.rect = pygame.Rect(x, y, c.FIELD_ZONE_W, c.FIELD_ZONE_H)
        # self.card_sprite = sprite.GroupSingle()


    def place_card(self, card_obj):
        if card_obj is None:
            return
        card_sprite = SmallCardSprite(card_obj, self.x + c.FIELD_ZONE_PADDING / 2, self.y + c.FIELD_ZONE_PADDING / 2)
        self.add(card_sprite)



