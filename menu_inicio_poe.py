import pygame


blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
violeta = (145, 61, 148)
naranja = (247, 95, 0)
pink = (255, 170, 170)

screen_size = (1300, 680)


def main():    
    pygame.init()
    pygame.mixer.init()

    pantalla_inicio = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("El Poe")

    fondo = pygame.image.load("fondo_main_menu.jpg").convert()
    icono_sonido = pygame.image.load("icono_sonido.png").convert()
    icono_sonido.set_colorkey(negro)

    jugar_pong = pygame.Rect(500, 260, 320, 70)
    fuente_pong = pygame.font.SysFont("Impact", 50)
    texto_pong = fuente_pong.render("Jugar Pong", True, negro)

    juego_comida = pygame.Rect(500, 350, 320, 70)
    fuente_comida = pygame.font.SysFont("Impact", 50)
    texto_comida = fuente_comida.render("Jugar Comida", True, negro)

    controles = pygame.Rect(500, 450, 320, 70)
    fuente_controles = pygame.font.SysFont("Impact", 50)
    texto_controles = fuente_controles.render("Controles", True, negro)

    cerrar = pygame.Rect(500, 570, 320, 70)
    fuente_cerrar = pygame.font.SysFont("Impact", 50)
    texto_cerrar = fuente_cerrar.render("Salir", True, negro)



    pygame.mixer.music.load("fade_alan_walker.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    musica_sonando = True

    clock = pygame.time.Clock()
    salir = False

    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if jugar_pong.collidepoint(pygame.mouse.get_pos()):
                    import pruebapong3PC
                    pruebapong3PC.main()

                elif juego_comida.collidepoint(pygame.mouse.get_pos()):
                    import juego_comidaVF
                    juego_comidaVF.main()

                elif controles.collidepoint(pygame.mouse.get_pos()):
                    import controles
                    controles.main()
                
                elif cerrar.collidepoint(pygame.mouse.get_pos()):
                    salir = True

                elif silenciar.collidepoint(pygame.mouse.get_pos()):
                    if musica_sonando:
                        pygame.mixer.music.pause()

                    else:
                        pygame.mixer.music.unpause()
                    musica_sonando = not musica_sonando




        pantalla_inicio.blit(fondo,[-25,-50])

        if jugar_pong.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla_inicio, naranja, jugar_pong, 0)
            
        else: 
            pygame.draw.rect(pantalla_inicio, violeta, jugar_pong, 0)

        if juego_comida.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla_inicio, naranja, juego_comida, 0)
            
        else:
            pygame.draw.rect(pantalla_inicio, violeta, juego_comida, 0)


        if controles.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla_inicio, naranja, controles, 0)
            
        else:
            pygame.draw.rect(pantalla_inicio, violeta, controles, 0)


        if cerrar.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla_inicio, naranja, cerrar, 0)

        else:
            pygame.draw.rect(pantalla_inicio, violeta, cerrar, 0)

        if musica_sonando:
            silenciar = pygame.draw.circle(pantalla_inicio, pink, (1200, 100), 50)
        else:
            silenciar = pygame.draw.circle(pantalla_inicio, negro, (1200, 100), 50)

        pantalla_inicio.blit(icono_sonido, (1175, 80))
        pantalla_inicio.blit(texto_pong, (500 + (jugar_pong.width - texto_pong.get_width())/2, 260))
        pantalla_inicio.blit(texto_comida, (500 +(juego_comida.width - texto_comida.get_width())/2, 350))
        pantalla_inicio.blit(texto_controles, (500 + (controles.width - texto_controles.get_width())/2, 450))
        pantalla_inicio.blit(texto_cerrar, (500 + (cerrar.width - texto_cerrar.get_width())/2, 570))
        
        
        pygame.display.flip()
    clock.tick(60)

pygame.quit()

if __name__ == "__main__":
    main()