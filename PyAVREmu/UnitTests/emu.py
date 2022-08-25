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

import ATmega
import Intel_hex



#MAX_INSTR_NUM = 90000
#MAX_INSTR_NUM = 6720
MAX_INSTR_NUM = 3147
#MAX_INSTR_NUM = 720
#MAX_INSTR_NUM = 10

HEX_PATH_PONG     = os.path.join('Datasets', 'GameAVR-Pong.hex')
HEX_PATH_PONG_168 = os.path.join('Datasets', 'GameAVR-Pong-168.hex')
HEX_PAHT_DEMO_ANY = os.path.join('Datasets', 'GameDemoSelect(Any_168).hex')
HEX_PAHT_AVR_GAME = os.path.join('Datasets', 'AVR_GAME.hex')

STATE_PATH      = os.path.join('3rdParty', 'uzem', 'Release', 'state.txt')
UZEM_EXE        = os.path.abspath(os.path.join('3rdParty', 'uzem', 'Release', 'uzem.exe'))
if not os.path.isfile(UZEM_EXE):
    STATE_PATH      = os.path.join('3rdParty', 'uzem', 'Debug', 'state.txt')
    UZEM_EXE        = os.path.abspath(os.path.join('3rdParty', 'uzem', 'Debug', 'uzem.exe'))

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
    def RunCPUs(self, cpu_type, hex_path):
        print('RunCPUs(cpu_type:' + cpu_type + ', hex_path:' +  hex_path + ')')
        # Read hex file.
        hex_fmt = Intel_hex.IntelHexReader()
        print(' Emu Test -> `%s\'' % hex_path)
        self.assertTrue(os.path.isfile(hex_path))
        self.assertTrue(hex_fmt.ReadFromFile(hex_path))

        # Delete `state.txt' file.
        if os.path.isfile(STATE_PATH):
            os.remove(STATE_PATH)
            print(' `%s\' removed!' % STATE_PATH)

        mega = ATmega.ATmega8() if cpu_type == 'ATmega8' else ATmega.ATmega168()
        mega.DecodeFlash(hex_fmt)

        cmd = [ UZEM_EXE, cpu_type, hex_path ]
        print(' cmd : [ %s ]' % ', '.join(cmd))
        instr_num = old_pc = 0
        my_state = uz_state = old_my_state = old_uz_state = ''
        AddCygwinPath()
        while instr_num < MAX_INSTR_NUM:
            # Run my CPU.
            mega.Exec()
            my_state = mega.Print()

            # Run UZEM CPU.
            exit_code, out_put, err = RunCommandQuiet(cmd)
            if exit_code != 0:
                print('******************************')
                print(' R U N   U Z E M   E R R O R')
                print('')
                print('Exit Code  : %x' % exit_code)
                print('Output     : `%s\'' % out_put)
                print('Error      : `%s\'' % err)
                print(' -- IN HEX : `%s\' -- ' % hex_path)
                print(' --    CPU : %s --' % cpu_type)
                print(' -- #INSTR : %4d --' % instr_num)
                print(' -- LST PC : %04x --' % ((old_pc * 2) & 0x1ffff))
                print(' -- MY  PC : %04x --' % ((mega.cpu.PC * 2) & 0x1ffff))
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
                print('******************************')
                print('   S T A T E S   E R R O R')
                print('')
                print(' -- IN HEX : `%s\' -- ' % hex_path)
                print(' --    CPU : %s --' % cpu_type)
                print(' -- #INSTR : %4d --' % instr_num)
                print(' -- LST PC : %04x --' % ((old_pc * 2) & 0x1ffff))
                print(' -- MY  PC : %04x --' % ((mega.cpu.PC * 2) & 0x1ffff))
                print('output: \n' + out_put + '\n')
                print('MY STATE:\n' + my_state + '\n')
                print('UZ STATE:\n' + uz_state)
                print('******************************')
                WriteStateToFile(my_state, uz_state, old_my_state, old_uz_state)
            self.assertEqual(my_state, uz_state)

            instr_num += 1
            old_pc = mega.cpu.PC
            old_my_state = my_state
            old_uz_state = uz_state
        print('\n Num Instructions: %d\n' % instr_num)
        RemoveCygwinPath()


    def test_Emu(self):
        if os.name == 'nt':
            global HEX_PAHT_DEMO_ANY
            HEX_PAHT_DEMO_ANY = HEX_PAHT_DEMO_ANY.replace('\\', '/')

        self.RunCPUs('ATmega8',   HEX_PATH_PONG)
        self.RunCPUs('ATmega168', HEX_PATH_PONG_168)
        self.RunCPUs('ATmega168', HEX_PAHT_DEMO_ANY)
        self.RunCPUs('ATmega8',   HEX_PAHT_AVR_GAME)



if __name__ == '__main__':
    unittest.main()

