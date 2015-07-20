/******************************************************************************
 *                                                                            *
 *                      Pong Game                                             *
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

#ifndef PONG_H
#define PIONG_H

#define BALL_KEYFRAMES      32 
#define RACKET_KEYFRAMES    16
#define RACKET_SPRIET       0x03
#define SHILD_SIZE          3

#include "BeginHeaderCode.h"

void Pong(void);
void PutShild(void);
void ResetShild(void);
void BallMove(void);
void RacketMove(void);
void PutSpriets(void);

#include "EndHeaderCode.h"

#endif 

