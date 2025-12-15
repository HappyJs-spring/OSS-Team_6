import pygame
import sys

def start_screen(screen):
    font = pygame.font.SysFont("malgun gothic", 60)
    small = pygame.font.SysFont("malgun gothic", 28)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        screen.fill((0, 0, 0))

        title = font.render("학점 F를 피해 탈출하라", True, (255, 255, 255))
        hint = small.render("아무 키나 누르세요", True, (180, 180, 180))

        screen.blit(title, (750 - title.get_width()//2, 260))
        screen.blit(hint, (750 - hint.get_width()//2, 350))

        pygame.display.flip()
