# main.py (스토리 진행 관리)

import pygame
import sys
# 필요한 게임 모듈 임포트
from hangman import HangmanGame # (이전 답변에서 분리한 행맨 클래스)
from up_down import UpDownGame   # (이번에 만든 업다운 클래스)
from dialogue_manager import DialogueManager


# --- 초기 설정 ---
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
    
    # 이 부분이 즉시 실행되어 화면이 전환되어야 합니다.
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
    # 게임 인스턴스 생성 및 실행
    game_instance = GameClass(screen, clock)
    
    # run() 메서드는 True(승리), False(패배), "QUIT" 중 하나를 반환해야 함
    return game_instance.run()


def game_story_sequence():
    """게임의 순차적인 스토리를 정의하는 메인 함수"""
    
    # --- 프롤로그 ---
    display_story_text("e8-1 4층에 조용히 올라간다.")
    display_story_text("올라가보니 연구실에 교수님이 계시는걸 확인한다.")
    display_story_text("교수님께 들키지 않기 위해 조용히 교수실로 갔는데")
    display_story_text("교수실 문이 잠겨있어 업다운 게임으로 교수실 문을 연다.")

    # --- 1단계: (업다운) ---
    display_story_text("교수실 문을 열어라!", 3000)
    
    game_result_updown = run_game(UpDownGame)
    
    if game_result_updown == "QUIT":
        return
        
    if game_result_updown is True: # 업다운 승리 가정
        display_story_text("잠금해제!\n잠긴 문이 열립니다!", 4000)
    else: # 업다운 패배 가정
        display_story_text("문을 여는데 실패했습니다..\n교수님게 발각되어 학점 F를 받게되었습니다.", 4000)
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
    
    if game_result_hangman is True: # 행맨 승리 가정
        display_story_text("성공! 다음 단계를 진행.", 3000)
    else: # 행맨 패배 가정
        display_story_text("실패.\n게임 종료.", 4000)
        return # 스토리 종료
    
    # --- 4단계: 에필로그 ---
    display_story_text("모든 여정이 끝났습니다.\n게임을 종료합니다.", 3000)


if __name__ == "__main__":
    try:
        # 💡 DialogueManager 초기화 시 clock 객체 전달이 필요
        dialogue_box = DialogueManager(screen, font) 
        dialogue_box.clock = clock # clock 객체를 DialogueManager에 전달
        
        game_story_sequence()
    finally:
        pygame.quit()
        sys.exit()