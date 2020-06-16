import pygame
import random
import math
import os
import sys


def main():
    '''-------------------Initialization------------------------------------'''
    pygame.init()
    framerate = 60
    running = True
    rows = 10
    collums = 20
    max_number = 100
    tile_size = 50
    font_color1 = (100, 10, 100)
    font_color = (213, 147, 11)
    shadow_color = (100, 100, 100)
    clock = pygame.time.Clock()
    font_size = 15
    zero_point_x = 10
    zero_point_y = 100
    background_color = (88, 47, 104)
    block_size = 1
    tile_num = 5
    active_rule = [0]
    ulam = 0
    lucky = 0
    prime = 0
    round_time = 300
    max_score = 20
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('PUL Game')
    font = pygame.font.SysFont('Calibri', 24, True, False)
    font1 = pygame.font.SysFont('Calibri', 28, True, False)
    font1.set_italic(True)
    game_field = [[0 for j in range(rows)]
                  for i in range(collums)]
    folder = os.path.dirname(os.path.abspath(__file__))
    tfolder = folder + '/Textures'
    mfolder = folder + '/Backgrounds'
    cfolder = folder + '/Characters'
    bfolder = folder + '/Buttons'
    pygame.display.set_icon(pygame.image.load(folder + '/icon.png'))
    tile_types = []
    for i in range(1, tile_num+1):
        tile_types.append(pygame.transform.scale(
         pygame.image.load(tfolder + "/BigGrass" + str(i) + ".jpg"),
         (tile_size - 1, tile_size - 1)))

    '''-------------------------------afk--------------------------------'''
    class afk:
        def __init__(self):
            self.size = 75
            self.sprite = pygame.transform.scale(pygame.image.load(
                                                cfolder + '/CS.png'),
                                                (self.size, self.size))
            self.x = 500
            self.y = 160
            self.speedx = 2
            self.speedy = 2
            self.timer = 0
            self.time = 20
            self.bgcolor = (105, 155, 255)
            return None
    '''----------------------------Character--------------------------------'''
    class Character:
        def __init__(self, i, j, im_name):
            self.sprites = []
            self.i = i
            self.j = j
            self.active_sprite = 0
            self.desti = i
            self.destj = j
            self.x, self.y = GetCoord(i, j)
            self.moving = False
            self.num_sprites = 0
            self.direction = 1
            self.speed = 1
            self.ticks = 0
            self.delay = 10
            self.score = 0
            self.lifes = 3
            self.casting = False
            self.dying = False
            self.busy = False
            self.alive = True
            self.state_func = self.idle
            for i in range(9):
                im = pygame.image.load(cfolder + im_name + str(i) + '.png')
                im.set_alpha(None)
                im.set_colorkey((255, 255, 255))
                self.add_sprite(im)
            self.walking_sprites = 4
            return None
    
        def idle(self):
            self.x, self.y = GetCoord(self.i, self.j)
    
        def update(self):
            self.state_func()
            return None

        def move(self, di, dj):
            if (self.busy or di < 0 or dj < 0 or
               di >= collums or dj >= rows
               or not self.alive):
                return None
            self.state_func = self.step
            self.busy = True
            self.desti = di
            self.destj = dj
            self.ticks = 0
            if (self.i - di)*self.direction < 0:
                self.direction = -self.direction
            return None

        def step(self):
            if GetCoord(self.desti, self.destj) == (self.x, self.y):
                self.state_func = self.idle
                self.busy = False
                self.active_sprite = 0
                self.i = self.desti
                self.j = self.destj
                self.ticks = 0
            else:
                self.ticks += 1
                if self.ticks == self.delay:
                    self.ticks = 0
                    self.active_sprite += 1
                    if self.active_sprite >= self.walking_sprites - 1:
                        self.active_sprite = 1
                if self.j < self.destj:
                    self.y += self.speed
                elif self.j > self.destj:
                    self.y -= self.speed
                if self.i < self.desti:
                    self.x += self.speed
                elif self.i > self.desti:
                    self.x -= self.speed

        def spell(self):
            if self.alive:
                self.ticks += 1
                if self.ticks == 20:
                    self.state_func = self.idle
                    self.busy = False
                    self.active_sprite = 0

        def fall(self):
            self.ticks += 1
            if self.active_sprite == 8:
                if self.ticks == 30:
                    self.busy = False
                    self.state_func = self.idle
                    self.active_sprite = 0
                    if self.lifes == 0:
                        self.destroy()
                return None
            if self.ticks == 10:
                self.ticks = 0
                self.active_sprite += 1
            return None

        def add_sprite(self, sprite):
            self.sprites.append(sprite)
            self.num_sprites += 1

        def blit(self):
            if not self.alive:
                return None
            if self.direction == 1:
                screen.blit(self.sprites[self.active_sprite], (self.x, self.y))
            else:
                screen.blit(pygame.transform.flip(
                            self.sprites[self.active_sprite], True, False),
                            (self.x + 10, self.y))
            return None

        def cast_magic(self):
            if ((game_field[self.i][self.j] > 0) and
               not(self.busy) and self.alive):
                if CheckNumber(game_field[self.i][self.j]):
                    self.score += 1
                    game_field[self.i][self.j] = 0
                    self.ticks = 0
                    self.state_func = self.spell
                    self.busy = True
                    self.active_sprite = 5
                    active_rule[0] = random.randint(0, 2)
                else:
                    self.lifes -= 1
                    self.die()
            return None

        def die(self):
            self.active_sprite = 6
            self.ticks = 0
            self.state_func = self.fall
            self.busy = True

        def destroy(self):
            self.alive = False

        def reset(self, i, j):
            self.direction = 1
            self.speed = 1
            self.ticks = 0
            self.delay = 10
            self.score = 0
            self.lifes = 3
            self.state_func = self.idle
            self.casting = False
            self.dying = False
            self.busy = False
            self.alive = True
            self.i = i
            self.j = j
            self.x, self.y = GetCoord(i, j)
    '''-----------------------------Buttons---------------------------------'''
    class Button:
        def __init__(self, x, y, image, click_image, action):
            self.x = x
            self.y = y
            self.w = image.get_width()
            self.h = image.get_height()
            self.image = image
            self.click_image = click_image
            self.active_image = self.image
            self.pressed = False
            self.blit()
            self.action = action
            return None

        def is_pressed(self, pos):
            return ((self.x < pos[0])and(self.x + self.w > pos[0])and
                    (self.y < pos[1])and(self.y + self.h > pos[1]))

        def update(self, ev):
            if ev.type == pygame.QUIT:
                return 'Exit'
            if ev.type == pygame.MOUSEMOTION:
                if self.pressed:
                    if not self.is_pressed(ev.pos):
                        self.pressed = False
                        self.active_image = self.image
                        self.blit()
                else:
                    if self.is_pressed(ev.pos):
                        self.pressed = True
                        self.active_image = self.click_image
                        self.blit()
            if ev.type == pygame.MOUSEBUTTONDOWN and self.is_pressed(ev.pos):
                return self.action
            return 0

        def blit(self):
            screen.blit(self.active_image, (self.x, self.y))
    '''
    |-------------------------------------------------------------------------|
    |------------------------------Functions----------------------------------|
    |-------------------------------------------------------------------------|
    '''
    '''---------------------coordinates <=> indexes------------------------'''
    def GetCoord(i, j):
        '''
        (int,int) -> int, int
        Return coordinates of a tile in pixels
        '''
        x = zero_point_x + i * tile_size
        y = zero_point_y + j * tile_size
        return(x, y)

    def GetIndex(pos):
        '''
        (int, int) -> int, int
        Return i and j of a tile
        '''
        i = (pos[0] - zero_point_x) // tile_size
        j = (pos[1] - zero_point_y) // tile_size
        return(i, j)
    '''---------------------------Graphics----------------------------------'''
    def blit_number(i, j, number):
        '''
        (int, int, int) -> None
        Print number on the tile(i,j)
        '''
        if number == 0:
            return None
        if number > 99:
            delta = 13
        elif number > 9:
            delta = 5
        else:
            delta = 0
        x = zero_point_x + i * tile_size + (tile_size-font_size)//2 - delta
        y = zero_point_y + j * tile_size + (tile_size-font_size)//2 - 4
        num_image = font.render(str(number), True, font_color)
        num_shadow = font.render(str(number), True, shadow_color)
        screen.blit(num_shadow, (x+2, y+2))
        screen.blit(num_image, (x, y))
        return(None)
    '''--------------------------Events----------------------------------'''
    def OnMouseClick(ev):
        '''
        (event) -> None
        Process MOUSEBUTTONDOWN event
        '''
        afk.timer = 0
        assert(ev.type == pygame.MOUSEBUTTONDOWN)
        if ev.button != 1:
            return None
        return None

    def OnKeyDown(key):
        afk.timer = 0
        if key == 276:
            char2.move(char2.i - 1, char2.j)
        elif key == 275:
            char2.move(char2.i + 1, char2.j)
        elif key == 273:
            char2.move(char2.i, char2.j - 1)
        elif key == 274:
            char2.move(char2.i, char2.j + 1)
        elif key == 305:
            char2.cast_magic()
        elif key == 119:
            char1.move(char1.i, char1.j - 1)
        elif key == 97:
            char1.move(char1.i - 1, char1.j)
        elif key == 115:
            char1.move(char1.i, char1.j + 1)
        elif key == 100:
            char1.move(char1.i + 1, char1.j)
        elif key == 32:
            char1.cast_magic()
        return None

    '''------------------------------AFKLoop--------------------------------'''
    def afk_loop(afk):
        run = True
        while run:
            for ev in pygame.event.get():
                if ev.type in [
                    pygame.MOUSEBUTTONDOWN,
                    pygame.KEYDOWN,
                    pygame.MOUSEMOTION,
                ]:
                    run = False
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill(afk.bgcolor)
            afk.y += afk.speedy
            afk.x += afk.speedx
            if afk.y < 0:
                afk.speedy = -afk.speedy
            if afk.y > rows*tile_size+zero_point_y - afk.size + 10:
                afk.speedy = -2
            if afk.x < 0:
                afk.speedx = -afk.speedx
            if afk.x > collums*tile_size+2*zero_point_x - afk.size:
                afk.speedx = -3
                afk.y += 1
            screen.blit(afk.sprite, (afk.x, afk.y))
            pygame.display.flip()
            clock.tick(framerate)
        return None

    '''
    |-------------------------------------------------------------------------|
    |----------------------------Preparations---------------------------------|
    |-------------------------------------------------------------------------|
    '''

    '''-------------------Lucky Numbers Generation--------------------------'''
    lucky = [2*i - 1 for i in range(1, (max_number // 2) + 1)]
    for i in range(1, max_number // 10):
        mult = lucky[i]
        lucky_next = [j for j in lucky]
        end = True
        for j in range(1, len(lucky)):
            if (j + 1) % mult == 0:
                lucky_next.remove(lucky[j])
        lucky = []
        lucky = [j for j in lucky_next]
        lucky_number = [False for i in range(max_number + 1)]
        for i in lucky:
            lucky_number[i] = True

    def IsLucky(a):
        return lucky_number[a]
    '''-------------------Prime Numbers Generation--------------------------'''
    prime_number = [True for i in range(max_number+1)]
    for i in range(2, max_number):
        for j in range(2, (max_number//i) + 1):
            prime_number[i*j] = False

    def IsPrime(a):
        return prime_number[a]
    '''------------------Ulam Numbers Generation----------------------------'''
    ulam_number = [True for i in range(max_number)]
    for i in range(3, max_number):
        num_sum = 0
        for j in range(1, (i // 2) + 1):
            if ulam_number[j] and ulam_number[i - j] and(j != (i - j)):
                num_sum += 1
        if num_sum != 1:
            ulam_number[i] = False

    def IsUlam(a):
        return ulam_number[a]
    '''--------------------Checking Number----------------------------------'''
    def CheckNumber(a):
        if active_rule[0] == 0:
            return IsPrime(a)
        elif active_rule[0] == 1:
            return IsUlam(a)
        elif active_rule[0] == 2:
            return IsLucky(a)

    def ActiveRule(active_rule):
        if active_rule[0] == 0:
            return 'Prime numbers'
        elif active_rule[0] == 1:
            return "Ulam numbers"
        elif active_rule[0] == 2:
            return 'Lucky numbers'
    '''----------------------Game Field Generation--------------------------'''
    def GenerateField(game_field):
        for i in range(collums):
            for j in range(rows):
                a = random.randint(1, max_number)
                game_field[i][j] = a
    '''--------------------Background Creation------------------------------'''
    '''-------------------------Starting Menu-------------------------------'''
    def StartingMenu():
        menu = True
        screen = pygame.display.set_mode((800, 600))
        game_menu = pygame.image.load(mfolder + "/Game_Menu2.png")

        screen.blit(game_menu, (0, 0))
        B1player = Button(266, 404,
                          pygame.image.load(bfolder + '/1player.png'),
                          pygame.image.load(bfolder + '/1player_pressed.png'),
                          '1player')
        B2player = Button(266, 486,
                          pygame.image.load(bfolder + '/2player.png'),
                          pygame.image.load(bfolder + '/2player_pressed.png'),
                          '2player')
        Bexit = Button(22, 19, pygame.image.load(bfolder + '/exit.png'),
                       pygame.image.load(bfolder + '/exit_pressed.png'),
                       'exit')
        Babout = Button(685, 19, pygame.image.load(bfolder + '/about.png'),
                        pygame.image.load(bfolder + '/about_pressed.png'),
                        'about')
        while menu:
            res = 0
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return 'exit'
                a = B1player.update(ev)
                if a:
                    res = a
                a = B2player.update(ev)
                if a:
                    res = a
                a = Bexit.update(ev)
                if a:
                    res = a
                a = Babout.update(ev)
                if a:
                    res = a
                if res != 0:
                    return res
            pygame.display.flip()
        return 0

    '''---------------------------About menu-------------------------------'''
    def About():
        about_text = [pygame.image.load(mfolder + '/text1.png')]
        about_text.append(pygame.image.load(mfolder + '/text2.png'))
        active_text = 0
        screen.blit(pygame.image.load(mfolder + '/About_menu.png'), (0, 0))
        Bback = Button(340, 467, pygame.image.load(bfolder + '/back.png'),
                       pygame.image.load(bfolder + '/back_pressed.png'),
                       'menu')
        Bprev = Button(76, 467, pygame.transform.flip(
                       pygame.image.load(bfolder + '/arrow.png'),
                       True, False),
                       pygame.transform.flip(
                       pygame.image.load(bfolder + '/arrow_pressed.png'),
                       True, False), 'prev')
        Bnext = Button(682, 467, pygame.image.load(bfolder + '/arrow.png'),
                       pygame.image.load(bfolder + '/arrow_pressed.png'),
                       'next')
        res = 0
        screen.blit(about_text[active_text], (104, 62))
        while res == 0:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return 'exit'
                res = Bback.update(ev)
                if res:
                    return res
                res = Bprev.update(ev)
                if res == 'prev':
                    active_text = 0
                res = Bnext.update(ev)
                if res == 'next':
                    active_text = 1
            res = 0
            screen.blit(about_text[active_text], (100, 61))
            pygame.display.flip()
        return res

    '''-----------------------Game over menu--------------------------------'''
    def GameOver(multiplayer, victory):
        screen = pygame.display.set_mode((800, 600))
        if victory:
            screen.blit(pygame.image.load(mfolder + '/Victory.png'), (0, 0))
            Brestart = Button(266, 486,
                              pygame.image.load(bfolder +
                                                '/restart.png'),
                              pygame.image.load(bfolder +
                                                '/restart_pressed.png'),
                              'restart')
            Bmenu = Button(265, 403, pygame.image.load(bfolder + '/menu.png'),
                           pygame.image.load(bfolder + '/menu_pressed.png'),
                           'menu')
        else:
            screen.blit(pygame.image.load(mfolder + '/Defeat.png'), (0, 0))
            Bmenu = Button(265, 403,
                           pygame.image.load(bfolder + '/defmenu.png'),
                           pygame.image.load(bfolder + '/defmenu_pressed.png'),
                           'menu')
            Brestart = Button(265, 486, pygame.image.load(bfolder +
                              '/restart1.png'),
                              pygame.image.load(bfolder +
                              '/restart1_pressed.png'),
                              'restart')
        Bexit = Button(22, 19, pygame.image.load(bfolder + '/exit.png'),
                       pygame.image.load(bfolder + '/exit_pressed.png'),
                       'exit')
        res = 0
        while res == 0:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return 'exit'
                a = Bmenu.update(ev)
                if a != 0:
                    res = a
                a = Bexit.update(ev)
                if a != 0:
                    res = a
                a = Brestart.update(ev)
                if a != 0:
                    res = a
            pygame.display.flip()
        if res == 'restart':
            if multiplayer:
                return '2player'
            else:
                return '1player'
        return res

    '''---------------------------Pause-------------------------------------'''
    def Pause(multiplayer):
        x = collums*tile_size//2
        pause_menu = pygame.image.load(mfolder + '/pause_menu.png')
        screen.blit(pause_menu, (x - 201, 132))
        Bmenu = Button(x - 140, 200, pygame.image.load(bfolder + '/menu.png'),
                       pygame.image.load(bfolder + '/menu_pressed.png'),
                       'menu')
        Bres = Button(x - 140, 282,
                      pygame.image.load(bfolder + '/restart.png'),
                      pygame.image.load(bfolder + '/restart_pressed.png'),
                      'restart')
        Bback = Button(x - 140, 364,
                       pygame.image.load(bfolder + '/resume.png'),
                       pygame.image.load(bfolder + '/resume_pressed.png'),
                       'back')
        res = 0
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return 'exit'
                res = Bmenu.update(ev)
                if res:
                    return res
                res = Bres.update(ev)
                if res == 'restart':
                    if multiplayer:
                        return '2player'
                    else:
                        return '1player'
                res = Bback.update(ev)
                if res == 'back':
                    return 0
                pygame.display.flip()
    '''
    |-------------------------------------------------------------------------|
    |-----------------------------Gameplay------------------------------------|
    |-------------------------------------------------------------------------|
    '''
    def Game(multiplayer):
        timer = pygame.time.Clock()
        time = 0
        res = 0
        round_time = 300
        max_score = 20
        screen = pygame.display.set_mode((collums*tile_size+2*zero_point_x,
                                          rows*tile_size+zero_point_y+10))
        Bmenu = Button(collums*tile_size - 100, 20,
                       pygame.image.load(bfolder + '/Pause.png'),
                       pygame.image.load(bfolder + '/Pause_pressed.png'),
                       'pause')
        GenerateField(game_field)
        char1.reset(0, 0)
        char1.direction = -1
        char2.reset(collums - 1, rows - 1)
        if not multiplayer:
            char2.alive = False
        tile = [
                [tile_types[game_field[i][j] % tile_num]
                 for j in range(rows)]
                for i in range(collums)]
        background = pygame.Surface((collums*tile_size+2*zero_point_x,
                                    rows*tile_size+zero_point_y+10))
        background.fill(background_color)
        background.blit(pygame.image.load(mfolder + '/score_board.png'),
                        (0, 0))
        for i in range(collums):
            for j in range(rows):
                if (i % block_size == 0)and (j % block_size == 0):
                    background.blit(tile[i][j], GetCoord(i, j))
        running = True
        char1.active_sprite = char1.num_sprites
        screen.blit(background, (0, 0))
        char1.blit()
        pygame.display.flip()
        timer.tick(1)
        screen.blit(background, (0, 0))
        char1.active_sprite = 0
        char1.blit()
        pygame.display.flip()
        while running:
            screen.blit(background, (0, 0))
            Bmenu.blit()
            for ev in pygame.event.get():
                res = Bmenu.update(ev)
                if ev.type == pygame.QUIT:
                    return 'exit'
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if res:
                        time += timer.tick()
                        res = Pause(multiplayer)
                        if res:
                            return res
                        timer.tick()
                elif ev.type == pygame.KEYDOWN:
                    OnKeyDown(ev.key)
            if (afk.timer // framerate) >= afk.time:
                time += timer.tick()
                afk_loop(afk)
                timer.tick()
                afk.timer = 0
            afk.timer += 1
            for i in range(collums):
                for j in range(rows):
                    if (i % block_size == 0)and (j % block_size == 0):
                        blit_number(i, j, game_field[i][j])
        # Top menu
            screen.blit(font1.render(ActiveRule(active_rule),
                                     True, (font_color)),
                        (12, 11))
            screen.blit(font1.render(str(char1.score),
                                     True, (font_color)), (300, 16))
            screen.blit(font1.render(str(char1.lifes),
                                     True, (font_color)), (460, 16))
            secs = round_time - time//1000
            mins = secs//60
            secs -= mins * 60
            screen.blit(font1.render(str(mins) + ':' +
                        ('00' if secs == 0 else str(secs)),
                                    True, (font_color)), (600, 30))
            if not multiplayer and char1.score >= max_score:
                screen.blit(font.render('Victory!', True, (shadow_color)),
                            (13, 51))
                screen.blit(font.render('Victory!', True, (font_color)),
                            (12, 50))
            if multiplayer:
                screen.blit(font1.render(str(char2.lifes),
                                         True, (font_color)), (460, 40))
                screen.blit(font1.render(str(char2.score),
                                         True, (font_color)), (300, 40))
            char1.update()
            char1.blit()
            char2.update()
            char2.blit()
            pygame.display.flip()
            clock.tick(framerate)
            time += timer.tick()
            if multiplayer:
                if not(char1.alive or char2.alive) or(mins + secs <= 0):
                    if char1.score >= char2.score:
                        return GameOver(multiplayer, True)
                    return GameOver(multiplayer, False)
            else:
                if (not char1.alive)or (mins + secs <= 0):
                    if char1.score >= max_score:
                        return GameOver(multiplayer, True)
                    else:
                        return GameOver(multiplayer, False)
        return 'menu'
    '''
    |=============================Main Loop===================================|
    '''
    afk = afk()
    char1 = Character(0, 0, "/Char")
    char1.add_sprite(pygame.image.load(cfolder+'/Cured.png'))
    char1.num_sprites -= 1
    char2 = Character(collums - 1, rows - 1, "/NChar")
    res = 'menu'
    while res != 'exit':
        if res == 'menu':
            res = StartingMenu()
        elif res == '2player':
            res = Game(True)
        elif res == 'about':
            res = About()
        elif res == '1player':
            res = Game(False)
    pygame.quit()


if __name__ == "__main__":
    main()
