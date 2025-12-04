#include <stdio.h>  
#include "music.h"
#include <ctime>

int main() {
    srand((unsigned)time(NULL));

    char seq[SEQ_LEN];

    GenerateSequence(seq);
    ShowSequence(seq);

    if (PlayGame(seq))
        printf("\n 성공! 단서 +25\n");

    return 0;
}
