#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os
import subprocess
import time
import unittest

import AVR_disassemble



PRINT_INSTRUCTIONS = False
IS_VERBOSE         = True
IS_APPEND_FILE     = False
CYGWIN_PATH        = os.path.join('C:\\', 'cygwin64', 'bin')



def Log(msg, is_append_file=IS_APPEND_FILE, is_verbose=IS_VERBOSE):
    if not is_verbose:
        return

    time_str = time.ctime(time.time())
    out_msg = time_str + ' ' + str(msg)
    print(out_msg)

    if is_append_file:
        log_file_date = time.strftime('%Y%m%d')
        with open('log-py-{}.txt'.format(log_file_date), 'a') as f:
            f.write(out_msg + '\n')
            f.flush()


def AddCygwinPath():
    if os.name != 'nt':
        return
    env_path = os.environ['PATH']
    paths = [ p.lower() for p in env_path.split(';') ]
    if CYGWIN_PATH not in paths:
        Log('Add cygwin path . . .')
        new_env = CYGWIN_PATH + ';' + env_path
        os.environ['PATH'] = new_env
    else:
        Log('cygwin path exists!')


def RemoveCygwinPath():
    if os.name != 'nt':
        return
    env_path = os.environ['PATH']
    paths = [ p.lower() for p in env_path.split(';') ]
    if CYGWIN_PATH in paths:
        Log('remove cygwin path . . .')
        paths.remove(CYGWIN_PATH)
        new_env = ''
        for p in paths:
            new_env += p + ';'
        os.environ['PATH'] = new_env


def RunCommand(cmd):
    AddCygwinPath()
    Log('START : ' + time.ctime(time.time()))
    cmd = [str(c) for c in cmd]
    Log(' '.join(cmd))

    prc = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd='.')
    (output, err) = prc.communicate()
    exit_code = prc.wait()

    if exit_code != 0:
        Log('  Exit Code : %d' % exit_code)
        Log('  Output    : `%s\'' % output)
        Log('  Error     : `%s\'' % err)
    Log('END   : ' + time.ctime(time.time()))
    RemoveCygwinPath()
    return exit_code, output, err



class MiscellaneousTestCases(unittest.TestCase):
    def test_OprChrs(self):
        INSTRS = AVR_disassemble.INSTRUCTIONS
        opr_chrs = set([ c for c in ''.join([r[1].replace(' ', '') for r in INSTRS]) if c not in '01' ])
        print(opr_chrs)
        expt_list = ['A', 'H', 'K', 'P', 'b', 'd', 'h', 'k', 'p', 'q', 'r']
        self.assertEqual(expt_list, sorted(list(opr_chrs)))

        if PRINT_INSTRUCTIONS:
            for r in INSTRS:
                opc, opc_mask, oprd_set, oprd_masks = AVR_disassemble.GetMasks(r)
                print(r[0], hex(opc_mask), oprd_set, ['{:04x}'.format(o) for o in oprd_masks])


    def test_MkAbsoluteOperand(self):
        self.assertEqual((0x0001, 4), AVR_disassemble.MkAbsoluteOperand('K', '0100KKKK0000', 0xe15))
        self.assertEqual((0x001f, 5), AVR_disassemble.MkAbsoluteOperand('K', '01K0KKKK0000', 0xfff))
        self.assertEqual((0x003a, 6), AVR_disassemble.MkAbsoluteOperand('K', 'K1K0KKKK0000', 0xaaf))


    def test_7bit(self):
        self.assertEqual(-18, AVR_disassemble.GetRelative7bit(0xf7b9 >> 3))


    def test_FmtException(self):
        # True value is:
        # ( 'LDS       Rd, K',            '1001 000d dddd 0000 KKKK KKKK KKKK KKKK' ),
        # 0 <= d <= 31, 0 <= K <= 65535
        #
        # But this format makes exception `IndexError: tuple index out of # range'!
        # By replacing 'Rd' with 'Rr' this exception solved.
        v = 30
        num_bits = 5
        inst_fmt = 'LDS       Rr, 0x016d'
        oprd_chr = 'r'
        inst_fmt = inst_fmt.replace(oprd_chr, '{}').format(v)
        print(inst_fmt)


class DisassembleTestCases(unittest.TestCase):
    def ReadFile(self, file_path):
        self.assertTrue(os.path.isfile(file_path))
        with open(file_path, 'r') as f:
            lines = f.read()
        return lines


    def RunAVRDisassemble(self, hex_path):
        exit_code, output, err = RunCommand([ 'python', 'AVR_disassemble.py', hex_path ])
        self.assertEqual(0, exit_code)
        self.assertEqual(None, err)
        return output


    def PrepareLines(self, lines):
        # Remove '\r' chars and split into lines.
        lines = lines.replace('\r', '')
        lines = lines.replace('$', '0x')
        lines = lines.split('\n')
        lines = [ l.strip() for l in lines if len(l.strip()) ]

        # Find menemonic field.
        st_tab = lines[0].find('\t') + 1
        st_off = lines[0].find('\t', st_tab) + 1
        for i in range(len(lines)):
            l = lines[i].lower()
            #if l[st_off].islower():
                #sp_idx = l.find(' ', st_off)
                #l = l[ : st_off] + l[st_off : sp_idx].lower() + l[sp_idx + 1 : ]
            l = l.replace('\t', ' ')
            while l.find('  ') > 0:
                l = l.replace('  ', ' ')
            lines[i] = l
        return lines


    def CheckAssemblyFile(self, file_path):
        print('Checking file -> `%s\' . . .' % file_path)
        dis_path = file_path + '-disasm.txt'
        self.assertTrue(os.path.isfile(dis_path))
        exp_lines = self.PrepareLines(self.ReadFile(dis_path))

        hex_path = file_path + '.hex'
        self.assertTrue(os.path.isfile(hex_path))
        asm_lines = self.PrepareLines(self.RunAVRDisassemble(hex_path))

        self.assertEqual(len(asm_lines), len(exp_lines))
        for i in range(len(asm_lines)):
            if asm_lines[i] != exp_lines[i]:
                print('  line {}:{}'.format(file_path, i + 1))
                print('  ' + asm_lines[i])
                print('  ' + exp_lines[i])
                print('')
            self.assertEqual(asm_lines[i], exp_lines[i])


    def test_AVRDisassemble(self):
        file_path_1 = os.path.join('Datasets', 'GameAVR')
        self.CheckAssemblyFile(file_path_1)

        file_path_2 = os.path.join('Datasets', 'GameDemoSelect(Any_168)')
        self.CheckAssemblyFile(file_path_2)



if __name__ == '__main__':
    unittest.main()

