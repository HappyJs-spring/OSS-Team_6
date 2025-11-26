#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <windows.h>
#include <time.h>

#include "avoid.h"

char map[ROW][COL];
int px, py;

void init_map() {
    for (int i = 0; i < ROW; i++)
        for (int j = 0; j < COL; j++)
            map[i][j] = '.';

    map[0][9] = 'E';
    map[1][3] = 'C';
    map[6][6] = 'C';
    map[8][2] = 'C';

    while (1) {
        px = rand() % ROW;
        py = rand() % COL;

        if (map[px][py] == '.') {
            map[px][py] = '#';
            break;
        }
    }
}

void print_map() {
    system("cls");
    for (int i = 0; i < ROW; i++) {
        for (int j = 0; j < COL; j++)
            printf("%c ", map[i][j]);
        printf("\n");
    }
    printf("\nMove (W/A/S/D) ");
}

void move_player(char key) {
    int nx = px, ny = py;

    if (key == 'w') nx--;
    else if (key == 's') nx++;
    else if (key == 'a') ny--;
    else if (key == 'd') ny++;

    if (nx < 0 || nx >= ROW || ny < 0 || ny >= COL)
        return;

    if (map[nx][ny] == 'E') {
        px = nx;
        py = ny;
        map[px][py] = '#';
        print_map();
        printf("\n성공! 단서 +25\n");
        exit(0);
    }

    if (map[nx][ny] == '.') {
        map[px][py] = '.';
        px = nx;
        py = ny;
        map[px][py] = '#';
    }
}

void move_couples() {
    int cx[50], cy[50], cnt = 0;

    for (int i = 0; i < ROW; i++)
        for (int j = 0; j < COL; j++)
            if (map[i][j] == 'C') {
                cx[cnt] = i;
                cy[cnt] = j;
                cnt++;
            }

    for (int k = 0; k < cnt; k++) {
        int i = cx[k], j = cy[k];

        if (map[i][j] != 'C') continue;

        int dir = rand() % 5;
        int di = 0, dj = 0;

        if (dir == 1) di = -1;
        else if (dir == 2) di = 1;
        else if (dir == 3) dj = -1;
        else if (dir == 4) dj = 1;

        int ni = i + di;
        int nj = j + dj;

        if (ni < 0 || ni >= ROW || nj < 0 || nj >= COL) continue;

        if (map[ni][nj] == '#') {
            map[i][j] = '.';
            map[ni][nj] = 'C';
            return;
        }

        if (map[ni][nj] == '.') {
            map[i][j] = '.';
            map[ni][nj] = 'C';
        }
    }
}
