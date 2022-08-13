#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

#
#          +---+--------+-------------+---------+-----------+----------+
#  Generl  |   |        |             |         |           |          |
#  Record  | : | RecLen | Load Offset | RecType | Info/Data | Checksum |
#  Format: |   |        |             |         |           |          |
#          +---+--------+-------------+---------+-----------+----------+
#  Byte(s):  1     1           2           1          n           1
#  char(s):  1     2           4           2         2*n          2
#

import os



MAX_LINE_LEN = 30

REC_TYPE_DATA = 0
REC_TYPE_END_OF_FILE = 1
REC_TYPE_EXT_SEG = 2
REC_TYPE_START_SEG = 3
REC_TYPE_EXT_LINEAR = 4
REC_TYPE_START_LINEAR = 5

RECORD_TYPES = {
    REC_TYPE_DATA         : 'Data Record',
    REC_TYPE_END_OF_FILE  : 'End of File Record',
    REC_TYPE_EXT_SEG      : 'Extended Segment Address Record',
    REC_TYPE_START_SEG    : 'Start Segment Address Record',
    REC_TYPE_EXT_LINEAR   : 'Extended Linear Address Record',
    REC_TYPE_START_LINEAR : 'Start Linear Address Record',
}

END_OF_FILE_REC = ':00000001FF'



class IntelHexReader:
    def __init__(self):
        self.error = ''
        self.memory_bytes = []


    def Reset(self):
        self.error = ''
        self.memory_bytes = []


    def HasError(self):
        return len(self.error) != 0


    def AppendError(self, msg):
        if self.error:
            self.error += '\n'
        self.error += msg


    def GetErrorMessage(self):
        return self.error


    def ReadFromFile(self, hex_path):
        self.Reset()
        if not os.path.isfile(hex_path):
            self.AppendError('No such file: ``%s\'\'' % hex_path)
            return False
        with open(hex_path, 'r') as f:
            hex_lines = f.readlines()
        if not self.IsInHexFormat(hex_lines):
            self.AppendError('The file ``%s\'\' is not in Intel hex format' % hex_path)
            return False
        self.FillMemoryBytes(hex_lines)
        return True


    def ReadFromString(self, hex_str):
        self.Reset()
        hex_lines = hex_str.split('\n')
        if not self.IsInHexFormat(hex_lines):
            self.AppendError('Input string is not in Intel hex format')
            return False
        self.FillMemoryBytes(hex_lines)
        return True


    def GetRecLen(self, hex_line):
        if len(hex_line) < 3:
            raise IndexError('line length is less than `RecLen\' length!')
        rec_len = int(hex_line[1:3], 16)
        return rec_len


    def GetLoadOffset(self, hex_line):
        if len(hex_line) < 7:
            raise IndexError('line length is less than `LoadOffset\' length!')
        load_offset = int(hex_line[3:7], 16)
        return load_offset


    def GetRecType(self, hex_line):
        if len(hex_line) < 9:
            raise IndexError('line length is less than `RecType\' length!')
        rec_type = int(hex_line[7:9], 16)
        return rec_type


    def GetData(self, hex_line):
        rec_len = self.GetRecLen(hex_line)
        data_bytes = []
        chr_idx = 9
        for i in range(rec_len):
            data_byte = int(hex_line[chr_idx : chr_idx + 2], 16)
            data_bytes.append(data_byte)
            chr_idx += 2
        return data_bytes


    def GetChecksum(self, hex_line):
        chk_sum = int(hex_line[-2:], 16)
        return chk_sum


    def GetMemoryBytes(self):
        return self.memory_bytes


    def GetNumBytes(self):
        return len(self.GetMemoryBytes())


    def IsChecksumOK(self, ln_num, hex_line):
        if len(hex_line) % 2 != 1:
            fmt_rec = (len(hex_line), ln_num + 1)
            self.AppendError('Length of characters (%d) in line %d is not correct!' % fmt_rec)
            return False

        num_bytes = (len(hex_line) - 3) / 2
        rec_len = self.GetRecLen(hex_line)
        if (rec_len + 4) != num_bytes:
            self.AppendError('Number of bytes (%d) is not equal to RECLEN (%d + 4)!' % (num_bytes, rec_len))
            return False

        chk_sum = self.GetChecksum(hex_line)
        sm = 0
        for i in range(num_bytes):
            idx_start = 1 + i * 2
            byte_val = int(hex_line[idx_start : idx_start + 2], 16)
            sm += byte_val
        res = (sm + chk_sum) & 0xFF
        if res != 0:
            self.AppendError('Checksum is not zero (0x%s)!' % hex(res))
            return False
        return True


    def IsInHexFormat(self, hex_lines):
        for i in range(len(hex_lines)):
            ln = hex_lines[i].strip()
            # Check RECORD MARK `:' character.
            if not ln.startswith(':'):
                ln_len = min(len(ln), MAX_LINE_LEN)
                ln_str = ln[0 : ln_len] + (' ...' if len(ln) != ln_len else '')
                self.AppendError('Line %d (`%s\') does not start with `:\' mark!' % ((i + 1), ln_str))
                return False

            # Check for invalid characters.
            for j in range(len(ln)):
                c = ln[j]
                if not c in ':0123456789ABCDEFabcdef':
                    INVALID_CHRS = [ '\r', '\n', '\t' ]
                    INVALID_CHRS_NAMES = [ '\\r', '\\n', '\\t' ]
                    if c in INVALID_CHRS:
                        c = INVALID_CHRS_NAMES[INVALID_CHRS.index(c)]
                    ln_len = min(len(ln), MAX_LINE_LEN)
                    ln_str = ln[0 : ln_len] + (' ...' if len(ln) != ln_len else '')
                    fmt_rec = (i + 1, j + 1, ln_str, c)
                    self.AppendError('Line %d,%d (`%s\') does contains invalid character `%s\'!' % fmt_rec)
                    return False

            # Check for checksum integrity.
            if not self.IsChecksumOK(i, ln):
                ln_len = min(len(ln), MAX_LINE_LEN)
                ln_str = ln[0 : ln_len] + (' ...' if len(ln) != ln_len else '')
                self.AppendError('Line %d (`%s\') checksum is not correct!' % ((i + 1, ln_str)))
                return False
        return True


    def FillMemoryBytes(self, hex_lines):
        for i in range(len(hex_lines)):
            ln = hex_lines[i].strip()
            if ln == END_OF_FILE_REC:
                break
            rec_type = self.GetRecType(ln)
            if rec_type == REC_TYPE_DATA:
                data_bytes = self.GetData(ln)
                self.memory_bytes += data_bytes

