#ifndef GAME_H
#define GAME_H

#define ROW 10
#define COL 10

extern char map[ROW][COL];
extern int px, py;

void init_map();
void print_map();
int move_player(char key);
int move_couples();

#endif
