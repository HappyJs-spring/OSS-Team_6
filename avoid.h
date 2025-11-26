#ifndef GAME_H
#define GAME_H

#include <stdio.h>

#define ROW 10
#define COL 10

extern char map[ROW][COL];
extern int px, py;

void init_map();
void print_map();
void move_player(char key);
void move_couples();

#endif
#pragma once
