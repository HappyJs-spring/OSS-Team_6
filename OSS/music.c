#include "music.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

char seq_global[SEQ_LEN];

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

// DLL 초기화
__declspec(dllexport) void init_game() {
    srand((unsigned)time(NULL));
    for (int i = 0; i < SEQ_LEN; i++)
        seq_global[i] = RandomNote();
}

// seq 안의 노트 하나 가져오기
__declspec(dllexport) char get_note(int index) {
    if (index < 0 || index >= SEQ_LEN) return ' ';
    return seq_global[index];
}

// 플레이어 입력 체크
__declspec(dllexport) int check_input(int index, char input) {
    if (index < 0 || index >= SEQ_LEN) return -1;
    return (seq_global[index] == input) ? 1 : 0;
}
