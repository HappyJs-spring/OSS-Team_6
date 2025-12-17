import pygame
import sys
import json
import os 
from start_screen import start_screen
from ending_screen import show_ending
from clue_popup import show_clue_popup
import random

from hangman import HangmanGame 
from up_down import UpDownGame
from find_card import FindCard
from timer_10 import Timer
from BR31 import BR31
from music import MusicGame

from dialogue_manager import DialogueManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
CLUE_IMG_PATH = os.path.join(PROJECT_ROOT, "OSS", "UI", "Status", "clue.png")

def gain_clue(player, amount=25):
    player["clue"] = min(100, player["clue"] + amount)


def get_clue_level(player):
    return min(4, player["clue"] // 25)


def check_ending():
    # 1. 배드 엔딩 (체력 0)
    if player["health"] <= 0:
        show_ending(screen, "bad", display_story_text)
        pygame.quit()
        sys.exit()

    # 탈출 안 했으면 아직 엔딩 아님
    if not player.get("escaped", False):
        return

    # 2. 히든 엔딩 (체력 > 0 && 단서 4개)
    if player["clue"] >= 100:
        show_ending(screen, "hidden", display_story_text)

        pygame.quit()
        sys.exit()

    # 3. 해피 엔딩 (체력 > 0 && 단서 부족)
    show_ending(screen, "happy", display_story_text)

    pygame.quit()
    sys.exit()



def change_health(amount):
    player["health"] += amount
    player["health"] = max(0, min(100, player["health"]))
    check_ending()




def draw_wrapped_text(surface, text, font, color, rect, line_spacing=6):
    """
    한국어 대응 자동 줄바꿈 + \n 개행 지원
    rect 영역을 넘지 않도록 렌더링
    """
    max_width = rect.width - 30
    x = rect.x + 15
    y = rect.y + 15

    lines = []

    for paragraph in text.split("\n"):
        current_line = ""
        for char in paragraph:
            test_line = current_line + char
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = char
        lines.append(current_line)

    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (x, y))
        y += rendered.get_height() + line_spacing

        # 박스 높이 초과 시 중단 (안 넘치게)
        if y > rect.bottom - 10:
            break


def choice_dialogue(options):
    """
    options: ["선택지1", "선택지2", ..., "선택지N"]
    return: 선택된 index (0부터 시작)
    """
    box_width = 900
    box_height = 90
    gap = 15

    total_height = len(options) * box_height + (len(options) - 1) * gap
    start_y = SCREEN_HEIGHT - total_height - 40

    boxes = []
    for i in range(len(options)):
        rect = pygame.Rect(
            SCREEN_WIDTH // 2 - box_width // 2,
            start_y + i * (box_height + gap),
            box_width,
            box_height
        )
        boxes.append(rect)

    selected = 0
    blink_alpha = 0
    blink_dir = 1
    clock_local = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        hover_index = -1
        for i, rect in enumerate(boxes):
            if rect.collidepoint(mouse_pos):
                hover_index = i
                selected = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    idx = event.key - pygame.K_1
                    if idx < len(options):
                        return idx

                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return selected

            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover_index != -1:
                    return hover_index

        # 깜빡임
        blink_alpha += blink_dir * 6
        if blink_alpha >= 120 or blink_alpha <= 40:
            blink_dir *= -1

        # ===== 배경 =====
        screen.blit(background, (0, 0))

        if character is not None:
            x = (SCREEN_WIDTH - character.get_width()) // 2
            y = SCREEN_HEIGHT - character.get_height()
            screen.blit(character, (x, y))

        # ===== 선택지 =====
        for i, rect in enumerate(boxes):
            hovered = (i == selected)

            base_color = (40, 40, 40)
            hover_color = (90, 90, 90)

            pygame.draw.rect(
                screen,
                hover_color if hovered else base_color,
                rect,
                border_radius=16
            )

            if hovered:
                border_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
                pygame.draw.rect(
                    border_surface,
                    (255, 255, 255, blink_alpha),
                    border_surface.get_rect(),
                    4,
                    border_radius=16
                )
                screen.blit(border_surface, rect.topleft)
            else:
                pygame.draw.rect(
                    screen,
                    (180, 180, 180),
                    rect,
                    2,
                    border_radius=16
                )

            draw_wrapped_text(
                screen,
                f"{i+1}. {options[i]}",
                font,
                (255, 255, 255),
                rect
            )

        draw_player_status(screen, font, player)

        pygame.display.flip()
        clock_local.tick(60)




def draw_player_status(screen, font, player):
    # 단서 단계 계산
    clue_level = get_clue_level(player)

    # 단계에 맞는 status 이미지 선택
    status_img = STATUS_IMAGES[clue_level]

    img_w, img_h = status_img.get_size()

    # 화면 오른쪽 상단
    x = SCREEN_WIDTH - img_w - 20
    y = 20

    # UI 이미지
    screen.blit(status_img, (x, y))


    # 체력바 설정
    max_hp = 100
    current_hp = player['health']
    hp_ratio = max(0, current_hp / max_hp)

    bar_x = x + 80
    bar_y = y + 45
    bar_width = 120
    bar_height = 14

    # 배경 바
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (bar_x, bar_y, bar_width, bar_height)
    )

    # 체력 바 색상
    if hp_ratio > 0.6:
        color = (0, 200, 0)
    elif hp_ratio > 0.3:
        color = (255, 200, 0)
    else:
        color = (200, 0, 0)

    # 현재 체력
    pygame.draw.rect(
        screen,
        color,
        (bar_x, bar_y, bar_width * hp_ratio, bar_height)
    )

    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (bar_x, bar_y, bar_width, bar_height),
        2
    )




BASE = os.path.dirname(os.path.abspath(__file__))  # main.py가 있는 폴더
json_path = os.path.join(BASE, "test", "game.json")  # test/game.json을 지정

with open(json_path, "r", encoding="utf-8") as f:
    GAME_DATA = json.load(f)


player = GAME_DATA["player"]  


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
start_screen(screen)

pygame.display.set_caption("Story Game Sequence")
clock = pygame.time.Clock()
font = pygame.font.SysFont("malgun gothic", 40)

# 상태창 이미지 로드
STATUS_DIR = os.path.join(BASE, "UI", "Status")
STATUS_WIDTH = 300
STATUS_HEIGHT = 180

STATUS_IMAGES = {}

for i in range(5):
    path = os.path.join(STATUS_DIR, f"status_{i}.PNG")
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.smoothscale(img, (STATUS_WIDTH, STATUS_HEIGHT))
    STATUS_IMAGES[i] = img


# # 모니터 해상도 자동 인식 
# info = pygame.display.Info()
# SCREEN_WIDTH = info.current_w
# SCREEN_HEIGHT = info.current_h

# # 전체 화면 모드로 실행
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

dialogue_box = DialogueManager(screen, font)

def display_story_text(text, nexttime=600, bg=None, ch=None):
    global background
    global character

    # --- 배경 처리 ---
    if isinstance(bg, str):
        if bg in backgrounds:
            background = backgrounds[bg]
        else:
            print(f"[WARNING] 배경 '{bg}' 파일이 없습니다.")
    elif bg is not None:
        background = bg

    # --- 캐릭터 처리 ---
    if isinstance(ch, str):
        if ch in characters:
            character = characters[ch]
        elif ch is None:
            character = None
        else:
            print(f"[WARNING] 캐릭터 '{ch}' 파일이 없습니다.")
    elif ch is not None:
        character = ch   # Surface 직접 넣기 가능

    dialogue_box.set_text(text)
    dialogue_box.wait_for_input()

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < nexttime:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- 배경 출력 ---
        screen.blit(background, (0, 0))

        # --- 캐릭터 출력 (배경 위 / 대사창 아래에 위치해야 자연스러움) ---
    if character is not None:
        x = (SCREEN_WIDTH - character.get_width()) // 2    # 가운데 정렬
        y = SCREEN_HEIGHT - character.get_height()         # 하단에 위치
        screen.blit(character, (x, y))

        # --- 대사창 ---
        dialogue_box.draw()

        # --- HUD ---
        draw_player_status(screen, font, player)

        pygame.display.flip()
        clock.tick(60)




def run_game(GameClass):
    """선택된 게임 클래스를 실행하고 결과를 반환합니다."""
    game_instance = GameClass(screen, clock)
    return game_instance.run()

# ==== 배경 자동 로드 시스템 ====
# ==== 배경 자동 로드 시스템 ====


BACKGROUND_DIR = os.path.join(BASE, "background")

backgrounds = {}  # {"e8-1(1)": Surface, ...}

for root, dirs, files in os.walk(BACKGROUND_DIR):
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(root, file)

            # key = 예: “e8-1(1)”  <-- 폴더 상관없이 파일 이름으로 접근 가능
            key = os.path.splitext(file)[0]

            img = pygame.image.load(full_path)
            img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

            backgrounds[key] = img

print("[INFO] Loaded backgrounds:", list(backgrounds.keys()))

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill((0, 0, 0))   # 기본 배경 = 검정색 (필요 없으면 삭제)

CHAR_DIR = os.path.join(BASE, "character")
characters = {}   # {"hero_smile": Surface, ...}

for root, dirs, files in os.walk(CHAR_DIR):
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(root, file)

            key = os.path.splitext(file)[0]  # "hero_smile" 같은 이름

            img = pygame.image.load(full_path).convert_alpha()
        
            max_height = int(SCREEN_HEIGHT * 1.0)  # 화면 높이의 70%
            scale_ratio = max_height / img.get_height()
            new_width = int(img.get_width() * scale_ratio)

            img = pygame.transform.smoothscale(img, (new_width, max_height))

            characters[key] = img

print("[INFO] Loaded characters:", list(characters.keys()))

character = None   # 현재 화면에 표시될 캐릭터 Surface


def game_story_sequence():
    # # """게임의 순차적인 스토리를 정의하는 메인 함수"""

    # 1  ------------------ <프롤로그> ---------------------------  
    display_story_text("당신은 충북대학교 컴퓨터공학과 학생입니다. 당일 자정까지 전공과목의 기말대체 과제 제출이 있었으나 깜빡하고 제출하지 못했습니다.")
    display_story_text("해당 과제를 제출하지 못하면 당신은 F를 받고야 맙니다.")
    display_story_text("당신은 교수님 몰래 과제를 제출하기 위해 교수님들이 모두 퇴근하신 새벽에 전공 교수님 사무실이 위치한 공과대학 건물에 왔습니다.")

    display_story_text("나 : (일부러 교수님이 모두 퇴근하신 시간대에 왔으니까. 과제 제출만하면 될꺼야!)", bg="e8-1(3rd stairs)")
    display_story_text("(공대건물 4층으로 조용히 올라간다.)", bg="e8-1(6)")
    display_story_text("(당신은 연구실 불이 켜져 있는 것을 보고 깜짝 놀란다.)")
    display_story_text("나 : 분명 이 시간엔 아무도 없을 거라 생각했는데, 누구지?")
    display_story_text("(당신은 연구실에서 교수님을 발견한다.)")
    display_story_text("나 : 이런 교수님이 아직도 퇴근하지 않으셨을 줄이야… 교수님 몰래 과제를 제출하고 빨리 나가야겠어..!")

    # 2.—---------------------------------------------
    # 업다운 게임
    display_story_text("(교수연구실 앞으로 이동한다.)", 600, bg="e8-1(2)")
    display_story_text("나 : 이런.. 교수연구실 문이 잠겨있잖아.. 5번 틀리면 경보가 울릴테니 그 전에 숫자를 맞춰야겠어..")
    display_story_text("교수실 문을 열어라!", 3000)
    
    game_result_updown = run_game(UpDownGame)
    
    if game_result_updown == "QUIT":
        return
        
    if game_result_updown is True: # 업다운 승리
        display_story_text("잠금해제! 잠긴 문이 열립니다!", 3000)
    else: # 업다운 패배
        display_story_text('자네 거기서 지금 뭐하는건가!')
        display_story_text("문을 여는데 실패했습니다.. 교수님게 발각되어 학점 F를 받게되었습니다.", 3000)
        return

    # 3.—---------------------------------------------
    # 행맨게임
    display_story_text("(교수실 문을 여는데 성공했다.)")
    display_story_text("나 : 후.. 운 좋게 성공했다.")
    display_story_text("나 : 그나저나. 과제물이 있는 케비넷이 어딨지..?")
    display_story_text("나 : 찾았다!")
    display_story_text("(과제물 케비넷이 잠겨있다.)")

    display_story_text("나 : 이런..! 이번엔 영문자물쇠네.. 오랜 시간을 지체하면 교수님께 들킬거야..!")
 
    game_result_hangman = run_game(HangmanGame)
    if game_result_hangman == "QUIT":
        return
    
    if game_result_hangman is True: # 행맨 승리
        display_story_text("(철컥)")
        display_story_text("열렸다!")
        display_story_text("(자물쇠를 해제 하였습니다)", 3000)
    else: # 행맨 패배
        display_story_text('자네 거기서 지금 뭐하는건가!')
        display_story_text("문을 여는데 실패했습니다.. 교수님게 발각되어 학점 F를 받게되었습니다.", 3000)
        return # 스토리 종료
    
    # # 4.—---------------------------------------------
    # # 올바른 대화 선택지
    
    display_story_text("(무사히 과제를 제출하고 교수연구실 밖으로 나왔다.)")
    display_story_text("나 : 후.. 이번에도 운이 좋았어.. 이제 빨리 나가야겠다.")
    display_story_text("(복도 끝에서 교수연구실 쪽으로 걸어오는 발소리가 들린다.)", bg="e8-1(6)")
    display_story_text("나 : 누군가 온다..! 숨어야 해!", bg="e8-1(1)")
    display_story_text("(급하게 오픈소스SW 강의실로 몸을 숨긴다.)", bg="e8-1(4)")
    display_story_text("??? : 이 시간에 왜 강의실에 불이 켜져 있지?", ch="professor")
    display_story_text("(???이 들어온다.)")
    display_story_text("전공교수님 : 자네. 이 시간까지 강의실에서 뭐하는 건가?")

    choice1 = choice_dialogue([
    "강의실에 남아 공부하고 있었다고 이야기한다.",
    "과제 제출하러 왔다고 말한다."
    ])

    if choice1 == 0:
            display_story_text("나 : 강의실에 남아서 복습하고 있었습니다.", ch="professor_smile")
            display_story_text("전공교수님 : 훌륭한 학생이군. 열심히 하게.", ch="clear")
            display_story_text("(전공 교수님이 밖으로 나간다.)")
            display_story_text("나 : (휴… 살았다..)")

    elif choice1 == 1:
        display_story_text("나 : 과제 제출하러 왔습니다.", ch="professor_angry")
        display_story_text("전공교수 : 과제제출은 어제까지 인걸로 알고있는데..?")
        display_story_text("나 : 하하.. 들켰네.")
        display_story_text("교수님게 발각되어 학점 F를 받게되었습니다.", 3000)
        return


    # # 5.—---------------------------------------------
    # # 올바른 대화 선택지 2

    display_story_text("나 : 교수님과 다시 마주치기 전에 빨리 건물을 나가야겠어!", bg="e8-1(3rd floor)")
    display_story_text("(1층으로 내려가던 중 3층에서 대학원생과 마주쳤다.)", ch="grad_student")
    display_story_text("대학원생 : 학생. 이 시간에 학교에는 어쩐일인가?")
    display_story_text("나 : (아.. 뭐라고 둘러대지?)")
    
    choice2 = choice_dialogue([
    "강의실에 남아 공부하고 있었다고 이야기한다.",
    "과제 제출하러 왔다고 말한다."
    ])

    if choice2 == 0:
        display_story_text("나 : 안녕하세요. 선배님. 강의실에 남아서 공부하다가 집에 가는 중이에요.", ch="grad_student_smile")
        display_story_text("대학원생 : 지금 교수님 연구 중이시라 예민하셔. 조심히가렴.", ch="clear")
        display_story_text("나 : 네. 알겠습니다.", bg="e8-1외부")
        display_story_text("(무사히 학과 건물을 빠져나왔다.)", ch="professor_embarrassed")
        display_story_text("(갑자기 뒤에서 전공교수님이 뛰어온다.)")
        display_story_text("전공교수님 : 자네 잠깐만 거기 서 보세..!")
        display_story_text("나 : (도망친다.)")
        display_story_text("전공교수님 : 헉헉… 분명 교수연구실 문과 과제물 케비넷이 잠겨있었는데..! 저 학생이 범인이 분명해 꼭 잡고야 말겠어..!", ch="clear")

    elif choice2 == 1:
        display_story_text("대학원생 : 이 자식봐라 수상한데? 거기 학생 잠깐 나 좀 볼까?", ch="grad_student_angry")
        display_story_text("나 : 네..? 저..저요?")
        display_story_text("대학원생 : 그래. 지금 여기 학생 말고 또 누가 있나?")
        display_story_text("(갑자기 전공교수님이 뛰어온다)")
        display_story_text("전공교수님 : 이봐 자네! 그 학생 잡아!", ch="grad_student_embrrassed")
        display_story_text("대학원생 : 이 학생이요..?")
        display_story_text("(대학원생에게 붙잡혔다.)", ch="professor_angry")
        display_story_text("전공교수 : 이 새벽에 강의실에 혼자 있던 것도 수상했는데, 교수실과 과제 제출 캐비닛까지 열려있다니!")
        display_story_text("나 : (아.. 망했다)")
        display_story_text("교수님게 발각되어 학점 F를 받게되었습니다.", 3000)
        return

   
    # -------------------------------------
    # <전개, E8-1 건물 나감, 랜덤 이벤트 발생>
    # 랜덤 이벤트 기본은 8개 제작, 이 중 4개 이벤트 발생, 중복 X
    lst = [1, 2, 3, 4, 5, 6, 7, 8]
    play = random.sample(lst, 4)

    for i in play:
        if i == 1:
            display_story_text('교수님께 잡히면 안되니 최대한 빨리 학교를 나가야해!.', bg="e8-1외부")
            display_story_text('(몇몇 정신을 공격하는 이벤트에 실패하면 그 자리에서 체력을 모두 잃어 기절하게 된다.)')
            display_story_text('(기절하게 되면 교수님에게 붙잡힐 수 있으니 되도록 이벤트를 성공해야 한다.)')
            # —-----------------------------------
            # '''

            # # 1.산책하던 충북대학교 총장과 마주침. -----------------------------------
            display_story_text("(멀리서 조용한 충북대 캠퍼스에서 한 사람의 실루엣이 보인다. 그가 다가왔다.)", bg="솔못", ch="president")
            display_story_text("총장 : 어? 이 시간에 학생이 여길 왜 다니고 있지?")
            display_story_text("총장 : 혹시… 나를 알아보겠나?")
            display_story_text("나 : 아..! 총장님..! (왜 하필 지금…!) 네, 당연하죠.")
            display_story_text("총장 : 그렇다면 내 이름이 무엇인지 말해보게.")
            display_story_text("(초성 : ㄱㅊㅅ)")

            choice3 = choice_dialogue([
            "김창섭",
            "고창섭",
            "김치신",
            "강창섭",
            "구창섭"
            ])

            if choice3 == 1:
                display_story_text("총장 : 흠… 정확하게 알고 있군!", ch="president_smile")
                display_story_text("(기분이 좋아져 미소를 짓는다)")
                display_story_text("총장 : 이 정도면 우리 학교 학생으로서 충분히 자랑스럽네.")
                display_story_text("총장 : 오늘 만난 것도 인연이지. 자네에게 작은 도움을 주도록 하지.", ch="clear")
                display_story_text("(딱히 도움이 되진 않으나 총장의 호감도가 상승했다.)")
                display_story_text("(단서 획득!)")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )

            else:
                display_story_text("총장 : …흠. 그렇군.", ch="president_disappointed")
                display_story_text("(씁쓸한 표정을 짓는다.)")
                display_story_text("총장 : 내 이름도 모르는 학생이 요즘 왜 이렇게 많나… 하여간… 에휴…", ch="clear")
                display_story_text("(총장이 실망했다. 하지만 딱히 상관은 없다.)")

        elif i == 2:
            # # 2.공업 법규와 창업. 강봉희 교수를 만남 -----------------------------------
            display_story_text("(학연산 건물 앞을 지나가던 도중, 공업법규와 창업 강봉희 교수님을 만났다.)", bg="학연산", ch="monica")
            display_story_text("강봉희 교수님 : 어이 학생. 잠깐 거기 서봐.")
            display_story_text("(당황하며 얼어붙는다.)")
            display_story_text("나 : 네.. 교수님… (큰일났다…!)")
            display_story_text("강봉희 교수님 : 마침 잘 됐군. 방금 APEC 회의 자료를 검토하고 있었거든.")
            display_story_text("강봉희 교수님 : APEC이 뭔지 정도는 알겠지? 아시아 태평양 경제협력체 말이야.")
            display_story_text("(강봉희 교수님이 서류를 덮고 플레이어를 바라본다)", ch="monica_serious")
            display_story_text("강봉희 교수님 : 근데 말이지… 학생, 혹시 내 영어 이름을 알고 있나?!")
            display_story_text("나 : (뜨끔!)")
            display_story_text("강봉희 교수님 : 정확한 스펠링을 맞혀야 한다. 틀리면…", ch="monica_smile2")
            display_story_text("(강봉희 교수님이 씨익 웃는다)")
            display_story_text("강봉희 교수님 : 가차 없어 F를 주지!")


            choice4 = choice_dialogue([
            "MONICA",
            "MONIKA",
            "MONICAH",
            "MONISSA",
            "MONICAE"
            ])

            if choice4 == 0:
                display_story_text("강봉희 교수님 : 오~ 정확하군! MONICA, 맞네.", ch="monica_smile")
                display_story_text("강봉희 교수님 : 수업을 아주 집중해서 들었군. 대단한데?")
                display_story_text("(강봉희 교수님이 만족한 듯 고개를 끄덕인다.)")
                display_story_text("강봉희 교수님 : 좋아. 통과! 이만 가봐도 좋다네.", ch="clear")
                display_story_text("(단서 획득!)")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )
            else:
                display_story_text("강봉희 교수님 : 땡! 틀렸어.", ch="monica_serious")
                display_story_text("강봉희 교수님 : 이봐, 내가 뭐랬지? 스펠링 틀리면 F라고 했지?")
                display_story_text("(갑자기 진지해지며)", ch="monica_smile2")
                display_story_text("강봉희 교수님 : 자네… 공법창 F다.")
                display_story_text("나 : 아이고.. 아이고.. (하지만 어차피 중간 성적대로 가면 D+였기 때문에 큰 타격이 없다. 교양이기도 하고)", ch="clear")
                display_story_text("(공법창 학점 F확정^^)")
        elif i == 3:
            # # 3.학연산 (충북 산학협력단 rise와 만남.) -----------------------------------
            display_story_text("(학연산 건물 앞을 지나던 중 산학협력단 관계자로 보이는 사람이 서류를 들고 이동중이다.)", bg="학연산", ch="rise")
            display_story_text("RISE 관계자 : 학생, 잠시만요.")
            display_story_text("RISE 관계자 : 혹시 우리 충북대학교 산학협력단 RISE에 대해 알고 있나요?")
            choice5 = choice_dialogue([
                "아이돌 아님?",
                "롤 챔프 아님?",
                "상승이라는 뜻 아님?",
                "연구 및 기술개발을 지원하는 ‘산학협력단’",
                "로켓 발사 프로젝트 아님?"])

            if choice5 == 3:
                display_story_text("RISE 관계자 : 맞습니다! RISE는 충북대의 산학연 협력, 기술사업화, 기업 지원을 담당하는 핵심 조직이에요.", ch="rise_smile")
                display_story_text("RISE 관계자 : 학생이 아주 잘 알고 있네요.")
                display_story_text("RISE 관계자 : 이해도가 높으니, 도움이 될 만한 정보를 더 드릴게요.", ch="clear")
                display_story_text("(단서 획득!)")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )
            else:
                display_story_text("RISE 관계자 : RISE는 ‘Regional Innovation & Start-up Education’의 약자로,", ch="rise_smile")
                display_story_text("충북대학교 산학협력단이 지역 기업·연구기관·정부와 협업하여 기술 개발 지원, 창업 보육 및 기업 컨설팅, 산학 공동 R&D, 지식재산(IP) 관리, 현장실습·취업 연계, 지역산업 혁신 프로젝트 등을 수행하는 기관입니다. 우리 학교의 연구 역량을 지역 산업과 직접 연결해...")
                display_story_text("...학생·기업·지역사회가 함께 성장할 수 있도록 돕는 핵심 조직이죠.")
                display_story_text("RISE 관계자 : 다음엔 꼭 맞추세요, 학생.")
                display_story_text("나 : (아.. 피곤해..)", ch="clear")
                display_story_text("(긴 설명으로 인해 체력이 감소합니다.)")
                display_story_text("(체력 -30)")
                change_health(-30)

        elif i == 4:
            # # 4.솔못 (커플 피하기 게임) -----------------------------------
            display_story_text("(솔못 근처를 조용히 지나가려는데, 벤치에 앉아 있는 닭살 커플이 갑자기 당신을 발견하고 말을 건다.)", bg="솔못", ch="couple")
            display_story_text("커플남 : 어? 자기야, 저 사람 혼자 다닌다~ 우리랑 얘기 좀 하면 안 돼?")
            display_story_text("커플녀 : 그러게~ 솔못은 커플들이 오는 명소인데… 혼자 오니까 뭔가 신기하다~ 헤헤.")
            display_story_text("(둘이 서로 팔짱을 끼고 부비부비 거리며 다가온다.)")
            display_story_text("나 : (하…)")
            display_story_text("제한시간 내에 커플을 피해 솔못을 빠져나가야 한다.")
            display_story_text("올바른 방향키와 스페이스바를 눌러 커플을 피해 빠져나가자!")
            display_story_text("기회는 1번이다!")

            game_result_music = run_game(MusicGame)
            if game_result_music == "QUIT":
                return
            
            if game_result_music is True:
                display_story_text("(커플을 피해 무사히 솔못을 빠져나갔다.)")
                display_story_text("(단서 획득!)")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )
            else: 
                display_story_text("커플녀 : 솔못은 원래 커플 성지야~ 우리도 여기서 200일 기념했거든~ 헤헤.", ch="couple_sneer")
                display_story_text("커플남 : 맞아~ 여기 벤치에서 처음으로 손도 잡고~ 첫 데이트도 하고~")
                display_story_text("(둘이 갑자기 과한 스킨십을 시전한다. 당신은 정신적으로 데미지를 입기 시작한다.)")
                display_story_text("커플녀 : 너도 얼른 커플 만들어~ 요즘 혼자 다니면 외로워~")
                display_story_text("(당신은 닭살 커플의 과한 애정행각에 정신적 데미지를 입었습니다.)", ch="clear")
                display_story_text("(당신은 털썩한 마음으로 솔못을 벗어난다.)")
                display_story_text("(체력 -50)")
                change_health(-50)

        elif i == 5:
            # 5.coopsket (1+1 삼김 짝 맞추기) -----------------------------------
            display_story_text("나: 아 배고파.. 편의점좀 가야겠다..", bg="쿱스켓")
            display_story_text("(쿱스켓에 도착했다.)", ch="clerk")
            display_story_text("편의점 직원: 어서오세요 손님~")
            display_story_text("편의점 직원: 오늘의 특별 이벤트! 삼김 1+1 COOPSKET 매칭 챌린지에 참여하시겠습니까?")
            display_story_text("나: 그게 뭔데요?")
            display_story_text("편의점 직원: 선반에 놓인 4×4 총 16개의 삼김 중, 같은 종류끼리 짝을 맞추면 공짜로 가져가시는 거죠!")
            display_story_text("(마침 돈도 얼마 없던참이라 좋은일이라고 생각했다.)")
            display_story_text("나: 오 좋은데요?")

            game_result_findcard = run_game(FindCard)
            
            if game_result_findcard == "QUIT":
                return
            
            if game_result_findcard is True: # 카드 찾기 게임 승리 
                display_story_text("나: 이거 다 가져가도 돼요?")
                display_story_text("편의점 직원: 다 가져가도 됩니다!")
                display_story_text("나: 배부르니까 하나만 먹을게요~ 많이파세요~~")
                display_story_text("편의점 직원: 감사합니다 또오세요~ ", ch="clear")
                display_story_text("( 단서 획득!)")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )
            else:
                display_story_text("편의점 직원: 아이고.. 아쉽네요..")
                display_story_text("나: 이걸로 결제 해 주세요….( 카드를 건넨다)", ch="clear")
                display_story_text("(체력 -30)")
                change_health(-30)
        
        elif i == 6:
            # 6. B:last 홍보 부스 (10초에 맞춰 버튼 입력하는 게임) -----------------------------------
            display_story_text("나: 조금 걷다가… 아, 저기 부스가 있네. 뭐하는 곳이지?", bg="중도부스", ch="booth_promoter")
            # //(배경 부스로 바뀜)
            display_story_text("홍보 관계자: 어서 오세요, 손님! 오늘은 특별한 체험 이벤트가 있어요!")
            display_story_text("B:last 10초 버튼 챌린지’에 참여하시겠어요?")
            display_story_text("나: …버튼을 10초에 딱 맞추라고요?")
            display_story_text("나: 오 재밌겠는데?")
            display_story_text("홍보 관계자: 좋아요! 10초에 스페이스바 버튼을 정확히 누르세요!")
            display_story_text("성공하면 단서 +25, 실패하면 체력이 조금 줄어듭니다. 준비, 시작!")


            game_result_timer = run_game(Timer)

            if game_result_timer == "QUIT":
                return

            if game_result_timer is True:
                display_story_text("와! 대단하시네요! 완벽하게 성공하셨습니다!", ch="booth_promoter_smile")
                display_story_text("나: (정확히 10초는 아니지만) 오..오예!")
                display_story_text("홍보 관계자: 좋아요, 덕분에 오늘도 즐거운 이벤트였어요! 또 오세요~", ch="clear")
                display_story_text("단서 획득!")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )
            else:
                display_story_text("홍보 관계자: 앗, 아쉽네요… 다음 기회에 다시 도전하세요!", ch="booth_promoter_disappointed")
                
        elif i == 7:
            # 7.중도 앞 길가에서 쓰레기 발견 (중도 앞 길가에서 쓰레기를 발견함)-----------------------------------
            display_story_text("나:  어? 뭐지? 땅에 쓰레기가…", bg="중앙도서관")

            choice6 = choice_dialogue([
                "쓰레기를 줍는다",
                "무시하고 지나간다."
            ])
            if choice6 == 0:
                display_story_text("나: 에이, 귀찮아도… 환경은 지켜야지!")
                display_story_text("나: 흠… 손은 더러워졌지만, 뭔가 기분이 좋네")
                display_story_text("(단서 획득!)")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )

            elif choice6 == 1:
                display_story_text("(그냥 지나간다)", ch="environmentalist_angry")
                display_story_text("환경봉사 동아리 부원 등장")
                display_story_text("환경봉사 동아리 부원: 학생! 여기서 쓰레기를 무시하고 지나가다니… 환경 의식이 너무 부족하군요!")
                display_story_text("나: 죄송합니다… 다음부터 꼭 챙길게요!", ch="environmentalist")
                display_story_text("환경봉사 동아리 부원: 좋아요, 이번 한 번만 봐줄게요. 앞으로는 주의하세요!", ch="Clear")
                display_story_text("(체력 -20)")
                change_health(-20)

        elif i == 8:
            # 8.중문에서 나타나는 보드게임 중독(홀덤 중독자) 학과 동기와 만남-----------------------------------
            display_story_text("하하하하하", bg="n-14")
            display_story_text("나: 저게 무슨소리지?")
            display_story_text("나: 저 사람 컴공 동기인가? 왜 이렇게 진지하게 게임을 하고 있지?", ch="schoolmate_smile")
            display_story_text("동기: 오! 너도 들어와! 베스킨라빈스 31, 한 판 하자고!")
            display_story_text("동기: …지금? 체력도 좀 남았는데, 한 번만 해보지 뭐. 들어오쇼 ㅋ")
            display_story_text("동기: 규칙은 간단해, 31을 넘기지 않고 돌아가면서 최대 3개 최소 1개씩 숫자를 말하면 되고 31을 말하면 지는거야!")
            
            game_result_BR31 = run_game(BR31)
            if game_result_BR31== "QUIT":
                return
            
            if game_result_BR31 is True:
                display_story_text("동기: 와! 대단한데? 역시 네가 우리 중에 제일 센스 있네!", ch="schoolmate_smile")
                display_story_text("(단서 획득!)", ch="clear")
                gain_clue(player, amount=25)
                show_clue_popup(
                    screen=screen,
                    clock=clock,
                    clue_img_path=CLUE_IMG_PATH,
                    background=background,
                    character=character
                )
            else:
                display_story_text("동기:ㅋ 아쉽다! 넌 아직 부족하군.", ch="schoolmate_sneer")
                display_story_text("이제 더 집중해야지, 그래도 열심히 하셨잖아~", ch="clear")
                display_story_text("(체력 -50)")
                change_health(-50)

 # 9. 엔딩-----------------------------------    
    player["escaped"] = True
    check_ending()





if __name__ == "__main__":
    try:
        dialogue_box = DialogueManager(screen, font) 
        dialogue_box.clock = clock
        
        game_story_sequence()
    finally:
        pygame.quit()
        sys.exit()