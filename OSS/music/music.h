#include <windows.h>

#define TIME 15
#define SEQ_LEN 20

char RandomNote();
void printArrow(char c);
void move(int col, int row);

void GenerateSequence(char* seq);
void ShowSequence(char* seq);
int PlayGame(char* seq);
#pragma once