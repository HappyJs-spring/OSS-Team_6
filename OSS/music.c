#include "music.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

char seq_global[SEQ_LEN];

__declspec(dllexport) void init_game() {
    srand((unsigned)time(NULL));
    for (int i = 0; i < SEQ_LEN; i++)
        seq_global[i] = RandomNote();
}

__declspec(dllexport) char get_note(int index) {
    if (index < 0 || index >= SEQ_LEN) return ' ';
    return seq_global[index];
}

__declspec(dllexport) int check_input(int index, char input) {
    if (index < 0 || index >= SEQ_LEN) return -1;
    return (seq_global[index] == input) ? 1 : 0;
}
