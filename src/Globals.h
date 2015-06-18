/******************************************************************************
 *                                                                            *
 *                Global variables                                            *
 *                                                                            *
 * This is AVRGame project. AVRGame is a small, low cost, and open source     *
 * hand held console based on AVR microcontroller.                            *
 ******************************************************************************/

/**
 * Copyright (C) 2015  Vahid Heidari (DeltaCode)
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef GLOBALS_H_
#define GLOBALS_H_

#define MAX_GAMES       3

/// Tetris
#define brik_x          player_x
#define brik_y          player_y
#define brik_keycnt     player_frame_cnt
#define move_keycnt     input_frame_cnt

/// Pong
#define racket_x        player_x
#define racket_framecnt player_frame_cnt
#define ball_framecnt   ball_frame_cnt

///Snake
#define head_x          player_x
#define head_y          player_y
#define food_x          ball_x
#define food_y          ball_y
#define snake_frame_cnt player_frame_cnt
#define food_blink_cnt  ball_frame_cnt

/// loop variables
extern int i;
extern int j;
extern int displrep;

/// Player variables
extern int player_x;
extern int player_y;
extern int player_frame_cnt;

/// Ball variables
extern int ball_x;
extern int ball_y;
extern int ball_frame_cnt;

/// Input variables
extern int input_frame_cnt;

/// Game function
typedef void (*Game)(void);

/// Games
extern Game games[MAX_GAMES];

#endif

