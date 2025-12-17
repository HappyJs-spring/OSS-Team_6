import ctypes
import pygame
import os
from PIL import Image, ImageOps


# =============== 경로 설정 ===============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))     # OSS 폴더
ASSET_DIR = os.path.join(BASE_DIR, "asset")               # OSS/asset
BG_DIR = os.path.join(BASE_DIR, "background")             # OSS/background
BG_PATH = os.path.join(BG_DIR, "coop.jpg")                # OSS/background/coop.jpg
DLL_PATH = os.path.join(BASE_DIR, "find_card.dll")        # OSS/find_card.dll


# =============== EXIF 회전 자동 보정 + Surface 변환 ===============
def load_corrected_background(path, screen_size):
    try:
        img = Image.open(path)

        # EXIF 회전 자동 적용
        img = ImageOps.exif_transpose(img)

        # 화면 크기에 맞게 스케일 변환
        img = img.resize(screen_size)

        # pygame Surface로 변환
        mode = img.mode
        size = img.size
        data = img.tobytes()

        return pygame.image.fromstring(data, size, mode)

    except Exception as e:
        print("배경 이미지 로드 실패:", e)
        return None


class FindCard:
    CARD_SIZE = 125
    GAP = 26

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.message = ""

        self.SCREEN_W, self.SCREEN_H = self.screen.get_size()

        self.font_big = pygame.font.SysFont("malgun gothic", 60)
        self.font = pygame.font.SysFont("malgun gothic", 26)

        # 카드 이미지 로딩
        self.symbol_images = self._load_symbol_images()

        # DLL 초기화
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

        self.flip_pending = False
        self.flip_time = 0

        # 미리보기
        self.preview_mode = True
        self.preview_duration = 2000
        self.preview_end_time = pygame.time.get_ticks() + self.preview_duration

        # ================================
        # 배경 이미지 로드 + 자동 회전 보정
        # ================================
        self.bg_image = load_corrected_background(BG_PATH, (self.SCREEN_W, self.SCREEN_H))

    # ---------------------------------------------------------
    def _calculate_center_positions(self):
        board_w = self.CARD_SIZE * 4 + self.GAP * 3
        board_h = self.CARD_SIZE * 4 + self.GAP * 3
        self.START_X = (self.SCREEN_W - board_w) // 2
        self.START_Y = (self.SCREEN_H - board_h) // 2

    # ---------------------------------------------------------
    def _trim_image_alpha(self, img):
        rect = img.get_bounding_rect()
        return img.subsurface(rect).copy()

    # ---------------------------------------------------------
    def _load_symbol_images(self):
        images = []
        filenames = [
            "images.png", "images1.png", "images2.png", "images3.png",
            "images4.png", "images5.png", "images6.png", "images7.png",
        ]

        for name in filenames:
            path = os.path.join(ASSET_DIR, name)
            try:
                img = pygame.image.load(path).convert_alpha()
                img = self._trim_image_alpha(img)
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


        self.c_lib.is_time_over.restype = ctypes.c_int                    
        self.c_lib.get_remaining_time.restype = ctypes.c_int              
    # ---------------------------------------------------------
    def _card_rect(self, x, y):
        return pygame.Rect(
            self.START_X + x * (self.CARD_SIZE + self.GAP),
            self.START_Y + y * (self.CARD_SIZE + self.GAP),
            self.CARD_SIZE,
            self.CARD_SIZE,
        )

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
        pygame.draw.rect(shadow, (0,0,0,35), shadow.get_rect(), border_radius=28)
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
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((230, 235, 245))

    # ---------------------------------------------------------
    def _draw_board(self):
        self.c_lib.get_board_nums(self.nums_arr)
        self.c_lib.get_board_state(self.states_arr)

        self._draw_background()

        # title = self.font_big.render("Find Card", True, (80,85,95))
        # self.screen.blit(title, ((self.SCREEN_W - title.get_width())//2, 40))

        remaining = self.c_lib.get_remaining_time()    
        timer_text = self.font.render(f"남은 시간: {remaining}초", True, (80, 80, 90))  
        self.screen.blit( 
            timer_text,   
            (self.SCREEN_W - timer_text.get_width() - 40, 40)  
        ) 

        idx = 0
        for y in range(4):
            for x in range(4):
                rect = self._card_rect(x, y)

                state = 1 if self.preview_mode else self.states_arr[idx]
                self._draw_soft_card(rect, state, self.nums_arr[idx])
                idx += 1

        msg = self.font.render(self.message, True, (60,60,70))
        self.screen.blit(msg, (self.START_X, self.START_Y + 4*(self.CARD_SIZE + self.GAP) + 30))

        pygame.display.flip()

    # ---------------------------------------------------------
    def run(self):
        while True:
            if self.c_lib.is_time_over():   
                self.message = "시간 초과!"   
                self._draw_board()  
                pygame.time.wait(1500)  
                return False  

            if self.c_lib.is_finished():
                self.message = "성공!"
                self._draw_board()
                pygame.time.wait(1500)
                return True

            now = pygame.time.get_ticks()

            if self.preview_mode and now >= self.preview_end_time:
                self.preview_mode = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    if self.preview_mode or self.flip_pending:
                        continue

                    mx, my = event.pos

                    for y in range(4):
                        for x in range(4):
                            if self._card_rect(x, y).collidepoint(mx, my):
                                r = self.c_lib.select_card(x, y)


                                if r == 5:
                                    self.message = "시간 초과!"   
                                    self._draw_board()     
                                    pygame.time.wait(1500)  
                                    return False   

                                if r == 2:
                                    self.flip_pending = True
                                    self.flip_time = now + 700
                                break

            if self.flip_pending and pygame.time.get_ticks() >= self.flip_time:
                self.c_lib.reset_temp()
                self.flip_pending = False

            self._draw_board()
            self.clock.tick(60)
