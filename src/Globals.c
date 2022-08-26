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

#include "Globals.h"

#include "Tetris.h"
#include "Pong.h"
#include "Snake.h"
#include "Quarth.h"

int i;
int j;
int displrep;

int player_x;
int player_y;
int player_frame_cnt;

int ball_x;
int ball_y;
int ball_frame_cnt;

int input_frame_cnt;

GameFunction games[MAX_GAMES] = { (GameFunction)Pong, Tetris, Snake, Quarth };

