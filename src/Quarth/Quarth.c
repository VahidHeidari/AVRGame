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

#include "Quarth.h"

#include <stdlib.h>

#include "Globals.h"
#include "Display.h"
#include "Joystick.h"

#ifndef FALSE
#define FALSE 0
#endif

#ifndef TRUE
#define TRUE 1
#endif

#ifndef MIN
#define MIN(X, Y) (((X) < (Y)) ? (X) : (Y))
#endif

#ifndef MAX
#define MAX(X, Y) (((X) > (Y)) ? (X) : (Y))
#endif

static int building_height;
static unsigned char shoot_right;

void Quarth()
{
    InitializeQuarth();

    while (1) {
		GetQuarthInput();
		MoveBullet();
		ShiftBuilding();
        disp();
    }
}

void InitializeQuarth()
{
    clear_mon();

    building_height = 0;
	building_frame_cnt = BUILDING_FRAME_CNT;

    player_x = 3;
    player_frame_cnt = PLAYER_FRAME_CNT;

    bullet_x = 0;
    bullet_y = -1;
    bullet_frame_cnt = BULLET_FRAME_CNT;

    shoot_right = TRUE;

    srand(displrep);

    PUT_PLAYER(player_x);
}

/**
 *
 * Shifts one step down building and generate a new blocks at top of screen, and checks
 * to see building is reaching to the end of screen or not.
 *
 *
 *           -------------                -------------                -------------     
 *           | o ooo oo  |                |           |                |oo ooo  ooo|
 * building  |o o ooo oo |                | o ooo oo  |                | o ooo oo  |
 * height -> |           |  =>  building  |o o ooo oo |  =>  building  |o o ooo oo |
 *           |           |      height -> |           |      height -> |           |
 *           |           |                |           |                |           |
 *           |           |                |           |                |           |
 *           -------------                -------------                -------------
 */
void ShiftBuilding()
{
    int r;

    if (--building_frame_cnt < 0) {
        building_frame_cnt = BUILDING_FRAME_CNT;

		// Shift building.
        for (i = building_height; i > 0; --i)
            monitor[i] = monitor[i - 1];

		// Generate new blocks.
        do {
            r = (unsigned char)rand();
        } while (r == COMPLETE_LINE);

        if ((monitor[0] |= r) == COMPLETE_LINE)
            monitor[0] ^= (1 << (r % DISPLAY_WIDTH));

		// Check end of game.
        if (++building_height > PLAYER_BASE_Y)
            InitializeQuarth();     // End of game
    }
}

void GetQuarthInput()
{
    if (--player_frame_cnt < 0) {
        player_frame_cnt = PLAYER_FRAME_CNT;

        if (LEFT_PRESSED() && (player_x < (DISPLAY_WIDTH - PLAYER_WIDTH))) {
            CLEAR_PLAYER(player_x);
            ++player_x;
            PUT_PLAYER(player_x);
        }
        else if (RIGHT_PRESSED() && player_x > 0) {
            CLEAR_PLAYER(player_x);
            --player_x;
            PUT_PLAYER(player_x);
        }
        else if (FIRE_PRESSED() && bullet_y < 0) {
            bullet_x = shoot_right ? player_x : player_x + PLAYER_WIDTH - 1;
            shoot_right ^= TRUE;
            bullet_y = BULLET_START_Y;
            bullet_frame_cnt = BULLET_FRAME_CNT;
            PUT_BULLET(bullet_x, bullet_y);
        }
    }
}

void MoveBullet()
{
    if (bullet_y >= -1 && --bullet_frame_cnt < 0) {
        bullet_frame_cnt = BULLET_FRAME_CNT;

        if (bullet_y >= 0) {
            // Check upper head of bullet.
            if (bullet_y == 0 || (monitor[bullet_y - 1] & (1 << bullet_x))) {
                building_height = MAX(building_height, bullet_y + 1);
                bullet_y = -1;                          // Move bullet off screen.
                CheckHuntedLine();
            } else {
                CLEAR_BULLET(bullet_x, bullet_y);       // Clear bullet.
                --bullet_y;                             // Move bullet one step up.
                PUT_BULLET(bullet_x, bullet_y);         // Put at new position.
            }
		}
    }
}

void CheckHuntedLine()
{
    for (i = 0; i < building_height; ++i) {
        if (monitor[i] == COMPLETE_LINE) {

            // Shift one step up.
            for (j = i; j < building_height && ((j + 1) < PLAYER_BASE_Y); ++j)
                monitor[j] = monitor[j + 1];

            monitor[j] ^= monitor[j];                   // Clear last building line.
            --i;                                        // Re-check this line.
            --building_height;
        }
    }
}

