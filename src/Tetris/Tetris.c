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

// This file library
#include "Tetris.h"

// Standard libraries
#include <stdlib.h>

// Other libraries

// Project libraries
#include "Config.h"
#include "Globals.h"
#include "Display.h"
#include "Joystick.h"
#include "FlashConstant.h"

static unsigned char stack[STACK_HEIGHT] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

/// Bricks Spirits
static FLASH_CONSTANT(unsigned char sp_brick[NUMBER_OF_BRIKS][BRIK_HEIGHT]) =
{
    {           //----------
        0x00,
        0x03,          ////
        0x03,          ////
    },          //----------
    {          //---------
        0x00,
        0x06,        ////
        0x03,          ////
    },
    {
        0x02,         //
        0x03,         ////
        0x01,           //
    },         //----------

    {         //----------
        0x01,          //
        0x01,          //
        0x01,          //
    },
    {
        0x00,
        0x00,       //////
        0x07,
    },         //----------

    {         //----------
        0x02,        //
        0x02,        //
        0x03,        ////
    },
    {
        0x00,
        0x07,      //////
        0x04,      //
    },
    {
        0x03,       ////
        0x01,         //
        0x01,         //
    },
    {
        0x00,          //
        0x01,      //////
        0x07,
    },          //----------

    {          //----------
        0x01,           //
        0x01,           //
        0x03,         ////
    },
    {
        0x00,
        0x04,      //
        0x07,      //////
    },
    {
        0x03,        ////
        0x02,        //
        0x02,        //
    },
    {
        0x00,
        0x07,     //////
        0x01,         //
    }        //----------

};

static unsigned char brick[BRIK_HEIGHT];
static unsigned char checkmove = NOCHANGE;              // Brick Move To Left Checking.
static unsigned char num;
static unsigned char change = NOCHANGE;

void MyMove(void)
{
    if (move_keycnt <= 0)
    {
        move_keycnt = MOVE_KEYFRAMES;

        if(LEFT_PRESSED())
        {
            for (i = 0; i < BRIK_HEIGHT; ++i)
                checkmove |= brick[i];
            
            if ((checkmove & 0x80) == 0)
                brick_x++;

            checkmove = 0;
        }
        else if (RIGHT_PRESSED())
            if (brick_x > 0)
                brick_x--;

        for (i = 0; i < BRIK_HEIGHT; ++i)
            brick[i] = READ_BYTE(sp_brick[num][i]) << brick_x;
    }

    // Run rotating brick at full speed.    
    if (ROTATE_PRESSED())
        change = NEXT;
        
    if (change == NEXT && ROTATE_RELEASED())
    {
        // Rotate and change brick.
        num = (num + 1) % NUMBER_OF_BRIKS;
        change = NOCHANGE;
    }

    move_keycnt--;
}

void BrickMove(void)
{
    if (brick_keycnt <= 0)
    {
        brick_keycnt = BRIKE_KEYFRAMES;

        // Check below of brick
        if ((brick[2] & stack[brick_y + STACK_OFF_SCREEN]) != 0)
        {
            stack[brick_y + 2] |= brick[2];
            stack[brick_y + 1] |= brick[1];
            stack[brick_y + 0] |= brick[0];

            NextBrick();
        }
        else
            brick_y++;       // go one step down.
    }

    if ((brick_keycnt <= 1) && (brick_y == 8))
    {
        // Brick erceived at end of stack
        stack[10] |= brick[2];
        stack[9]  |= brick[1];
        stack[8]  |= brick[0];

        NextBrick();
    }

    brick_keycnt--;
}

void CheckLine(void)
{
    if (brick_keycnt <= 1)
    {
        for (i = STACK_HEIGHT - 1; i >= STACK_OFF_SCREEN; --i)
        {
            if (stack[i] == (unsigned char)0xff)        // Full line?
            {
                // Clear line.
                for (j = 0; j < DISPLAY_BUFFER_SIZE; ++j)
                {
                    stack[i] &= ~(0x01 << j);        // Clear one block.

                    for (displrep = 0; displrep < DISPLAY_BUFFER_SIZE; ++displrep)
                        monitor[displrep] = stack[displrep + STACK_OFF_SCREEN];     // Update video buffer

                    for (displrep = 0; displrep <= 10; ++displrep)      // Display cleared block.
                        disp();

                    clear_mon();
                }

                // Shift stack one step down.
                for (j = i; j >= STACK_OFF_SCREEN; --j)
                    stack[j] = stack[j - 1];

                ++i;        // Search reminding full lines again.
            }
        }

        // Is stack full?    
        if (stack[2] != 0)
            for (i = 0; i < STACK_HEIGHT; ++i)
                stack[i] = 0;        // Simply clear it.
    }
}

void PutBrick(void)
{
    for (i = 0; i < DISPLAY_BUFFER_SIZE; ++i)
        monitor[i] = stack[i + STACK_OFF_SCREEN];

    for (i = 0; i < BRIK_HEIGHT; ++i)
        monitor[brick_y + i - BRIK_HEIGHT] |= brick[i];
}

void Tetris(void)
{
    // Initialize game
    brick_keycnt = BRIKE_KEYFRAMES;     // Brick Frame Counter
    move_keycnt = MOVE_KEYFRAMES;      // Move Brick Control Frame Counter

    clear_mon();

    NextBrick();

    while (1)
    {
        MyMove();
        BrickMove();
        CheckLine();
        PutBrick();
        disp();
        clear_mon();
    };
}

void NextBrick(void)
{
    // Reset position.
    brick_x = 3;
    brick_y = 0;
    num = (unsigned char)rand() % NUMBER_OF_BRIKS;        // Get random number

    for (i = 0; i < BRIK_HEIGHT; ++i)
        brick[i] = READ_BYTE(sp_brick[num][i]) << brick_x;
}

