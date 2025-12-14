import pygame

def draw_status_ui(screen, state, status_img, clue_icon):
    x, y = screen.get_width() - 320, 20
    screen.blit(status_img, (x, y))

    # HP
    pygame.draw.rect(screen, (60,60,60), (x+80, y+45, 150, 14))
    pygame.draw.rect(
        screen, (200,0,0),
        (x+80, y+45, int(150 * state.health / 100), 14)
    )

    # CLUE
    pygame.draw.rect(screen, (60,60,60), (x+80, y+75, 150, 14))
    pygame.draw.rect(
        screen, (0,200,255),
        (x+80, y+75, int(150 * state.clue / 100), 14)
    )

    screen.blit(clue_icon, (x+40, y+70))
