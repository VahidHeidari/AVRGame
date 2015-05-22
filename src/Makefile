F_CPU=8000000
AVR_CHIP=__AVR_ATmega8__
CC=avr-gcc
FLAGS=-g -Wall -Wextra -pedantic -std=c99 -Os -DF_CPU=$(F_CPU) -D$(AVR_CHIP)
OBJ=display.o font.o joystick.o pong.o tetris.o main.o

all: $(OBJ)
	$(CC) $(FLAGS) $(OBJ) -o AVR_GAME.elf
	avr-objcopy -O coff-avr AVR_GAME.elf AVR_GAME.cof
	avr-objcopy -O ihex AVR_GAME.elf AVR_GAME.hex

display.o:
	$(CC) $(FLAGS) -c Display.c -o display.o

font.o:
	$(CC) $(FLAGS) -c Font.c -o font.o

joystick.o:
	$(CC) $(FLAGS) -c Joystick.c -o joystick.o

main.o:
	$(CC) $(FLAGS) -c Main.c -o main.o

pong.o:
	$(CC) $(FLAGS) -c Pong.c -o pong.o

tetris.o:
	$(CC) $(FLAGS) -c Tetris.c -o tetris.o

clean:
	rm -rf AVR_GAME.elf AVR_GAME.cof AVR_GAME.hex *.o *~
