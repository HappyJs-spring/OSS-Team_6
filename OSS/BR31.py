import ctypes
import pygame
import os
import time

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
    def draw_screen(self, highlight=False):
        """화면 그림. highlight=True면 숫자를 밝게 강조함."""
        self.screen.fill((25, 25, 40))

        current = self.c.get_current()
        t_title = self.font_mid.render("Baskin Robbins 31", True, (240, 240, 240))
        self.screen.blit(t_title, (50, 40))

        color = (255, 240, 120) if highlight else (250, 250, 250)
        t_num = self.font_big.render(str(current), True, color)
        self.screen.blit(t_num, (60, 160))

        t_msg = self.font_mid.render(self.message, True, (200, 200, 200))
        self.screen.blit(t_msg, (50, 280))

        t_info = self.font.render("Press 1, 2, 3 to call numbers", True, (180, 180, 180))
        self.screen.blit(t_info, (50, 350))

        pygame.display.flip()

    # ---------------------------------------------------------
    def animate_increase(self, target):
        """
        현재 숫자에서 target까지 하나씩 증가하는 애니메이션
        예) 12 → 13 → 14 → 15
        """
        while True:
            current = self.c.get_current()
            if current >= target:
                break

            # 1 증가시키기 위한 내부용 (C코드 직접 증가는 안됨 → 애니메이션용 표시만)
            self.c.current = current + 1  # DLL 값 증가 X → get_current() 값 유지됨

            # 화면 표시(강조)
            self.draw_screen(highlight=True)
            pygame.time.wait(200)

            # 실제 현재값 증가 반영 (강제 반영)
            self.c.get_current.restype = ctypes.c_int
            # DLL 내부 current를 직접 바꿀 수 없어 아래 방식 사용
            # → 강제 값 업데이트를 위해 player_turn(0) 이용 (0은 의미없는 호출)
            # 혹은 별도 업데이트 함수가 필요하지만 여기서는 단순화
            self._force_update_current(current + 1)

            # 일반 화면
            self.draw_screen()

    def _force_update_current(self, new_value):
        """DLL 구조상 current 값을 직접 바꿀 수 없어서 강제 업데이트용 헬퍼"""
        # DLL C코드에서 현재값을 수정하는 함수가 필요하지만,
        # 여기서는 ctypes의 '메모리 직접 접근'으로 해결
        addr = ctypes.addressof(self.c)  # DLL 베이스 주소
        # 실제 current가 배치되는 메모리 오프셋을 수동으로 찾는 건 어려우므로
        # 간단하게 '가짜 증가 애니메이션 전용' 방식으로 대체
        pass
        # 주의: DLL 내부 current 변경은 player_turn 또는 computer_turn으로만 가능
        # 따라서 애니메이션 후에 player_turn/comp 호출 전까지는 get_current 기준으로 다시 그린다.
        # 핵심: 애니메이션은 시각 효과이며 DLL 데이터는 변하지 않음.

    # ---------------------------------------------------------
    def animate_player(self, count_before_call, num_called):
        """player_turn 하기 전에 숫자가 num_called 만큼 차오르는 효과"""
        for _ in range(num_called):
            count_before_call += 1
            self.draw_screen(highlight=True)
            pygame.time.wait(200)
            self.draw_screen()

    # ---------------------------------------------------------
    def animate_computer(self, num_called):
        """컴퓨터의 호출 숫자를 1개씩 증가 표시"""
        for _ in range(num_called):
            current = self.c.get_current() + 1
            self.draw_screen(highlight=True)
            pygame.time.wait(200)
            self.draw_screen()

    # ---------------------------------------------------------
    def run(self):
        if self.game_over:
            return False

        running = True

        while running:
            self.draw_screen()

            if self.c.is_finished():
                result = self.c.get_result()
                if result == 1:
                    self.message = "You Win!"
                else:
                    self.message = "You Lose!"
                self.draw_screen()
                pygame.time.wait(2000)
                return (result == 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        num = 1
                    elif event.key == pygame.K_2:
                        num = 2
                    elif event.key == pygame.K_3:
                        num = 3
                    else:
                        continue

                    # 애니메이션: 숫자 하나씩 증가 표시
                    self.message = f"You call {num}"
                    before = self.c.get_current()
                    self.animate_player(before, num)

                    # 실제 C 함수 실행
                    r = self.c.player_turn(num)
                    if r == -1:
                        self.message = "You Lose!"
                        self.draw_screen()
                        pygame.time.wait(1800)
                        return False

                    pygame.time.wait(300)

                    # 컴퓨터 턴
                    c = self.c.computer_turn()
                    if c == -1:
                        self.message = "You Win!"
                        self.draw_screen()
                        pygame.time.wait(1800)
                        return True

                    self.message = f"Computer calls {c}"
                    self.animate_computer(c)
                    pygame.time.wait(500)

            self.clock.tick(60)
