/******************************************************************************
 *                                                                            *
 *          Joystick Library For Processing User inputs.                      *
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

#ifndef JOYSTICK_H
#define JOYSTICK_H

// Project libraries
#include "Config.h"

#define JOYSTICK_PORT       PORTC
#define JOYSTICK_PIN        PINC
#define JOYSTICK_DDR        DDRC

#define BUTTON_STATUS_NONE      0
#define BUTTON_STATUS_PRESSED   1
#define BUTTON_STATUS_RELEASED  2

// Arrow keys
#define LEFT_BUTTON         0
#define RIGHT_BUTTON        1
#define DOWN_BUTTON         2
#define UP_BUTTON           3

// Single key aliases
#define SELECT_BUTTON       4
#define FIRE_BUTTON         SELECT_BUTTON
#define ROTATE_BUTTON       SELECT_BUTTON
#define SPEED_BUTTON        SeLECT_BUTTON

// CodeVision style
#ifndef __GNUC__
#define LEFT_PRESSED()        (JOYSTICK_PIN.LEFT_BUTTON == 0)
#define LEFT_RELEASED()       (JOYSTICK_PIN.LEFT_BUTTON == 1)

#define RIGHT_PRESSED()       (JOYSTICK_PIN.RIGHT_BUTTON == 0)
#define RIGHT_RELEASED()      (JOYSTICK_PIN.RIGHT_BUTTON == 1)

#define DOWN_PRESSED()        (JOYSTICK_PIN.DOWN_BUTTON == 0)
#define DOWN_RELEASED()       (JOYSTICK_PIN.DOWN_BUTTON == 1)

#define UP_PRESSED()          (JOYSTICK_PIN.UP_BUTTON == 0)
#define UP_RELEASED()         (JOYSTICK_PIN.UP_BUTTON == 1)

#define SELECT_PRESSED()      (JOYSTICK_PIN.SELECT_BUTTON == 0)
#define SELECT_RELEASED()     (JOYSTICK_PIN.SELECT_BUTTON == 1)

// GCC style
#else
#define LEFT_PRESSED()        ((JOYSTICK_PIN & _BV(LEFT_BUTTON)) == 0)
#define LEFT_RELEASED()       ((JOYSTICK_PIN & _BV(LEFT_BUTTON)) == _BV(LEFT_BUTTON))

#define RIGHT_PRESSED()       ((JOYSTICK_PIN & _BV(RIGHT_BUTTON)) == 0)
#define RIGHT_RELEASED()      ((JOYSTICK_PIN & _BV(RIGHT_BUTTON)) == _BV(RIGHT_BUTTON))

#define DOWN_PRESSED()        ((JOYSTICK_PIN & _BV(DOWN_BUTTON)) == 0)
#define DOWN_RELEASED()       ((JOYSTICK_PIN & _BV(DOWN_BUTTON)) == _BV(DOWN_BUTTON))

#define UP_PRESSED()          ((JOYSTICK_PIN & _BV(UP_BUTTON)) == 0)
#define UP_RELEASED()         ((JOYSTICK_PIN & _BV(UP_BUTTON)) == _BV(UP_BUTTON))

#define SELECT_PRESSED()      ((JOYSTICK_PIN & _BV(SELECT_BUTTON)) == 0)
#define SELECT_RELEASED()     ((JOYSTICK_PIN & _BV(SELECT_BUTTON)) == _BV(SELECT_BUTTON))
#endif

#define FIRE_PRESSED()        SELECT_PRESSED()
#define FIRE_RELEASED()       SELECT_RELEASED()
#define ROTATE_PRESSED()      SELECT_PRESSED()
#define ROTATE_RELEASED()     SELECT_RELEASED()
#define SPEED_PRESSED()       SELECT_PRESSED()
#define SPEED_RELEASED()      SELECT_RELEASED()

#define IS_KEY_PRESSED(BUTTON, KEYS)    (((KEYS & (0x01 << BUTTON)) == 0) ? 1 : 0)
#define IS_KEY_RELEASED(BUTTON, KEYS)   (((KEYS & (0x01 << BUTTON)) == (0x01 << BUTTON)) ? 1 : 0)

#define GET_KEYS()      JOYSTICK_PIN

#include "BeginHeaderCode.h"

void initialize_joystick(void);
unsigned char get_keys(void);

#include "EndHeaderCode.h"

#endif 

