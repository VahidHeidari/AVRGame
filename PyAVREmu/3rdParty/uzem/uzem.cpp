/*
(The MIT License)

Copyright (c) 2008-2016 by
David Etherton, Eric Anderton, Alec Bourque (Uze), Filipe Rinaldi,
Sandor Zsuga (Jubatian), Matt Pandina (Artcfox)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

#include <stdio.h>			// stderr error!

#include <fstream>

#include "uzem.h"
#include "avr8.h"

#define printerr(fmt,...) fprintf(stderr,fmt,##__VA_ARGS__)



avr8 uzebox;



void showHelp(char* programName)
{
    printerr("Uzebox Emulator %s\n"
			"- Runs an Uzebox game file in either .hex or .uze format.\n"
			"Usage:\n",
		VERSION);
    printerr("\t%s HEX_PATH NUM_CYCLES\n",programName);
}

std::string MakeStatePath(const char* hex_img_path)
{
	std::string state_path = hex_img_path;
	auto idx = state_path.rfind('/');
	if (idx == std::string::npos) {
		idx = state_path.rfind('\\');
		if (idx == std::string::npos)
			return "state.txt";
	}

	state_path = state_path.substr(0, idx + 1);
	state_path += "state.txt";
	return state_path;
}

int main(int argc,char **argv)
{
    if(argc < 2) {
        showHelp(argv[0]);
		return 1;
    }

	// Get command line arguments.
	char* heximage = argv[1];
	std::cout << "loading    : `" << heximage << '\'' << std::endl;
	std::string state_path = MakeStatePath(argv[0]);
	std::cout << "State Path : `" << state_path << '\'' << std::endl;

	unsigned char* buffer = (unsigned char*)(uzebox.progmem);
	if (!loadHex(heximage, buffer)) {
		printerr("Error: cannot load HEX image '%s'.\n\n", heximage);
		showHelp(argv[0]);
		return 2;
	}
	uzebox.decodeFlash();

	uzebox.LoadStateFile(state_path.c_str());
	uzebox.exec();
	//uzebox.Print();
	uzebox.DumpState(state_path.c_str());
	return 0;
}

