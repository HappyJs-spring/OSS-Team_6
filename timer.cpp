#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <conio.h>
#include "timer.h"

void display_time(double elapsed) {
    system("cls");

    printf("\n");
    printf("      10.00초 맞추기 게임 \n");
    printf("         현재 시간: %.2f 초\n\n", elapsed);
    printf(" %.2f초에 스페이스 바를 눌러 멈추세요!\n", TARGET_TIME);
}
