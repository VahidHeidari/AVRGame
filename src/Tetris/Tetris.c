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
#ifdef __GNUC__
#include <avr/pgmspace.h>
#endif

// Project libraries
#include "Config.h"
#include "Display.h"
#include "Joystick.h"

extern int i, j, displrep;

static unsigned char stack[STACK_HEIGHT] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

/// Briks Spirits
#ifndef __GNUC__
flash unsigned char sp_brik[NUMBER_OF_BRIKS][BRIK_HEIGHT]=
#else
static unsigned char sp_brik[NUMBER_OF_BRIKS][BRIK_HEIGHT] PROGMEM =
#endif
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

static unsigned char brik[BRIK_HEIGHT];
static int brik_x;
static int brik_y;                     // Brik <X,Y> coordinate
static unsigned char checkmove = NOCHANGE;              // Brik Move To Left Chacking
static unsigned char brik_keycnt = BRIKE_KEYFRAMES;     // Brik Frame Counter
static unsigned char num;
static unsigned char move_keycnt = MOVE_KEYFRAMES;      // Move Brik Control Frame Counter
static unsigned char change = NOCHANGE;

void MyMove(void)
{
    if (move_keycnt <= 0)
    {
        move_keycnt = MOVE_KEYFRAMES;

        if(LEFT_PRESSED())
        {
            for (i = 0; i < BRIK_HEIGHT; ++i)
                checkmove |= brik[i];
            
            if ((checkmove & 0x80) == 0)
                brik_x++;

            checkmove = 0;
        }
        else if (RIGHT_PRESSED())
            if (brik_x > 0)
                brik_x--;
                
#ifndef __GNUC__
        for (i = 0; i < BRIK_HEIGHT; ++i)
            brik[i] = sp_brik[num][i] << brik_x;
#else
		for (i = 0; i < BRIK_HEIGHT; ++i) {
			brik[i] = pgm_read_byte(&sp_brik[num][i]);
			brik[i] <<= brik_x;
		}
#endif
    }

    // Run rotating brik at full speed.    
    if (ROTATE_PRESSED())
        change = NEXT;
        
    if (change == NEXT && ROTATE_RELEASED())
    {
        // Rotate and change brik.
        num = (num + 1) % NUMBER_OF_BRIKS;
        change = NOCHANGE;
    }

    move_keycnt--;
}

void BrikMove(void)
{
    if (brik_keycnt <= 0)
    {
        brik_keycnt = BRIKE_KEYFRAMES;

        // Check below of brik
        if ((brik[2] & stack[brik_y + STACK_OFF_SCREEN]) != 0)
        {
            stack[brik_y + 2] |= brik[2];
            stack[brik_y + 1] |= brik[1];
            stack[brik_y + 0] |= brik[0];

            NextBrik();
        }
        else
            brik_y++;       // go one step down.
    }

    if ((brik_keycnt <= 1) && (brik_y == 8))
    {
        // Brik erceived at end of stack
        stack[10] |= brik[2];
        stack[9]  |= brik[1];
        stack[8]  |= brik[0];

        NextBrik();
    }

    brik_keycnt--;
}

void CheckLine(void)
{
    if (brik_keycnt <= 1)
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

void PutBrik(void)
{
    for (i = 0; i < DISPLAY_BUFFER_SIZE; ++i)
        monitor[i] = stack[i + STACK_OFF_SCREEN];

    for (i = 0; i < BRIK_HEIGHT; ++i)
        monitor[brik_y + i - BRIK_HEIGHT] |= brik[i];
}

void Tetris(void)
{
	srand(displrep * 7 % 17);
    clear_mon();

    NextBrik();

    while (1)
    {
        MyMove();
        BrikMove();
        CheckLine();
        PutBrik();
        disp();
        clear_mon();
    };
}

void NextBrik(void)
{
    // Reset position.
    brik_x = 3;
    brik_y = 0;
    num = (unsigned char)rand() % NUMBER_OF_BRIKS;        // Get random number
	//num = 0;

#ifndef __GNUC__
    for (i = 0; i < BRIK_HEIGHT; ++i)
        brik[i] = sp_brik[num][i] << brik_x;    
#else
	for (i = 0; i < BRIK_HEIGHT; ++i) {
		brik[i] = pgm_read_byte(&sp_brik[num][i]);
		brik[i] <<= brik_x;
	}
#endif
}
