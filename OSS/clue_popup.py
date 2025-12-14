import pygame

def show_clue_popup(
    screen,
    clock,
    clue_img_path,
    background=None,
    character=None
):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    # 단서 이미지 로드
    clue_img = pygame.image.load(clue_img_path).convert_alpha()
    clue_rect = clue_img.get_rect(center=screen.get_rect().center)

    # 캐릭터 위치 미리 계산
    if character:
        char_x = (screen.get_width() - character.get_width()) // 2
        char_y = screen.get_height() - character.get_height()

    # ===== 페이드 인 =====
    for alpha in range(0, 181, 10):
        overlay.fill((0, 0, 0, alpha))

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        if character:
            screen.blit(character, (char_x, char_y))

        screen.blit(overlay, (0, 0))
        screen.blit(clue_img, clue_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.time.delay(600)

    # ===== 페이드 아웃 =====
    for alpha in range(180, -1, -10):
        overlay.fill((0, 0, 0, alpha))

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        if character:
            screen.blit(character, (char_x, char_y))

        screen.blit(overlay, (0, 0))
        screen.blit(clue_img, clue_rect)

        pygame.display.flip()
        clock.tick(30)
