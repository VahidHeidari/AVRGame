/******************************************************************************
 *                                                                            *
 *                      Snake Game                                            *
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

#ifndef SNAKE_H_
#define SNAKE_H_

#define INITIAL_LENGTH          3
#define MAX_SNAKE_LENGTH        20
#define SNAKE_FRAME_CNT         32
#define SNAKE_INPUT_FRAME_CNT   8
#define FOOD_BLINK_CNT          10

typedef enum
{
    NONE = 0,
    UP,
    DOWN,
    RIGHT,
    LEFT
} Direction;

#include "BeginHeaderCode.h"

void Snake(void);
void InitializeSnake(void);
void GetInput(void);
void GenerateFood(void);
void GetNextPos(Direction dir, int* x, int* y);
void GetPrevPos(Direction dir, int* x, int* y);
void CheckSelfEat(void);
void CheckFeed(void);
void PutFood(void);
void PutSnake(void);
void MoveSnake(void);

#include "EndHeaderCode.h"

#endif

