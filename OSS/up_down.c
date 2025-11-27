#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "up_down.h"

static int answer = 0;
static int remaining_attempts = MAX_ATTEMPTS;
static int last_result = 3; 
// 0 = correct
// 1 = up
// 2 = down
// 3 = invalid

DLLEXPORT void init_game() {
    srand((unsigned int)time(NULL));
    answer = rand() % MAX_NUM + MIN_NUM;
    remaining_attempts = MAX_ATTEMPTS;
    last_result = 3;
}

DLLEXPORT int guess_number(int num) {
    if (num < MIN_NUM || num > MAX_NUM) {
        last_result = 3;
        return last_result; 
    }

    // 이미 끝난 게임이면 invalid 반환
    if (is_finished()) {
        last_result = 3;
        return last_result;
    }

    // 정답 처리 (기회 감소 없음)
    if (num == answer) {
        last_result = 0;
        return last_result;
    }

    // 정답이 아니면 기회 소모
    remaining_attempts--;

    if (num < answer) {
        last_result = 1;
    } else {
        last_result = 2;
    }

    return last_result;
}

DLLEXPORT int get_remaining_attempts() {
    return remaining_attempts;
}

DLLEXPORT int get_answer() {
    return answer;
}

DLLEXPORT int is_finished() {
    // 정답을 우선으로 확인하고
    if (last_result == 0) return 1;

    // 기회를 소진하게 수정
    if (remaining_attempts <= 0) return 1;

    return 0;
}

DLLEXPORT int get_last_result() {
    return last_result;
}
