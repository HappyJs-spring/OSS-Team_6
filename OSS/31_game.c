#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "31_game.h"

#define MAX_TARGET 31
#define MIN_CALL 1
#define MAX_CALL 3

static int current = 0;
static int game_finished = 0;     // 1: 종료, 0: 진행 중
static int game_result = 0;       // 1: 플레이어 승리, -1: 패배

void init_game(void) {
    current = 0;
    game_finished = 0;
    game_result = 0;
    srand((unsigned)time(NULL));
}

/*
    return 값:
    1 = 정상 진행
    0 = 범위 오류
    -1 = 플레이어 패배
*/
int player_turn(int count) {
    if (game_finished) return game_result;

    if (count < MIN_CALL || count > MAX_CALL)
        return 0; // 범위 초과

    for (int i = 0; i < count && current < MAX_TARGET; i++)
        current++;

    if (current >= MAX_TARGET) {
        game_finished = 1;
        game_result = -1; // 패배
        return -1;
    }
    return 1;
}

/*
    return 값:
    숫자 개수 반환
    -1 = 컴퓨터 승리 (플레이어 패배 아님)
*/
int computer_turn(void) {
    if (game_finished) return game_result;

    int target = MAX_TARGET - current;
    int num;

    if (target > MAX_CALL) {
        if (target % (MAX_CALL + 1) == 0)
            num = rand() % MAX_CALL + 1;
        else
            num = target % (MAX_CALL + 1);
    } else {
        if (target == 1) num = 1;
        else num = target - 1;
    }

    for (int i = 0; i < num && current < MAX_TARGET; i++)
        current++;

    if (current >= MAX_TARGET) {
        game_finished = 1;
        game_result = 1; // 플레이어 승리 (컴퓨터가 31 말함)
        return -1;
    }

    return num;
}

int get_current(void) {
    return current;
}

int is_finished(void) {
    return game_finished;
}

int get_result(void) {
    return game_result; // 1 = 승리, -1 = 패배
}
