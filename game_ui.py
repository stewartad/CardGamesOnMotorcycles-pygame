import constants as c
import pygame
import pygame.sprite as sprite


class CardBackground(sprite.Sprite):
    def __init__(self):
        super(CardBackground, self).__init__()
        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.image.fill(c.WHITE)


class CardImage(sprite.Sprite):
    def __init__(self, card_id):
        super(CardImage, self).__init__()
        self.image = pygame.image.load('resources/{:0>3d}.png'.format(card_id))
        self.image.convert()


class CardSprite(sprite.Sprite):
    def __init__(self, card_obj):
        super(CardSprite, self).__init__()

        self.card = card_obj
        self.name = self.card.name
        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()
        self._font = c.F_TIMES

        name_font = pygame.font.SysFont(self._font, 14)
        stat_font = pygame.font.SysFont(self._font, 12)

        self.card_name = name_font.render(self.card.name, True, c.BLACK)
        self.card_image = CardImage(self.card.id).image
        self.card_image = pygame.transform.scale(self.card_image, (c.IMG_WIDTH, c.IMG_HEIGHT))
        self.card_atk = stat_font.render(str(self.card.attack), True, c.BLACK)
        self.card_def = stat_font.render(str(self.card.defense), True, c.BLACK)

        self.image.blit(self.card_name, (c.NAME_LEFT, c.NAME_TOP))
        self.image.blit(self.card_image, (c.IMG_LEFT, c.IMG_TOP))
        if self.card.card_type == 'MONSTER':
            self.image.blit(self.card_atk, (c.STAT_LEFT, c.STAT_TOP))
            self.image.blit(self.card_def, (c.STAT_LEFT, c.STAT_TOP + 20))

    def swap_size(self):
        return CardSpriteSmall(self.card)


class CardSpriteSmall(CardSprite):
    def __init__(self, card_obj):
        super(CardSpriteSmall, self).__init__(card_obj)

        self.image = pygame.Surface([c.S_CARD_WIDTH, c.S_CARD_HEIGHT])
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()
        self.card_image = pygame.transform.scale(self.card_image, (c.S_IMG_WIDTH, c.S_IMG_HEIGHT))
        name_font = pygame.font.SysFont(self._font, 10)

        self.image.blit(self.card_name, (c.S_NAME_LEFT, c.S_NAME_TOP))
        self.image.blit(self.card_image, (c.S_IMG_LEFT, c.S_IMG_TOP))
        if self.card.card_type == 'MONSTER':
            self.image.blit(self.card_atk, (c.S_STAT_LEFT, c.S_STAT_TOP))
            self.image.blit(self.card_def, (c.S_STAT_LEFT + 50, c.S_STAT_TOP))

    def swap_size(self):
        return CardSprite(self.card)
        

class CardPreview(sprite.Sprite):
    def __init__(self, card_sprite, x, y):
        super(CardPreview, self).__init__()
        self.image = pygame.Surface((c.VIEW_WIDTH, c.VIEW_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.card = card_sprite.card
        self.card_sprite = card_sprite
        self.name = self.card_sprite.name
        self._font = c.F_TIMES

        stat_font = pygame.font.SysFont(self._font, 12)
        self.type_label = stat_font.render('Type: {}'.format(self.card.card_type), True, c.BLACK)
        self.attr_label = stat_font.render('Attribute: {}'.format(self.card.attribute), True, c.BLACK)

        self.image.fill(c.BG_BLUE)
        self.image.blit(self.card_sprite.image, (50, 20))
        self.image.blit(self.type_label, (50, 285))
        self.image.blit(self.attr_label, (50, 315))


class GameLabel(sprite.Sprite):
    def __init__(self, text, x, y, size=12):
        super(GameLabel, self).__init__()
        self._font = pygame.font.SysFont(c.F_TIMES, size)
        self.text = text
        self.label_text = self._font.render(self.text, True, c.BLACK)
        self.label_w = self._font.size(self.text)[0]
        self.label_h = self._font.size(self.text)[1]
        self.label_center_x = self.label_w / 2
        self.label_center_y = self.label_h / 2

        self.image = pygame.Surface((self.label_w, self.label_h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.center_x = self.rect.width / 2
        self.center_y = self.rect.height / 2

        self.update()

    def update_text(self, text):
        self.text = text
        self.label_text = self._font.render(self.text, True, c.BLACK)

    def update(self, *args):
        self.image.fill(c.BG_BLUE)
        self.image.blit(self.label_text, (self.center_x - self.label_center_x, self.center_y - self.label_center_y))


class GameButton(GameLabel):
    def __init__(self, text, x, y):
        super(GameButton, self).__init__(text, x, y, c.BUTTON_SIZE)
        self.image = pygame.Surface((c.BUTTON_W, c.BUTTON_H))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.center_x = self.rect.width / 2
        self.center_y = self.rect.height / 2
        self.update()

    def update(self, *args):
        self.image.fill(c.BUTTON_COLOR)
        self.image.blit(self.label_text, (self.center_x - self.label_center_x, self.center_y - self.label_center_y))


class Cursor(sprite.Sprite):
    def __init__(self, x, y):
        super(Cursor, self).__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y