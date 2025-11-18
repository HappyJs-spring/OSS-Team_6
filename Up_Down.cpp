#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "up&down.h"


int generate_random_number(void) {
    srand((unsigned int)time(NULL));
    return rand() % MAX_NUM + MIN_NUM;
}


int get_valid_input(void) {
    char input[100];
    int is_digit = 1;

    if (scanf("%s", input) != 1) {
        printf("입력 오류!\n");
        exit(1);
    }

    
    for (int i = 0; input[i] != '\0'; i++) {
        if (input[i] < '0' || input[i] > '9') {
            is_digit = 0;
            break;
        }
    }

    if (!is_digit) {
        printf("잘못된 입력입니다! 숫자만 입력하세요.\n\n");
        return -1;
    }

    int num = atoi(input);
    if (num < MIN_NUM || num > MAX_NUM) {
        printf("%d에서 %d 사이 숫자만 입력하세요!\n\n", MIN_NUM, MAX_NUM);
        return -1;
    }

    return num;
}


void play_game(void) {
    int answer = generate_random_number();
    int guess;
    int attempts = 0;

    printf("=== Up-Down 게임 ===\n");
    printf("%d부터 %d 사이의 숫자를 맞춰보세요! (최대 %d번 시도 가능)\n\n",
        MIN_NUM, MAX_NUM, MAX_ATTEMPTS);

    while (attempts < MAX_ATTEMPTS) {
        printf("%d번째 시도: ", attempts + 1);
        guess = get_valid_input();

        if (guess == -1)
            continue; 

        attempts++;

        if (guess > answer)
            printf("Down!\n\n");
        else if (guess < answer)
            printf("Up!\n\n");
        else {
            printf("\n 정답입니다! %d번 만에 맞추셨네요!\n", attempts);
            return;
        }
    }

    printf("\n기회를 모두 사용했습니다. 정답은 %d였습니다.\n", answer);
    printf("게임 종료!\n");
}

