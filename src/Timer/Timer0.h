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

#ifndef TIMER_0_H_
#define TIMER_0_H_

#define SEC2MSEC(X)             ((X) * 1000L)
#define MSEC2SEC(X)             ((X) / 1000.0)
#define USEC2SEC(X)             ((X) / 1000000.0)
#define SEC2USEC(X)             ((X) * 1000000L)

#define TIMER0_PRESCALER        1024L
#define TIMER0_OVF_INTERVALS    ((1000.0 / (F_CPU / (TIMER0_PRESCALER * 256.0))))

#define IDLE_TIME_SECONDS       2L
#define IDLE_TIME_MSEC          (SEC2MSEC(IDLE_TIME_SECONDS))
#define IDLE_TIME_USEC          (SEC2USEC(IDLE_TIME_SECONDS))

#define STOP_TIMER0()   do {    \
    TCCR0 = 0;                  \
} while (0)

#include "BeginHeaderCode.h"

void initialize_timer0(void);

#include "EndHeaderCode.h"

#endif

