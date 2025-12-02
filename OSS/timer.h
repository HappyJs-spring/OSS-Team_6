#ifndef TIMER_H
#define TIMER_H

#define TARGET_TIME 10.00

void init_timer();
void start_timer();
void stop_timer();
double get_elapsed_time();
double get_difference();
int is_success();

#endif
