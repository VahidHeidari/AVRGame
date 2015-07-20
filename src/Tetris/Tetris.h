/******************************************************************************
 *                                                                            *
 *                      Tetris Game                                           *
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

#ifndef TETRIS_H
#define TETRIS_H

#define NEXT                1
#define NOCHANGE            0
#define MOVE_KEYFRAMES      16
#define BRIKE_KEYFRAMES     32

#define STACK_HEIGHT        11
#define STACK_OFF_SCREEN    3

#define NUMBER_OF_BRIKS     13
#define BRIK_HEIGHT         3
#define BRIK_WIDTH          3

#include "BeginHeaderCode.h"

void Tetris(void);
void MyMove(void);
void BrickMove(void);
void CheckLine(void);
void PutBrick(void);
void NextBrick(void);

#include "EndHeaderCode.h"

#endif 

