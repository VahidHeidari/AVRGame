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
 * 	 but WITHOUT ANY WARRANTY; without even the implied warranty of
 * 	 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * 	 GNU General Public License for more details.
 * 
 * 	 You should have received a copy of the GNU General Public License
 * 	 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

// This file library
#include "Font.h"

#ifndef __GNUC__
flash unsigned char one[] =
#else
unsigned char one[] PROGMEM =
#endif
{
    0xFF,		// 0b11111111,
    0x81,		// 0b10000001,
    0x89,		// 0b10001001,
    0x99,		// 0b10011001,
    0x89,		// 0b10001001,
    0x89,		// 0b10001001,
    0x9D,		// 0b10011101,
    0xFF,		// 0b11111111,
};

#ifndef __GNUC__
flash unsigned char two[] =
#else
unsigned char two[] PROGMEM =
#endif
{
    0xFF,		// 0b11111111,
    0x81,		// 0b10000001,
    0x99,		// 0b10011001,
    0x85,		// 0b10000101,
    0x89,		// 0b10001001,
    0x91,		// 0b10010001,
    0x9D,		// 0b10011101,
    0xFF,		// 0b11111111,
};
