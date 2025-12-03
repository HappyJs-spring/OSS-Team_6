#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "31_game.h"

#define MAX_TARGET 31
#define MIN_CALL 1
#define MAX_CALL 3

static int current = 0; 

void init_game(void) {
    current = 0;
    srand((unsigned)time(NULL));
    printf("배스킨라빈스 31 게임\n");
    printf("한 번에 1~3개의 숫자를 말할 수 있습니다.\n\n");
}

int player_turn(void) {
    int num;

    printf("부를 숫자 개수: ");
    if (scanf_s("%d", &num) != 1) return 0;

    if (num < MIN_CALL || num > MAX_CALL) {
        printf("1부터 3사이 수만 가능합니다.\n");
        return 1;  
    }

    printf("플레이어:");
    for (int i = 0; i < num && current < MAX_TARGET; i++) {
        current++;
        printf(" %d", current);
    }
    printf("\n");

    if (current >= MAX_TARGET) {
        printf("\n실패! 체력 -50\n");
        return 0;  
    }
    return 1;  
}

int computer_turn(void) {
    int target = MAX_TARGET - current;
    int num;

    if (target > MAX_CALL) {
        if (target % (MAX_CALL + 1) == 0) num = rand() % MAX_CALL + 1;
        else num = target % (MAX_CALL + 1);
    }
    else {
        if (target == 1) num = 1;
        else num = target - 1;
    }

    printf("동기:");
    for (int i = 0; i < num && current < MAX_TARGET; i++) {
        current++;
        printf(" %d", current);
    }
    printf("\n\n");

    if (current >= MAX_TARGET) {
        printf("\n성공! 단서 +25\n");
        return 0;
    }
    return 1;
}