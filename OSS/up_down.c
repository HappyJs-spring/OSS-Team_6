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

    if (remaining_attempts <= 0) {
        last_result = 3;
        return last_result;
    }

    remaining_attempts--;

    if (num == answer) {
        last_result = 0;
    } else if (num < answer) {
        last_result = 1; // Up
    } else {
        last_result = 2; // Down
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
    if (remaining_attempts <= 0) return 1;
    if (last_result == 0) return 1;
    return 0;
}

DLLEXPORT int get_last_result() {
    return last_result;
}
