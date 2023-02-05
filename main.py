import pygame
import os
import sys
import random


CONST = None
FPS = 50


# обновление констант, система реализации цикличного запуска игры,
# то есть после победы или поражения игрок сразу же может начать играть новую игру
def const_update():
    global CONST
    CONST = {'SIZE_FIELD': 3700, 'RANGEPOINTRADIUS': (3, 7),
             'MOBBORDERWIDTH': 8, 'MOBCOUNT': random.randint(5, 10), 'POINTCOUNT': random.randint(300, 400),
             'PLAYERBORDERWIDTH': 8, 'RATEPOINT': 30, 'RATEMOB': 300, 'MOBTRIGGER': 150}


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
        self.loss = False
        self.score = 20
        self.speed = 4
        self.image = pygame.Surface(((2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2),
                                     (2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2)), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("white"), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, pygame.Color('green'), (self.radius, self.radius), self.radius,
                           CONST['PLAYERBORDERWIDTH'] - self.speed)

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
            # игрок съел поинт
            if pygame.sprite.collide_mask(self, i):
                sound_point.play()

                self.radius += (i.rect.w // 4)
                self.score += (i.rect.w // 4)
                point_group.remove(i)
                all_sprites.remove(i)

                self.image = pygame.Surface(((2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2),
                                             (2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2)), pygame.SRCALPHA, 32)
                pygame.draw.circle(self.image, pygame.Color("white"), (self.radius, self.radius), self.radius)
                pygame.draw.circle(self.image, pygame.Color('green'), (self.radius, self.radius), self.radius,
                                   CONST['PLAYERBORDERWIDTH'] - self.speed)

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
        self.radius = random.randint(CONST['RANGEPOINTRADIUS'][0], CONST['RANGEPOINTRADIUS'][1])
        self.score = self.radius
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                           (self.radius, self.radius), self.radius)
        x, y = random.randint(1, CONST['SIZE_FIELD'] - self.radius * 2), \
            random.randint(1, CONST['SIZE_FIELD'] - self.radius * 2)

        # расчет координат новых микробов, учитывая положение камеры
        if limited_pos:
            x, y = random.randint(limited_pos['x'][0], limited_pos['x'][1]), random.randint(limited_pos['y'][0],
                                                                                            limited_pos['y'][1])

        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)


class Mob(pygame.sprite.Sprite):
    def __init__(self, limited_pos=None):
        super().__init__(all_sprites, mob_group)
        self.level = 0
        self.radius = 10
        self.speed = 3
        self.score = 20
        self.image = pygame.Surface(((2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2),
                                     (2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2)), pygame.SRCALPHA, 32)
        self.mob_color = 'white'
        pygame.draw.circle(self.image, self.mob_color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, pygame.Color('red'), (self.radius, self.radius), self.radius,
                           CONST['MOBBORDERWIDTH'] - self.speed)
        x, y = random.randint(1, CONST['SIZE_FIELD'] - self.radius * 2), \
            random.randint(1, CONST['SIZE_FIELD'] - self.radius * 2)

        # расчет координат новых мобов, учитывая положение камеры
        if limited_pos:
            x, y = random.randint(limited_pos['x'][0], limited_pos['x'][1]), random.randint(limited_pos['y'][0],
                                                                                            limited_pos['y'][1])

        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.move_x = self.move_y = 0

    def mob_destination(self, player):
        # мобы идут на поинты, если есть
        if point_group.sprites():
            new_rect = random.choice(point_group.sprites()).rect
            new_move_x, new_move_y = new_rect.x - self.radius, new_rect.y - self.radius
            for i in point_group:
                if abs(abs(self.rect.x) - abs(i.rect.x)) + abs(abs(self.rect.y) - abs(i.rect.y)) <\
                        abs(abs(self.rect.x) - abs(new_move_x)) + abs(abs(self.rect.y) - abs(new_move_y)):
                    new_move_x = i.rect.x - self.radius
                    new_move_y = i.rect.y - self.radius
        # мобы идут на игрока, если расстояние до него меньше MOBTRIGGER и разница в размере не менее 10px
        if player.rect.x in tuple(map(lambda x: x,
                                      range(self.rect.x - CONST['MOBTRIGGER'],
                                            self.rect.x + self.rect.w + CONST['MOBTRIGGER']))) and \
                player.rect.y in \
                tuple(map(lambda y: y, range(self.rect.y - CONST['MOBTRIGGER'],
                                             self.rect.y + self.rect.h + CONST['MOBTRIGGER']))) and \
                abs(player.radius - self.radius) > 5:
            if player.radius < self.radius:
                new_move_x, new_move_y = player.rect.x, player.rect.y
            else:
                new_move_x, new_move_y = player.rect.x * -1, player.rect.y * -1

        self.move_x, self.move_y = new_move_x, new_move_y

    def point_collide(self, player):
        def check_spritecollid(obj=self):
            coef = 1
            # по оси Oy
            while pygame.sprite.spritecollideany(obj, horizontal_borders):
                print(coef)

                obj.rect = obj.rect.move((0, coef))
                if pygame.sprite.spritecollideany(obj, horizontal_borders):
                    coef *= -1
                    obj.rect = obj.rect.move((0, coef))
                else:
                    continue

                obj.rect = obj.rect.move((0, coef))
                if pygame.sprite.spritecollideany(obj, horizontal_borders):
                    coef *= -1
                    obj.rect = obj.rect.move((0, coef))
                    coef += 1

            coef = 1
            # по оси Ox
            while pygame.sprite.spritecollideany(obj, vertical_borders):
                print(coef)
                obj.rect = obj.rect.move((coef, 0))
                if pygame.sprite.spritecollideany(obj, vertical_borders):
                    coef *= -1
                    obj.rect = obj.rect.move((coef, 0))
                else:
                    continue

                obj.rect = obj.rect.move((coef, 0))
                if pygame.sprite.spritecollideany(obj, vertical_borders):
                    coef *= -1
                    obj.rect = obj.rect.move((coef, 0))
                    coef += 1

        old_radius = self.radius
        for i in point_group:
            if pygame.sprite.collide_mask(self, i):
                self.radius += (i.rect.w // 4)
                self.score += (i.rect.w // 4)
                point_group.remove(i)
                all_sprites.remove(i)

                self.image = pygame.Surface(((2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2),
                                             (2 * self.radius) + (CONST['MOBBORDERWIDTH'] * 2)), pygame.SRCALPHA, 32)
                pygame.draw.circle(self.image, self.mob_color,
                                   (self.radius, self.radius), self.radius)
                pygame.draw.circle(self.image, pygame.Color('red'), (self.radius, self.radius), self.radius,
                                   CONST['MOBBORDERWIDTH'] - self.speed)

                self.rect.x, self.rect.y = self.rect.x - (self.radius - old_radius), \
                                           self.rect.y - (self.radius - old_radius)
                self.rect.w, self.rect.h = self.radius * 2, self.radius * 2
                self.mask = pygame.mask.from_surface(self.image)
                check_spritecollid()

        # координаты моба
        mob_coords = [set(map(lambda x: x, range(self.rect.x, self.rect.x + self.rect.w + 1))),
                      set(map(lambda y: y, range(self.rect.y, self.rect.y + self.rect.h + 1)))]
        # координаты ядра(зона смерти) игнрока, если оно попадет в моба - игрок проиграл
        player_loss_coords = [set(map(lambda x: x, range(player.rect.x + (player.radius // 2),
                                                         player.rect.x + player.rect.w - (player.radius // 2)))),
                              set(map(lambda y: y,
                                      range(player.rect.y + (player.radius // 2),
                                            player.rect.y + player.rect.h - (player.radius // 2))))]
        # координаты игрока
        player_coords = \
            [set(map(lambda x: x, range(player.rect.x, player.rect.x + player.rect.w + 1))),
             set(map(lambda y: y, range(player.rect.y, player.rect.y + player.rect.h + 1)))]
        # координаты ядра(зона смерти) моба, если оно попадет в игрока - моб проиграл
        mob_loss_coords = [set(map(lambda x: x, range(self.rect.x + (self.radius // 2),
                                                      self.rect.x + self.rect.w - (self.radius // 2)))),
                           set(map(lambda y: y,
                                   range(self.rect.y + (self.radius // 2),
                                         self.rect.y + self.rect.h - (self.radius // 2))))]

        # проверка на проигрыш игрока или моба
        if not player.loss and \
                player_loss_coords[0] & mob_coords[0] == player_loss_coords[0] and \
                player_loss_coords[1] & mob_coords[1] == player_loss_coords[1] and \
                pygame.sprite.collide_mask(player, self) and player.radius < self.radius:
            player.loss = True
        elif not player.loss and \
                mob_loss_coords[0] & player_coords[0] == mob_loss_coords[0] and \
                mob_loss_coords[1] & player_coords[1] == mob_loss_coords[1] and \
                pygame.sprite.collide_mask(self, player) and self.radius < player.radius:
            sound_eat.play()

            # если игрок съел моба, начисление очков игроку происходит постепенно, чтобы не выйти за пределы поля
            player.score += (self.rect.w // 6)
            for i in range(self.rect.w // 8):
                old_radius = player.radius
                player.radius += 1

                player.image = pygame.Surface(((2 * player.radius) + (CONST['MOBBORDERWIDTH'] * 2),
                                              (2 * player.radius) + (CONST['MOBBORDERWIDTH'] * 2)), pygame.SRCALPHA, 32)
                pygame.draw.circle(player.image, pygame.Color("white"), (player.radius, player.radius), player.radius)
                pygame.draw.circle(player.image, pygame.Color('green'), (player.radius, player.radius), player.radius,
                                   CONST['PLAYERBORDERWIDTH'] - player.speed)

                player.rect.x, player.rect.y = player.rect.x - (player.radius - old_radius), \
                    player.rect.y - (player.radius - old_radius)
                player.rect.w, player.rect.h = player.radius * 2, player.radius * 2
                player.mask = pygame.mask.from_surface(player.image)

                check_spritecollid(obj=player)

            mob_group.remove(self)
            all_sprites.remove(self)

    def update(self, player):

        self.mob_destination(player)

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

        self.point_collide(player)


def generate_field(player=None):
    global CONST
    if not player:
        Border(0, 0, CONST['SIZE_FIELD'] - 1, 0)
        Border(0, CONST['SIZE_FIELD'] - 1, CONST['SIZE_FIELD'] - 1, CONST['SIZE_FIELD'] - 1)
        Border(0, 0, 0, CONST['SIZE_FIELD'] - 1)
        Border(CONST['SIZE_FIELD'] - 1, 0, CONST['SIZE_FIELD'] - 1, CONST['SIZE_FIELD'] - 1)

        for i in range(CONST['POINTCOUNT']):
            Point()

        for i in range(CONST['MOBCOUNT']):
            Mob()

        player = Player()

        screen2 = pygame.Surface((CONST['SIZE_FIELD'], CONST['SIZE_FIELD']))

        return player, screen2
    else:
        player.radius //= 2
        player.image = pygame.Surface(((2 * player.radius) + (CONST['MOBBORDERWIDTH'] * 2),
                                       (2 * player.radius) + (CONST['MOBBORDERWIDTH'] * 2)), pygame.SRCALPHA, 32)
        pygame.draw.circle(player.image, pygame.Color("white"), (player.radius, player.radius), player.radius)
        pygame.draw.circle(player.image, pygame.Color('green'), (player.radius, player.radius), player.radius,
                           CONST['PLAYERBORDERWIDTH'] - player.speed)
        player.rect.x, player.rect.y = player.rect.x // 2, player.rect.y // 2
        player.rect.w, player.rect.h = player.radius * 2, player.radius * 2

        for i in horizontal_borders:
            i.rect.w //= 2

            i.rect.y, i.rect.x = i.rect.y // 2, i.rect.x // 2
            i.image = pygame.Surface([i.rect.w, 1])
            i.image.fill('red')
            CONST['SIZE_FIELD'] = i.rect.w

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
        CONST['RANGEPOINTRADIUS'] = (2 if CONST['RANGEPOINTRADIUS'][0] // 2 < 2 else CONST['RANGEPOINTRADIUS'][0] // 2,
                                     4 if CONST['RANGEPOINTRADIUS'][1] // 2 < 2 else CONST['RANGEPOINTRADIUS'][1] // 2)

        for i in mob_group:
            i.rect.y //= 2
            i.rect.x //= 2
            i.radius //= 2
            i.image = pygame.Surface(((2 * i.radius) + (CONST['MOBBORDERWIDTH'] * 2),
                                      (2 * i.radius) + (CONST['MOBBORDERWIDTH'] * 2)), pygame.SRCALPHA, 32)
            i.mob_color = 'white'
            pygame.draw.circle(i.image, i.mob_color, (i.radius, i.radius), i.radius)
            pygame.draw.circle(i.image, pygame.Color('red'), (i.radius, i.radius), i.radius,
                               CONST['MOBBORDERWIDTH'] - i.speed)
            i.rect.w, i.rect.h = i.radius * 2, i.radius * 2

        return player


def start_screen():
    global CONST
    intro_text = ['"ЭВОЛЮЦИЯ"',
                  "Правила игры:",
                  "-поедать микробов",
                  "-съесть врагов",
                  "-увеличивыться в размерах"]
    outro_text_win = ['Поздравляем!', '',
                      'Вы Прошли Игру.']
    outro_text_loss = ['Сожалеем!', '',
                       'Вы Проиграли.', '',
                       'Не отчаивайтесь и начните сначала,',
                       'зажав мышку или клавишу.']
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
            const_update()
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

        # процессы, возможные только при жизни игроке
        if player:
            # управление игроком
            if K_UP:
                pos[1] = player.speed * -1
            elif K_DOWN:
                pos[1] = player.speed * 1
            if K_LEFT:
                pos[0] = player.speed * -1
            elif K_RIGHT:
                pos[0] = player.speed * 1

            # изменение скорости у мобов, отлична от алгоритма расчета скорости для игрока
            for i in mob_group:
                if i.score // 100 > i.level:
                    i.level += 1
                    i.speed -= (1 if i.speed > 1 else 0)

            # изменение скорости, по соотношению с размером игрока, и масштаба
            if player.radius >= 200:
                new_level.play()
                player.speed -= (1 if player.speed > 1 else 0)
                CONST['MOBBORDERWIDTH'] -= (1 if player.speed > 1 else 0)
                CONST['SIZE_FIELD'] //= 2
                CONST['POINTCOUNT'] //= 3
                CONST['MOBTRIGGER'] //= 2
                player = generate_field(player=player)

            # спавн мобов на поле, если их количество меньше чем должно быть
            if len(mob_group.sprites()) < CONST['MOBCOUNT'] and \
                    random.choice(list(map(lambda x: 0, range(CONST['RATEMOB']))) + [1]):
                limited_pos = {'x': [], 'y': []}
                # расчет координат новых микробов учитывая положение камеры
                for i in vertical_borders:
                    limited_pos['x'].append(i.rect.x)
                for i in horizontal_borders:
                    limited_pos['y'].append(i.rect.y)

                m = Mob(limited_pos)

            # спавн микробов на поле, если их количество меньше чем должно быть
            if len(point_group.sprites()) < CONST['POINTCOUNT'] and \
                    random.choice(list(map(lambda x: 0, range(CONST['RATEPOINT']))) + [1]):
                limited_pos = {'x': [], 'y': []}
                # расчет координат новых микробов учитывая положение камеры
                for i in vertical_borders:
                    limited_pos['x'].append(i.rect.x)
                for i in horizontal_borders:
                    limited_pos['y'].append(i.rect.y)

                p = Point(limited_pos)

            # изменение ракурса камеры относительно игрока
            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            screen2.fill('black')

            # табол счета игрока
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

            # при выйгрыше или проигрыше
            if player.loss or player.rect.w >= CONST['SIZE_FIELD'] * 0.7:
                # нужно для корректной отрисовки экрана после смери игрока
                for i in all_sprites:
                    i.kill()

                screen.fill('black')
                screen2 = pygame.Surface(screen.get_size())
                screen2.fill('black')

                text = {'SCORE': 'yellow', str(player.score): 'white'}
                for line in text:
                    string_rendered = font.render(line, True, text[line])
                    intro_rect = string_rendered.get_rect()
                    intro_rect.y = 200
                    if text[line] == 'white':
                        intro_rect.x = (width // 2) - (intro_rect.w // 2) + 20
                    else:
                        intro_rect.x = (width // 2) - (intro_rect.w // 2) - 20
                    screen2.blit(string_rendered, intro_rect)

                font = pygame.font.Font(None, 40)
                text_coord = 30

                # алгоритм срабатывания звуков завершения игры
                if player.loss:
                    pygame.mixer.music.load("data/sounds/loss.ogg")
                    pygame.mixer.music.play(0)
                    outro_text = outro_text_loss
                elif not player.loss:
                    pygame.mixer.music.load("data/sounds/win.ogg")
                    pygame.mixer.music.play(0)
                    outro_text = outro_text_win

                for line in outro_text:
                    string_rendered = font.render(line, True, 'white')
                    intro_rect = string_rendered.get_rect()
                    text_coord += 10
                    intro_rect.top = text_coord
                    intro_rect.x = (width // 2) - (intro_rect.w // 2)
                    intro_rect.y += (height // 2) - 50 - 40 - 40
                    text_coord += intro_rect.height
                    screen2.blit(string_rendered, intro_rect)
                screen.blit(screen2, (0, 0))

                # удаляем игрока
                player = None

        all_sprites.draw(screen2)

        screen.blit(screen2, (0, 0))

        if player:
            player_group.update(pos)
            mob_group.update(player)

            # больший объект - сверху
            new_all_sprites = sorted(all_sprites.sprites(), key=lambda x: x.rect.w)
            for i in new_all_sprites:
                all_sprites.remove(i)
                all_sprites.add(i)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption('Evolution')
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)

    sound_point = pygame.mixer.Sound('data/sounds/point.ogg')
    sound_eat = pygame.mixer.Sound('data/sounds/eat.ogg')
    new_level = pygame.mixer.Sound('data/sounds/new_level.ogg')

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    mob_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    point_group = pygame.sprite.Group()

    start_screen()