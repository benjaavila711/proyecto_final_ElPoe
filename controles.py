import pygame
negro = (0, 0, 0)
rojo = (255, 0, 0)
azul = (0, 0, 255)
screen_size = (1300, 680)

def main():
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Controles")

    cerrar = pygame.Rect(980, 2, 320, 65)
    fuente_cerrar = pygame.font.SysFont("Impact", 60)
    texto_cerrar = fuente_cerrar.render("Salir", True, negro)

    controles_imagen = pygame.image.load("fondo_controles.png").convert()

    corriendo = True

    while corriendo == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cerrar.collidepoint(pygame.mouse.get_pos()):
                    corriendo = "menu"
                    if corriendo == "menu":
                        import menu_inicio_poe
                        menu_inicio_poe.main()

        screen.blit(controles_imagen, [0, 0])
        pygame.draw.rect(screen, rojo, cerrar, 0)
        screen.blit(texto_cerrar, cerrar.topleft)
        pygame.display.flip()
    
    
    
    clock.tick(60)
pygame.quit()

if __name__ == "__main__":
    main()