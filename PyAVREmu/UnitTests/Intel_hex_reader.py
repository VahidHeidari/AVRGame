#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os
import unittest

import Intel_hex



class IntelHexFormatTestCases(unittest.TestCase):
    def test_IsInHexFormat(self):
        hex_fmt = Intel_hex.IntelHexReader()

        self.assertFalse(hex_fmt.IsInHexFormat(['abcd', 'efgh']))
        self.assertTrue(hex_fmt.HasError())
        hex_fmt.AppendError('--------')
        print(hex_fmt.GetErrorMessage())
        hex_fmt.Reset()

        self.assertTrue(hex_fmt.IsInHexFormat([':00000001FF']))
        self.assertFalse(hex_fmt.HasError())

        self.assertFalse(hex_fmt.IsInHexFormat([':AB112201FE']))
        self.assertTrue(hex_fmt.HasError())
        hex_fmt.AppendError('--------')
        print(hex_fmt.GetErrorMessage())
        hex_fmt.Reset()

        self.assertTrue(hex_fmt.IsInHexFormat([
            ':100000005CC0FECFFDCFFCCFFBCFFACFF9CFF8CF4E',
            ':10001000F7CFF6CFF5CFF4CFF3CFF2CFF1CFF0CFCC',
            ':10002000EFCFEECFEDCF0003030006030203010183',
            ':10003000010100000702020300070403010100019F',
            ':100040000701010300040703020200070100030087',
            ':100050001000FFFFFF00030001000603FF01030083',
            ':10006000FFFF20000E00100001002D4E414E000049',
        ]))
        self.assertFalse(hex_fmt.HasError())

        self.assertFalse(hex_fmt.IsInHexFormat([
            ':100000005CC0FECFFDCFFCCFFBCFFACFF9CFF8CF4E',
            ':10001000F7CFF6CFF5CFF4CFF3CFF2CFF1CFF0CFCC',
            ':10002000EFCFEECFEDCF0003030006030203010183',
            ':100030000101000007020203000704030101009F',
            ':100040000701010300040703020200070100030087',
            ':100050001000FFFFFF00030001000603FF01030083',
            ':10006000FFFF20000E00100001002D4E414E000049',
        ]))
        self.assertTrue(hex_fmt.HasError())
        hex_fmt.AppendError('--------')
        print(hex_fmt.GetErrorMessage())
        hex_fmt.Reset()


    def test_ReadFromString(self):
        hex_fmt = Intel_hex.IntelHexReader()
        self.assertTrue(hex_fmt.ReadFromString('\n'.join([
            ':100000005CC0FECFFDCFFCCFFBCFFACFF9CFF8CF4E',
            ':00000001FF',
        ])))
        self.assertFalse(hex_fmt.HasError())
        self.assertEqual(16, len(hex_fmt.GetMemoryBytes()))
        self.assertEqual([
            0x5C, 0xC0, 0xFE, 0xCF, 0xFD, 0xCF, 0xFC, 0xCF,
            0xFB, 0xCF, 0xFA, 0xCF, 0xF9, 0xCF, 0xF8, 0xCF,
        ], hex_fmt.GetMemoryBytes())


    def ReadByte(self, hex_fmt, addr, exp):
        b1 = hex_fmt.GetMemoryBytes()[addr]
        self.assertEqual(exp, b1)


    def test_ReadProgMem(self):
        hex_fmt = Intel_hex.IntelHexReader()
        hex_path = os.path.join('Datasets', 'GameAVR.hex')
        self.assertTrue(hex_fmt.ReadFromFile(hex_path))

        self.ReadByte(hex_fmt, 0x60, 0xff)
        self.ReadByte(hex_fmt, 0x61, 0xff)

        self.ReadByte(hex_fmt, 0x70, 0x01)
        self.ReadByte(hex_fmt, 0x71, 0x00)

        self.ReadByte(hex_fmt, 0x72, 0x69)
        self.ReadByte(hex_fmt, 0x73, 0x01)

        self.ReadByte(hex_fmt, 0x25c, 0x8c)
        self.ReadByte(hex_fmt, 0x25d, 0xd2)



if __name__ == '__main__':
    unittest.main()

