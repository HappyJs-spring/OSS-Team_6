import pygame
import sys
import json # 추가
import os # 추가

from hangman import HangmanGame 
from up_down import UpDownGame
from find_card import FindCard
from dialogue_manager import DialogueManager

def draw_player_status(screen, font, player):
    health_surf = font.render(f"HP: {player['health']}", True, (255, 50, 50))
    clue_surf = font.render(f"Clue: {player['clue']}", True, (255, 255, 0))

    x = SCREEN_WIDTH - 200
    y = 20

    pygame.draw.rect(screen, (0, 0, 0), (x - 20, y - 20, 180, 100))
    pygame.draw.rect(screen, (255, 255, 255), (x - 20, y - 20, 180, 100), 2)

    screen.blit(health_surf, (x, y))
    screen.blit(clue_surf, (x, y + 40))


BASE = os.path.dirname(os.path.abspath(__file__))  # main.py가 있는 폴더
json_path = os.path.join(BASE, "test", "game.json")  # test/game.json을 지정

with open(json_path, "r", encoding="utf-8") as f:
    GAME_DATA = json.load(f)


player = GAME_DATA["player"]  


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

    draw_player_status(screen, font, player)
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
    
    # 1 —--------------------------------------------- <프롤로그>
    display_story_text("e8-1 4층에 조용히 올라간다.");
    display_story_text("올라가보니 연구실에 교수님이 계시는걸 확인한다.")
    display_story_text("교수님께 들키지 않기 위해 조용히 교수실로 갔는데")
    display_story_text("교수실 문이 잠겨있어 업다운 게임으로 교수실 문을 연다.")

    # 2.—---------------------------------------------
    
    # 3.—---------------------------------------------
    # (업다운 게임)
    display_story_text("교수실 문을 열어라!", 3000)
    
    game_result_updown = run_game(UpDownGame)
    
    if game_result_updown == "QUIT":
        return
        
    if game_result_updown is True: # 업다운 승리
        display_story_text("잠금해제! 잠긴 문이 열립니다!", 4000)
    else: # 업다운 패배
        display_story_text("문을 여는데 실패했습니다.. 교수님게 발각되어 학점 F를 받게되었습니다.", 4000)
        return
    
    # 4.—---------------------------------------------
    # (행맨게임)
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

    # 5.—---------------------------------------------


    # 6.—---------------------------------------------
   
    '''-------------------------------------
    <전개, E8-1 건물 나감, 랜덤 이벤트 발생>
    랜덤 이벤트 기본은 8개 제작, 이 중 4개 이벤트 발생, 중복 X

    <설명 : 몇몇 정신을 공격하는 이벤트에 실패하면 
    그 자리에서 체력을 모두 잃어 기절하게 된다. 
    한 시라도 학교에서 나가야 되는 상황에서 기절하게 되면 
    교수님에게 붙잡힐 수 있으니 되도록 이벤트에서 성공해야 한다>
    —-----------------------------------
    '''

    # 1.산책하던 충북대학교 총장과 마주침. -----------------------------------
    display_story_text("모든 여정이 끝났습니다. 게임을 종료합니다.", 3000)

    # 2.공업 법규와 창업. 강봉희 교수를 만남 -----------------------------------
    

    # 3.학연산 (충북 산학협력단 rise와 만남.) -----------------------------------
    

    # 4.솔못 (데이트 중인 커플만나기) -----------------------------------


    # 5.coopsket (1+1 삼김 짝 맞추기) -----------------------------------
    game_result_findcard = run_game(FindCard)
    
    if game_result_findcard == "QUIT":
        return
    
    if game_result_findcard is True: # 카드 찾기 게임 승리 
        display_story_text("성공! 다음 단계를 진행.", 3000)
    else: # 패배
        display_story_text("실패. 게임 종료.", 4000)
        return # 스토리 종료
    
    # 6. B:last 홍보 부스 (10초에 맞춰 버튼 입력하는 게임) -----------------------------------
    

    # 7.중도 앞 길가에서 쓰레기 발견 (중도 앞 길가에서 쓰레기를 발견함)-----------------------------------
    

    # 8.중문에서 나타나는 보드게임 중독(홀덤 중독자) 학과 동기와 만남-----------------------------------
    

    # 9. 엔딩-----------------------------------



if __name__ == "__main__":
    try:
        dialogue_box = DialogueManager(screen, font) 
        dialogue_box.clock = clock
        
        game_story_sequence()
    finally:
        pygame.quit()
        sys.exit()