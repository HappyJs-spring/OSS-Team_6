#ifndef __CARD_H__
#define __CARD_H__

// 카드의 상태
enum Status{HIDDEN, OPEN, TEMP, HINT};

typedef struct
{
	int Num;
	enum Status St;

} CARD;

extern CARD Card[4][4];

extern int nx, ny;
extern int count;
extern int NumOpen;
extern int NumHint;
extern int success;

#endif
