from pygame import *
from random import randint
lost = 0
font.init()
font1 = font.Font(None,80)
lose = font1.render("YOU LOSE!", True,(180,0,0))
win = font1.render('YOU WIN!', True,(110,0,0))

font2 = font.Font(None, 36)
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_monster = "ufo.png"
img_bullet = "bullet.png"
win_width = 700
win_height = 500 
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
img=image.load(img_back)
background = transform.scale(img,(win_width, win_height))
bullets = sprite.Group()
score = 0

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self): 
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 88:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

            

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
    def draw(self, window):
        window.blit(self.image, self.rect)

class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y<0:
            self.kill()








ship = Player(img_hero, win_width//2, win_height-100, 80, 100, 10)
monsters = sprite.Group()
for i in range (1,6):
    monster = Enemy(img_monster, 5, randint(80, win_width - 80), 60, 80,  randint(1, 5))
    monsters.add(monster)


finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type ==KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()

    if not finish:
        window.blit(background,(0,0))
        text = font2.render('Пропущено:'+ str(lost), 1,(255, 255, 255))
        window.blit(text, (50, 50))
        text2 = font2.render("Счет:"+str(score), 1, (255,255,255))
        window.blit(text2,(50,80))
        ship.update()

        monsters.update()
        ship.reset()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for i in collides:
            score = score + 1
            monster = Enemy(img_monster, 5, randint(80, win_width - 80), 60, 80,  randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False)or lost>= 5:
            finish=True
            window.blit(lose,(200,200))
        if score>= 10:
            finish = True
            window.blit(win,(200,200))
    display.update()
    time.delay(20)












