#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <windows.h>
#include "hangman.h"

#define MAX_TRIES 6
#define WORD_COUNT 6

const char* words[WORD_COUNT] = {
    "computer",
    "hangman",
    "programming",
    "developer",
    "python",
    "artificial"
};

static void displayWord(const char* word, const int guessed[]) {
    for (int i = 0; i < (int)strlen(word); i++) {
        if (guessed[i])
            printf("%c ", word[i]);
        else
            printf("_ ");
    }
    printf("\n");
}

static int isWordGuessed(const int guessed[], int length) {
    for (int i = 0; i < length; i++) {
        if (!guessed[i])
            return 0;
    }
    return 1;
}

void playHangman(void) {
    srand((unsigned int)time(NULL));
    const char* word = words[rand() % WORD_COUNT];
    int length = (int)strlen(word);

    int* guessed = (int*)malloc(length * sizeof(int));
    if (!guessed) {
        printf("메모리 할당 실패\n");
        return;
    }
    memset(guessed, 0, length * sizeof(int));

    char usedLetters[26] = { 0 };
    int attempts = MAX_TRIES;
    clock_t start_time = clock();

    while (attempts > 0) {
        system("cls");
        double elapsed = (double)(clock() - start_time) / CLOCKS_PER_SEC;

        printf("행맨 단어 추리 게임\n");
        printf("------------------\n");
        printf("남은 기회: %d\n", attempts);
        printf("경과 시간: %.1f초\n", elapsed);
        printf("------------------\n");

        printf("단어: ");
        displayWord(word, guessed);

        printf("입력된 글자: ");
        for (int i = 0; i < 26; i++) {
            if (usedLetters[i]) printf("%c ", 'a' + i);
        }
        printf("\n\n");

        printf("알파벳 한 글자를 입력하세요: ");
        char guess;
        scanf_s(" %c", &guess, 1);

        // 입력 버퍼 비우기 (여러 글자 방지)
        while (getchar() != '\n');

        guess = (char)tolower(guess);

        if (!isalpha((unsigned char)guess)) {
            printf("알파벳만 입력하세요.\n");
            Sleep(1000);
            continue;
        }

        int index = guess - 'a';
        if (usedLetters[index]) {
            printf("이미 입력한 글자입니다.\n");
            Sleep(1000);
            continue;
        }
        usedLetters[index] = 1;

        int correct = 0;
        for (int i = 0; i < length; i++) {
            if (word[i] == guess) {
                guessed[i] = 1;
                correct = 1;
            }
        }

        if (correct) {
            printf("맞았습니다!\n");
        }
        else {
            printf("틀렸습니다!\n");
            attempts--;
        }

        Sleep(1000);

        if (isWordGuessed(guessed, length)) {
            system("cls");
            double total_time = (double)(clock() - start_time) / CLOCKS_PER_SEC;
            printf("정답입니다! 단어는 '%s' 입니다.\n", word);
            printf("총 플레이 시간: %.1f초\n", total_time);
            free(guessed);
            return;
        }
    }

    system("cls");
    double total_time = (double)(clock() - start_time) / CLOCKS_PER_SEC;
    printf("기회를 모두 소진했습니다. 정답은 '%s' 입니다.\n", word);
    printf("총 플레이 시간: %.1f초\n", total_time);

    free(guessed);
}
