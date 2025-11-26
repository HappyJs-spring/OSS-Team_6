#ifndef __FC_CONTROL_H__
#define __FC_CONTROL_H__

void GamePan(bool Start);
void InitGame();
void SetColor(int color);
const char* NumToWord(int x, int y);
void Hint(int hx, int hy);
void PlayerKeyAction();
void PlayerSpacebar();
void GetTemp(int* tx, int* ty);
enum
{
	BLACK,
	DARK_BLUE,
	DARK_GREEN,
	DARK_SKYBLUE,
	DARK_RED,
	DARK_VIOLET,
	DARK_YELLOW,
	GRAY,
	DARK_GRAY,
	BLUE,
	GREEN,
	SKYBLUE,
	RED,
	VIOLET,
	YELLOW,
	WHITE
};

#endif
