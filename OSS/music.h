#pragma once
#include <windows.h>

#define TIME 15
#define SEQ_LEN 20

char RandomNote();
void printArrow(char c);
void move(int col, int row);

__declspec(dllexport) void init_game();
__declspec(dllexport) char get_note(int index);
__declspec(dllexport) int check_input(int index, char input);
