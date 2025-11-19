import ctypes
import pygame
import sys

DLL_PATH = r'C:\Users\mun20\OneDrive\바탕 화면\Coding\OSS\OSS-Team_6\OSS\hangman.dll'

class HangmanGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.message = ""
        self.game_result = None
        
        # 폰트
        self.font_big = pygame.font.SysFont("malgun gothic", 50)
        self.font = pygame.font.SysFont("malgun gothic", 30)

        #DLL 로드 에러검증
        try:
            self.c_lib = ctypes.CDLL(DLL_PATH)
            self._setup_c_functions()
            self.c_lib.init_game()
        except OSError:
            print(f"오류: {DLL_PATH} 파일을 로드할 수 없습니다.")
            self.game_result = False
            
    def _setup_c_functions(self):
        self.c_lib.init_game.restype = None
        self.c_lib.guess_char.argtypes = [ctypes.c_char]
        self.c_lib.guess_char.restype = ctypes.c_int
        self.c_lib.get_current.restype = ctypes.c_char_p
        self.c_lib.get_used.restype = ctypes.c_char_p
        self.c_lib.get_remaining.restype = ctypes.c_int
        self.c_lib.is_finished.restype = ctypes.c_int
        
    def _draw_screen(self):
        #화면 구성
        self.screen.fill((25, 25, 25))
        current = self.c_lib.get_current().decode()
        used = self.c_lib.get_used().decode()
        remaining = self.c_lib.get_remaining()
        
        text_word = self.font_big.render(" ".join(current), True, (255, 255, 255))
        self.screen.blit(text_word, (50, 100))
        text_used = self.font.render(f"Used: {used}", True, (200, 200, 200))
        self.screen.blit(text_used, (50, 200))
        text_life = self.font.render(f"Lives: {remaining}", True, (255, 150, 150))
        self.screen.blit(text_life, (50, 250))
        msg = self.font.render(self.message, True, (255, 255, 100))
        self.screen.blit(msg, (50, 320))
        pygame.display.flip()

    def run(self):
        """행맨 게임의 메인 루프 (핵심 수정 부분)"""
        
        if self.game_result is not None: 
             return self.game_result
             
        running = True
        while running:
            self._draw_screen()

            # 게임 종료 확인
            if self.c_lib.is_finished():
                current_word = self.c_lib.get_current().decode()
                
                #승패 결과 판단 및 저장
                if '_' not in current_word:
                    self.message = "You Won! "
                    self.game_result = True  # 승리 시 True 반환
                else:
                    self.message = "Game Over! You Lost! "
                    self.game_result = False # 패배 시 False 반환
                
                self._draw_screen() 
                pygame.time.wait(3000)
                running = False
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                if event.type == pygame.KEYDOWN:
                    key = event.unicode.lower()
                    if 'a' <= key <= 'z':
                        result = self.c_lib.guess_char(key.encode())
                        if result == 1:
                            self.message = f"Correct! ({key})"
                        elif result == 0:
                            self.message = f"Wrong! ({key})"
                        elif result == 2:
                            self.message = f"Already used: {key}"

            self.clock.tick(30)
        
        return self.game_result # 최종 결과 (True/False) 반환