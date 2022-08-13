#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

IO_REGS_OFFSET = 0x20

IO_NAMES = [
    'TWBR',         # 0x20
    'TWSR',         # 0x21
    'TWAR',         # 0x22
    'TWDR',         # 0x23
    'ADCL',         # 0x24
    'ADCH',         # 0x25
    'ADCSRA',       # 0x26
    'ADMUX',        # 0x27
    'ACSR',         # 0x28
    'UBRRL',        # 0x29
    'UCSRB',        # 0x2a
    'UCSRA',        # 0x2b
    'UDR',          # 0x2c
    'SPCR',         # 0x2d
    'SPSR',         # 0x2e
    'SPDR',         # 0x2f
    'PIND',         # 0x30
    'DDRD',         # 0x31
    'PORTD',        # 0x32
    'PINC',         # 0x33
    'DDRC',         # 0x34
    'PORTC',        # 0x35
    'PINB',         # 0x36
    'DDRB',         # 0x37
    'PORTB',        # 0x38
    'reserved0x39', # 0x39
    'reserved0x3a', # 0x3a
    'reserved0x3b', # 0x3b
    'EECR',         # 0x3c
    'EEDR',         # 0x3d
    'EEARL',        # 0x3e
    'EEARH',        # 0x3f
    'UBRRH/UCSRC',  # 0x40
    'WDTCR',        # 0x41
    'ASSR',         # 0x42
    'OCR2',         # 0x43
    'TCNT2',        # 0x44
    'TCCR2',        # 0x45
    'ICR1L',        # 0x46
    'ICR1H',        # 0x47
    'OCR1BL',       # 0x48
    'OCR1BH',       # 0x49
    'OCR1AL',       # 0x4a
    'OCR1H',        # 0x4b
    'TCNT1L',       # 0x4c
    'TCNT1H',       # 0x4d
    'TCCR1B',       # 0x4e
    'TCCR1A',       # 0x4f
    'SFIOR',        # 0x50
    'OSCCAL',       # 0x51
    'TCNT0',        # 0x52
    'TCCR0',        # 0x53
    'MCUCSR',       # 0x54
    'MCUCR',        # 0x55
    'TWCR',         # 0x56
    'SPMCR',        # 0x57
    'TIFR',         # 0x58
    'TIMSK',        # 0x59
    'GIFR',         # 0x5a
    'GICR',         # 0x5b
    'reserved0x5c', # 0x5c
    'SPL',          # 0x5d
    'SPH',          # 0x5e
    'SREG',         # 0x5f
]

