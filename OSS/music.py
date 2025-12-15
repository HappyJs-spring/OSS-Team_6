import ctypes
import pygame
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "music.dll")
PROJECT_ROOT = os.path.dirname(BASE_DIR)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (120, 220, 140)
GRAY = (160, 160, 160)
RED = (255, 80, 80)


class MusicGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.font = pygame.font.SysFont("malgun gothic", 28)
        self.font_big = pygame.font.SysFont("malgun gothic", 64)

        # 키 이미지
        self.key_img = pygame.image.load(
            os.path.join(PROJECT_ROOT, 'UI', 'Rhythmic game UI image', "keyboard.png")
        ).convert_alpha()
        self.key_img = pygame.transform.scale(self.key_img, (70, 70))
        self.key_big = pygame.transform.scale(self.key_img, (160, 160))

        # 플레이어 이미지
        self.player_img = pygame.image.load(
            os.path.join(PROJECT_ROOT, "UI", 'Rhythmic game UI image',"couple_sneer.png")
        ).convert_alpha()
        self.player_img = pygame.transform.smoothscale(self.player_img, (260, 420))

        # DLL
        try:
            self.c = ctypes.CDLL(DLL_PATH)
            self._setup()
            self.c.init_game()
        except OSError:
            self.c = None

        self.sequence = [self.c.get_note(i).decode() for i in range(20)]
        self.index = 0
        self.start_time = 0

    # --------------------------------
    def _setup(self):
        self.c.init_game.restype = None
        self.c.get_note.argtypes = [ctypes.c_int]
        self.c.get_note.restype = ctypes.c_char
        self.c.check_input.argtypes = [ctypes.c_int, ctypes.c_char]
        self.c.check_input.restype = ctypes.c_int

    def arrow_to_text(self, c):
        return {'w': '↑', 's': '↓', 'a': '←', 'd': '→', ' ': '●'}[c]

    # --------------------------------
    def countdown(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        for i in range(3, 0, -1):
            self.screen.fill(WHITE)
            t = self.font_big.render(str(i), True, BLACK)
            self.screen.blit(
                t,
                (w // 2 - t.get_width() // 2,
                 h // 2 - t.get_height() // 2)
            )
            pygame.display.flip()
            pygame.time.wait(1000)

    # --------------------------------
    def draw_screen(self, message=""):
        w, h = self.screen.get_width(), self.screen.get_height()
        self.screen.fill(WHITE)

        col_w = w // 3
        left_cx = col_w // 2
        center_cx = col_w + col_w // 2
        right_cx = col_w * 2 + col_w // 2

        # ===== 제목 =====
        title = self.font_big.render("커플 피하기", True, BLACK)
        self.screen.blit(title, (w // 2 - title.get_width() // 2, 20))

        # ===== 타이머 =====
        left = 15 - int(time.time() - self.start_time)
        timer = self.font.render(f"남은 시간 : {left}초", True, BLACK)
        self.screen.blit(timer, (w // 2 - timer.get_width() // 2, 120))

        # ================= LEFT : 플레이어 이미지 =================
        self.screen.blit(
            self.player_img,
            (left_cx - self.player_img.get_width() // 2, 200)
        )

        # ================= CENTER : 시퀀스 =================
        seq_total_w = 10 * 80
        seq_start_x = center_cx - seq_total_w // 2
        seq_start_y = 200

        for i, c in enumerate(self.sequence):
            x = seq_start_x + (i % 10) * 80
            y = seq_start_y + (i // 10) * 110

            self.screen.blit(self.key_img, (x, y))

            arrow = self.font.render(self.arrow_to_text(c), True, BLACK)
            self.screen.blit(
                arrow,
                (x + 35 - arrow.get_width() // 2,
                 y + 35 - arrow.get_height() // 2)
            )

            if i == self.index:
                pygame.draw.rect(self.screen, RED, (x - 4, y - 4, 78, 78), 3)
            elif i < self.index:
                pygame.draw.rect(self.screen, GRAY, (x - 2, y - 2, 74, 74), 2)

        # ================= RIGHT : 현재 키 =================
        guide_title = self.font.render("지금 눌러야 할 키", True, BLACK)
        self.screen.blit(
            guide_title,
            (right_cx - guide_title.get_width() // 2, 180)
        )

        if self.index < 20:
            self.screen.blit(
                self.key_big,
                (right_cx - self.key_big.get_width() // 2, 240)
            )
            arrow = self.font_big.render(
                self.arrow_to_text(self.sequence[self.index]),
                True, BLACK
            )
            self.screen.blit(
                arrow,
                (right_cx - arrow.get_width() // 2,
                 240 + self.key_big.get_height() // 2 - arrow.get_height() // 2)
            )

        # ===== 하단 경고 =====
        pygame.draw.rect(self.screen, GREEN, (0, h - 100, w, 100))
        warn = self.font_big.render("기회는 단 한 번뿐입니다", True, BLACK)
        self.screen.blit(warn, (w // 2 - warn.get_width() // 2, h - 80))

        # ===== 성공 / 실패 메시지 (아래로 이동) =====
        if message:
            msg = self.font_big.render(message, True, RED)
            self.screen.blit(
                msg,
                (w // 2 - msg.get_width() // 2,
                 h // 2 + 120)
            )

        pygame.display.flip()

    # --------------------------------
    def run(self):
        if self.c is None:
            return False

        self.countdown()
        self.start_time = time.time()
        self.index = 0

        while True:
            self.draw_screen()

            if time.time() - self.start_time >= 15:
                self.draw_screen("실패!")
                pygame.time.wait(1500)
                return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: key = 'w'
                    elif event.key == pygame.K_DOWN: key = 's'
                    elif event.key == pygame.K_LEFT: key = 'a'
                    elif event.key == pygame.K_RIGHT: key = 'd'
                    elif event.key == pygame.K_SPACE: key = ' '
                    else:
                        continue

                    if self.c.check_input(self.index, key.encode()) == 0:
                        self.draw_screen("실패!")
                        pygame.time.wait(1500)
                        return False

                    self.index += 1
                    if self.index >= 20:
                        self.draw_screen("성공!")
                        pygame.time.wait(1500)
                        return True

            self.clock.tick(60)
