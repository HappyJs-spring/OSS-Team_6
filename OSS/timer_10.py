import ctypes
import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "timer.dll")

class Timer:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.font_big = pygame.font.SysFont("malgun gothic", 70)
        self.font = pygame.font.SysFont("malgun gothic", 40)

        self.running = True
        self.timer_started = False
        self.elapsed = 0.0
        self.message = ""

        # DLL 로드
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_timer()
        except OSError:
            print(f"오류: {DLL_PATH} 로드 실패!")
            self.running = False
            self.game_result = False

    def _setup_c_functions(self):
        self.c_lib.init_timer.restype = None
        self.c_lib.start_timer.restype = None
        self.c_lib.stop_timer.restype = None

        self.c_lib.get_elapsed_time.restype = ctypes.c_double
        self.c_lib.get_difference.restype = ctypes.c_double
        self.c_lib.is_success.restype = ctypes.c_int

    def _draw_screen(self):
        self.screen.fill((0, 0, 0))

        title = self.font_big.render("10초 맞추기 게임", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 80))

        time_text = self.font.render(f"시간: {self.elapsed:.2f} 초", True, (255, 255, 0))
        self.screen.blit(time_text, (self.screen.get_width() // 2 - time_text.get_width() // 2, 250))

        msg = self.font.render(self.message, True, (200, 255, 200))
        self.screen.blit(msg, (self.screen.get_width() // 2 - msg.get_width() // 2, 350))

        guide = self.font.render("스페이스바를 눌러 시작 / 종료", True, (150, 150, 255))
        self.screen.blit(guide, (self.screen.get_width() // 2 - guide.get_width() // 2, 500))

        pygame.display.flip()

    def run(self):

        while self.running:
            self.elapsed = self.c_lib.get_elapsed_time()
            self._draw_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # 타이머가 아직 안 시작됨 → 시작
                        if not self.timer_started:
                            self.c_lib.init_timer()
                            self.c_lib.start_timer()
                            self.timer_started = True
                            self.message = "측정 중..."
                        # 이미 진행 중 → 종료
                        else:
                            self.c_lib.stop_timer()
                            self.timer_started = False
                            self.elapsed = self.c_lib.get_elapsed_time()

                            success = self.c_lib.is_success()

                            if success == 1:
                                self.message = f"성공! 기록: {self.elapsed:.2f} 초"
                                self._draw_screen()
                                pygame.time.wait(3000)
                                return True
                            else:
                                self.message = f"실패! 기록: {self.elapsed:.2f} 초"
                                self._draw_screen()
                                pygame.time.wait(3000)
                                return False

            self.clock.tick(30)

        return False
