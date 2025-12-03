import ctypes
import pygame
import os

# DLL 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "BR31.dll")

class BR31:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.message = ""
        self.game_over = False
        self.player_input = 0

        self.font_big = pygame.font.SysFont("malgun gothic", 60)
        self.font_mid = pygame.font.SysFont("malgun gothic", 40)
        self.font = pygame.font.SysFont("malgun gothic", 28)

        try:
            self.c = ctypes.CDLL(DLL_PATH)
            self._setup_functions()
            self.c.init_game()
        except OSError:
            print("DLL 로드 실패")
            self.game_over = True

    def _setup_functions(self):
        self.c.init_game.restype = None
        self.c.player_turn.argtypes = [ctypes.c_int]
        self.c.player_turn.restype = ctypes.c_int
        self.c.computer_turn.restype = ctypes.c_int
        self.c.get_current.restype = ctypes.c_int
        self.c.is_finished.restype = ctypes.c_int
        self.c.get_result.restype = ctypes.c_int

    # ---------------------------------------------------------
    def _draw_screen(self):
        self.screen.fill((20, 20, 35))

        current = self.c.get_current()

        t1 = self.font_big.render(f"BR31 GAME", True, (250, 250, 250))
        self.screen.blit(t1, (50, 40))

        t2 = self.font_mid.render(f"Current Number : {current}", True, (230, 230, 240))
        self.screen.blit(t2, (50, 140))

        t3 = self.font.render("Press 1~3 to call numbers", True, (180, 180, 180))
        self.screen.blit(t3, (50, 210))

        msg = self.font_mid.render(self.message, True, (255, 200, 120))
        self.screen.blit(msg, (50, 280))

        pygame.display.flip()

    # ---------------------------------------------------------
    def run(self):
        if self.game_over:
            return False

        running = True

        while running:
            self._draw_screen()

            # 게임 종료 상태
            if self.c.is_finished():
                result = self.c.get_result()
                if result == 1:
                    self.message = "You Win!"
                else:
                    self.message = "You Lose!"

                self._draw_screen()
                pygame.time.wait(2500)
                return (result == 1)

            # 이벤트 처리
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player_input = 1
                    elif event.key == pygame.K_2:
                        self.player_input = 2
                    elif event.key == pygame.K_3:
                        self.player_input = 3
                    else:
                        continue

                    # 플레이어 턴
                    r = self.c.player_turn(self.player_input)
                    if r == 0:
                        self.message = "Invalid input (1~3)"
                    elif r == -1:
                        self.message = "You Lose!"
                        pygame.time.wait(1800)
                        return False
                    else:
                        self.message = f"You called {self.player_input}!"

                    pygame.time.wait(600)

                    # 컴퓨터 턴
                    c = self.c.computer_turn()
                    if c == -1:
                        self.message = "Computer failed! You Win!"
                        pygame.time.wait(1800)
                        return True

                    self.message = f"Computer calls {c}"
                    pygame.time.wait(800)

            self.clock.tick(60)
