/******************************************************************************
 *                                                                            *
 *                      Timer\Counter 0 operation                             *
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

#include "Timer0.h"

#include <avr/interrupt.h>

#include "Config.h"

static long current_time = 0;

void initialize_timer0()
{
    TCCR0 = 0x05;           // 1024 prescaler (clk i/o / 1024). F = 15.3 Hz, T = 65 ms
    TIMSK |= (1 << TOIE0);  // Enable Timer0 overflow interrupt.

    sei();      // Enable global intrrupt.
}

static ISR(TIMER0_OVF_vect)
{
    ++current_time;
}

