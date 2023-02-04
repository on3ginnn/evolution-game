import pygame
import os
import sys
import random

FPS = 50
SIZE_FIELD = 3700
RANGEPOINTRADIUS = (3, 7)
MOBBORDERWIDTH = 8
MOBCOUNT = random.randint(10, 15)
POINTCOUNT = random.randint(300, 400)
PLAYERBORDERWIDTH = 8

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    return image


def terminate():
    pygame.quit()
    sys.exit()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player_group)
        self.radius = 10
        self.score = 20
        self.speed = 5
        self.image = pygame.Surface(((2 * self.radius) + (MOBBORDERWIDTH * 2),
                                     (2 * self.radius) + (MOBBORDERWIDTH * 2)), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, pygame.Color('green'), (self.radius, self.radius), self.radius,
                           PLAYERBORDERWIDTH - self.speed)

        self.rect = self.image.get_rect().move(10, 10)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, pos):
        self.rect = self.rect.move((pos[0], pos[1]))
        if pygame.sprite.spritecollideany(self, horizontal_borders) and pos[1]:
            self.rect.y += (pos[1] * -1)

        if pygame.sprite.spritecollideany(self, vertical_borders) and pos[0]:
            self.rect.x += (pos[0] * -1)

        def check_spritecollid():
            coef = 1
            # по оси Oy
            while pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect = self.rect.move((0, coef))
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    coef *= -1
                    self.rect = self.rect.move((0, coef))
                else:
                    continue

                self.rect = self.rect.move((0, coef))
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    coef *= -1
                    self.rect = self.rect.move((0, coef))
                    coef += 1

            coef = 1
            # по оси Ox
            while pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect = self.rect.move((coef, 0))
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    coef *= -1
                    self.rect = self.rect.move((coef, 0))
                else:
                    continue

                self.rect = self.rect.move((coef, 0))
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    coef *= -1
                    self.rect = self.rect.move((coef, 0))
                    coef += 1

        old_radius = self.radius
        for i in point_group:
            if pygame.sprite.collide_mask(self, i):
                self.radius += (i.rect.w // 4)
                self.score += (i.rect.w // 4)
                point_group.remove(i)
                all_sprites.remove(i)

                self.image = pygame.Surface(((2 * self.radius) + (MOBBORDERWIDTH * 2),
                                             (2 * self.radius) + (MOBBORDERWIDTH * 2)), pygame.SRCALPHA, 32)
                pygame.draw.circle(self.image, pygame.Color("white"), (self.radius, self.radius), self.radius)
                pygame.draw.circle(self.image, pygame.Color('green'), (self.radius, self.radius), self.radius,
                                   PLAYERBORDERWIDTH - self.speed)

                self.rect.x, self.rect.y = self.rect.x - (self.radius - old_radius), \
                    self.rect.y - (self.radius - old_radius)
                self.rect.w, self.rect.h = self.radius * 2, self.radius * 2
                self.mask = pygame.mask.from_surface(self.image)

                check_spritecollid()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.image.fill('red')
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill('red')
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Point(pygame.sprite.Sprite):
    def __init__(self, limited_pos=None):
        super().__init__(all_sprites, point_group)
        self.radius = random.randint(RANGEPOINTRADIUS[0], RANGEPOINTRADIUS[1])
        self.score = self.radius
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                           (self.radius, self.radius), self.radius)
        x, y = random.randint(1, SIZE_FIELD - self.radius * 2), random.randint(1, SIZE_FIELD - self.radius * 2)
        if limited_pos:
            x, y = random.randint(limited_pos['x'][0], limited_pos['x'][1]), random.randint(limited_pos['y'][0],
                                                                                            limited_pos['y'][1])
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, mob_group)
        self.level = 0
        self.radius = 10
        self.speed = 3
        self.score = 20
        self.image = pygame.Surface(((2 * self.radius) + (MOBBORDERWIDTH * 2),
                                     (2 * self.radius) + (MOBBORDERWIDTH * 2)), pygame.SRCALPHA, 32)
        self.mob_color = 'white'
        pygame.draw.circle(self.image, self.mob_color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, pygame.Color('red'), (self.radius, self.radius), self.radius,
                           MOBBORDERWIDTH - self.speed)
        x, y = random.randint(1, SIZE_FIELD - self.radius * 2), random.randint(1, SIZE_FIELD - self.radius * 2)
        # if limited_pos:
        #     x, y = random.randint(limited_pos['x'][0], limited_pos['x'][1]), random.randint(limited_pos['y'][0],
        #                                                                                     limited_pos['y'][1])
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.move_x = self.move_y = 0

    def mob_destination(self):
        if point_group.sprites():
            new_rect = random.choice(point_group.sprites()).rect
            new_move_x, new_move_y = new_rect.x - self.radius, new_rect.y - self.radius
            for i in point_group:
                if abs(abs(self.rect.x) - abs(i.rect.x)) + abs(abs(self.rect.y) - abs(i.rect.y)) <\
                        abs(abs(self.rect.x) - abs(new_move_x)) + abs(abs(self.rect.y) - abs(new_move_y)):
                    new_move_x = i.rect.x - self.radius
                    new_move_y = i.rect.y - self.radius

            self.move_x, self.move_y = new_move_x, new_move_y


    def point_collide(self):
        def check_spritecollid():
            coef = 1
            # по оси Oy
            while pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect = self.rect.move((0, coef))
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    coef *= -1
                    self.rect = self.rect.move((0, coef))
                else:
                    continue

                self.rect = self.rect.move((0, coef))
                if pygame.sprite.spritecollideany(self, horizontal_borders):
                    coef *= -1
                    self.rect = self.rect.move((0, coef))
                    coef += 1

            coef = 1
            # по оси Ox
            while pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect = self.rect.move((coef, 0))
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    coef *= -1
                    self.rect = self.rect.move((coef, 0))
                else:
                    continue

                self.rect = self.rect.move((coef, 0))
                if pygame.sprite.spritecollideany(self, vertical_borders):
                    coef *= -1
                    self.rect = self.rect.move((coef, 0))
                    coef += 1

        old_radius = self.radius
        for i in point_group:
            if pygame.sprite.collide_mask(self, i):
                self.radius += (i.rect.w // 4)
                self.score += (i.rect.w // 4)
                point_group.remove(i)
                all_sprites.remove(i)

                self.image = pygame.Surface(((2 * self.radius) + (MOBBORDERWIDTH * 2),
                                             (2 * self.radius) + (MOBBORDERWIDTH * 2)), pygame.SRCALPHA, 32)
                pygame.draw.circle(self.image, self.mob_color,
                                   (self.radius, self.radius), self.radius)
                pygame.draw.circle(self.image, pygame.Color('red'), (self.radius, self.radius), self.radius,
                                   MOBBORDERWIDTH - self.speed)

                self.rect.x, self.rect.y = self.rect.x - (self.radius - old_radius), \
                                           self.rect.y - (self.radius - old_radius)
                self.rect.w, self.rect.h = self.radius * 2, self.radius * 2
                self.mask = pygame.mask.from_surface(self.image)
                check_spritecollid()

    def update(self, *args):
        self.mob_destination()

        move_x_const = move_y_const = 0

        if self.rect.y > self.move_y:
            move_y_const = -1
        elif self.rect.y < self.move_y:
            move_y_const = +1
        self.rect = self.rect.move(0, move_y_const * self.speed)

        if self.rect.x > self.move_x:
            move_x_const = -1
        elif self.rect.x < self.move_x:
            move_x_const = +1
        self.rect = self.rect.move(move_x_const * self.speed, 0)

        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move((move_x_const * -1) * self.speed, 0)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.rect = self.rect.move(0, (move_y_const * -1) * self.speed)

        self.point_collide()


def generate_field(player=None):
    global RANGEPOINTRADIUS, SIZE_FIELD, POINTCOUNT, MOBCOUNT
    if not player:

        Border(0, 0, SIZE_FIELD - 1, 0)
        Border(0, SIZE_FIELD - 1, SIZE_FIELD - 1, SIZE_FIELD - 1)
        Border(0, 0, 0, SIZE_FIELD - 1)
        Border(SIZE_FIELD - 1, 0, SIZE_FIELD - 1, SIZE_FIELD - 1)

        for i in range(POINTCOUNT):
            Point()

        for i in range(MOBCOUNT):
            Mob()

        player = Player()

        screen2 = pygame.Surface((SIZE_FIELD, SIZE_FIELD))

        return player, screen2
    else:
        player.radius //= 2
        player.image = pygame.Surface(((2 * player.radius) + (MOBBORDERWIDTH * 2),
                                       (2 * player.radius) + (MOBBORDERWIDTH * 2)), pygame.SRCALPHA, 32)
        pygame.draw.circle(player.image, pygame.Color("white"), (player.radius, player.radius), player.radius)
        pygame.draw.circle(player.image, pygame.Color('#09ab3f'), (player.radius, player.radius), player.radius,
                           PLAYERBORDERWIDTH - player.speed)
        player.rect.x, player.rect.y = player.rect.x // 2, player.rect.y // 2
        player.rect.w, player.rect.h = player.radius * 2, player.radius * 2

        for i in horizontal_borders:
            i.rect.w //= 2

            i.rect.y, i.rect.x = i.rect.y // 2, i.rect.x // 2
            i.image = pygame.Surface([i.rect.w, 1])
            i.image.fill('red')
            SIZE_FIELD = i.rect.w

        for i in vertical_borders:
            i.rect.h //= 2
            i.rect.y, i.rect.x = i.rect.y // 2, i.rect.x // 2
            i.image = pygame.Surface([1, i.rect.h])
            i.image.fill('red')
        for i in point_group:
            i.rect.y //= 2
            i.rect.x //= 2
            if i.rect.w <= 1:
                point_group.remove(i)
                all_sprites.remove(i)
            else:
                i_radius = i.rect.w // 2
                i.image = pygame.Surface((2 * i_radius, 2 * i_radius),
                                            pygame.SRCALPHA, 32)
                pygame.draw.circle(i.image,
                                   (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                                   (i.radius, i.radius), i.radius)
        RANGEPOINTRADIUS = (2 if RANGEPOINTRADIUS[0] // 2 < 2 else RANGEPOINTRADIUS[0] // 2,
                            4 if RANGEPOINTRADIUS[1] // 2 < 2 else RANGEPOINTRADIUS[1] // 2)

        for i in mob_group:
            i.rect.y //= 2
            i.rect.x //= 2
            i.radius //= 2
            i.image = pygame.Surface(((2 * i.radius) + (MOBBORDERWIDTH * 2),
                                      (2 * i.radius) + (MOBBORDERWIDTH * 2)), pygame.SRCALPHA, 32)
            i.mob_color = 'white'
            pygame.draw.circle(i.image, i.mob_color, (i.radius, i.radius), i.radius)
            pygame.draw.circle(i.image, pygame.Color('red'), (i.radius, i.radius), i.radius,
                               MOBBORDERWIDTH - i.speed)
            i.rect.w, i.rect.h = i.radius * 2, i.radius * 2

        return player


def start_screen():
    global POINTCOUNT, SIZE_FIELD, MOBBORDERWIDTH
    intro_text = ['"ЭВОЛЮЦИЯ"', "",
                  "Правила игры:",
                  "-поедать микробов",
                  "-увеличиться в размере"]
    outro_text = ['Поздравляем!', '',
                  'Вы Прошли Игру.']

    screen2 = pygame.Surface(screen.get_size())

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen2.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, 'white')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (width // 2) - (intro_rect.w // 2) + 90
        intro_rect.y += 45
        text_coord += intro_rect.height
        screen2.blit(string_rendered, intro_rect)

    player = None
    K_RIGHT = K_LEFT = K_UP = K_DOWN = False
    camera = Camera()
    starting = False
    win = False

    while True:
        pos = [0, 0]

        if starting:
            player, screen2 = generate_field()
            starting = False
            screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if player and not win:
                    if event.key == pygame.K_RIGHT:
                        if K_LEFT:
                            K_LEFT = False
                        K_RIGHT = True
                    elif event.key == pygame.K_LEFT:
                        if K_RIGHT:
                            K_RIGHT = False
                        K_LEFT = True
                    elif event.key == pygame.K_UP:
                        if K_DOWN:
                            K_DOWN = False
                        K_UP = True
                    elif event.key == pygame.K_DOWN:
                        if K_UP:
                            K_UP = False
                        K_DOWN = True

                if player is None:
                    starting = True
            elif event.type == pygame.KEYUP:
                if player and not win:
                    if event.key == pygame.K_RIGHT:
                        K_RIGHT = False
                    elif event.key == pygame.K_LEFT:
                        K_LEFT = False
                    elif event.key == pygame.K_UP:
                        K_UP = False
                    elif event.key == pygame.K_DOWN:
                        K_DOWN = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if player is None and not win:
                    starting = True
        if K_UP:
            pos[1] = player.speed * -1
        elif K_DOWN:
            pos[1] = player.speed * 1
        if K_LEFT:
            pos[0] = player.speed * -1
        elif K_RIGHT:
            pos[0] = player.speed * 1

        if player:
            # изменение скорости у мобов, отлична от алгоритма расчета скорости для игрока
            for i in mob_group:
                if i.score // 100 > i.level:
                    i.level += 1
                    i.speed -= (1 if i.speed > 1 else 0)

            # изменение скорости, по соотношению с размером игрока, и масштаба
            if player.radius >= 200:
                player.speed -= (1 if player.speed > 1 else 0)
                MOBBORDERWIDTH -= (1 if player.speed > 1 else 0)
                SIZE_FIELD = 1450
                POINTCOUNT //= 2
                player = generate_field(player=player)

            # добавление микробов на поле
            if len(list(point_group)) < POINTCOUNT and random.choice(list(map(lambda x: 0, range(30))) + [1]):
                limited_pos = {'x': [], 'y': []}
                # расчет координат новых микробов учитывая положение камеры
                for i in vertical_borders:
                    limited_pos['x'].append(i.rect.x)
                for i in horizontal_borders:
                    limited_pos['y'].append(i.rect.y)

                p = Point(limited_pos)
            while len(list(point_group)) > POINTCOUNT:
                remove_obj = random.choice(list(point_group))
                point_group.remove(remove_obj)
                all_sprites.remove(remove_obj)

            # изменение ракурса камеры относительно игрока
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            font = pygame.font.Font(None, 20)
            text_coord = 10
            text = {'SCORE': 'yellow', str(player.score): 'white'}
            for line in text:
                string_rendered = font.render(line, True, text[line])
                intro_rect = string_rendered.get_rect()
                intro_rect.y = text_coord
                if text[line] == 'white':
                    intro_rect.x += 70
                else:
                    intro_rect.x += 10
                screen2.blit(string_rendered, intro_rect)

        all_sprites.draw(screen2)

        screen.blit(screen2, (0, 0))

        player_group.update(pos)
        mob_group.update()
        # all_sprites.update(pos)
        print()

        # больший объект - сверху
        new_all_sprites = sorted(all_sprites.sprites(), key=lambda x: x.rect.w)
        for i in new_all_sprites:
            all_sprites.remove(i)
            all_sprites.add(i)


        if player:
            screen2.fill('black')
            if player.rect.w >= SIZE_FIELD * 0.7:

                screen.fill('black')

                screen2 = pygame.Surface(screen.get_size())
                screen2.fill('black')

                font = pygame.font.Font(None, 40)
                text_coord = 50
                for line in outro_text:
                    string_rendered = font.render(line, True, 'white')
                    intro_rect = string_rendered.get_rect()
                    text_coord += 10
                    intro_rect.top = text_coord
                    intro_rect.x = (width // 2) - (intro_rect.w // 2)
                    intro_rect.y += (height // 2) - 50 - 40
                    text_coord += intro_rect.height
                    screen2.blit(string_rendered, intro_rect)
                screen.blit(screen2, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Перемещение героя. Новый уровень')
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    mob_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    point_group = pygame.sprite.Group()

    start_screen()