/******************************************************************************
 *                                                                            *
 *                   Constant Definitions In Flash.                           *
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

#ifndef FLASH_CONSTANT_H_
#define FLASH_CONSTANT_H_

// GCC compiler
#ifdef __GNUC__
#include <avr/pgmspace.h>

#define FLASH_CONSTANT(X)		X PROGMEM
#define READ_BYTE(X)			pgm_read_byte(&X)

// CodeVision compiler
#else

#define FLASH_CONST(X)			flash X
#define READ_BYTE(X)			(X)
#define memcpy_P				memcpy

#endif

#endif

