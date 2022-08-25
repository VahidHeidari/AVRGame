#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

REG_FILE_SIZE   = 32
IO_SIZE         = 64
IO_MEM_MAP_SIZE = 160
RAM_SIZE        = 1024
RAM_START       = REG_FILE_SIZE + IO_SIZE + IO_MEM_MAP_SIZE
RAM_END         = REG_FILE_SIZE + IO_SIZE + IO_MEM_MAP_SIZE + RAM_SIZE

IO_NAMES = [
    'TWBR',         # 0x20    0x00
    'TWSR',         # 0x21    0x01
    'TWAR',         # 0x22    0x02
    'TWDR',         # 0x23    0x03
    'ADCL',         # 0x24    0x04
    'ADCH',         # 0x25    0x05
    'ADCSRA',       # 0x26    0x06
    'ADMUX',        # 0x27    0x07
    'ACSR',         # 0x28    0x08
    'UBRRL',        # 0x29    0x09
    'UCSRB',        # 0x2a    0x0a
    'UCSRA',        # 0x2b    0x0b
    'UDR',          # 0x2c    0x0c
    'SPCR',         # 0x2d    0x0d
    'SPSR',         # 0x2e    0x0e
    'SPDR',         # 0x2f    0x0f
    'PIND',         # 0x30    0x10
    'DDRD',         # 0x31    0x11
    'PORTD',        # 0x32    0x12
    'PINC',         # 0x33    0x13
    'DDRC',         # 0x34    0x14
    'PORTC',        # 0x35    0x15
    'PINB',         # 0x36    0x16
    'DDRB',         # 0x37    0x17
    'PORTB',        # 0x38    0x18
    'reserved0x39', # 0x39    0x19
    'reserved0x3a', # 0x3a    0x1a
    'reserved0x3b', # 0x3b    0x1b
    'EECR',         # 0x3c    0x1c
    'EEDR',         # 0x3d    0x1d
    'EEARL',        # 0x3e    0x1e
    'EEARH',        # 0x3f    0x1f
    'UBRRH/UCSRC',  # 0x40    0x20
    'WDTCR',        # 0x41    0x21
    'ASSR',         # 0x42    0x22
    'OCR2',         # 0x43    0x23
    'TCNT2',        # 0x44    0x24
    'TCCR2',        # 0x45    0x25
    'ICR1L',        # 0x46    0x26
    'ICR1H',        # 0x47    0x27
    'OCR1BL',       # 0x48    0x28
    'OCR1BH',       # 0x49    0x29
    'OCR1AL',       # 0x4a    0x2a
    'OCR1H',        # 0x4b    0x2b
    'TCNT1L',       # 0x4c    0x2c
    'TCNT1H',       # 0x4d    0x2d
    'TCCR1B',       # 0x4e    0x2e
    'TCCR1A',       # 0x4f    0x2f
    'SFIOR',        # 0x50    0x30
    'OSCCAL',       # 0x51    0x31
    'TCNT0',        # 0x52    0x32
    'TCCR0',        # 0x53    0x33
    'MCUCSR',       # 0x54    0x34
    'MCUCR',        # 0x55    0x35
    'TWCR',         # 0x56    0x36
    'SPMCR',        # 0x57    0x37
    'TIFR',         # 0x58    0x38
    'TIMSK',        # 0x59    0x39
    'GIFR',         # 0x5a    0x3a
    'GICR',         # 0x5b    0x3b
    'reserved0x5c', # 0x5c    0x3c
    'SPL',          # 0x5d    0x3d
    'SPH',          # 0x5e    0x3e
    'SREG',         # 0x5f    0x3f
]

INTERRUPT_NAMES = [
    'RESET',                # 1    0x000
    'INT0',                 # 2    0x002
    'INT1',                 # 3    0x004
    'TIMER2_COMP',          # 4    0x006
    'TIMER2_OVF',           # 5    0x008
    'TIMER1_CAPT',          # 6    0x00a
    'TIMER1_COMPA',         # 7    0x00c
    'TIMER1_COMPB',         # 8    0x00e
    'TIMER1_OVF',           # 9    0x010
    'TIMER0_OVF',           # 10   0x012
    'SPI_STC',              # 11   0x014
    'USART_RXC',            # 12   0x016
    'USART_UDRE',           # 13   0x018
    'USART_TXC',            # 14   0x01a
    'ADC',                  # 15   0x01c
    'EE_RDY',               # 16   0x01e
    'ANA_COMP',             # 17   0x020
    'TWI',                  # 18   0x022
    'SPM_RDY',              # 19   0x024
]

