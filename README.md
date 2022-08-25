 Introduction:
===============

 AVRGame is a small, open source, and low cost handheld game console based on
 AVR microcontroller. It works with 2 AA size batteries, and have a 8x8 dot
 matrix display. Its joystick have 4 directional, and 1 fire/rotate push buttons.

 ![Completed AVRGame Board](Schematic/AVRGameBoard.jpg?raw=true "Completed AVRGame Board")

 AVRGame project contains the following modules and games:

 * Schematics
 * Configuration
 * Cross platform utilities
 * Global variables
 * Graphics display driver and fonts
 * Joystick
 * Pong game
 * Quarth game
 * Snake game
 * Tetris game


 Screenshots:
==============

Screenshot are captured by AVR Emulator that is written in Python.

 ![Pong](Images/Pong.gif?raw=true "Pong Game")


 ![Pong](Images/Pong-200x100.gif?raw=true "Pong Game Buttons")
 ![Tetris](Images/Tetris-200x100.gif?raw=true "Tetris Game")
 ![Snake](Images/Snake-200x100.gif?raw=true "Snake Game")


 Known issues:
===============
  * No collision detection in down moving ball in Pong game.
  * Only bottom of tetromino collision detection in tetris game.
  * Quarth have a bug when bullet fired and building moves down.


 Features:
===========
  * Main development compiler and platform is gcc-avr.
  * AVRGame is compatible with Codvision also, or can be compiled with it with minor changes.
