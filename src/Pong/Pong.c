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

// This file library
#include "Pong.h"

// Project libraries
#include "Config.h"
#include "Display.h"
#include "Joystick.h"
#include "Font.h"

#define one     0
#define two     1

/**
 * Ball dx
 *
 * (dx = direction of x)
 * if dx == 1 ball moving to left
 * if dx == -1 ball moving to right
 */
static signed char dx = 1;

/**
 * Ball dy
 *
 * (dy = direction of y)
 * if dy == -1 ball moving upward
 * if dy == 1 ball moving downward
 */
static signed char dy = -1;

static unsigned char shild[SHILD_SIZE] = {0xFF, 0xFF, 0xFF};   /// Shilds
static char life = 3;                                          /// Number of lifes
static char stage = 1;                                         /// Speed Of Game

FLASH_CONSTANT(Game) pong = {InitializePong, Pong, GameNullFunction, PutSpriets};

void PutShild(void)
{
    if((ball_y >= 1) && (ball_y <= 3) && (dy == -1) && (ball_framecnt >= 1))
    {
        /** 
         * Check upper head of ball
         *  ________
         * |xxxxxxxx|
         * |xxxxxxxx|
         * | xxxx   |
         * |  o     |
         * |        |
         * |        |
         * |        |
         * |___==___|
         */
        if((0x01 << ball_x) & shild[ball_y - 1])
        {
            // Ball collided with shild block.
            dy = 1;     // Change direction of ball.
            shild[ball_y - 1] &= ~(0x01 << ball_x);     // Clear block.
        }
        else if ((ball_y > 0) && (ball_y < 4))
        {
            /** 
             * Check Left of ball (Ball moving <- and up).
             *  ________
             * |xxxxxxxx|
             * |xxxxxxxx|
             * | xxxx   |
             * |     o  |
             * |        |
             * |        |
             * |        |
             * |___==___|
             */
            if ((dx == 1) && ((0x01 << (ball_x + 1)) & shild[ball_y - 1]))
            {
                dy = 1;         // Change direction of ball.
                dx = -1;
                shild[ball_y - 1] &= ~(0x01 << (ball_x + 1));     // Clear block.
            }
            else
                if ((dx == -1) && ((0x01 << (ball_x - 1)) & (shild[ball_y - 1])))
                {
                    /** 
                     * Check Right of ball (ball moving -> and up).
                     *  ________
                     * |xxxxxxxx|
                     * |xxxxxxxx|
                     * |  xxxx  |
                     * | o      |
                     * |        |
                     * |        |
                     * |        |
                     * |___==___|
                     */
                    dy = 1;     // Change direction of ball.
                    dx = 1;
                    shild[ball_y - 1] &= ~(0x01 << (ball_x - 1));     // Clear block.
                }
        }

        if ((shild[0] | shild[1] | shild[2]) == 0)      // All shilds cleared
        {
            if(stage > 10)
                stage = 0;          // Reset game
            else
                stage += 3;         // Next level

            ResetShild();
        }
    }
}

void ResetShild(void)
{
    // Reset game variables
    racket_x = 3;
    ball_x = 3;
    ball_y = 6;
    dy = -1;

    // Reset shild
    shild[0] = 0xff;
    shild[1] = 0xff;
    shild[2] = 0xff;

	clear_mon();
}

void BallMove(void)
{
#ifndef __GNUC__
    int i;
#endif
    int displrep;
    // Speed up ball movement.
    if (SPEED_PRESSED())
        ball_framecnt -= 2;

    if (ball_framecnt <= 0)
    {
        //Player Ball Speed Controll
        ball_framecnt = BALL_KEYFRAMES - stage;                       // Frame cunter
        monitor[ball_y] &= ~(0x01 << ball_x);

        // Change direction of ball if collided with left, right, or upper side of screen.
        if(ball_x <= 0) dx = 1;
        if(ball_x >= 7) dx =-1;
        if(ball_y <= 0) dy = 1;

        // Check for colliding with racket
        if (ball_y == 6)
        {
            /**
             * Ball landed at racket.
             *
             * |        |        |        |
             * |  o     |        |   o    |
             * |__==____|   or   |__==____|
             */
            if ((ball_x == racket_x) || (ball_x == racket_x + 1))
                dy = -1;        // Chenge direction of ball.
            else
                if ((dx > 0) && (ball_x + 1 == racket_x))
                {
                    /**
                     * Check right collition (Ball moving <- and down).
                     *
                     * |        |
                     * |    o   |
                     * |__==____|
                     */
                    dy = -1;        // Chenge direction of ball.
                    dx = -1;
                }
                else
                    if ((dx < 0) && (ball_x - 1 == racket_x + 1))
                    {
                        /**
                         * Check left collition (Ball moving -> and down).
                         *
                         * |        |
                         * | o      |
                         * |__==____|
                         */
                        dy = -1;    // Change direction of ball.
                        dx = 1;
                    }
        }

        // Racket failed to catch ball and ball received to floor
        if (ball_y >= 7)
        {
            int number = one;        // Pointer to number of life

            // Initialize game variables for new game
            life--;
            ball_x = racket_x;
            ball_y = 6;
            dy = -1;

             // Game over, initialize variables for new game.
            if(life <= 0)
            {
                life = 3;
                ResetShild();
                clear_mon();
            }
            else
            {
                switch (life)
                {
                    case 2:
                        number = two;
                        break;

                    case 1:
                        number = one;
                        break;
                }
#ifndef __GNUC__
                // Display number of lifes
                for (i = 0; i < DISPLAY_BUFFER_SIZE; ++i)
                    monitor[i] = font[number * FONT_HEIGHT + i]
#else
                memcpy_P(monitor, &font[number * FONT_HEIGHT], DISPLAY_BUFFER_SIZE);
#endif

                displrep = 0;
                while (displrep++ <= 128)
                    disp();

                clear_mon();
            }
        }

        // Change direction of ball
        if(ball_x <= 0) dx = 1;
        if(ball_x >= 7) dx =-1;
        if(ball_y <= 0) dy = 1;

        // Move ball
        ball_y += dy;
        ball_x += dx;
    }

    ball_framecnt--;
}

void RacketMove(void)
{
    if(racket_framecnt <= 0)
    {
        racket_framecnt = RACKET_KEYFRAMES;     // Update racket frame counter

        monitor[7] &= ~(0x03 << racket_x);      // Clear racket from video buffer

        // Update racket position by user input
        if (LEFT_PRESSED())
            if(racket_x + 1 <= 6)
                racket_x++;

        if (RIGHT_PRESSED())
            if (racket_x > 0)
                racket_x--;
    }

    racket_framecnt--;
}

void PutSpriets(void)
{
    int i;
    for (i = 0; i < SHILD_SIZE; ++i)            // Put shild
        monitor[i] = shild[i];

    monitor[ball_y] |= 0x01 << ball_x;  // Put ball

    monitor[7] |= 0x03 << racket_x;     // Put racket
}

char Pong(void)
{

    InitializePong();

    while (1)
    {
        PutShild();
        BallMove();
        RacketMove();
        PutSpriets();
        disp();
    };

    return 1;
}

void InitializePong(void)
{
    // Initialize game.
    racket_framecnt = RACKET_KEYFRAMES;         // Raket Key Frame Counter
    ball_framecnt = BALL_KEYFRAMES;             // Ball Key Frame Counter
	racket_x = 3;
	ball_x = 3;
	ball_y = 6;

    clear_mon();
}

