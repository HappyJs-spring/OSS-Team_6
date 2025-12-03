#include "music.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>


char RandomNote() {
    int r = rand() % 5;
    switch (r) {
    case 0: return 'w';
    case 1: return 's';
    case 2: return 'a';
    case 3: return 'd';
    default: return ' ';
    }
}

void printArrow(char c) {
    switch (c) {
    case 'w': printf("↑ "); break;
    case 's': printf("↓ "); break;
    case 'a': printf("← "); break;
    case 'd': printf("→ "); break;
    case ' ': printf("o "); break;
    }
}

void move(int col, int row) {
    COORD pos = { col, row };
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), pos);
}


void GenerateSequence(char* seq) {
    for (int i = 0; i < SEQ_LEN; i++)
        seq[i] = RandomNote();
}

void ShowSequence(char* seq) {
    printf("↑:W  ↓:S  ←:A  →:D  o:SPACE\n\n");

    for (int i = 0; i < SEQ_LEN; i++)
        printArrow(seq[i]);

    printf("\n\n시작하려면 아무 키나 누르세요!\n");
    _getch();
}

int PlayGame(char* seq) {
    time_t start = time(NULL);

    for (int i = 0; i < SEQ_LEN; i++) {
        while (!_kbhit()) {
            int left = TIME - (time(NULL) - start);
            if (left <= 0) {
                move(0, 10);
                printf("\n시간 초과!\n실패! 체력 -50\n");
                return 0;
            }

            move(0, 8);
            printf(" 남은 시간: %2d초   ", left);
            Sleep(100);
        }

        char input = _getch();
        if (input != seq[i]) {
            move(0, 10);
            printf("\n틀렸습니다!\n실패! 체력 -50\n");
            return 0;
        }
    }
    return 1;
}