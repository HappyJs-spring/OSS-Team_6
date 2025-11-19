#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>
#include "hangman.h"

#define MAX_TRIES 6
#define WORD_COUNT 6

const char* words[WORD_COUNT] = {
    "computer",
    "hangman",
    "programming",
    "developer",
    "python",
    "artificial"
};

static char answer[100];
static char current[100];
static char used[100];
static int used_count = 0;
static int remaining = MAX_TRIES;


DLLEXPORT void init_game() {
    srand((unsigned int)time(NULL));

    strcpy(answer, words[rand() % WORD_COUNT]);

    int len = strlen(answer);
    for (int i = 0; i < len; i++)
        current[i] = '_';
    current[len] = '\0';

    used_count = 0;
    used[0] = '\0';
    remaining = MAX_TRIES;
}


static int already_used(char c) {
    for (int i = 0; i < used_count; i++) {
        if (used[i] == c) return 1;
    }
    return 0;
}


DLLEXPORT int guess_char(char c) {
    c = tolower(c);

    if (already_used(c))
        return 2;

    used[used_count++] = c;
    used[used_count] = '\0';

    int len = strlen(answer);
    int correct = 0;

    for (int i = 0; i < len; i++) {
        if (answer[i] == c) {
            current[i] = c;
            correct = 1;
        }
    }

    if (!correct)
        remaining--;

    return correct;
}

DLLEXPORT const char* get_current() {
    return current;
}

DLLEXPORT const char* get_used() {
    return used;
}

DLLEXPORT int get_remaining() {
    return remaining;
}

DLLEXPORT int is_finished() {
    if (remaining <= 0)
        return 1;
    if (strcmp(current, answer) == 0)
        return 1;
    return 0;
}
