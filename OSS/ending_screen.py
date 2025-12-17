import pygame
import sys

def show_grade(screen, text, color):
    font = pygame.font.SysFont("malgun gothic", 160)
    clock = pygame.time.Clock()

    alpha = 0
    grade_surf = font.render(text, True, color)
    grade_surf.set_alpha(alpha)

    while alpha < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        grade_surf.set_alpha(alpha)
        screen.blit(
            grade_surf,
            (screen.get_width() // 2 - grade_surf.get_width() // 2,
             screen.get_height() // 2 - grade_surf.get_height() // 2)
        )

        pygame.display.flip()
        alpha += 6
        clock.tick(60)

    pygame.time.wait(2000)


def show_ending(screen, ending_type, display_story_text):
    """
    ending_type: "bad" | "happy" | "hidden"
    """

    # ======================
    # BAD ENDING
    # ======================
    if ending_type == "fail":
        show_grade(screen, "F", (200, 0, 0))
        return       
    
    if ending_type == "bad":
        display_story_text(
            "(교수님의 목소리가 들려온다…)",
            ch="professor_embarrassed"
        )
        display_story_text("교수님: 학생! 지금 여기서 뭐하고 있는거야?")
        display_story_text(
            "(나는 대답조차 할 힘이 없었다. 교수님의 손에 이끌려 연구실로 향한다.)"
        )

        display_story_text(
            "교수님: 아니, 이 시간에 왜 돌아다니는 겁니까?",
            ch="professor_suspicion"
        )
        display_story_text(
            "교수님: 이 시간에 여기 있는 이유… 과제 제출 문제 때문인가요?"
        )
        display_story_text(
            "(말문이 막힌 당신은 변명조차 하지 못한다.\n교수님의 눈은 이미 모든 것을 알고 있다는 듯하다.)"
        )

        display_story_text(
            "교수님: 규정은 규정입니다. 부정 제출은 인정할 수 없어요.\n해당 과제는… 0점 처리입니다.",
            ch="professor_angry"
        )

        display_story_text("(과제는 제출했지만, 그 과정이 들켜버린 순간)")
        display_story_text("(모든 노력은 물거품이 되었다.)")
        display_story_text(
            "(밤새 숨죽이고 도망쳤던 발자국들이\n교수님 앞에서 허망하게 지워진다.)"
        )

        show_grade(screen, "F", (200, 0, 0))
        return

    # ======================
    # HAPPY ENDING
    # ======================
    if ending_type == "happy":
        display_story_text(
            "(새벽의 충북대학교 캠퍼스는 차갑고 고요한 공기만이 흐르고 있었다.)"
        )
        display_story_text(
            "(E8-1 건물 안에서 쫓기듯 보냈던 시간들을 지나\n당신은 마침내 건물 밖으로 빠져나왔다.)"
        )
        display_story_text(
            "(수많은 사건이 당신을 가로막았지만,\n당신은 끝내 쓰러지지 않았다.)"
        )
        display_story_text(
            "(심장은 쿵쾅거리고 다리는 무겁지만,\n당신은 마지막 힘을 짜내 정문으로 달린다.)"
        )
        display_story_text(
            "(거리의 공기가 바뀌고,\n캠퍼스의 긴장감이 사라지는 순간)"
        )
        display_story_text(
            "나: 하… 끝났다.. 진짜… 끝났구나."
        )

        show_grade(screen, "A+", (0, 200, 0))
        return

    # ======================
    # HIDDEN ENDING
    # ======================
    if ending_type == "hidden":
        display_story_text(
            "나: 드디어… 끝났다.\n교수님의 추격도, 신비한 랜덤 이벤트들도…"
        )
        display_story_text(
            "(모든 단서를 모은 당신은,\n충북대학교를 완전히 빠져나왔다.)"
        )
        display_story_text("(갑자기 스마트폰 알림이 울린다.)")
        display_story_text("나: …뭐지, 이 시간에?")

        display_story_text(
            "[충북대학교 장학센터]\n성적 우수자 선정 안내"
        )
        display_story_text(
            "“충북대 어딘가에 숨겨진 단서를 모두 모은 학생에게\n특별 장학금을 지급한다는 소문… 당신은 그걸 정말로 해냈다.”"
        )

        show_grade(screen, "성적장학금!!", (180, 120, 255))
        return
