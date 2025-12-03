#ifndef GAME_H
#define GAME_H

void init_game(void);
int player_turn(int count);
int computer_turn(void);

int get_current(void);
int is_finished(void);
int get_result(void);

#endif
