import ctypes
import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "up_down.dll")

class UpDownGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.input_buffer = ""
        self.message = ""
        self.game_result = None

        # 폰트 (pygame.init()은 main에서 이미 호출되었다고 가정)
        self.font_big = pygame.font.SysFont("malgun gothic", 80)
        self.font_mid = pygame.font.SysFont("malgun gothic", 60)
        self.font = pygame.font.SysFont("malgun gothic", 30)

        # 이미지 관련 초기값
        self.lock_img = None
        self.person_img = None
        self.images_ok = False

        # 이미지 로드(안전하게)
        try:
            lock_path = os.path.join(BASE_DIR, "images1.png")
            person_path = os.path.join(BASE_DIR, "images2.png")
            if not os.path.isfile(lock_path):
                raise FileNotFoundError(f"{lock_path} not found")
            if not os.path.isfile(person_path):
                raise FileNotFoundError(f"{person_path} not found")

            self.lock_img = pygame.image.load(lock_path).convert_alpha()
            self.person_img = pygame.image.load(person_path).convert_alpha()

            # 크기 조정 (화면 크기 따라 상대적 조정 원하면 변경)
            self.lock_img = pygame.transform.smoothscale(self.lock_img, (240, 380))
            self.person_img = pygame.transform.smoothscale(self.person_img, (260, 350))
            self.images_ok = True
        except Exception as e:
            # 파일 없거나 로드 실패하면 에러 출력하고 도형으로 대체
            print("이미지 로드 오류:", e)
            print("이미지가 없으므로 도형으로 대체하여 그립니다.")
            self.images_ok = False

        # DLL 로드
        self.dll_loaded = False
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_game()
            self.dll_loaded = True
        except OSError as e:
            print(f"오류: {DLL_PATH} 파일을 로드할 수 없습니다. DLL 경로 확인 필요.")
            print("세부:", e)
            # self.game_result = False  <-- 제거: 즉시 종료되지 않도록 함
            self.c_lib = None

    def _setup_c_functions(self):
        # C 함수들의 인자 타입 및 반환 타입 설정
        self.c_lib.init_game.restype = None
        self.c_lib.guess_number.argtypes = [ctypes.c_int]
        self.c_lib.guess_number.restype = ctypes.c_int
        self.c_lib.get_remaining_attempts.restype = ctypes.c_int
        self.c_lib.get_last_result.restype = ctypes.c_int
        self.c_lib.is_finished.restype = ctypes.c_int
        self.c_lib.get_answer.restype = ctypes.c_int

    def _draw_screen(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        self.screen.fill((255, 255, 255))

        # 제목
        title = self.font_big.render("UP & DOWN GAME", True, (0, 0, 0))
        self.screen.blit(title, (w//2 - title.get_width()//2, 40))

        # 이미지가 준비되어 있으면 blit, 아니면 도형으로 대체
        lock_x, lock_y = 80, 150
        if self.images_ok and self.lock_img:
            self.screen.blit(self.lock_img, (lock_x, lock_y))
        else:
            # 도형으로 대체(간단한 자물쇠 모양)
            pygame.draw.rect(self.screen, (200, 200, 200), (lock_x, lock_y, 240, 380), border_radius=40)
            # 버튼
            btn_w, btn_h = 50, 50
            for row in range(4):
                for col in range(3):
                    bx = lock_x + 25 + col * 60
                    by = lock_y + 40 + row * 60
                    pygame.draw.rect(self.screen, (90, 100, 110), (bx, by, btn_w, btn_h), border_radius=10)
            pygame.draw.rect(self.screen, (70, 80, 100), (lock_x + 20, lock_y + 260, 200, 65), border_radius=25)

        person_x, person_y = w - 350, 150
        if self.images_ok and self.person_img:
            self.screen.blit(self.person_img, (person_x, person_y))
        else:
            # 도형 대체(사람 실루엣)
            pygame.draw.circle(self.screen, (40, 30, 30), (person_x + 125, person_y + 80), 70)
            pygame.draw.ellipse(self.screen, (40, 30, 30), (person_x + 45, person_y + 130, 160, 200))
            # 배경 점들 (고정 시드)
            import random
            random.seed(0)
            for _ in range(80):
                sx = person_x + random.randint(-30, 230)
                sy = person_y + random.randint(20, 260)
                pygame.draw.circle(self.screen, (120, 120, 120), (sx, sy), random.randint(6, 12))

        # 안내문 / 입력 / 메시지
        guide = self.font_mid.render("비밀번호를 입력하세요:", True, (0, 0, 0))
        self.screen.blit(guide, (w//2 - guide.get_width()//2, 230))

        input_text = self.font_mid.render(self.input_buffer if self.input_buffer else "_ _", True, (0, 0, 0))
        self.screen.blit(input_text, (w//2 - input_text.get_width()//2, 320))

        msg = self.font.render(self.message, True, (60, 60, 60))
        self.screen.blit(msg, (w//2 - msg.get_width()//2, 420))

        # 남은 시도 (DLL 없으면 '-' 표시)
        attempts_str = "-"
        if self.dll_loaded and self.c_lib:
            try:
                attempts_str = str(self.c_lib.get_remaining_attempts())
            except Exception:
                attempts_str = "?"
        attempt_text = self.font.render(f"남은 시도: {attempts_str}회", True, (60, 60, 60))
        self.screen.blit(attempt_text, (w//2 - attempt_text.get_width()//2, 480))


        pygame.display.flip()

    def run(self):
        """업다운 게임의 메인 루프"""
        # DLL이 전혀 로드되지 않았다면 실행시키기 전에 상위에서 처리하도록 할 수도 있음.
        if not self.dll_loaded:
            print("경고: DLL이 로드되지 않았습니다. 게임 로직이 동작하지 않을 수 있습니다.")
            # 여기서 바로 return하지 않음 — 화면은 보이게 함.

        running = True
        while running:
            self._draw_screen()

            # 안전하게 DLL 호출 (로드되지 않았으면 skip)
            if self.dll_loaded and self.c_lib and self.c_lib.is_finished():
                answer = self.c_lib.get_answer()
                if self.c_lib.get_remaining_attempts() == 0:
                    self.message = f"Game Over! 실패! 정답은 {answer}였습니다."
                    self.game_result = False
                else:
                    self.message = f"Perfect! 정답: {answer}"
                    self.game_result = True

                self._draw_screen()
                pygame.time.wait(1500)
                running = False
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    if event.unicode and event.unicode.isdigit():
                        if len(self.input_buffer) < 5:
                            self.input_buffer += event.unicode
                            self.message = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_buffer = self.input_buffer[:-1]
                        self.message = ""
                    elif event.key == pygame.K_RETURN:
                        if not self.input_buffer:
                            self.message = "입력 없음!"
                            continue

                        # DLL이 없으면 로컬 체크 (테스트용 랜덤)
                        if not self.dll_loaded or not self.c_lib:
                            # 임시 동작: 1~100 사이 랜덤 정답 시뮬
                            try:
                                guess = int(self.input_buffer)
                                # 단순 시뮬: 50을 정답으로 가정
                                correct = 50
                                if guess == correct:
                                    self.message = f"Correct! {guess}"
                                    self.game_result = True
                                    self._draw_screen()
                                    pygame.time.wait(1200)
                                    return True
                                elif guess < correct:
                                    self.message = "Up! (더 크게!)"
                                else:
                                    self.message = "Down! (더 작게!)"
                            except ValueError:
                                self.message = "유효하지 않은 숫자 입력입니다."
                            finally:
                                self.input_buffer = ""
                            continue

                        # 실제 DLL이 있는 경우
                        try:
                            guess = int(self.input_buffer)
                            result = self.c_lib.guess_number(guess)
                            # C 라이브러리의 반환값 규약에 따라 처리
                            if result == 0:
                                self.message = f"Correct! {guess}"
                                # 즉시 승리 처리 (DLL 내부에서 is_finished가 true가 됨)
                                self.game_result = True
                                self._draw_screen()
                                pygame.time.wait(1200)
                                return True
                            elif result == 1:
                                self.message = "Up! (더 크게!)"
                            elif result == 2:
                                self.message = "Down! (더 작게!)"
                            elif result == 3:
                                self.message = "범위 밖의 잘못된 입력입니다."
                            else:
                                self.message = f"알 수 없는 반환값: {result}"
                        except ValueError:
                            self.message = "유효하지 않은 숫자 입력입니다."
                        except Exception as e:
                            self.message = f"오류: {e}"
                            print("guess_number 호출 오류:", e)
                        finally:
                            self.input_buffer = ""

            self.clock.tick(30)

        return self.game_result
