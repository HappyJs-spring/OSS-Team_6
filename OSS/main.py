import pygame
import sys

from hangman import HangmanGame 
from up_down import UpDownGame
from find_card import FindCard

from dialogue_manager import DialogueManager


pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Story Game Sequence")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgun gothic", 40)
dialogue_box = DialogueManager(screen, font)

def display_story_text(text, nexttime = 600):
    """DialogueManager를 사용하여 스토리 텍스트를 표시하고 사용자의 입력을 기다립니다."""
    
    dialogue_box.set_text(text)
    dialogue_box.wait_for_input()
    
    screen.fill((0, 0, 0)) 
    pygame.display.flip()
    
    
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < nexttime:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(30)


def run_game(GameClass):
    """선택된 게임 클래스를 실행하고 결과를 반환합니다."""
    game_instance = GameClass(screen, clock)
    return game_instance.run()


def game_story_sequence():
    """게임의 순차적인 스토리를 정의하는 메인 함수"""
    
    # --- 프롤로그 ---
    display_story_text("e8-1 4층에 조용히 올라간다.")
    display_story_text("올라가보니 연구실에 교수님이 계시는걸 확인한다.")
    display_story_text("교수님께 들키지 않기 위해 조용히 교수실로 갔는데")
    display_story_text("교수실 문이 잠겨있어 업다운 게임으로 교수실 문을 연다.")

    # -- test new game ---
    game_result_findcard = run_game(FindCard)
    
    if game_result_findcard == "QUIT":
        return
    
    if game_result_findcard is True: # 카드 찾기 게임 승리
        display_story_text("성공! 다음 단계를 진행.", 3000)
    else: # 패배
        display_story_text("실패. 게임 종료.", 4000)
        return # 스토리 종료

    # --- 1단계: (업다운) ---
    display_story_text("교수실 문을 열어라!", 3000)
    
    game_result_updown = run_game(UpDownGame)
    
    if game_result_updown == "QUIT":
        return
        
    if game_result_updown is True: # 업다운 승리
        display_story_text("잠금해제! 잠긴 문이 열립니다!", 4000)
    else: # 업다운 패배
        display_story_text("문을 여는데 실패했습니다.. 교수님게 발각되어 학점 F를 받게되었습니다.", 4000)
        return
        
    # --- 2단계: (행맨) ---
    display_story_text("e8-1 4층에 조용히 올라간다.", 2000)
    display_story_text("올라가보니 연구실에 교수님이 계시는걸 확인한다..", 2000)
    display_story_text("교수님께 들키지 않기 위해 조용히 교수실로 갔는데", 2000)
    display_story_text("교수실 문이 잠겨있어 업다운 게임으로 교수실 문을 연다. ", 2000)
    display_story_text("첫 번째 게임: 행맨게임.", 3000)
    
    game_result_hangman = run_game(HangmanGame)
    
    if game_result_hangman == "QUIT":
        return
    
    if game_result_hangman is True: # 행맨 승리
        display_story_text("성공! 다음 단계를 진행.", 3000)
    else: # 행맨 패배
        display_story_text("실패. 게임 종료.", 4000)
        return # 스토리 종료
    
    # --- 4단계: 에필로그 ---
    display_story_text("모든 여정이 끝났습니다. 게임을 종료합니다.", 3000)


if __name__ == "__main__":
    try:
        dialogue_box = DialogueManager(screen, font) 
        dialogue_box.clock = clock
        
        game_story_sequence()
    finally:
        pygame.quit()
        sys.exit()