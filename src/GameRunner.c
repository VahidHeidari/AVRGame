/******************************************************************************
 *                                                                            *
 *                           Game Runner                                      *
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

#include "GameRunner.h"

#include "Display.h"
#include "Pong.h"

static int free_slot_index;
static Game* registered_games[MAX_GAMES];

void RunGame(pGame game)
{
    game->Initialize();

    while (1)
    {
        clear_mon();
        game->GetInput();

        if (!game->Run())
            break;

        game->Render();
        disp();
    }
}

void InitializeGames()
{
    RegisterGame(&pong);
    //RegisterGame(&tetris);
    //RegisterGame(&snake);
    //RegisterGame(&quarth);
}

int RegisterGame(pGame game)
{
    if (free_slot_index < MAX_GAMES) {
        registered_games[free_slot_index] = game;

        if (!game->Run)
            return FALSE;

        if (!game->Initialize)
            game->Initialize = GameNullFunction;

        if (!game->GetInput)
            game->GetInput = GameNullFunction;

        if (!game->Render)
            game->Render = GameNullFunction;

        ++free_slot_index;

        return TRUE;
    }
    
    return FALSE;
}

int NumberOfRegisteredGames()
{
    return free_slot_index;
}

void GameNullFunction()
{
}

