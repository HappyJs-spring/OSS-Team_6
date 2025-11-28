import ctypes
import pygame
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "asset")
DLL_PATH = os.path.join(BASE_DIR, "find_card.dll")


class FindCard:
    CARD_SIZE = 125
    GAP = 26

    BG_TOP = (240, 245, 255)
    BG_BOTTOM = (225, 235, 245)

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.message = ""

        self.SCREEN_W, self.SCREEN_H = self.screen.get_size()

        self.font_big = pygame.font.SysFont("malgun gothic", 60)
        self.font = pygame.font.SysFont("malgun gothic", 26)

        # 이미지 로드 (안전한 여백 제거 포함)
        self.symbol_images = self._load_symbol_images()

        # DLL
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_game()
        except Exception as e:
            print("DLL 로드 실패:", e)
            self.game_result = False
            return

        self.nums_arr = (ctypes.c_int * 16)()
        self.states_arr = (ctypes.c_int * 16)()

        self._calculate_center_positions()

    # ---------------------------------------------------------
    # 중앙 정렬 계산
    # ---------------------------------------------------------
    def _calculate_center_positions(self):
        board_w = self.CARD_SIZE * 4 + self.GAP * 3
        board_h = self.CARD_SIZE * 4 + self.GAP * 3

        self.START_X = (self.SCREEN_W - board_w) // 2
        self.START_Y = (self.SCREEN_H - board_h) // 2

    # ---------------------------------------------------------
    # 안전한 JPG/PNG 여백 제거 (numpy 기반)
    # ---------------------------------------------------------
    def _trim_image_safe(self, img, tolerance=20):
        """배경색(좌상단 픽셀과 비슷한 색) 제거 — PNG/JPG 모두 안정적"""

        arr = pygame.surfarray.pixels3d(img).copy()  # (w,h,3)
        arr = np.transpose(arr, (1, 0, 2))  # (h,w,3)

        h, w, _ = arr.shape
        bg = arr[0, 0]  # 좌상단 색

        # 배경색과 비슷한 픽셀 마스크
        diff = np.abs(arr - bg)
        mask = np.sum(diff, axis=2) > tolerance  # True = 캐릭터

        coords = np.argwhere(mask)

        if coords.size == 0:
            return img  # 트리밍 불가 → 원래 이미지 사용

        y1, x1 = coords.min(axis=0)
        y2, x2 = coords.max(axis=0)

        rect = pygame.Rect(x1, y1, x2 - x1 + 1, y2 - y1 + 1)
        trimmed = img.subsurface(rect).copy()
        return trimmed

    # ---------------------------------------------------------
    # 이미지 로드
    # ---------------------------------------------------------
    def _load_symbol_images(self):
        images = []
        filenames = [
            "images.png","images1.png","images2.png","images3.png",
            "images4.png","images5.png","images6.png","images7.png",
        ]

        for name in filenames:
            path = os.path.join(ASSET_DIR, name)
            try:
                img = pygame.image.load(path).convert_alpha()

                # 🔥 안정적인 여백 제거 적용
                img = self._trim_image_safe(img, tolerance=25)

                images.append(img)
            except Exception as e:
                print("이미지 로드 실패:", name, e)
                images.append(None)

        return images

    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    def _card_rect(self, x, y):
        return pygame.Rect(
            self.START_X + x * (self.CARD_SIZE + self.GAP),
            self.START_Y + y * (self.CARD_SIZE + self.GAP),
            self.CARD_SIZE,
            self.CARD_SIZE,
        )

    # ---------------------------------------------------------
    # 카드 중심에 꽉 차게 이미지 배치
    # ---------------------------------------------------------
    def _draw_image_center(self, image, rect):
        if image:
            padding = 10
            max_w = rect.width - padding * 2
            max_h = rect.height - padding * 2

            img_w, img_h = image.get_size()
            scale_ratio = min(max_w / img_w, max_h / img_h)

            new_w = int(img_w * scale_ratio)
            new_h = int(img_h * scale_ratio)

            scaled = pygame.transform.smoothscale(image, (new_w, new_h))

            cx = rect.x + (rect.width - new_w) // 2
            cy = rect.y + (rect.height - new_h) // 2

            self.screen.blit(scaled, (cx, cy))

    # ---------------------------------------------------------
    def _draw_soft_card(self, rect, state, num):
        shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0,0,0,35), (0,0,rect.width,rect.height), border_radius=28)
        self.screen.blit(shadow, (rect.x, rect.y+5))

        pygame.draw.rect(self.screen, (255,255,255), rect, border_radius=28)
        pygame.draw.rect(self.screen, (200,205,215), rect, width=3, border_radius=28)

        if state == 2:
            pygame.draw.rect(self.screen, (255,210,120), rect, width=5, border_radius=28)
        elif state == 3:
            pygame.draw.rect(self.screen, (150,255,180), rect, width=5, border_radius=28)
        elif state == 1:
            pygame.draw.rect(self.screen, (240,240,240), rect, width=4, border_radius=28)

        if state in (1,2,3):
            img = self.symbol_images[num % len(self.symbol_images)]
            self._draw_image_center(img, rect)

    # ---------------------------------------------------------
    def _draw_background(self):
        w, h = self.SCREEN_W, self.SCREEN_H
        for y in range(h):
            ratio = y / h
            r = int(self.BG_TOP[0] + (self.BG_BOTTOM[0] - self.BG_TOP[0]) * ratio)
            g = int(self.BG_TOP[1] + (self.BG_BOTTOM[1] - self.BG_TOP[1]) * ratio)
            b = int(self.BG_TOP[2] + (self.BG_BOTTOM[2] - self.BG_TOP[2]) * ratio)
            pygame.draw.line(self.screen, (r,g,b), (0,y), (w,y))

    # ---------------------------------------------------------
    def _draw_board(self):
        self.c_lib.get_board_nums(self.nums_arr)
        self.c_lib.get_board_state(self.states_arr)

        self._draw_background()

        title = self.font_big.render("Find Card", True, (80,85,95))
        self.screen.blit(title, ((self.SCREEN_W - title.get_width())//2, 40))

        idx = 0
        for y in range(4):
            for x in range(4):
                rect = self._card_rect(x, y)
                self._draw_soft_card(rect, self.states_arr[idx], self.nums_arr[idx])
                idx += 1

        msg = self.font.render(self.message, True, (60,60,70))
        self.screen.blit(msg, (self.START_X, self.START_Y + 4*(self.CARD_SIZE + self.GAP) + 30))

        pygame.display.flip()

    # ---------------------------------------------------------
    def run(self):
        while True:
            if self.c_lib.is_finished():
                self.message = "성공!"
                self._draw_board()
                pygame.time.wait(1500)
                return True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for y in range(4):
                        for x in range(4):
                            if self._card_rect(x, y).collidepoint(mx, my):
                                r = self.c_lib.select_card(x, y)

                                if r == 2:
                                    self._draw_board()
                                    pygame.time.wait(700)
                                    self.c_lib.reset_temp()
                                break

            self._draw_board()
            self.clock.tick(30)
