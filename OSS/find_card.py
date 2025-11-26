# FindCard.py
import ctypes
import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "find_card.dll")

class FindCard:
    CARD_SIZE = 120
    GAP = 20
    START_X = 50
    START_Y = 50

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.message = ""
        self.game_result = None

        # 폰트
        self.font_big = pygame.font.SysFont("malgun gothic", 48)
        self.font = pygame.font.SysFont("malgun gothic", 28)

        # C 라이브러리
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_game()
        except OSError:
            print(f"오류: {DLL_PATH} 파일을 로드할 수 없습니다. DLL 경로 확인 필요.")
            self.game_result = False
            return

        # ctypes 배열 (16개)
        self.nums_arr = (ctypes.c_int * 16)()
        self.states_arr = (ctypes.c_int * 16)()

        # 클릭 처리 잠금 (미스 후 지연동안 추가 클릭 방지)
        self.click_locked = False
        self.lock_until = 0

    def _setup_c_functions(self):
        # 시그니처 설정
        self.c_lib.init_game.restype = None

        self.c_lib.select_card.argtypes = [ctypes.c_int, ctypes.c_int]
        self.c_lib.select_card.restype = ctypes.c_int

        self.c_lib.reset_temp.restype = None

        self.c_lib.get_board_nums.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.c_lib.get_board_nums.restype = None

        self.c_lib.get_board_state.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.c_lib.get_board_state.restype = None

        self.c_lib.is_finished.restype = ctypes.c_int

    def _card_rect(self, x, y):
        return pygame.Rect(
            self.START_X + x * (self.CARD_SIZE + self.GAP),
            self.START_Y + y * (self.CARD_SIZE + self.GAP),
            self.CARD_SIZE,
            self.CARD_SIZE
        )

    def _symbol_for_num(self, n):
        # 카드 번호를 간단한 기호로 변환 (원하면 변경)
        symbols = ["★","♨","■","◎","◆","♣","♠","☎"]
        if 0 <= n < len(symbols):
            return symbols[n]
        return str(n)

    def _draw_board(self):
        # C로부터 최신 보드 정보 가져오기
        self.c_lib.get_board_nums(self.nums_arr)
        self.c_lib.get_board_state(self.states_arr)

        self.screen.fill((25, 25, 30))

        # 제목
        title = self.font_big.render("Find Card", True, (240,240,240))
        self.screen.blit(title, ((self.screen.get_width()-title.get_width())//2, 10))

        idx = 0
        for y in range(4):
            for x in range(4):
                rect = self._card_rect(x, y)
                state = int(self.states_arr[idx])
                num = int(self.nums_arr[idx])

                # 상태별 색상/표시
                if state == 0:  # HIDDEN
                    pygame.draw.rect(self.screen, (80,80,80), rect, border_radius=8)
                    # 카드 뒷면 디자인 (간단)
                    pygame.draw.rect(self.screen, (100,100,100), rect.inflate(-10, -10), border_radius=6)
                elif state == 1:  # OPEN
                    pygame.draw.rect(self.screen, (60,180,120), rect, border_radius=8)
                    self._draw_center_text(self._symbol_for_num(num), rect, (0,0,0))
                elif state == 2:  # TEMP (선택된 임시)
                    pygame.draw.rect(self.screen, (230,200,60), rect, border_radius=8)
                    self._draw_center_text(self._symbol_for_num(num), rect, (0,0,0))
                elif state == 3:  # HINT
                    pygame.draw.rect(self.screen, (80,140,240), rect, border_radius=8)
                    self._draw_center_text(self._symbol_for_num(num), rect, (0,0,0))
                else:
                    pygame.draw.rect(self.screen, (80,80,80), rect, border_radius=8)

                idx += 1

        # 하단 메시지
        msg_surf = self.font.render(self.message, True, (240,240,240))
        self.screen.blit(msg_surf, (50, self.START_Y + 4*(self.CARD_SIZE+self.GAP) + 20))

        pygame.display.flip()

    def _draw_center_text(self, text, rect, color=(0,0,0)):
        text_surf = self.font.render(text, True, color)
        tx = rect.x + rect.width//2 - text_surf.get_width()//2
        ty = rect.y + rect.height//2 - text_surf.get_height()//2
        self.screen.blit(text_surf, (tx, ty))

    def run(self):
        """FindCard 게임 메인 루프 (클래스 메서드)"""
        # DLL 로드 실패 시 바로 반환
        if self.game_result is not None:
            return self.game_result

        running = True
        while running:
            # 잠금 해제 시간 체크
            if self.click_locked and pygame.time.get_ticks() >= self.lock_until:
                self.click_locked = False

            # 게임 종료 확인
            if self.c_lib.is_finished():
                # 성공
                self.message = "🎉 모든 카드를 찾았습니다!"
                self._draw_board()
                pygame.time.wait(2000)
                self.game_result = True
                return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.click_locked:
                        # 잠금 중엔 클릭 무시
                        continue

                    mx, my = event.pos
                    clicked = False
                    for y in range(4):
                        for x in range(4):
                            rect = self._card_rect(x, y)
                            if rect.collidepoint(mx, my):
                                clicked = True
                                result = self.c_lib.select_card(x, y)
                                # C 함수 반환값 처리
                                if result == 0:
                                    self.message = "카드 선택되었습니다."
                                elif result == 1:
                                    self.message = "일치! 카드가 열렸습니다."
                                elif result == 2:
                                    # 불일치: TEMP 상태가 된 두 카드를 잠시 보여주고 숨김 처리
                                    self.message = "불일치! 잠시 후 다시 숨깁니다."
                                    # 즉시 한 프레임 더 그려서 TEMP 상태 보이게 함
                                    self._draw_board()
                                    pygame.time.wait(700)
                                    # C에 TEMP->HIDDEN 처리 요청
                                    self.c_lib.reset_temp()
                                elif result == 3:
                                    self.message = "이미 열려있는 카드입니다."
                                elif result == 4:
                                    self.message = "이미 두 장 선택된 상태입니다."
                                else:
                                    self.message = "알 수 없는 응답."
                                break
                        if clicked:
                            break

                # 키 입력으로 힌트(예: H) 등 추가 기능 처리 가능
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        # 힌트 기능: 간단히 첫 Hidden 카드의 번호를 찾아 use_hint 호출
                        # (DLL에 use_hint(num) 구현이 있을 경우 사용)
                        # 여기서는 get_board_nums로 찾아서 첫 hidden 카드의 num을 이용해 호출 시도
                        nums = (ctypes.c_int * 16)()
                        states = (ctypes.c_int * 16)()
                        self.c_lib.get_board_nums(nums)
                        self.c_lib.get_board_state(states)
                        target_num = None
                        for i in range(16):
                            if states[i] == 0:  # hidden
                                target_num = nums[i]
                                break
                        if target_num is not None:
                            try:
                                # use_hint 존재 여부를 체크하여 안전 호출
                                if hasattr(self.c_lib, "use_hint"):
                                    self.c_lib.use_hint(ctypes.c_int(target_num))
                                    self.message = "힌트 사용!"
                                else:
                                    self.message = "힌트 기능이 없습니다."
                            except Exception:
                                self.message = "힌트 호출 중 오류."

            self._draw_board()
            self.clock.tick(30)

        return self.game_result
