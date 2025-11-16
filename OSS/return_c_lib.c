// return_c_lib.c
#include <stdio.h>

// Windows DLL에서 함수를 노출
#ifdef _WIN32
    #define DLLEXPORT __declspec(dllexport)
#else
    #define DLLEXPORT
#endif

// 테스트용: 정수 하나를 받아서 *2 로 반환하는 함수
DLLEXPORT int play_game(int num) {
    num *= 2;
    return num; // Python으로 전달.
}