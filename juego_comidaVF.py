import pygame
import random
import sys

screen_size = (500, 670)
negro = (0, 0, 0)
blanco = (255, 255, 255)

class Comida(pygame.sprite.Sprite):
    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo
        
        if tipo == "nacho":
            self.image = pygame.image.load("nacho.png").convert()

        elif tipo == "pancho":
            self.image = pygame.image.load("pancho.png").convert()
        
        elif tipo == "hamburguesa":
            self.image = pygame.image.load("amburgecha.png").convert()
        
        elif tipo == "bebida":
            self.image = pygame.image.load("bebida.png").convert()
        
        elif tipo == "bomba":
            self.image = pygame.image.load("bomba.png").convert()
        
        else:
            raise ValueError("Tipo de comida no válido")
        
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()



    def update(self):
        self.velocidad = 1.6
        self.rect.y += self.velocidad
        if self.rect.y > screen_size[1]:
            self.kill()
    



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pou_xD.png").convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()    
        self.rect.x = mouse_pos[0]
        self.rect.y = 550
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 410:
            self.rect.x = 410
    

class Juego(object):
    def __init__(self):
        self.reiniciar_juego()
        self.fondo = pygame.image.load("fondo_juego_comida.png").convert()
        self.fuente_score = pygame.font.SysFont("comic sans", 50)

        self.fuente_rein_esc = pygame.font.SysFont("comic sans", 20)

        pygame.mixer.music.load("nice_sprites.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        self.sonido_comer = pygame.mixer.Sound("sonido_comer.mp3")
        self.sonido_bomba = pygame.mixer.Sound("bomba.mp3")

        self.musica_sonando = True

        self.silenciar = pygame.Rect(50, 50, 100, 100)

    def reiniciar_juego(self):
        self.score = 0
        self.done = False

        try:
            if self.done == False:
                pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(e)

        self.lista_comida = pygame.sprite.Group()
        self.todos_sprite = pygame.sprite.Group()
        self.tipos_comida = ["nacho", "pancho", "hamburguesa", "bebida", "bomba"]

        for i in range(100):
            tipo = random.choice(self.tipos_comida)
            comida = Comida(tipo)
            comida.rect.x = random.randrange(30, 470)
            comida.rect.y = random.randrange(-7000, 10)

            self.lista_comida.add(comida)
            self.todos_sprite.add(comida)

        self.poe = Player()
        self.todos_sprite.add(self.poe)



    def procesar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN:
                if self.done: 
                    pygame.mixer.music.stop()
                    if event.key == pygame.K_r:
                        self.reiniciar_juego()
                    elif event.key == pygame.K_ESCAPE:
                        import menu_inicio_poe
                        menu_inicio_poe.main()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.silenciar.collidepoint(pygame.mouse.get_pos()):
                    if self.musica_sonando:
                        pygame.mixer.music.pause()  
                        pygame.mixer.music.set_volume(0)  
                        self.sonido_comer.set_volume(0)  
                        self.sonido_bomba.set_volume(0)  
                        self.musica_sonando = False
                    else:
                        pygame.mixer.music.unpause()  
                        pygame.mixer.music.set_volume(0.5)  
                        self.sonido_comer.set_volume(1)  
                        self.sonido_bomba.set_volume(1)  
                        self.musica_sonando = True

        return False
        
        
    def logica(self):
        self.todos_sprite.update()

        colision_comida = pygame.sprite.spritecollide(self.poe, self.lista_comida, True)
        for comida in colision_comida:
            if comida.tipo in self.tipos_comida[:4]:
                self.score += 1
                self.sonido_comer.play()

            elif comida.tipo == self.tipos_comida[4]:
                self.score -= 1
                self.sonido_bomba.play()

        if len(self.todos_sprite) <= 1:
            self.done = True
        


    def display(self, screen):
        screen.blit(self.fondo, [0, 0])
        self.todos_sprite.draw(screen)
        self.texto_score = self.fuente_score.render(f"{self.score}", True, negro)

        screen.blit(self.texto_score, (430, 50))
        
        if self.musica_sonando:
            pygame.draw.circle(screen, (255, 170, 170), (50, 50), 50) 
        else:
            pygame.draw.circle(screen, negro, (50, 50), 50)  

        if self.done == True:
            self.texto_reinyesc = self.fuente_rein_esc.render(f"'R' para reiniciar o ESC para volver", True, negro)
            screen.blit(self.texto_reinyesc, (80, 100))
        pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Juego comida Poe")

    clock = pygame.time.Clock()

    juego_comida = Juego()

    done = False

    while not done: 
        done = juego_comida.procesar_eventos()

        if not juego_comida.done:
            juego_comida.logica()

        juego_comida.display(screen)

        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()