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

static unsigned long current_time;
static unsigned long callback_interval;
static unsigned long next_interval_time;
static Timer0Callback timer0_callback;

void initialize_timer0()
{
    current_time = 0;
    callback_interval = 0;
    next_interval_time = 0;
    timer0_callback = 0;        // TODO: Replace NULL insted of 0.

    START_TIMER0();         // 1024 prescaler (clk i/o / 1024). F = 15.3 Hz, T = 65 ms
    TIMSK |= (1 << TOIE0);  // Enable Timer0 overflow interrupt.

    sei();      // Enable global intrrupt.
}

unsigned long timer0_get_time_ms()
{
    return (current_time * TIMER0_OVF_INTERVALS);
}

void timer0_set_callback_interval(unsigned long interval)
{
    callback_interval = interval;

    next_interval_time = current_time + callback_interval;
}

unsigned long timer0_get_callback_interval()
{
    return callback_interval;
}

void timer0_set_callback_interval_ms(unsigned long interval)
{
    if (interval && interval < TIMER0_OVF_INTERVALS)        // Minimum interval guaranteed.
        interval = TIMER0_OVF_INTERVALS;

    callback_interval = interval / TIMER0_OVF_INTERVALS;

    next_interval_time = current_time + callback_interval;
}

unsigned long timer0_get_callback_interval_ms()
{
    return callback_interval * TIMER0_OVF_INTERVALS;
}

void timer0_set_callback(Timer0Callback callback)
{
    timer0_callback = callback;
}

static ISR(TIMER0_OVF_vect)
{
    ++current_time;     // Advance current time.

    if (callback_interval && current_time == next_interval_time) {
        next_interval_time += callback_interval;        // Advance next interval time.

        /// TODO: Reset CPU if execution of callback is too long.
        if (timer0_callback)
            timer0_callback();      // Execute callback.
    }
}

