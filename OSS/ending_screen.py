import pygame
import sys

def show_ending(screen, ending_type):
    font = pygame.font.SysFont("malgun gothic", 60)

    text = {
        "bad": "BAD ENDING\nF를 받았습니다",
        "happy": "HAPPY ENDING\n무사히 탈출!"
    }.get(ending_type, "ENDING")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return

        screen.fill((0, 0, 0))

        for i, line in enumerate(text.split("\n")):
            t = font.render(line, True, (255, 255, 255))
            screen.blit(t, (750 - t.get_width()//2, 300 + i*70))

        pygame.display.flip()
