import pygame, sys
import os

pygame.init()
size = WIDTH, HEIGHT = 800, 800
tile_width = tile_height = 25
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('green'))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
inwiz_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
int_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
grib_group = pygame.sprite.Group()
flash_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
GRAV = [1]
DASH = 10
REVIVE = 10
ROKY = 15


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def obstacle(self, obj1, *obj2):
        for i in obj2:
            sp = pygame.sprite.spritecollide(obj1, i, False)
            if len(sp) != 0:
                return True
        return False

    def gravity(self, grav=False):
        # for i in range(3):
        #     self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1] + GRAV[0]
        #     if self.obsFtacle(self, wall_group):
        #         self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1] - GRAV[0]
        #         break
        # if grav:
        #     GRAV[0] = GRAV[0] * -1
        #     self.flip(0, 1)
        if grav and GUMP[0] == 0:
            GRAV[0] = GRAV[0] * -1
            GUMP[0] = 1
            self.flip(0, 1)
        for i in range(3):
            self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1] + GRAV[0]
            if self.obstacle(self, wall_group):
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1] - GRAV[0]
                GUMP[0] = 0
                if self.obstacle(self, enemy_group) and self.damage and HP[0] < 3:
                    HP[0] += 1
                    self.damage = False
                    pygame.time.set_timer(REVIVE, 1000)
                if grav:
                    GRAV[0] = GRAV[0] * -1
                    GUMP[0] = 1
                    self.flip(0, 1)
                break

    def flip(self, vect1, vect2):
        self.image = pygame.transform.flip(self.image, vect1, vect2)



class Finish(GameObject):
    def __init__(self, pos_x, pos_y, size):
        self.image = pygame.Surface(size)
        self.image.fill([0, 0, 255])
        super().__init__(self.image, pos_x, pos_y)
        finish_group.add(self)


class Tile(GameObject):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_images[tile_type], pos_x, pos_y)
        if tile_type != 'zone':
            tiles_group.add(self)
        if tile_type in ['wall', 'box']:
            wall_group.add(self)
        elif tile_type == 'zone':
            inwiz_group.add(self)


class Enemy(GameObject):
    def __init__(self, npc_type, pos_x, pos_y, log):
        super().__init__(npc_images[npc_type], pos_x, pos_y)
        self.vect = 3
        self.log = log
        self.roky = []
        enemy_group.add(self)
        if self.log[0] == 'z':
            self.vect_x = self.log[1]
            self.vect_y = self.log[2]
            self.roky.append(Rocket('roky', self.rect.x, self.rect.y, self.vect_x, self.vect_y))
            pygame.time.set_timer(ROKY, 2000)
        if self.log == 'm':
            wall_group.add(self)

    def update(self):
        if COM[0]:
            if self.log[0] == 'z':
                self.roky.append(Rocket('roky', self.rect.x, self.rect.y, self.vect_x, self.vect_y))
            return None
        if self.log == 'x':
            self.alf = self.rect.topleft
            self.rect.topleft = self.rect.topleft[0] + self.vect, self.rect.topleft[1]
            if self.obstacle(self, inwiz_group) or self.obstacle(self, wall_group):
                self.rect.topleft = self.alf
                self.vect *= -1
        elif self.log == 'y':
            self.alf = self.rect.topleft
            self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1] + self.vect
            if self.obstacle(self, inwiz_group) or self.obstacle(self, wall_group):
                self.rect.topleft = self.alf
                self.vect *= -1
        elif self.log[0] == 'z':
            for i in self.roky:
                i.update()


class Rocket(GameObject):
    def __init__(self, npc_type, pos_x, pos_y, x, y):
        super().__init__(npc_images[npc_type], pos_x // 25, pos_y // 25)
        self.vect = 1
        self.x = x * self.vect
        self.y = y * self.vect
        enemy_group.add(self)

    def update(self):
        self.rect.topleft = self.rect.topleft[0] + self.x, self.rect.topleft[1] + self.y
        if self.rect.x not in range(0, WIDTH + 1) or self.rect.y not in range(0, HEIGHT + 1) or \
                self.obstacle(self, wall_group):
            enemy_group.remove(self)



class Item(GameObject):
    def __init__(self, item_type, pos_x, pos_y):
        super().__init__(item_images[item_type], pos_x, pos_y)
        item_group.add(self)
        if item_type == 'grib':
            grib_group.add(self)
        if item_type == 'flash':
            flash_group.add(self)


class Player(GameObject):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_image, pos_x, pos_y)
        self.iter = 0
        self.damage = True
        player_group.add(self)

    def update(self, com=0):
        self.alf = self.rect.topleft
        if com == 'damage':
            self.damage = True
        elif com == 1:
            self.rect.topleft = self.rect.topleft[0] - 3, self.rect.topleft[1]
        elif com == 2:
            self.rect.topleft = self.rect.topleft[0] + 3, self.rect.topleft[1]
        if self.obstacle(self, enemy_group) and self.damage and HP[0] < 3:
            HP[0] += 1
            self.damage = False
            pygame.time.set_timer(REVIVE, 1000)
        if self.obstacle(self, wall_group):
            self.rect.topleft = self.alf
        if self.obstacle(self, grib_group) and HP[0] > 0:
            pygame.sprite.spritecollide(self, grib_group, True)
            HP[0] -= 1
        if self.obstacle(self, flash_group):
            DASH[0] = True
        if self.obstacle(self, finish_group):
            fin[0] = True

    def l_dash(self):
        self.iter += 1
        for i in range(6):
            self.rect.topleft = self.rect.topleft[0] - 1, self.rect.topleft[1]
            if self.obstacle(self, wall_group) or self.iter == 30:
                self.iter = 0
                self.rect.topleft = self.rect.topleft[0] + 1, self.rect.topleft[1]
                DASH[0] = False
                return False
        return True

    def r_dash(self):
        self.iter += 1
        for i in range(6):
            self.rect.topleft = self.rect.topleft[0] + 1, self.rect.topleft[1]
            if self.obstacle(self, wall_group) or self.iter == 30:
                self.iter = 0
                self.rect.topleft = self.rect.topleft[0] - 1, self.rect.topleft[1]
                DASH[0] = False
                return False
        return True


class InterFace(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(int_group)
        self.image = int_images[type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        int_group.add(self)

    def update(self, com):
        if com == 'death':
            self.image = int_images[com]
        elif com == 'life':
            self.image = int_images[com]


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target1, target2):
        self.dx = -(target1.rect.x + target1.rect.w // 2 - WIDTH // 2)
        self.dy = -(target2.rect.y + target2.rect.h // 2 - HEIGHT // 2)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if colorkey == -2:
        image = pygame.image.load(fullname).convert_alpha()
    else:
        image = pygame.image.load(fullname).convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    return image


def generate_level(level):
    new_player, ghost, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '^':
                Tile('box', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '%':
                Enemy('mob', x, y, 'x')
            elif level[y][x] == 'M':
                Enemy('mob', x, y, 'm')
            elif level[y][x] == 'L':
                Enemy('rocket', x, y, ('z', -1, 0))
            elif level[y][x] == 'U':
                Enemy('rocket', x, y, ('z', 0, -1))
            elif level[y][x] == 'R':
                Enemy('rocket', x, y, ('z', 1, 0))
            elif level[y][x] == 'D':
                Enemy('rocket', x, y, ('z', 0, 1))
            elif level[y][x] == '*':
                Enemy('bird', x, y, 'y')
            elif level[y][x] == '№':
                ghost = Ghost('ghost', x, y)
            elif level[y][x] == '$':
                Tile('zone', x, y)
            elif level[y][x] == 'F':
                Finish(x, y, (25, 50))
            elif level[y][x] == '&':
                Item('grib', x, y)
            elif level[y][x] == '=':
                Item('flash', x, y)
    return new_player, ghost, x, y


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(text):
    intro_text = text
    fon = pygame.transform.scale(load_image('box.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


start_screen(['START', 'CLICK TO PLAY'])
camera = Camera()
tile_images = {'wall': pygame.transform.scale(load_image('plot.png'), (50, 25)),
               'box': pygame.transform.scale(load_image('box.png'), (25, 25)),
               'zone': pygame.transform.scale(load_image('zone.png', -1), (25, 25))}
npc_images = {'mob': pygame.transform.scale(load_image('mob.png', -1), (25, 25)),
              'bird': pygame.transform.scale(load_image('mob.png', -1), (25, 25)),
              'rocket': pygame.transform.scale(load_image('mob.png', -1), (25, 25)),
              'roky': pygame.transform.scale(load_image('ball.jpg', -1), (25, 25)),
              'ghost': pygame.transform.scale(load_image('zone.png', -1), (25, 25))}
int_images = {'life': pygame.transform.scale(load_image('life.png', -1), (50, 50)),
              'death': pygame.transform.scale(load_image('dead.png', -1), (50, 50))}
item_images = {'grib': pygame.transform.scale(load_image('grib.png', -1), (25, 25)),
               'flash': pygame.transform.scale(load_image('grass.png', -1), (25, 25))}
player_image = pygame.transform.scale(load_image('boy.jpg', -1), (25, 50))

maps = os.listdir(os.getcwd() + '/data')
print('choose the map:')
for i in maps:
    if i[i.find('.'):] == '.txt':
        print(i[:i.find('.')])
map0 = load_level(input() + '.txt')
player, ghost, level_x, level_y = generate_level(map0)
op = False
fin = [False]
fail = [False]
left = False
right = False
l_dash = False
r_dash = False
l_vect = False
r_vect = False
DASH = [False]
HP = [0]
GUMP = [0]
COM = [False]
flip = 0
# for i, j, siz in [(-50, 0, (10, 500)), (0, -50, (500, 10)), (WIDTH, 0, (10, 500)), (0, HEIGHT, (500, 10))]:
#     Border(i, j, siz)
for i in [0, 3, 6]:
    InterFace('life', i, 0)
while True:
    grav = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if fail[0] == 1 or fin[0] == 1:
            if event.type == pygame.MOUSEBUTTONDOWN or \
                    event.type == pygame.KEYDOWN:
                terminate()
            continue
        if event.type == REVIVE:
            pygame.time.set_timer(REVIVE, 0)
            player.update('damage')
        if event.type == ROKY:
            COM[0] = True
            for en in enemy_group:
                en.update()
            COM[0] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            op = True
        if event.type == pygame.KEYDOWN:
            op = True
            if event.key == pygame.K_LEFT:
                left = True
                l_vect = True
                r_vect = False
                if flip == 0:
                    player.flip(1, 0)
                    flip = 1
            elif event.key == pygame.K_RIGHT:
                right = True
                r_vect = True
                l_vect = False
                if flip == 1:
                    player.flip(1, 0)
                    flip = 0
            elif event.key == pygame.K_SPACE:
                grav = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            elif event.key == pygame.K_RIGHT:
                right = False

    if left and not l_dash and not r_dash:
        player.update(1)
    if right and not l_dash and not r_dash:
        player.update(2)
    if l_vect:
        if DASH[0]:
            l_dash = True
            r_dash = False
    if r_vect:
        if DASH[0]:
            r_dash = True
            l_dash = False
    if l_dash:
        l_dash = player.l_dash()
        if flip == 0:
            player.flip(1, 0)
            flip = 1
    if r_dash:
        r_dash = player.r_dash()
        if flip == 1:
            player.flip(1, 0)
            flip = 0
    player.gravity(grav)
    player.update()
    for en in enemy_group:
        en.update()
    if op:
        for i, j in enumerate(int_group):
            if int(i) + 1 <= HP[0]:
                j.update('death')
            else:
                j.update('life')
        camera.update(player, player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill(pygame.Color('green'))
        tiles_group.draw(screen)
        enemy_group.draw(screen)
        item_group.draw(screen)
        player_group.draw(screen)
        finish_group.draw(screen)
        int_group.draw(screen)
        if HP[0] == 3:
            start_screen(['GAME OVER', 'CLICK TO ESCAPE'])
            fail[0] = 1
            op = False
            HP[0] = 0
        if fin[0] == True:
            start_screen(['WIN', 'CLICK TO ESCAPE'])
            op = False
            fin[0] = 1

    pygame.display.flip()
    clock.tick(60)
