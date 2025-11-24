#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>
#include <windows.h>
#include "timer.h"

int main() {
    clock_t start_time, stop_time;
    double elapsed_time;
    double difference;

    printf("     10.00초 맞추기 게임을 시작합니다!\n\n");
    printf("스페이스 바를 눌러서 타이머를 시작하세요...");

    _getch();

    start_time = clock();

    while (1) {
        elapsed_time = (double)(clock() - start_time) / CLOCKS_PER_SEC;

        display_time(elapsed_time);

        Sleep(10);

        if (_kbhit()) {
            _getch();
            stop_time = clock();
            break;
        }
    }

    elapsed_time = (double)(stop_time - start_time) / CLOCKS_PER_SEC;
    difference = elapsed_time - TARGET_TIME;

    system("cls");

    printf("           게임 결과 \n");
    printf("=========================================\n\n");
    printf("       기록: %.2f초\n", elapsed_time);

    double abs_diff = (difference < 0) ? -difference : difference;

    if (abs_diff <= 0.5) {
        printf("       성공! 단서 +25\n");
    }
    else {
        printf("       실패! 체력 -10\n");
    }

    return 0;
}
