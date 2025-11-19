import ctypes
import pygame

DLL_PATH = r'C:\Users\mun20\OneDrive\바탕 화면\Coding\OSS\OSS-Team_6\OSS\up_down.dll'

class UpDownGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.input_buffer = ""
        self.message = ""
        self.game_result = None

        # 폰트
        self.font_big = pygame.font.SysFont("malgun gothic", 60)
        self.font = pygame.font.SysFont("malgun gothic", 30)

        #DLL 로드 에러검증
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_game()
        except OSError:
            print(f"오류: {DLL_PATH} 파일을 로드할 수 없습니다. DLL 경로 확인 필요.")
            self.game_result = False
            
    def _setup_c_functions(self):
        self.c_lib.init_game.restype = None
        self.c_lib.guess_number.argtypes = [ctypes.c_int]
        self.c_lib.guess_number.restype = ctypes.c_int
        self.c_lib.get_remaining_attempts.restype = ctypes.c_int
        self.c_lib.get_last_result.restype = ctypes.c_int
        self.c_lib.is_finished.restype = ctypes.c_int
        self.c_lib.get_answer.restype = ctypes.c_int
        
    def _draw_screen(self):
        self.screen.fill((30, 30, 30))

        attempts = self.c_lib.get_remaining_attempts()

        text_title = self.font_big.render("UP & DOWN", True, (255, 255, 255))
        self.screen.blit(text_title, (self.screen.get_width() // 2 - text_title.get_width() // 2, 50))

        text_attempt = self.font.render(f"남은 시도: {attempts}회", True, (255, 200, 200))
        self.screen.blit(text_attempt, (50, 200))

        text_input = self.font.render(f"입력: {self.input_buffer}", True, (200, 255, 200))
        self.screen.blit(text_input, (50, 260))

        text_msg = self.font.render(self.message, True, (255, 255, 100))
        self.screen.blit(text_msg, (50, 330))

        pygame.display.flip()

    def run(self):
        """업다운 게임의 메인 루프"""
        
        # DLL 로드 에러 -> 즉시 종료
        if self.game_result is not None: 
            return self.game_result

        running = True
        while running:
            self._draw_screen()
            
            if self.c_lib.is_finished():
                answer = self.c_lib.get_answer()
                
                # 시도 횟수가 0이면 패배, 아니면 승리 (Correct 메시지 출력 후 is_finished가 True가 됨) -------------------------- 1일 때 시도해서 정답을 적으면 0이 되는데 그때 실패하는 오류가 있음
                if self.c_lib.get_remaining_attempts() == 0:
                     self.message = f"실패! 정답은 {answer}였습니다."
                     self.game_result = False

                elif self.message.startswith("Correct!"):
                     self.message = f"Perfect! 정답: {answer}"
                     self.game_result = True
                
                self._draw_screen()
                pygame.time.wait(3000) # 결과 화면 표시 시간
                running = False
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                if event.type == pygame.KEYDOWN:
                    
                    if event.unicode.isdigit():
                        maxnum = 5  # 최대 입력 길이 제한
                        if len(self.input_buffer) < maxnum:
                            self.input_buffer += event.unicode
                            self.message = ""

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_buffer = self.input_buffer[:-1]
                        self.message = ""

                    elif event.key == pygame.K_RETURN:
                        if not self.input_buffer:
                            self.message = "입력 없음!"
                            continue

                        try:
                            guess = int(self.input_buffer)
                            result = self.c_lib.guess_number(guess)

                            if result == 0: # 정답 (Correct)
                                self.message = f"Correct! {guess}"
                                # running = False # is_finished에서 처리되도록 변경
                            elif result == 1: # Up
                                self.message = "Up! (더 크게!)"
                            elif result == 2: # Down
                                self.message = "Down! (더 작게!)"
                            elif result == 3: # 범위 초과 등 잘못된 입력
                                self.message = "범위 밖의 잘못된 입력입니다."
                        except ValueError:
                             self.message = "유효하지 않은 숫자 입력입니다."
                        finally:
                            self.input_buffer = "" # 입력 후 버퍼 초기화

            self.clock.tick(30)
        
        return self.game_result # 최종 결과 (True/False) 반환