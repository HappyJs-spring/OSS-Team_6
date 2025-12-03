#define _CRT_SECURE_NO_WARNINGS
#include <conio.h>
#include <windows.h>
#include <time.h>
#include <stdio.h>
#include "avoid.h"

int main() {
    srand((unsigned)time(NULL));
    init_map();

    while (1) {
        print_map();

        
        if (GetAsyncKeyState('W') & 0x8000) {
            if (move_player('w') == 1) { printf("\n성공! 단서 +25\n"); break; }
        }
        if (GetAsyncKeyState('A') & 0x8000) {
            if (move_player('a') == 1) { printf("\n성공! 단서 +25\n"); break; }
        }
        if (GetAsyncKeyState('S') & 0x8000) {
            if (move_player('s') == 1) { printf("\n성공! 단서 +25\n"); break; }
        }
        if (GetAsyncKeyState('D') & 0x8000) {
            if (move_player('d') == 1) { printf("\n성공! 단서 +25\n"); break; }
        }

       
        int r = move_couples();
        if (r == -1) {
            print_map();
            printf("\n실패! 체력 -50\n");
            break;
        }

        
        Sleep(300);
    }

    return 0;
}