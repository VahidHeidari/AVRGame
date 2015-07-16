/******************************************************************************
 *                                                                            *
 *          Fonts Used For Displaying Game information.                       *
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
#include "Font.h"

#ifndef __GNUC__
flash unsigned char font[] =
#else
unsigned char font[] PROGMEM =
#endif
{
    0xFF,       // 0b11111111,     1
    0x81,       // 0b10000001,
    0x89,       // 0b10001001,
    0x99,       // 0b10011001,
    0x89,       // 0b10001001,
    0x89,       // 0b10001001,
    0x9D,       // 0b10011101,
    0xFF,       // 0b11111111,

    0xFF,       // 0b11111111,     2
    0x81,       // 0b10000001,
    0x99,       // 0b10011001,
    0x85,       // 0b10000101,
    0x89,       // 0b10001001,
    0x91,       // 0b10010001,
    0x9D,       // 0b10011101,
    0xFF,       // 0b11111111,

    0xFF,       // 0b11111111,     3
    0x81,       // 0b10000001,
    0xBD,       // 0b10111101,
    0x85,       // 0b10000101,
    0x89,       // 0b10001001,
    0xA5,       // 0b10100101,
    0x99,       // 0b10011001,
    0xFF,       // 0b11111111,

    0xFF,       // 0b11111111,     4
    0x81,       // 0b10000001,
    0xA1,       // 0b10100001,
    0xA9,       // 0b10101001,
    0xA9,       // 0b10101001,
    0xBD,       // 0b10111101,
    0x89,       // 0b10001001,
    0xFF,       // 0b11111111,
};

