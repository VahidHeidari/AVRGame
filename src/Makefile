#
# This is AVRGame project. AVRGame is a small, low cost, and open source
# hand held console based on AVR microcontroller.
# Copyright (C) 2015  Vahid Heidari (DeltaCode)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

F_CPU=8000000
AVR_CHIP=__AVR_ATmega8__
CC=avr-gcc
FLAGS=-gdwarf-2 -Wall -Wextra -pedantic -std=c99 -Os -DF_CPU=$(F_CPU) -D$(AVR_CHIP) \
	  -ITetris -IPong -IGraphics -IJoystick -ISnake -I.
OBJ=display.o font.o joystick.o pong.o tetris.o snake.o main.o

all: $(OBJ)
	$(CC) $(FLAGS) $(OBJ) -o AVR_GAME.elf
	avr-objcopy -O coff-avr AVR_GAME.elf AVR_GAME.cof
	avr-objcopy -O ihex AVR_GAME.elf AVR_GAME.hex

display.o:
	$(CC) $(FLAGS) -c Graphics/Display.c -o display.o

font.o:
	$(CC) $(FLAGS) -c Graphics/Font.c -o font.o

joystick.o:
	$(CC) $(FLAGS) -c Joystick/Joystick.c -o joystick.o

main.o:
	$(CC) $(FLAGS) -c Main.c -o main.o

pong.o:
	$(CC) $(FLAGS) -c Pong/Pong.c -o pong.o

tetris.o:
	$(CC) $(FLAGS) -c Tetris/Tetris.c -o tetris.o

snake.o:
	$(CC) $(FLAGS) -c Snake/Snake.c -o snake.o

clean:
	rm -rf AVR_GAME.elf AVR_GAME.cof AVR_GAME.hex *.o *~ *.aps
	rm -rf Tetris/*.o Tetris/*~
	rm -rf Pong/*.o Pong/*~
	rm -rf Graphics/*.o Graphics/*~
	rm -rf Snake/*.o Snake/*~
	rm -rf Joystick/*.o Joystick/*~
