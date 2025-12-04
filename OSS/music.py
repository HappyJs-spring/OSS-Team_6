import ctypes
import pygame
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "music.dll")

class MusicGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.font = pygame.font.SysFont("malgun gothic", 40)
        self.font_big = pygame.font.SysFont("malgun gothic", 80)

        # DLL Load
        try:
            self.c = ctypes.CDLL(DLL_PATH)
            self._setup()
            self.c.init_game()
        except OSError:
            print("DLL 로드 실패")
            self.c = None

        self.index = 0
        self.start_time = time.time()
        self.sequence = []

        # DLL에서 note 20개 미리 읽기
        for i in range(20):
            note = self.c.get_note(i)      # returns c_char → bytes
            self.sequence.append(note.decode())  # "w","a","s","d"," "

        # 애니메이션 관련
        self.showing_computer = False
        self.animation_step = 0
        self.animation_delay = 0.7  # 애니메이션 한 칸 보여줄 시간
        self.last_anim = time.time()

    # DLL function settings
    def _setup(self):
        self.c.init_game.restype = None
        self.c.get_note.argtypes = [ctypes.c_int]
        self.c.get_note.restype = ctypes.c_char
        self.c.check_input.argtypes = [ctypes.c_int, ctypes.c_char]
        self.c.check_input.restype = ctypes.c_int

    # 화면 그리기 함수
    def draw_screen(self, message=""):
        self.screen.fill((25, 30, 45))

        # 남은 시간
        if not self.showing_computer:
            left = 15 - int(time.time() - self.start_time)
            t_time = self.font.render(f"남은 시간: {left}초", True, (255, 255, 110))
            self.screen.blit(t_time, (50, 30))

        # 전체 시퀀스 출력
        x = 40
        y = 150

        for i, c in enumerate(self.sequence):
            arrow = self.arrow_to_text(c)
            color = (100, 100, 100)

            # 플레이어 턴
            if i == self.index:
                color = (255, 255, 255)

            text = self.font.render(arrow, True, color)
            self.screen.blit(text, (x + (i % 10) * 60, y + (i // 10) * 80))

        # 메시지 표시
        msg = self.font.render(message, True, (200, 200, 200))
        self.screen.blit(msg, (50, 400))

        pygame.display.flip()

    def arrow_to_text(self, c):
        if c == 'w': return "↑"
        if c == 's': return "↓"
        if c == 'a': return "←"
        if c == 'd': return "→"
        if c == ' ': return "●"
        return "?"

    # -------------------------------------------------------
    def run(self):
        if self.c is None:
            return False

        message = ""

        while True:
            self.draw_screen(message)

            # 시간 초과
            if time.time() - self.start_time >= 15:
                self.draw_screen("시간 초과! 실패!")
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

                    # C DLL 체크
                    r = self.c.check_input(self.index, key.encode())

                    if r == 0:
                        self.draw_screen("틀렸습니다! 실패!")
                        pygame.time.wait(1500)
                        return False

                    self.index += 1

                    # 모든 입력 성공 
                    if self.index >= 20:
                        self.draw_screen("성공! 단서 획득!")
                        pygame.time.wait(1500)
                        return True

            self.clock.tick(60)
