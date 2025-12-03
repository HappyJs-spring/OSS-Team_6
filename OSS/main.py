import pygame
import sys
import json
import os 

from hangman import HangmanGame 
from up_down import UpDownGame
from find_card import FindCard
from timer_10 import Timer
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
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# # 모니터 해상도 자동 인식
# info = pygame.display.Info()
# SCREEN_WIDTH = info.current_w
# SCREEN_HEIGHT = info.current_h

# # 전체 화면 모드로 실행
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

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
    # """게임의 순차적인 스토리를 정의하는 메인 함수"""
    
    # # 1  ------------------ <프롤로그> ---------------------------  
    # display_story_text("당신은 충북대학교 컴퓨터공학과 학생입니다. 당일 자정까지 전공과목의 기말대체 과제 제출이 있었으나 깜빡하고 제출하지 못했습니다. 해당 과제를 제출하지 못하면 당신은 F를 받고야 맙니다. 당신은 교수님 몰래 과제를 제출하기 위해 교수님들이 모두 퇴근하신 새벽에 전공 교수님 사무실이 위치한 공과대학 건물에 왔습니다.")

    # display_story_text("나 : (일부러 교수님이 모두 퇴근하신 시간대에 왔으니까. 과제 제출만하면 될꺼야!)")
    # display_story_text("(공대건물 4층으로 조용히 올라간다.)")
    # display_story_text("(당신은 연구실 불이 켜져 있는 것을 보고 깜짝 놀란다.)")
    # display_story_text("나 : 분명 이 시간엔 아무도 없을 거라 생각했는데, 누구지?")
    # display_story_text("(당신은 연구실에서 교수님을 발견한다.)")
    # display_story_text("나 : 이런 교수님이 아직도 퇴근하지 않으셨을 줄이야… 교수님 몰래 과제를 제출하고 빨리 나가야겠어..!")

    # # 2.—---------------------------------------------
    # # 업다운 게임
    # display_story_text("(교수연구실 앞으로 이동한다.)")
    # display_story_text("나 : 이런.. 교수연구실 문이 잠겨있잖아.. 5번 틀리면 경보가 울릴테니 그 전에 숫자를 맞춰야겠어..")
    # display_story_text("교수실 문을 열어라!", 3000)
    
    # game_result_updown = run_game(UpDownGame)
    
    # if game_result_updown == "QUIT":
    #     return
        
    # if game_result_updown is True: # 업다운 승리
    #     display_story_text("잠금해제! 잠긴 문이 열립니다!", 4000)
    # else: # 업다운 패배
    #     display_story_text("문을 여는데 실패했습니다.. 교수님게 발각되어 학점 F를 받게되었습니다.", 4000)
    #     return

    # # 3.—---------------------------------------------
    # # 행맨게임
    # display_story_text("(교수실 문을 여는데 성공했다.)")
    # display_story_text("나 : 후.. 운 좋게 성공했다.")
    # display_story_text("나 : 그나저나. 과제물이 있는 케비넷이 어딨지..?")
    # display_story_text("나 : 찾았다!")
    # display_story_text("(과제물 케비넷이 잠겨있다.)")

    # display_story_text("나 : 이런..! 이번엔 영문자물쇠네.. 오랜 시간을 지체하면 교수님께 들킬거야..!")

    # game_result_hangman = run_game(HangmanGame)
    # if game_result_hangman == "QUIT":
    #     return
    
    # if game_result_hangman is True: # 행맨 승리
    #     display_story_text("성공! 다음 단계를 진행.", 3000)
    # else: # 행맨 패배
    #     display_story_text("실패. 게임 종료.", 4000)
    #     return # 스토리 종료
    
    # # 4.—---------------------------------------------
    # # 올바른 대화 선택지
    # display_story_text("(무사히 과제를 제출하고 교수연구실 밖으로 나왔다.)")
    # display_story_text("나 : 후.. 이번에도 운이 좋았어.. 이제 빨리 나가야겠다.")
    # display_story_text("(복도 끝에서 교수연구실 쪽으로 걸어오는 발소리가 들린다.)")
    # display_story_text("나 : 누군가 온다..! 숨어야 해!")
    # display_story_text("(급하게 오픈소스SW 강의실로 몸을 숨긴다.)")
    # display_story_text("??? : 이 시간에 왜 강의실에 불이 켜져 있지?")
    # display_story_text("(???이 들어온다.)")
    # display_story_text("전공교수님 : 자네. 이 시간까지 강의실에서 뭐하는 건가?")

    # display_story_text("1.강의실에 남아 공부하고 있었었다고 이야기한다.\n
    # 2.과제 제출하러 왔다고 한다.") --------------------------------------------------- 수정

    # //1번
    # display_story_text("나 : 강의실에 남아서 복습하고 있었습니다.");
    # display_story_text("전공교수님 : 훌륭한 학생이군. 열심히 하게.");
    # display_story_text("(전공 교수님이 밖으로 나간다.)");
    # display_story_text("나 : (휴… 살았다..)");

    # //2번
    # display_story_text("나 : 과제 제출하러 왔습니다.");
    # display_story_text("전공교수 : 과제제출은 어제까지 인걸로 알고있는데..?");
    # display_story_text("나 : 하하.. 들켰네.");
    # //게임오버

    # # 5.—---------------------------------------------
    # # 올바른 대화 선택지 2

    # display_story_text("나 : 교수님과 다시 마주치기 전에 빨리 건물을 나가야겠어!")
    # display_story_text("(1층으로 내려가던 중 3층에서 대학원생과 마주쳤다.)")
    # display_story_text("대학원생 : 학생. 이 시간에 학교에는 어쩐일인가?")
    # display_story_text("나 : (아.. 뭐하고 둘러대지?)")
    # display_story_text("1. 공손하게 인사하고 공부하다가 집에 가려고 한다고 말한다.\n2.(말을 무시하고 지나친다)");
    
    # 1번
    # display_story_text("나 : 안녕하세요. 선배님. 강의실에 남아서 공부하다가 집에 가는 중이에요.")
    # display_story_text("대학원생 : 지금 교수님 연구 중이시라 예민하셔. 조심히가렴.")
    # display_story_text("나 : 네. 알겠습니다.")
    # display_story_text("(무사히 학과 건물을 빠져나왔다.)")
    # display_story_text("(갑자기 뒤에서 전공교수님이 뛰어온다.)")
    # display_story_text("전공교수님 : 자네 잠깐만 거기 서 보세..!")
    # display_story_text("나 : (도망친다.)")
    # display_story_text("전공교수님 : 헉헉… 분명 교수연구실 문과 과제물 케비넷이 잠겨있었는데..! 저 학생이 범인이 분명해 꼭 잡고야 말겠어..!")

    # 2번
    # display_story_text("대학원생 : 이 자식봐라 수상한데? 거기 학생 잠깐 나 좀 볼까?");
    # display_story_text("나 : 네..? 저..저요?");
    # display_story_text("대학원생 : 그래. 지금 여기 학생 말고 또 누가 있나?");
    # display_story_text("(갑자기 전공교수님이 뛰어온다)");
    # display_story_text("전공교수님 : 이봐 자네! 그 학생 잡아!")
    # display_story_text("대학원생 : 이 학생이요..?")
    # display_story_text("(대학원생에게 붙잡혔다.)")
    # display_story_text("전공교수 : 이 새벽에 강의실에 혼자 있던 것도 수상했는데, 교수실과 과제 제출 캐비닛까지 열려있다니!")
    # display_story_text("나 : (아.. 망했다)")
    # 게임오버

   
    # '''-------------------------------------
    # <전개, E8-1 건물 나감, 랜덤 이벤트 발생>
    # 랜덤 이벤트 기본은 8개 제작, 이 중 4개 이벤트 발생, 중복 X

    # <설명 : 몇몇 정신을 공격하는 이벤트에 실패하면 
    # 그 자리에서 체력을 모두 잃어 기절하게 된다. 
    # 한 시라도 학교에서 나가야 되는 상황에서 기절하게 되면 
    # 교수님에게 붙잡힐 수 있으니 되도록 이벤트에서 성공해야 한다>
    # —-----------------------------------
    # '''

    # # 1.산책하던 충북대학교 총장과 마주침. -----------------------------------
    # display_story_text("모든 여정이 끝났습니다. 게임을 종료합니다.", 3000)

    # # 2.공업 법규와 창업. 강봉희 교수를 만남 -----------------------------------
    

    # # 3.학연산 (충북 산학협력단 rise와 만남.) -----------------------------------
    

    # # 4.솔못 (커플 피하기 게임) -----------------------------------


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
    game_result_timer = run_game(Timer)

    if game_result_timer == "QUIT":
        return

    if game_result_timer is True:
        display_story_text("10초 맞추기 성공! 단서 +25", 3000)
        player["clue"] += 25
    else:
        display_story_text("10초 맞추기 실패! 체력 -10", 3000)
        player["health"] -= 10

    
    display_story_text("모든 여정이 끝났습니다. 게임을 종료합니다.", 3000)
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