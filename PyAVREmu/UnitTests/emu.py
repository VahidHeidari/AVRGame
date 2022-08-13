import os
import subprocess
import time
import unittest

import ATmega8
import Intel_hex



MAX_INSTR_NUM = 90000

HEX_PATH   = os.path.join('Datasets', 'GameAVR.hex')
STATE_PATH = os.path.join('3rdParty', 'uzem', 'Debug', 'state.txt')
UZEM_EXE   = os.path.abspath(os.path.join('3rdParty', 'uzem', 'Debug', 'uzem.exe'))

IS_VERBOSE     = True
IS_APPEND_FILE = False
CYGWIN_PATH    = os.path.join('C:\\', 'cygwin64', 'bin')



def Log(msg, is_append_file=IS_APPEND_FILE):
    if not IS_VERBOSE:
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
    #AddCygwinPath()
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
    #RemoveCygwinPath()
    return exit_code, output, err


def RunCommandQuiet(cmd):
    global IS_VERBOSE
    old_is_verb = IS_VERBOSE                        # Save logging state.
    IS_VERBOSE = False                              # Disable logging prints.
    exit_code, output, err = RunCommand(cmd)
    IS_VERBOSE = old_is_verb                        # Restore logging state.
    return exit_code, output, err


def WriteStateToFile(my_state, uz_state, old_my_state, old_uz_state):
    with open('my_state.txt', 'w') as f:
        f.write(my_state)
    with open('uz_state.txt', 'w') as f:
        f.write(uz_state)
    with open('old_my_state.txt', 'w') as f:
        f.write(old_my_state)
    with open('old_uz_state.txt', 'w') as f:
        f.write(old_uz_state)



class EmuTestCases(unittest.TestCase):
    def test_Emu(self):
        # Read hex file.
        hex_fmt = Intel_hex.IntelHexReader()
        print(' Emu Test -> `%s\'' % HEX_PATH)
        self.assertTrue(os.path.isfile(HEX_PATH))
        self.assertTrue(hex_fmt.ReadFromFile(HEX_PATH))

        # Delete `state.txt' file.
        if os.path.isfile(STATE_PATH):
            os.remove(STATE_PATH)
            print(' `%s\' removed!' % STATE_PATH)

        mega8 = ATmega8.ATmega8()
        mega8.DecodeFlash(hex_fmt)

        cmd = [ UZEM_EXE, HEX_PATH ]
        instr_num = old_pc = 0
        old_my_state = old_uz_state = ''
        AddCygwinPath()
        while instr_num < MAX_INSTR_NUM:
            # Run my CPU.
            mega8.Exec()
            my_state = mega8.Print()

            # Run UZEM CPU.
            exit_code, out_put, err = RunCommandQuiet(cmd)
            if exit_code != 0:
                print('******************************')
                print('Exit Code  : %x' % exit_code)
                print('Output     : `%s\'' % out_put)
                print('Error      : `%s\'' % err)
                print(' -- #INSTR : %4d --' % instr_num)
                print(' -- LST PC : %04x --' % old_pc)
                print(' -- MY  PC : %04x --' % mega8.cpu.PC)
                print('MY STATE:\n' + my_state + '\n')
                print('UZ STATE:\n' + uz_state)
                print('******************************')
                WriteStateToFile(my_state, uz_state, old_my_state, old_uz_state)
            self.assertEqual(0, exit_code)
            self.assertEqual(None, err)

            # Read UZ state file.
            self.assertTrue(os.path.isfile(STATE_PATH))
            with open(STATE_PATH, 'r') as f:
                uz_state = f.read()

            # Check states.
            if my_state != uz_state:
                print(' -- #INSTR: %4d --' % instr_num)
                print(' -- LST PC: %04x --' % old_pc)
                print(' -- MY  PC: %04x --' % mega8.cpu.PC)
                print('output: \n' + out_put + '\n')
                print('MY STATE:\n' + my_state + '\n')
                print('UZ STATE:\n' + uz_state)
                WriteStateToFile(my_state, uz_state, old_my_state, old_uz_state)
            self.assertEqual(my_state, uz_state)

            instr_num += 1
            old_pc = mega8.cpu.PC
            old_my_state = my_state
            old_uz_state = uz_state
        print('\n Num Instructions: %d\n' % instr_num)
        RemoveCygwinPath()



if __name__ == '__main__':
    unittest.main()

