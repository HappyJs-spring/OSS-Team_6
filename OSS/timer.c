#include <time.h>
#include "timer.h"

static clock_t start_time;
static clock_t stop_time;
static double elapsed;
static double diff;
static int timer_started = 0;

void init_timer() {
    timer_started = 0;
    elapsed = 0.0;
    diff = 0.0;
}

void start_timer() {
    timer_started = 1;
    start_time = clock();
}

void stop_timer() {
    stop_time = clock();
    elapsed = (double)(stop_time - start_time) / CLOCKS_PER_SEC;
    diff = elapsed - TARGET_TIME;
    timer_started = 0;
}

double get_elapsed_time() {
    if (!timer_started) return elapsed;
    return (double)(clock() - start_time) / CLOCKS_PER_SEC;
}

double get_difference() {
    return diff;
}

int is_success() {
    // 성공 조건 수정 필요
    double abs_diff = diff < 0 ? -diff : diff;

    if (abs_diff <= 0.5)  
        return 1;   // success
    else
        return 0;   // fail
}
