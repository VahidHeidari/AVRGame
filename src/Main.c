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

// Project libraries
#include "Config.h"
#include "Globals.h"
#include "Display.h"
#include "Font.h"
#include "Joystick.h"
#include "FlashConstant.h"

/// Hardware initialization.
void initialize_hardware(void)
{
    initialize_display();
    initialize_joystick();
}

/// Selecting and running game.
#ifndef __GNUC__
void
#else
int
#endif
main(void)
{
    initialize_hardware();

    memcpy_P(monitor, font, DISPLAY_BUFFER_SIZE);

    int selected_game = 0;
    while (1) {
        // Read input and select game number.
        if (LEFT_PRESSED()) {
            while (!LEFT_RELEASED())
                disp();

            if (--selected_game <= 0)
                selected_game = MAX_GAMES - 1;

            // Copy selected game to screen buffer.
            memcpy_P(monitor, font + (selected_game * FONT_HEIGHT), DISPLAY_BUFFER_SIZE);
        }
        else if (RIGHT_PRESSED()) {
            while (!RIGHT_RELEASED())
                disp();

            ++selected_game;
            selected_game %= MAX_GAMES;

            // Copy selected game to screen buffer.
            memcpy_P(monitor, font + (selected_game * FONT_HEIGHT), DISPLAY_BUFFER_SIZE);
        }


        // Run game, if selected.
        if (SELECT_PRESSED()) {
            while (SELECT_PRESSED())     // Wait untile select release.
                disp();

            games[selected_game]();     // Play game.
        }

        // Display selected game number.
        disp();
        ++displrep;
    }
}

