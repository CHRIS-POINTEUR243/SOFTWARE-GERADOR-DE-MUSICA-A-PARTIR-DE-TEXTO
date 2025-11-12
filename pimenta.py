
import pygame


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_BACKSPACE,
    QUIT,
    K_g,
    K_p
)


pygame.init()
pygame.mixer.init () 


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 36)


som = pygame.mixer.Sound("error-126627.wav")  

adicionada=1


texto = ""

running = True


while running:
    
    for event in pygame.event.get():
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key== K_BACKSPACE:
                texto = texto[:-1]
            elif event.key == K_g:  # Quando apertar G
                som.play()  # Toca o som
                texto += event.unicode
            elif event.key == K_p:  # Quando apertar G
                som.set_volume(0.2) # 20% do volume
                texto += event.unicode
            else:
                
                texto += event.unicode
#
#UNICODE - qual caractere eh
        elif event.type == QUIT:
            running = False

  
    screen.fill((0, 0, 0))
    texto_aqui= font.render(texto, True, (255, 255, 255))
    screen.blit(texto_aqui, (50, 50))

    instrucao = font.render("nada", True, (255, 255, 0))
    
    screen.blit(instrucao, (50, 100))
    
    pygame.display.flip()

pygame.quit()



#ABRACADARA