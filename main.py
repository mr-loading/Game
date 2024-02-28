import pygame.display
from pygame import *
from random import randint

win_width = 700
win_height = 500
score = 0
score_life = 50


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.update(0, 0, 70, 70)
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    bullets = sprite.Group()

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 35, self.rect.y ,10,10, 20)
        self.bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self .rect.y < 0:
            self.kill()


monsters = sprite.Group()


class Enemy(GameSprite):
    side = "left"

    def update(self):
        global score_life
        self.rect.y += self.speed
        if self.rect.x <= 0:
            self.side = "right"
        if self.rect.x >= win_width - 80:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed + 5
        else:
            self.rect.x += self.speed + 5
        if self.rect.y > win_height:
            self.rect.y = 0
            score_life -= 10




class Enemy_big(GameSprite):
    side = "left"

    def update(self):
        if self.rect.x <= 0:
            self.side = "right"
        if self.rect.x >= win_width:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

    bullets_enemy = sprite.Group

    def fire_enemy(self):
        bullet = Bullet_enemy('bullet.png', self.rect.x + 45, self.rect.y, 20, 20, 8)
        self.bullets_enemy.add(bullet)


class Bullet_enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.kill()


for i in range(1, 6):
    enemy = Enemy('ufo.png', randint(0, win_width - 80), 0, 80, 80, 5)
    while sprite.spritecollide(enemy, monsters, False):
        enemy = Enemy('ufo.png', randint(0, win_width - 80), 0, 80, 80, 5)
    monsters.add(enemy)


font.init()
font = font.Font(None, 36)
rocket = Player('rocket.png', 5, 400, 80, 80, 20)
boss = Enemy_big('ufo.png', win_width - 350, win_height - 300, 100, 100, 5)
display.set_caption("Ракета")
window = display.set_mode((win_width, win_height))
background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), (win_width, win_height))
window.blit(background, (0, 0))


finish = False
# игровой цикл
run = True
while run:
    # цикл срабатывает каждую 0.05 секунд
    pygame.time.delay(50)
    window.blit(background, (0, 0))

    # событие нажатия на кнопку “закрыть”
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            run = finish

        elif e. type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    # проверка, что игра еще не завершена
    if not finish:
        # обновляем фон каждую итерацию
        window.blit(background, (0, 0))

        rocket.reset()
        rocket.update()

        rocket.bullets.update()
        rocket.bullets.draw(window)

        monsters.update()
        monsters.draw(window)

        text = font.render("Счёт: " + str(score), True, (255, 255, 255))
        text2 = font.render("Осталось жизней: " + str(score_life), True, (255, 255, 255))

        window.blit(text, (10, 20))
        window.blit(text2, (10, 50))

        collides_bullets = sprite.groupcollide(monsters, Player.bullets, True, True)
        for c in collides_bullets:
            enemy = Enemy('ufo.png', randint(0, win_width - 80), 0, 80, 80, 5)
            while sprite.spritecollide(enemy, monsters, False):
                enemy = Enemy('ufo.png', randint(0, win_width - 80), 0, 80, 80, 5)

            monsters.add(enemy)
            score += 1

        collides_rocket_monsters = sprite.spritecollide(rocket, monsters, True)
        for n in collides_rocket_monsters:
            enemy = Enemy('ufo.png', randint(0, win_width - 80), 0, 80, 80, 5)
            while sprite.spritecollide(enemy, monsters, True):
                enemy = Enemy('ufo.png', randint(0, win_width - 80), 0, 80, 80, 5)

            monsters.add(enemy)
            score_life -= 10

        display.update()
        if score_life == 0:
            finish = True
            img = image.load('game-over.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))
            display.update()
        # if score == 10:
        #     boss.reset()
        #     boss.update()
        #     boss.bullets_enemy.update()
        #     boss.bullets_enemy.draw(window)
        elif score == 100:
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            display.update()

