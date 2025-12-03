#include "31_game.h"

int main(void) {
    init_game();

    while (1) {
        if (!player_turn()) break;
        if (!computer_turn()) break;
    }

    return 0;
}