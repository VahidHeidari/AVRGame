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
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
#include "Snake.h"

#define MAX_GAMES 3

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

	int selected_game = 0;
    while (1) {
		// Read input.
		if (LEFT_PRESSED()) {
			while (!LEFT_RELEASED())
				disp();

			if (--selected_game <= 0)
				selected_game = MAX_GAMES;
		}
		else if (RIGHT_PRESSED()) {
			while (!RIGHT_RELEASED())
				disp();

			++selected_game;
			selected_game %= MAX_GAMES;
		} 

		// Select Game.
		switch (selected_game) {
			case 0:
				memcpy_P(monitor, one, DISPLAY_BUFFER_SIZE);
				game = Pong;
				break;
			case 1:
				memcpy_P(monitor, two, DISPLAY_BUFFER_SIZE);
				game = Tetris;
				break;
			case 2:
				memcpy_P(monitor, three, DISPLAY_BUFFER_SIZE);
				game = Snake;
				break;
		}

		// Run game if selected.
		if (SELECT_PRESSED()) {
			while (SELECT_PRESSED())		// Wait untile select release.
				disp();

			game();		// Play game.
		}

		// Display selected game number.
        disp();
		++displrep;
	}
}

