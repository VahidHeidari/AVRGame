/******************************************************************************
 *                                                                            *
 *                      Quarth Game                                           *
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
#ifndef LINE_HUNTER_H_
#define LINE_HUNTER_H_

#define LINE_HUNTER_INPUT_FRAME_CNT     10

#define PLAYER_FRAME_CNT                LINE_HUNTER_INPUT_FRAME_CNT
#define PLAYER_WIDTH                    2
#define PLAYER_PAD                      0x03
#define PLAYER_BASE_Y                   (DISPLAY_HEIGHT - 1)
#define MOVE_PLAYER(X)                  (PLAYER_PAD << (X))
#define CLEAR_PLAYER(X)                 (monitor[PLAYER_BASE_Y] &= ~(MOVE_PLAYER(X)))
#define PUT_PLAYER(X)                   (monitor[PLAYER_BASE_Y] |=  (MOVE_PLAYER(X)))

#define BULLET_FRAME_CNT                10
#define BULLET_START_Y                  (PLAYER_BASE_Y - 1)
#define CLEAR_BULLET(X, Y)              (monitor[(Y)] &= ~(1 << (X)))
#define PUT_BULLET(X, Y)                (monitor[(Y)] |=  (1 << (X)))

#define BUILDING_FRAME_CNT              200
#define COMPLETE_LINE					0xFF

#ifndef __GNUC__
#pragma used+
#endif

void Quarth(void);
void InitializeQuarth(void);
void ShiftBuilding(void);
void GetQuarthInput(void);
void MoveBullet(void);
void CheckHuntedLine(void);

#ifndef __GNUC__
#pragma used-
#endif

#endif

