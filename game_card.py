import constants as c
import pygame
import pygame.sprite as sprite


class Card:
    def __init__(self, card_info):
        self.id = int(card_info[c.CARD_ID])
        self.name = card_info[c.CARD_NAME]
        self.image = card_info[c.CARD_IMAGE]
        self.card_type = card_info[c.CARD_TYPE]
        self.attribute = card_info[c.ATTRIBUTE]
        self.attack = card_info[c.ATK]
        self.defense = card_info[c.DEF]
        self.EFFECT = card_info[c.EFFECT]

    def __str__(self):
        return str(self.get_game_info().values())

    def get_game_info(self):
        return {'name': self.name,
                'image': self.image,
                'card type': self.card_type,
                'attribute': self.attribute,
                'attack': str(self.attack),
                'defense': str(self.defense)}


class CardBackground(sprite.Sprite):
    def __init__(self):
        super(CardBackground, self).__init__()

        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.image.fill(c.WHITE)


class CardImage(sprite.Sprite):
    def __init__(self, card_id):
        super(CardImage, self).__init__()

        self.image = pygame.image.load('resources/{:0>3d}.png'.format(card_id))


class CardSprite(sprite.Sprite):
    def __init__(self, card_obj):
        sprite.Sprite.__init__(self)

        self.card = card_obj
        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()

        name_font = pygame.font.SysFont("comicsansms", 14)
        stat_font = pygame.font.SysFont("comicsansms", 12)

        self.card_name = name_font.render(self.card.name, True, c.BLACK, c.GRAY)
        self.card_image = CardImage(self.card.id).image
        self.card_atk = stat_font.render(str(self.card.attack), True, c.BLACK, c.GRAY)
        self.card_def = stat_font.render(str(self.card.defense), True, c.BLACK, c.GRAY)

        self.image.blit(self.card_name, (c.NAME_LEFT, c.NAME_TOP))
        self.image.blit(self.card_image, (c.IMG_LEFT, c.IMG_TOP))
        self.image.blit(self.card_atk, (c.STAT_LEFT, c.STAT_TOP))
        self.image.blit(self.card_def, (c.STAT_LEFT, c.STAT_TOP + 20))
