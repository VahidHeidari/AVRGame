/******************************************************************************
 *                                                                            *
 *          8x8 Dot-Matrix Display Library                                    *
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
#include "Display.h"

// Standard libraries

// Other libraries
#ifdef __GNUC__
#include <util/delay.h>
#else
#include <delay.h>
#endif

// Project libraries
#include "Config.h"

/// Display buffer
unsigned char monitor[DISPLAY_BUFFER_SIZE] = {0, 0, 0, 0, 0, 0, 0, 0};

void initialize_display(void)
{
    // Out put display line scaner port.
    DISPLAY_LINE_PORT = 0xFF;
    DISPLAY_LINE_DDR  = 0xFF;

    // Out put display data port.
    DISPLAY_DATA_PORT = 0x00;
    DISPLAY_DATA_DDR  = 0xFF;

    clear_mon();
}

void disp(void)
{
    unsigned char i;

    for (i = 0; i < DISPLAY_BUFFER_SIZE; ++i)
    {
        DISPLAY_DATA_PORT = monitor[i];
        DISPLAY_LINE_PORT = ~(0x01 << i);
        delay_ms(1);
        DISPLAY_LINE_PORT = 0xFF;
    }
}

void clear_mon(void)
{
    unsigned char i;
    
    for (i = 0; i < DISPLAY_BUFFER_SIZE; ++i)
        monitor[i] = 0;
}

