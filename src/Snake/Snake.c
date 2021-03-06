/******************************************************************************
 *                                                                            *
 *                      Snake Game                                            *
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

#include "Snake.h"

#include <stdlib.h>

#include "Config.h"
#include "Globals.h"
#include "Display.h"
#include "Joystick.h"

static int snake_length;
static Direction snake[MAX_SNAKE_LENGTH];

void Snake()
{
    InitializeSnake();

    while (1) {
        // Clear screen buffer.
        clear_mon();

        // Check input.
        GetInput();

        // Do logic.
        CheckFeed();
        MoveSnake();

        // Put sprites on screen buffer.
        PutFood();
        PutSnake();

        // Display output.
        disp();
    }
}

void InitializeSnake()
{
    // Put head of snake at bottom left corner of screen.
    head_x = DISPLAY_WIDTH - 1;
    head_y = DISPLAY_HEIGHT - INITIAL_LENGTH;

    snake_length = INITIAL_LENGTH;
    for (i = 0; i < snake_length; ++i)
        snake[i] = UP;

    GenerateFood();

    snake_frame_cnt = SNAKE_FRAME_CNT;
    food_blink_cnt = FOOD_BLINK_CNT;

    input_frame_cnt = SNAKE_INPUT_FRAME_CNT;
}

void GenerateFood()
{
    // For checking that generated food doesn't overlap with snake, we must place
    // snake first to screen buffer. And also place last food position on screen
    // to prevent regenerating same position.
    PutSnake();
    monitor[food_y] |= 1 << food_x;

    do {
        food_x = rand() % DISPLAY_WIDTH;
        food_y = rand() % DISPLAY_HEIGHT;
    } while (monitor[food_y] & (1 << food_x));

    // Atlast clear artifacts.
    clear_mon();
}

void GetInput()
{
    if (--input_frame_cnt <= 0) {
        input_frame_cnt = SNAKE_INPUT_FRAME_CNT;

        if (LEFT_PRESSED() && snake[0] != RIGHT)
            snake[0] = LEFT;
        else if (RIGHT_PRESSED() && snake[0] != LEFT)
            snake[0] = RIGHT;
        else if (DOWN_PRESSED() && snake[0] != UP)
            snake[0] = DOWN;
        else if (UP_PRESSED() && snake[0] != DOWN)
            snake[0] = UP;
    }
}

void GetNextPos(Direction dir, int* x, int* y)
{
    switch (dir) {
        case UP:
            if (--*y < 0)
                *y = DISPLAY_HEIGHT - 1;
            break;
        case DOWN:
            ++*y;
            *y %= DISPLAY_HEIGHT;
            break;
        case RIGHT:
            if (--*x < 0)
                *x = DISPLAY_WIDTH - 1;
            break;
        case LEFT:
            ++*x;
            *x %= DISPLAY_WIDTH;
            break;
        default:
            break;
    }
}

void GetPrevPos(Direction dir, int* x, int* y)
{
    switch (dir) {
        case UP:
            ++*y;
            *y %= DISPLAY_HEIGHT;
            break;
        case DOWN:
            if (--*y < 0)
                *y = DISPLAY_HEIGHT - 1;
            break;
        case RIGHT:
            ++*x;
            *x %= DISPLAY_WIDTH;
            break;
        case LEFT:
            if (--*x < 0)
                *x = DISPLAY_WIDTH - 1;
            break;
        default:
            break;
    }
}

void CheckSelfEat(void)
{
    int x = head_x;
    int y = head_y;

    for (i = 1; i < snake_length; ++i) {
        GetPrevPos(snake[i], &x, &y);

        if (x == head_x && y == head_y)     // End of game
            InitializeSnake();
    }
}

void CheckFeed()
{
    if (snake_frame_cnt <= 0) {
        if (snake_length == MAX_SNAKE_LENGTH)       // End of game
            InitializeSnake();

        if (head_x == food_x && head_y == food_y) {
            ++snake_length;
            GenerateFood();
        }
    }
}

void PutFood()
{
    if (--food_blink_cnt < 0) {
        food_blink_cnt = FOOD_BLINK_CNT;
        monitor[food_y] ^= 1 << food_x; 
    }
}

void PutSnake()
{
    int x = head_x;
    int y = head_y;

    monitor[y] |= (1 << x);
    for (i = 1; i < snake_length; ++i) {
        GetPrevPos(snake[i], &x, &y);
        monitor[y] |= (1 << x);
    }
}

void MoveSnake()
{
    if (--snake_frame_cnt < 0) {
        snake_frame_cnt = SNAKE_FRAME_CNT;

        // Shift snake.
        for (i = snake_length - 1; i >= 1; --i)
            snake[i] = snake[i - 1];

        // Move head of snake to last direction.
        GetNextPos(snake[0], &head_x, &head_y);
        CheckSelfEat();
    }
}

