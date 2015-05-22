/******************************************************************************
 *                                                                            *
 *                      AVR Game Demo                                         *
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
 
// Other libraries
#include <avr/pgmspace.h>

// Project libraries
#include "Config.h"
#include "Display.h"
#include "Font.h"
#include "Joystick.h"
#include "Pong.h"
#include "Tetris.h"

/// Game function
typedef void (*Game)(void);

/// Global variables
int i, j, displrep;

/// Selected game
Game game = Pong;

/// Hardware initialization.
void initialize_hardware(void)
{
    initialize_display();
	initialize_joystick();
}

/// Selecting and running game.
#ifndef __GNUC__
void main(void)
#else
int main()
#endif
{
    initialize_hardware();
	
	memcpy_P(monitor, one, DISPLAY_BUFFER_SIZE);

    while (1) {
		// Read input
		if (LEFT_PRESSED()) {
			memcpy_P(monitor, one, DISPLAY_BUFFER_SIZE);
			game = Pong;
		}
		else if (RIGHT_PRESSED()) {
			memcpy_P(monitor, two, DISPLAY_BUFFER_SIZE);
			game = Tetris;
		} 
		else if (SELECT_PRESSED()) {
			while (SELECT_PRESSED())		// Wait untile select release.
				disp();

			game();		// Play game.
		}

        disp();
	}
}
