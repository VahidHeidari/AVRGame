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
#ifndef AVR8_H
#define AVR8_H

#include <stdint.h>
#include <stdio.h>		// FILE error!
#include <string.h>

#include <iostream>

#include "uzerom.h"

#if defined (_MSC_VER) && _MSC_VER >= 1400
	// don't whine about sprintf and fopen.
	// could switch to sprintf_s but that's not standard.
	#pragma warning(disable:4996)
#endif

#define IOBASE		32
#define SRAMBASE	(32 + ioSize)



typedef uint8_t u8;
typedef int8_t s8;
typedef uint16_t u16;
typedef int16_t s16;
typedef uint32_t u32;
typedef int32_t s32;

// 644 Overview:  http://www.atmel.com/dyn/resources/prod_documents/doc2593.pdf
// AVR8 insn set: http://www.atmel.com/dyn/resources/prod_documents/doc0856.pdf
// ATmega8
const unsigned sramSize = 1024;
const unsigned progSize = 8 * 1024;
const unsigned ioSize = 64;



typedef struct instrDec_Tag {
	s16  arg2;
	u8   arg1;
	u8   opNum;
} __attribute__((packed)) instructionDecode_t;

typedef struct instrList_Tag {
	u8   opNum;
	char opName[32];
	u8   arg1Type;
	u8   arg1Mul;
	u8   arg1Offset;
	u8   arg1Neg;
	u8   arg2Type;
	u8   arg2Mul;
	u8   arg2Offset;
	u8   arg2Neg;
	u8   words;
	u8   clocks;
	u16  mask;
	u16  arg1Mask;
	u16  arg2Mask;
} instructionList_t;



namespace ports
{

enum
{
	TWBR,         TWSR,         TWAR,         TWDR,         
	ADCL,         ADCH,         ADCSRA,       ADMUX,        
	ACSR,         UBRRL,        UCSRB,        UCSRA,        
	UDR,          SPCR,         SPSR,         SPDR,         
	PIND,         DDRD,         PORTD,        PINC,         
	DDRC,         PORTC,        PINB,         DDRB,         
	PORTB,        reserved0x39, reserved0x3a, reserved0x3b, 
	EECR,         EEDR,         EEARL,        EEARH,        
	UBRRH,        WDTCR,        ASSR,         OCR2,         
	TCNT2,        TCCR2,        ICR1L,        ICR1H,        
	OCR1BL,       OCR1BH,       OCR1AL,       OCR1H,        
	TCNT1L,       TCNT1H,       TCCR1B,       TCCR1A,       
	SFIOR,        OSCCAL,       TCNT0,        TCCR0,        
	MCUCSR,       MCUCR,        TWCR,         SPMCR,        
	TIFR,         TIMSK,        GIFR,         GICR,         
	reserved0x5c, SPL,          SPH,          SREG,         
};

extern const char* IO_NAMES[ioSize];

}

struct avr8
{
	avr8() :
		/*Core*/
		pc(0),
		cycleCounter(0)
	{
		memset(r, 0, 32 * sizeof(r[0]));
		memset(io, 0, ioSize * sizeof(io[0]));
		memset(sram, 0, sramSize * sizeof(sram[0]));
		memset(progmem, 0, (progSize / 2) * sizeof(progmem[0]));
		memset(progmemDecoded, 0, (progSize / 2) * sizeof(progmemDecoded[0]));
	}

	/*Core*/
	u16 progmem[progSize / 2];
	instructionDecode_t progmemDecoded[progSize / 2];
	u16 pc;
	u16 currentPc;

private:
	unsigned int cycleCounter;
	unsigned int cycle_ctr_ins;  // Used in update_hardware_ins to track elapsed cycles between calls
	// u8 eeClock; TODO: Only set at one location, never used. Maybe a never completed EEPROM timing code.

public:
	u16 decodeArg(u16 flash, u16 argMask, u8 argNeg);
	void instructionDecode(u16 address);
	void decodeFlash(void);
	void decodeFlash(u16 address);

	struct
	{
		union
		{
			u8 r[32];		// Register file
			struct
			{
				u8 r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15;
				u8 r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, XL, XH, YL, YH, ZL, ZH;
			};
		};
		union
		{
			u8 io[ioSize];		// Direct-mapped I/O space
			struct
			{
				u8 TWBR,         TWSR,         TWAR,         TWDR;
				u8 ADCL,         ADCH,         ADCSRA,       ADMUX;
				u8 ACSR,         UBRRL,        UCSRB,        UCSRA;
				u8 UDR,          SPCR,         SPSR,         SPDR;
				u8 PIND,         DDRD,         PORTD,        PINC;
				u8 DDRC,         PORTC,        PINB,         DDRB;
				u8 PORTB,        reserved0x39, reserved0x3a, reserved0x3b;
				u8 EECR,         EEDR,         EEARL,        EEARH;
				u8 UBRRH_UCSRC,  WDTCR,        ASSR,         OCR2;
				u8 TCNT2,        TCCR2,        ICR1L,        ICR1H;
				u8 OCR1BL,       OCR1BH,       OCR1AL,       OCR1H;
				u8 TCNT1L,       TCNT1H,       TCCR1B,       TCCR1A;
				u8 SFIOR,        OSCCAL,       TCNT0,        TCCR0;
				u8 MCUCSR,       MCUCR,        TWCR,         SPMCR;
				u8 TIFR,         TIMSK,        GIFR,         GICR;
				u8 reserved0x5c, SPL,          SPH,          SREG;
			};
		};
		u8 sram[sramSize];
	};


private:
	void write_io(u8 addr,u8 value);
	u8 read_io(u8 addr);
	// Should not be called directly (see write_io)
	void write_io_x(u8 addr,u8 value);

	inline u8 read_progmem(u16 addr)
	{
		u16 word = progmem[addr >> 1];
		u8 res = (addr & 1) ? word >> 8 : word;
		printf(" CPP: read_progmem(addr:0x%x)  wrd:0x%x   res:0x%x\n", addr, word, res);
		return res;
	}


	inline void write_sram(u16 addr,u8 value)
	{
		sram[(addr - SRAMBASE) & (sramSize - 1U)] = value;
	}

	void write_sram_io(u16 addr,u8 value)
	{
		if(addr>=SRAMBASE)
		{
			sram[(addr - SRAMBASE) & (sramSize-1)] = value;
		}
		else if (addr >= IOBASE)
		{
			write_io(addr - IOBASE, value);
		}
		else
		{
			r[addr] = value;		// Write a register
		}
	}

	inline u8 read_sram(u16 addr)
	{
		return sram[(addr - SRAMBASE) & (sramSize - 1U)];
	}

	u8 read_sram_io(u16 addr)
	{

		if(addr>=SRAMBASE)
		{
			return sram[(addr - SRAMBASE) & (sramSize-1)];
		}
		else if (addr >= IOBASE)
		{
			return read_io(addr - IOBASE);
		}
		else
		{
			return r[addr];		// Read a register
		}
	}

	inline static unsigned int get_insn_size(unsigned int insn)
	{
		/* 41  LDS Rd,k (next word is rest of address)
		   82  STS k,Rr (next word is rest of address)
		   30  JMP k (next word is rest of address)
		   14  CALL k (next word is rest of address) */
		// This code is simplified by assuming upper k bits are zero on 644
		
		if (insn == 14 || insn == 30 || insn == 41 || insn == 82) {
			return 2U;
		} else {
			return 1U;
		}
	}

public:
	void trigger_interrupt(unsigned int location);
	unsigned int exec();
	void update_hardware();
	void update_hardware_fast();
	void update_hardware_ins();

	bool LoadStateFile(const char* path="state.txt");
	void Print(std::ostream& o=std::cout) const;
	void DumpState(const char* path="state.txt") const;
};

#endif

