import pygame
import sys
import random
import menu_inicio_poe

negro = (0, 0, 0)
blanco = (255, 255, 255)
verde = (0, 255, 0)
rojo = (255, 0, 0)
amarillopatito = (237, 249, 68)
colorpou = (186, 177, 117)

tamano_pantalla = (1300, 650)

class Juego(object):
    def __init__(self):
        self.game_over = False
        self.score_p1 = 0
        self.score_p2 = 0
        self.coord_x_j1 = 200
        self.coord_y_j1 = 325
        self.coord_x_j2 = 1100
        self.coord_y_j2 = 325
        self.pelota_coordX = tamano_pantalla[0]// 2
        self.pelota_coordY = tamano_pantalla[1] // 2
        self.velocidad_pelota_x = 5
        self.velocidad_pelota_y = 7
        self.velocidad_y_j1 = 0
        self.velocidad_y_j2 = 0

        self.fondo = pygame.image.load("background_pong.jpeg").convert()
        self.player = pygame.image.load("pou_xD.png").convert()
        self.player.set_colorkey(negro)
        self.mascota = pygame.image.load("smiledog.png").convert()
        self.mascota.set_colorkey(negro)

        pygame.mixer.init()
        self.musica_fondo = pygame.mixer.music.load("helloomfg_musicafondo.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

        self.musica_sonando = True
        self.silenciar = pygame.Rect(1150, 50, 100, 100) 

        self.sonido_golpes = pygame.mixer.Sound("sonido_golpe_pong.wav")
        self.sonido_fin = pygame.mixer.Sound("trompeta_triste.mp3")


    def procesar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.velocidad_y_j1 = -7
                elif event.key == pygame.K_s:
                    self.velocidad_y_j1 = 7
                elif event.key == pygame.K_UP:
                    self.velocidad_y_j2 = -7
                elif event.key == pygame.K_DOWN:
                    self.velocidad_y_j2 = 7
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.velocidad_y_j1 = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.velocidad_y_j2 = 0
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.game_over:
                        self.__init__()
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        return "menu"
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.silenciar.collidepoint(pygame.mouse.get_pos()):
                    if self.musica_sonando:
                        pygame.mixer.music.pause()
                        pygame.mixer.music.set_volume(0)
                        self.sonido_fin.set_volume(0)
                        self.sonido_golpes.set_volume(0)
                        self.musica_sonando = False
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.music.set_volume(0.5)
                        self.sonido_fin.set_volume(1)
                        self.sonido_golpes.set_volume(1)
                        self.musica_sonando = True
        return False

    def logica(self):
        if not self.game_over:
            self.coord_y_j1 += self.velocidad_y_j1
            self.coord_y_j2 += self.velocidad_y_j2

            if self.coord_y_j1 <= 0:
                self.coord_y_j1 = 0
            elif self.coord_y_j1 >= 550:
                self.coord_y_j1 = 550

            if self.coord_y_j2 <= 0:
                self.coord_y_j2 = 0
            elif self.coord_y_j2 >= 550:
                self.coord_y_j2 = 550

            self.pelota_coordX += self.velocidad_pelota_x
            self.pelota_coordY += self.velocidad_pelota_y

            if self.pelota_coordY > tamano_pantalla[1] - 15 or self.pelota_coordY < 15:
                self.velocidad_pelota_y *= -1
                self.sonido_golpes.play()

            if self.pelota_coordX < 0:
                self.pelota_coordX = tamano_pantalla[0] // 2
                self.pelota_coordY = tamano_pantalla[1] // 2
                self.velocidad_pelota_x = 5
                self.velocidad_pelota_y = 7
                self.velocidad_pelota_x *= -1
                self.score_p2 += 1

            elif self.pelota_coordX > tamano_pantalla[0]:
                self.pelota_coordX = tamano_pantalla[0] // 2
                self.pelota_coordY = tamano_pantalla[1] // 2
                self.velocidad_pelota_x = 5
                self.velocidad_pelota_y = 7
                self.score_p1 += 1

            jugador1_rect = pygame.Rect(self.coord_x_j1, self.coord_y_j1, 20, 100)
            jugador2_rect = pygame.Rect(self.coord_x_j2, self.coord_y_j2, 20, 100)
            pelota_rect = pygame.Rect(self.pelota_coordX - 20, self.pelota_coordY - 20, 30, 30)

            if pelota_rect.colliderect(jugador1_rect) or pelota_rect.colliderect(jugador2_rect):
                self.sonido_golpes.play()
                self.velocidad_pelota_x *= -1.15
                self.velocidad_pelota_y *= random.choice([-1.1, 1.1])

            if self.score_p1 == 10 or self.score_p2 == 10:
                self.game_over = True
                pygame.mixer.music.stop()
                self.sonido_fin.play()

    def display_frame(self, pantalla):
        pantalla.blit(self.fondo, [0, 0])
        font = pygame.font.SysFont("comic sans", 50)
        text = font.render(f"{self.score_p1} | {self.score_p2}", True, rojo)
        texto_x = tamano_pantalla[0] // 2 - text.get_width() // 2
        texto_y = 20

        pantalla.blit(self.player, [self.coord_x_j1 - 90, self.coord_y_j1 - 5])
        pantalla.blit(self.mascota, [self.coord_x_j2 + 20 , self.coord_y_j2])
        
        jugador1 = pygame.draw.rect(pantalla, colorpou, (self.coord_x_j1, self.coord_y_j1, 20, 100))
        jugador2 = pygame.draw.rect(pantalla, amarillopatito, (self.coord_x_j2, self.coord_y_j2, 20, 100))
        lapelota = pygame.draw.circle(pantalla, verde, (self.pelota_coordX, self.pelota_coordY), 15)

        pantalla.blit(text, [texto_x, texto_y])

        if self.game_over:
            self.fuenteGO = pygame.font.SysFont("comic sans", 40)
            self.texto_go_Y = 100
            if self.score_p1 == 10:
                texto_gameover_p1 = self.fuenteGO.render("Felicidades, Poe. Has ganado el juego.", True, blanco)
                self.texto_go_1_X = (tamano_pantalla[0] // 2) - texto_gameover_p1.get_width()//2
                pantalla.blit(texto_gameover_p1, [self.texto_go_1_X, self.texto_go_Y])

            elif self.score_p2 == 10:
                texto_gameover_p2 = self.fuenteGO.render("Felicidades, mascota. Has ganado el juego.", True, blanco)
                self.texto_go_2_X = (tamano_pantalla[0]//2) - texto_gameover_p2.get_width()//2
                pantalla.blit(texto_gameover_p2, [self.texto_go_2_X, self.texto_go_Y])
            
            self.fuente_restart = pygame.font.SysFont("comic sans", 30)
            text_restart = self.fuente_restart.render("Pulsa 'R' para reiniciar, o pulsa 'esc' para salir.", True, blanco)
            self.text_rest_x = (tamano_pantalla[0] // 2) - text_restart.get_width() // 2
            self.text_rest_y = self.texto_go_Y + 50
            pantalla.blit(text_restart, [self.text_rest_x, self.text_rest_y])

        if self.musica_sonando:
            pygame.draw.circle(pantalla, (255, 170, 170), (1200, 100), 50) 
        else:
            pygame.draw.circle(pantalla, negro, (1200, 100), 50)  

        pygame.display.flip()

def main():
    pygame.init()
    pantalla = pygame.display.set_mode(tamano_pantalla)
    pygame.display.set_caption("Pong con Poe y Mascota")
    done = False
    clock = pygame.time.Clock()
    pong = Juego()

    while not done:
        resultado = pong.procesar_eventos()
        if resultado == "menu":
            menu_inicio_poe.main()
            return
        elif resultado == "quit":
            done = True
            pygame.quit()
        else:
            pong.logica()
            pong.display_frame(pantalla)
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()