#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

INTERRUPT_NAMES = [
    'RESET',                # 1    0x000
    'INT0',                 # 2    0x001
    'INT1',                 # 3    0x002
    'TIMER2_COMP',          # 4    0x003
    'TIMER2_OVF',           # 5    0x004
    'TIMER1_CAPT',          # 6    0x005
    'TIMER1_COMPA',         # 7    0x006
    'TIMER1_COMPB',         # 8    0x007
    'TIMER1_OVF',           # 9    0x008
    'TIMER0_OVF',           # 10   0x009
    'SPI_STC',              # 11   0x00A
    'USART_RXC',            # 12   0x00B
    'USART_UDRE',           # 13   0x00C
    'USART_TXC',            # 14   0x00D
    'ADC',                  # 15   0x00E
    'EE_RDY',               # 16   0x00F
    'ANA_COMP',             # 17   0x010
    'TWI',                  # 18   0x011
    'SPM_RDY',              # 19   0x012
]

