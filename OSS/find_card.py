import ctypes
import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # OSS/FindCard/
ASSET_DIR = os.path.join(BASE_DIR, "asset")           # OSS/asset/
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

        # 이미지 로드
        self.symbol_images = self._load_symbol_images()

        # C DLL 로드
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_game()
        except OSError:
            print(f"[ERROR] DLL 로드 실패: {DLL_PATH}")
            self.game_result = False
            return

        # 배열 준비
        self.nums_arr = (ctypes.c_int * 16)()
        self.states_arr = (ctypes.c_int * 16)()

        self.click_locked = False
        self.lock_until = 0

    # --------------------------------------------------------

    def _load_symbol_images(self):
        """asset 폴더 이미지 8개 로드"""
        images = []
        filenames = [
            "images.jpg",
            "images1.jpg",
            "images2.jpg",
            "images3.jpg",
            "images4.jpg",
            "images5.jpg",
            "images6.jpg",
            "images7.jpg",
        ]

        for name in filenames:
            path = os.path.join(ASSET_DIR, name)
            try:
                img = pygame.image.load(path).convert()   # JPG ➜ convert()
                img = pygame.transform.smoothscale(img, (90, 90))
                print("[LOAD OK]", path)
                images.append(img)
            except Exception as e:
                print("[LOAD FAIL]", path, e)
                images.append(None)

        return images

    # --------------------------------------------------------

    def _setup_c_functions(self):
        self.c_lib.init_game.restype = None
        self.c_lib.select_card.argtypes = [ctypes.c_int, ctypes.c_int]
        self.c_lib.select_card.restype = ctypes.c_int
        self.c_lib.reset_temp.restype = None
        self.c_lib.get_board_nums.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.c_lib.get_board_nums.restype = None
        self.c_lib.get_board_state.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.c_lib.get_board_state.restype = None
        self.c_lib.is_finished.restype = ctypes.c_int

    # --------------------------------------------------------

    def _card_rect(self, x, y):
        return pygame.Rect(
            self.START_X + x * (self.CARD_SIZE + self.GAP),
            self.START_Y + y * (self.CARD_SIZE + self.GAP),
            self.CARD_SIZE,
            self.CARD_SIZE,
        )

    def _draw_image_center(self, image, rect):
        if image is None:
            return
        cx = rect.x + rect.width//2 - image.get_width()//2
        cy = rect.y + rect.height//2 - image.get_height()//2
        self.screen.blit(image, (cx, cy))

    # --------------------------------------------------------

    def _draw_board(self):
        self.c_lib.get_board_nums(self.nums_arr)
        self.c_lib.get_board_state(self.states_arr)

        self.screen.fill((25, 25, 30))

        title = self.font_big.render("Find Card", True, (240, 240, 240))
        self.screen.blit(title, ((self.screen.get_width() - title.get_width())//2, 10))

        idx = 0
        for y in range(4):
            for x in range(4):
                rect = self._card_rect(x, y)
                state = int(self.states_arr[idx])
                num = int(self.nums_arr[idx])


                if state == 0:  # HIDDEN
                    pygame.draw.rect(self.screen, (80, 80, 80), rect, border_radius=8)
                    pygame.draw.rect(self.screen, (100, 100, 100),
                                     rect.inflate(-10, -10), border_radius=6)

                else:  # OPEN 또는 TEMP
                    pygame.draw.rect(self.screen, (220, 220, 220), rect, border_radius=8)

                    # 이미지 매핑 (DLL 값이 0~7이 아니어도 강제 조정)
                    mapped = num % len(self.symbol_images)
                    image = self.symbol_images[mapped]

                    if image is not None:
                        self._draw_image_center(image, rect)               
                idx += 1

        msg_surf = self.font.render(self.message, True, (240, 240, 240))
        self.screen.blit(
            msg_surf,
            (50, self.START_Y + 4*(self.CARD_SIZE + self.GAP) + 20)
        )

        pygame.display.flip()

    # --------------------------------------------------------

    def run(self):
        if self.game_result is not None:
            return self.game_result

        running = True
        while running:

            if self.click_locked and pygame.time.get_ticks() >= self.lock_until:
                self.click_locked = False

            if self.c_lib.is_finished():
                self.message = "모든 카드를 찾았습니다!"
                self._draw_board()
                pygame.time.wait(1200)
                return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.click_locked:
                        mx, my = event.pos
                        clicked = False

                        for y in range(4):
                            for x in range(4):
                                if self._card_rect(x, y).collidepoint(mx, my):
                                    result = self.c_lib.select_card(x, y)

                                    if result == 2:   # 카드 2개 잠깐 열림
                                        self._draw_board()
                                        pygame.time.wait(700)
                                        self.c_lib.reset_temp()

                                    clicked = True
                                    break
                            if clicked:
                                break

            self._draw_board()
            self.clock.tick(30)

        return self.game_result
