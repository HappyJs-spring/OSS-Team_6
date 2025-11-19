#pragma once
#ifndef UPDOWN_H
#define UPDOWN_H

#ifdef _WIN32
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#define MAX_ATTEMPTS 7
#define MIN_NUM 1
#define MAX_NUM 100

// DLL API
DLLEXPORT void init_game();
DLLEXPORT int guess_number(int num);
DLLEXPORT int get_remaining_attempts();
DLLEXPORT int get_answer();   // (디버그용) Python은 일반적으로 사용 X
DLLEXPORT int is_finished();
DLLEXPORT int get_last_result(); 
// 0 = correct, 1 = up, 2 = down, 3 = invalid

#endif
