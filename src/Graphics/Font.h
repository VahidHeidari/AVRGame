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

#ifndef FONT_H
#define FONT_H

#ifdef __GNUC__
#include <avr/pgmspace.h>
#endif
#include "Config.h"

#define FONT_WIDTH      8
#define FONT_HEIGHT     8

#ifndef __GNUC__
extern flash unsigned char one[];
extern flash unsigned char two[];
extern flash unsigned char three[];
#else
extern unsigned char one[] PROGMEM;
extern unsigned char two[] PROGMEM;
extern unsigned char three[] PROGMEM;
#endif

#endif 
