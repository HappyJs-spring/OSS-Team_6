// FindCard_DLL.c
#define DLLEXPORT __declspec(dllexport)
#include <stdlib.h>
#include <time.h>

static time_t start_time;
static int time_limit = 30;

enum Status { HIDDEN, OPEN, TEMP, HINT };

typedef struct {
    int Num;
    int St;
} CARD;

static CARD Board[4][4];
static int opened_pair = 0;
static int temp_count = 0;
static int temp_x[2];
static int temp_y[2];

// 초기화
DLLEXPORT void init_game() {
    srand((unsigned int)time(NULL));

    // 게임 시작 시간 기록
    start_time = time(NULL);

    // 초기화
    opened_pair = 0;
    temp_count = 0;

    // 모든 카드 초기화
    int used[8] = {0};
    for(int i=0;i<4;i++){
        for(int j=0;j<4;j++){
            Board[i][j].St = HIDDEN;
        }
    }

    // 카드 번호 2개씩 배치(0 ~ 7)
    for(int num=0;num<8;num++){
        for(int c=0;c<2;c++){
            int x,y;
            do{
                x = rand() % 4;
                y = rand() % 4;
            }while(Board[x][y].St != HIDDEN || Board[x][y].Num != 0);

            Board[x][y].Num = num;
        }
    }
}

// 카드 선택
DLLEXPORT int select_card(int x, int y) {

    // 이미 뒤집힌 카드
    if(Board[x][y].St == OPEN)
        return 3;

    // 이미 임시 카드 두 장이 뒤집힌 상태
    if(temp_count == 2)
        return 4;

    // TEMP 등록
    Board[x][y].St = TEMP;
    temp_x[temp_count] = x;
    temp_y[temp_count] = y;
    temp_count++;

    // 첫 번째 선택인 경우
    if(temp_count == 1)
        return 0;

    // 두 번째 선택일 때
    CARD *c1 = &Board[temp_x[0]][temp_y[0]];
    CARD *c2 = &Board[temp_x[1]][temp_y[1]];

    if(c1->Num == c2->Num){
        // 성공 → OPEN
        c1->St = OPEN;
        c2->St = OPEN;
        temp_count = 0;
        opened_pair++;
        return 1;
    }
    else {
        // 실패 → TEMP 유지, Python이 다시 숨김 처리
        return 2;
    }
}

// Python에서 실패 후 TEMP → HIDDEN으로 돌릴 때 호출
DLLEXPORT void reset_temp() {
    for(int i=0;i<temp_count;i++){
        Board[temp_x[i]][temp_y[i]].St = HIDDEN;
    }
    temp_count = 0;
}

// 전체 카드 번호 배열 반환
DLLEXPORT void get_board_nums(int* arr16) {
    int idx = 0;
    for(int y=0;y<4;y++){
        for(int x=0;x<4;x++){
            arr16[idx++] = Board[x][y].Num;
        }
    }
}

// 상태 반환
DLLEXPORT void get_board_state(int* arr16) {
    int idx = 0;
    for(int y=0;y<4;y++){
        for(int x=0;x<4;x++){
            arr16[idx++] = Board[x][y].St;
        }
    }
}

// 힌트: 동일 번호 카드 2개를 HINT로 표시
DLLEXPORT void use_hint(int num) {
    int cnt=0;
    for(int y=0;y<4;y++){
        for(int x=0;x<4;x++){
            if(Board[x][y].Num == num && Board[x][y].St == HIDDEN){
                Board[x][y].St = HINT;
                cnt++;
            }
        }
    }
}

// 게임 끝났는가?
DLLEXPORT int is_finished() {
    return (opened_pair == 8) ? 1 : 0;
}

DLLEXPORT int is_time_over() {
    time_t now = time(NULL);
    return (now - start_time >= time_limit) ? 1 : 0;
}

