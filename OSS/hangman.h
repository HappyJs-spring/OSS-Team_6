#pragma once
#ifndef HANGMAN_H
#define HANGMAN_H

#ifdef _WIN32
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT
#endif


DLLEXPORT void init_game();
DLLEXPORT int guess_char(char c);
DLLEXPORT const char* get_current();
DLLEXPORT const char* get_used();
DLLEXPORT int get_remaining();
DLLEXPORT int is_finished();

#endif
