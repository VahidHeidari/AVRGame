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

#ifndef DISPLAY_H
#define DISPLAY_H

#define DISPLAY_BUFFER_SIZE     8
#define DISPLAY_WIDTH			8
#define DISPLAY_HEIGHT			8

#define DISPLAY_DATA_PORT       PORTD
#define DISPLAY_DATA_PIN        PIND
#define DISPLAY_DATA_DDR        DDRD

#define DISPLAY_LINE_PORT       PORTB
#define DISPLAY_LINE_PIN        PINB
#define DISPLAY_LINE_DDR        DDRB

/// Display buffer
extern unsigned char monitor[DISPLAY_BUFFER_SIZE];

#ifndef __GNUC__
#pragma used+
#endif

void initialize_display(void);
void disp(void);
void clear_mon(void);

#ifndef __GNUC__
#pragma used-
#endif

#endif 
