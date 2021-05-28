import pygame
from network import Network
import os
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
global playerName

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        try:
            self.icon = pygame.image.load(os.path.join('images', self.text + '.png'))
        except:
            pass
    def draw(self, win,AllowText):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height),3)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        if AllowText:
            win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),self.y + round(self.height / 2) - round(text.get_height() / 2)))
        else:
            win.blit(self.icon, (self.x + round(self.width/2) - round(self.icon.get_width()/2), self.y + round(self.height/2) - round(self.icon.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Aguardando Jogador...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Sua jogada", 1, (0, 255,255))
        win.blit(text, (60, 200))

        text = font.render("Jogada do Oponente", 1, (0, 255, 255))
        win.blit(text, (340, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        name1 = font.render(game.names[0], 1, (0, 0, 0))
        name2 = font.render(game.names[1], 1, (0, 0, 0))

        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Pronto!", 1, (0, 0, 0))
            else:
                text1 = font.render("Aguardando...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Pronto!", 1, (0, 0, 0))
            else:
                text2 = font.render("Aguardando...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (60, 350))
            win.blit(text1, (390, 350))
            win.blit(name2,(60,50))
            win.blit(name1,(390,50))
        else:
            win.blit(text1, (60, 350))
            win.blit(text2, (390, 350))
            win.blit(name1, (60, 50))
            win.blit(name2, (390, 50))
        for btn in btns:
            btn.draw(win,False)

    pygame.display.update()


btns = [Button("Pedra", 50, 500, (0,0,0)),
        Button("Papel", 250, 500, (255,255,255)),
        Button("Tesoura", 450, 500, (0,255,0))]
def main():
    global playerName
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())

    print("Você é o jogador", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("O jogo não pode ser criado")
            break
        game = n.send(playerName + '/')
        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("O jogo não pode ser criado")
                break

            font = pygame.font.Font('Qabil.otf', 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Ganhou!", 1, (0,255,0))
            elif game.winner() == -1:
                text = font.render("Empate!", 1, (255,255,255))
            else:
                text = font.render("Perdeu...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2 - 40))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    global playerName
    run = True
    clock = pygame.time.Clock()
    textinput = InputBox(300,300,200,27)
    start = Button("jogar!",300,350,(0,0,0))
    font = pygame.font.Font('Qabil.otf', 60)
    font2 = pygame.font.SysFont("comicsans",40)
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        text = font.render("Pedra, Papel e tesoura", 1, (255,255,255))
        subtitle = font.render("Online!", 1, (255,255,255))
        text2 = font2.render("Digite seu nome:",1,(255,255,255))
        win.blit(text, (100,100))
        win.blit(subtitle,(250,150))
        win.blit(text2,(70,300))
        start.draw(win,True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start.click(pos):
                    run = False
                    if textinput.text != '':
                        playerName = textinput.text
                    else:
                        playerName = 'Anônimo'
            textinput.handle_event(event)
        textinput.update()
        textinput.draw(win)
        pygame.display.update()
    main()

while True:
    menu_screen()