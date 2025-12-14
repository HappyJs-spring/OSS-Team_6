import pygame, sys

def show_clue_popup(screen, clock, background, image):
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < 1500:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        screen.blit(background, (0,0))
        screen.blit(
            image,
            (screen.get_width()//2 - image.get_width()//2,
             screen.get_height()//2 - image.get_height()//2)
        )

        pygame.display.flip()
        clock.tick(60)
