#define SKOUT_PROTOTYPE_ONLY

#include "Skout.h"
#include "Card.h"
#include "FCcontrol.h"

#define LEFT 75
#define RIGHT 77
#define UP 72
#define DOWN 80
#define ESC 27
#define EXTENDASCII -32


extern int nx, ny;
extern int count;
extern int NumOpen;
extern int NumHint;
extern int success;
int tx, ty; // 임시 커서의 좌표


void PlayerKeyAction()
{
	char ch;

	gotoxy((nx * 5 + 2) + 15, (ny * 3 + 2) + 3);
	ch = _getch();
	if (ch == EXTENDASCII)
	{
		ch = _getch();
		switch (ch)
		{
		case LEFT:
			nx--;
			if (nx < 0)
			{
				nx = 3;
			}

			break;
		case RIGHT:
			nx++;
			if (nx > 3)
			{
				nx = 0;
			}
			break;
		case UP:
			ny--;
			if (ny < 0)
			{
				ny = 3;
			}
			break;
		case DOWN:
			ny++;
			if (ny > 3)
			{
				ny = 0;
			}
			break;
		}
	}
	else 
	{
		switch (ch)
		{
		case ESC:
			exit(0);
			break;
		case ' ':
			PlayerSpacebar();
			break;
		case 'H':
			Hint(nx, ny);
			break;
		case 'h':
			Hint(nx, ny);
			break;
		}
	}
}

void PlayerSpacebar()
{
	if (Card[nx][ny].St == HIDDEN)
	{
		GetTemp(&tx, &ty);
		if (tx == -1)
			Card[nx][ny].St = TEMP;

		else
		{
			count++;
			if (Card[tx][ty].Num == Card[nx][ny].Num)
			{
				++success;
				gotoxy(3, success);
				SetColor(GREEN); printf("NICE!\a");

				Card[tx][ty].St = OPEN;
				Card[nx][ny].St = OPEN;
				NumOpen -= 2;

			}
			else
			{
				Card[nx][ny].St = TEMP;
				GamePan(false);
				delay(300);
				Card[nx][ny].St = HIDDEN;
				Card[tx][ty].St = HIDDEN;
			}
		}
	}
}

void GetTemp(int* tx, int* ty)
{
	int i, j;

	for (i = 0; i < 4; i++)
	{
		for (j = 0; j < 4; j++)
		{
			if (Card[i][j].St == TEMP)
			{
				*tx = i;
				*ty = j;
				return;
			}
		}
	}
	*tx = -1;
}
