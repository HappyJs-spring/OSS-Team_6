#include "Card.h"
#include "FCcontrol.h"
#include "Skout.h"
#include <string.h>

CARD Card[4][4];

int nx, ny; // 현재 커서의 위치
int count; // 플레이어가 짝을 찾기 위해 카드를 열어본 시도 횟수를 저장하기 위한 변수

int NumOpen = 16;
int NumHint = 2;
int success = 0;




int main()
{
	randomize();
	setcursortype(SOLIDCURSOR);

	for (;;)
	{
		InitGame();
		for (;;)
		{
			PlayerKeyAction();
			GamePan(FALSE);

			if (NumOpen == 0)
			{
				clrscr();
				gotoxy(26, 4);
				SetColor(WHITE);
				puts("G A M E C L E A R");

				gotoxy(34, 6);
				puts("기다리시면 게임을 다시 시작합니다");
				delay(1500);
				clrscr();
				break;


			}
		}
	}
	return 0;
}

void InitGame()
{
	int i, j;
	int x, y;

	nx = 0;
	ny = 0;

	count = 0;
	NumOpen = 16;
	success = 3;
	NumHint = 2;

	memset(Card, 0, sizeof(Card));
	for (i = 0; i < 8; i++)
	{
		for (j = 0; j < 2; j++) // 두 개의 카드에 저ㅈ ㅏㅇ
		{
			do
			{
				x = random(4);
				y = random(4);
			} while (Card[x][y].Num != 0); // 위치 중복 방지

			Card[x][y].Num = i;
		}
	}

	GamePan(TRUE);
	delay(2000);
	clrscr();
	GamePan(FALSE);
}

void GamePan(BOOL Start)
{
	SetColor(WHITE);
	gotoxy(50, 2);     printf(" ┌──────────────────────┐ ");
	gotoxy(50, 3);     printf(" │    짝 카드 찾기 게임 │ ");
	gotoxy(50, 4);     printf(" └──────────────────────┘ ");

	gotoxy(56, 7);     printf("       UP");
	gotoxy(56, 8);     printf("       ↑");
	gotoxy(56, 9);     printf("LEFT ←   → RIGHT");
	gotoxy(56, 10);    printf("       ↓");
	gotoxy(56, 11);    printf("      DOWN");

	gotoxy(56, 14);    printf("찾기 : 스페이스바");
	gotoxy(56, 16);    printf("H : 힌트 보기");

	gotoxy(54, 17);	   printf("힌트 사용 가능 횟수 : %d", NumHint);
	gotoxy(56, 18);    printf("총 시도 횟수 : %d", count);
	SetColor(DARK_SKYBLUE);

	int x, y;
	for (y = 0; y < 4; y++)
	{
		for (x = 0; x < 4; x++)
		{
			gotoxy((x * 5 + 2) + 15, (y * 3 + 2) + 3);
			if (Start == TRUE || Card[x][y].St == OPEN)
			{
				SetColor(VIOLET);
				printf("%s", NumToWord(x, y));

				gotoxy(30, 1);
				SetColor(SKYBLUE);
				printf("※ 2초간 정답 공개! ※");
			}
			else if (Card[x][y].St == HINT)
			{
				SetColor(SKYBLUE);
				printf("%s", NumToWord(x, y));
				delay(1000);
			}
			else if (Card[x][y].St == HIDDEN)
			{
				SetColor(WHITE);
				printf("??");
			}
			else if (Card[x][y].St == TEMP)
			{
				SetColor(YELLOW);
				printf("%s", NumToWord(x, y));
			}
		}
	}

}

const char* NumToWord(int x, int y)
{
	switch (Card[x][y].Num)
	{
	case 0:
		return "★";
	case 1:
		return "♨";
	case 2:
		return "■";
	case 3:
		return "◎";
	case 4:
		return "◆";
	case 5:
		return "♣";
	case 6:
		return "♠";
	case 7:
		return "☎";
	default: return "??";
	}
}

void SetColor(int color)
{
	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

void Hint(int hx, int hy)
{
	int x, y;

	if (NumHint != 0)
	{

		for (y = 0; y < 4; y++)
		{
			for (x = 0; x < 4; x++)
			{
				if (Card[y][x].Num == Card[hy][hx].Num)
				{
					Card[y][x].St = HINT;
					GamePan(FALSE);
					Card[y][x].St = HIDDEN;
				}
			}
		}

	NumHint--;
	}
}
