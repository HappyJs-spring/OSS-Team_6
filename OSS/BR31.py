import ctypes
import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "BR31.dll")

class BR31:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.message = ""
        self.game_over = False
        self.font_big = pygame.font.SysFont("malgun gothic", 80)
        self.font_mid = pygame.font.SysFont("malgun gothic", 40)
        self.font = pygame.font.SysFont("malgun gothic", 28)

        try:
            self.c = ctypes.CDLL(DLL_PATH)
            self._setup_functions()
            self.c.init_game()
        except Exception as e:
            print("DLL 로드 실패:", e)
            self.game_over = True

    def _setup_functions(self):
        # DLL 안의 함수 시그니처를 맞춤
        self.c.init_game.restype = None
        self.c.player_turn.argtypes = [ctypes.c_int]
        self.c.player_turn.restype = ctypes.c_int
        self.c.computer_turn.restype = ctypes.c_int
        self.c.get_current.restype = ctypes.c_int
        self.c.is_finished.restype = ctypes.c_int
        self.c.get_result.restype = ctypes.c_int

    # ---------------------------------------------------------
    def draw_screen(self, show_number=None, highlight=False):
        """화면 그리기. show_number가 주어지면 그 숫자를 표시(애니메이션용 임시 값)."""
        self.screen.fill((25, 25, 40))

        title = self.font_mid.render("Baskin Robbins 31", True, (240, 240, 240))
        self.screen.blit(title, (50, 40))

        # 보여줄 숫자 결정 (애니메이션용 임시값 우선)
        if show_number is None:
            current = self.c.get_current()
        else:
            current = show_number

        color = (255, 240, 120) if highlight else (250, 250, 250)
        num_surf = self.font_big.render(str(current), True, color)
        self.screen.blit(num_surf, (60, 160))

        msg_surf = self.font_mid.render(self.message, True, (200, 200, 200))
        self.screen.blit(msg_surf, (50, 280))

        info = self.font.render("Press 1, 2, or 3 to call numbers", True, (180, 180, 180))
        self.screen.blit(info, (50, 350))

        pygame.display.update()

    # ---------------------------------------------------------
    def _player_step_animation(self, steps, step_delay=200):
        """
        플레이어가 steps 만큼 말할 때,
        실제로 player_turn(1)을 호출해서 DLL current를 1씩 올리고,
        각 스텝마다 화면을 갱신해 애니메이션으로 보여준다.
        """
        for i in range(steps):
            # 실제 DLL 상태를 1 증가시킨다
            r = self.c.player_turn(1)   # 1씩 올리기
            # r == -1 이면 즉시 패배(31을 말함) — 루프 종료
            # 화면에는 증가된 current가 반영되어 보인다.
            self.draw_screen(highlight=True)
            pygame.time.delay(step_delay)  # ms
            self.draw_screen()
            if r == -1:
                return -1
        return 1

    # ---------------------------------------------------------
    def _computer_animation_after_call(self, prev_current, step_delay=200):
        """
        컴퓨터가 이미 self.c.computer_turn()으로 내부적으로 current를
        증가시킨 뒤에 호출한다. 컴퓨터가 부른 개수 = new_current - prev_current.
        이 차이를 시각적으로 하나씩 증가하는 애니메이션으로 보여줌.
        """
        new_current = self.c.get_current()
        steps = max(0, new_current - prev_current)
        for i in range(1, steps + 1):
            show_val = prev_current + i
            self.draw_screen(show_number=show_val, highlight=True)
            pygame.time.delay(step_delay)
            self.draw_screen()
        return steps

    # ---------------------------------------------------------
    def run(self):
        if self.game_over:
            return False

        running = True

        while running:
            # 기본 화면
            self.draw_screen()

            # 게임 종료 체크
            if self.c.is_finished():
                res = self.c.get_result()
                if res == 1:
                    self.message = "You Win!"
                    self.draw_screen()
                    pygame.time.delay(1800)
                    return True
                else:
                    self.message = "You Lose!"
                    self.draw_screen()
                    pygame.time.delay(1800)
                    return False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    key = event.unicode
                    if key not in ('1', '2', '3'):
                        continue
                    num = int(key)

                    # --- 플레이어 턴: 한 번에 num 호출하지 말고 1씩 나눠 호출해서 DLL 상태가 단계적으로 바뀌게 함 ---
                    self.message = f"You call {num}"
                    self.draw_screen()
                    pygame.time.delay(120)

                    r = self._player_step_animation(num, step_delay=220)
                    if r == -1:
                        # 플레이어가 31을 말해 패배 처리됨 (DLL에서 이미 상태 반영)
                        self.message = "You Lose!"
                        self.draw_screen()
                        pygame.time.delay(1400)
                        return False

                    # 플레이어 후 짧은 휴지(턴 주기)
                    pygame.time.delay(700)

                    # --- 컴퓨터 턴: 한 번에 호출 (컴퓨터 내부 전략에 따라 여러 개 증가)
                    prev = self.c.get_current()
                    com_ret = self.c.computer_turn()  # 이 호출이 current를 내부에서 증가시킴
                    # com_ret may be -1 if computer reached 31 (then player wins)
                    if com_ret == -1:
                        # 컴퓨터가 31을 불러서 플레이어 승리
                        # 하지만 컴퓨터 내부에서 이미 current가 변경되었으니 시각적으로 단계별로 표시
                        self._computer_animation_after_call(prev, step_delay=220)
                        self.message = "You Win!"
                        self.draw_screen()
                        pygame.time.delay(1400)
                        return True

                    # 정상적으로 컴퓨터가 몇 개 불렀는지 시각적으로 표시
                    self._computer_animation_after_call(prev, step_delay=220)
                    self.message = f"Computer called {self.c.get_current() - prev}"
                    self.draw_screen()
                    pygame.time.delay(500)

            self.clock.tick(60)
