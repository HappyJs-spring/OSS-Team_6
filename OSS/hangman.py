import ctypes
import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "hangman.dll")


class HangmanGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.message = ""
        self.game_result = None  # True=승리, False=패배

        # 폰트
        self.font_big = pygame.font.SysFont("malgun gothic", 70)
        self.font_mid = pygame.font.SysFont("malgun gothic", 40)
        self.font = pygame.font.SysFont("malgun gothic", 30)

        # 이미지 경로
        PROJECT_ROOT = os.path.dirname(BASE_DIR)
        IMG_DIR = os.path.join(PROJECT_ROOT, "UI", "hangman UI Image")

        # 행맨 이미지 파츠 로드
        self.gallows = self._load_img(IMG_DIR, "gallows.png", (350, 450))
        self.head = self._load_img(IMG_DIR, "man head.png", (120, 120))
        self.body = self._load_img(IMG_DIR, "man body.png", (30, 160))
        self.armL = self._load_img(IMG_DIR, "man arm(L).png", (80, 80))
        self.armR = self._load_img(IMG_DIR, "man arm(R).png", (80, 80))
        self.legL = self._load_img(IMG_DIR, "man leg(L).png", (80, 100))
        self.legR = self._load_img(IMG_DIR, "man leg(R).png", (80, 100))
        self.ch = self._load_img(IMG_DIR, "player_back.png", (300, 450))

        self.parts_list = [self.head, self.body, self.armL, self.armR, self.legL, self.legR]

        # DLL 로드
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_game()
        except OSError:
            print(f"오류: {DLL_PATH} 파일을 로드할 수 없습니다.")
            self.game_result = False

    def _load_img(self, folder, name, size):
        """이미지 안전 로드 함수"""
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            print("이미지 없음:", path)
            return None
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, size)

    def _setup_c_functions(self):
        self.c_lib.init_game.restype = None
        self.c_lib.guess_char.argtypes = [ctypes.c_char]
        self.c_lib.guess_char.restype = ctypes.c_int
        self.c_lib.get_current.restype = ctypes.c_char_p
        self.c_lib.get_used.restype = ctypes.c_char_p
        self.c_lib.get_remaining.restype = ctypes.c_int
        self.c_lib.is_finished.restype = ctypes.c_int

    def _draw_hangman(self, remaining):
        """남은 목숨에 따라 행맨 파츠를 화면에 그림"""

        # 6개 파츠 → 6 라이프에서 0까지
        mistakes = 6 - remaining

        # 교수대 위치
        gx, gy = self.screen.get_width() - 450, 40
        if self.gallows:
            self.screen.blit(self.gallows, (gx, gy))

        # 행맨 중앙 좌표
        center_x = gx + 315
        head_y = gy + 70

        if mistakes >= 1 and self.head:
            self.screen.blit(self.head, (center_x - 60, head_y))

        if mistakes >= 2 and self.body:
            self.screen.blit(self.body, (center_x - 15, head_y + 80))

        if mistakes >= 3 and self.armL:
            self.screen.blit(self.armL, (center_x - 60, head_y + 110))

        if mistakes >= 4 and self.armR:
            self.screen.blit(self.armR, (center_x - 15 , head_y + 110))

        if mistakes >= 5 and self.legL:
            self.screen.blit(self.legL, (center_x - 60, head_y + 200))

        if mistakes >= 6 and self.legR:
            self.screen.blit(self.legR, (center_x - 15, head_y + 200))

    def _draw_screen(self):
        w, h = self.screen.get_width(), self.screen.get_height()

        # 배경
        self.screen.fill((255, 255, 255))
        #---- 캐릭터 이미지 ----
        self.screen.blit(self.ch, (w - 1200, h - 450))

        # ---- 위쪽 행맨 단어 표시 ----
        current = self.c_lib.get_current().decode()
        text_word = self.font_big.render(" ".join(current), True, (0, 0, 0))
        self.screen.blit(text_word, (50, 60))

        # ---- 사용된 글자 ----
        used = self.c_lib.get_used().decode()
        text_used = self.font_mid.render(f"사용된 글자: {used}", True, (40, 40, 40))
        self.screen.blit(text_used, (50, 150))

        # ---- 남은 목숨 ----
        remaining = self.c_lib.get_remaining()
        text_life = self.font_mid.render(f"남은 목숨: {remaining}", True, (200, 0, 0))
        self.screen.blit(text_life, (50, 200))

        # ---- 행맨 그림 ----
        self._draw_hangman(remaining)

        # ---- 아래 메세지 박스 ----
        pygame.draw.rect(self.screen, (120, 230, 160), (0, h - 140, w, 140))
        msg = self.font.render(self.message, True, (0, 0, 0))
        self.screen.blit(msg, (40, h - 100))

        pygame.display.flip()

    def run(self):
        if self.game_result is not None:
            return self.game_result

        running = True
        while running:
            self._draw_screen()

            # 게임 종료 체크
            if self.c_lib.is_finished():
                current_word = self.c_lib.get_current().decode()

                if "_" not in current_word:
                    self.message = "Perfect! 정답을 맞췄습니다!"
                    self.game_result = True
                else:
                    self.message = "Game Over! 실패했습니다."
                    self.game_result = False

                self._draw_screen()
                pygame.time.wait(2500)
                return self.game_result

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    key = event.unicode.lower()
                    if 'a' <= key <= 'z':
                        result = self.c_lib.guess_char(key.encode())
                        if result == 1:
                            self.message = f"정답! ({key})"
                        elif result == 0:
                            self.message = f"오답! ({key})"
                        elif result == 2:
                            self.message = f"이미 사용됨: {key}"

            self.clock.tick(30)

        return self.game_result
