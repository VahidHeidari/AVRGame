#******************************************************************************
#*                                                                            *
#*                      AVR Game Demo                                         *
#*                                                                            *
#* This is AVRGame project. AVRGame is a small, low cost, and open source     *
#* hand held console based on AVR microcontroller.                            *
#******************************************************************************

import os

import PIL
import PIL.ImageDraw
import PIL.Image



LED_WDITH  = 10
LED_OFF    = 3

BTN_OFF       = 3
BTN_WIDTH     = 20
BTN_WIDTH_IN  = BTN_WIDTH - 2 * BTN_OFF



def MkRect(x, y, w, h):
    return (x, y, x + w, y + h)


def DrawButton(drw, btn, x, y):
    if btn == 'X':
        drw.rectangle(MkRect(x, y, BTN_WIDTH, BTN_WIDTH), 'yellow')
        drw.ellipse(MkRect(x + BTN_OFF, y + BTN_OFF, BTN_WIDTH_IN, BTN_WIDTH_IN), 'black')
    else:
        drw.rectangle(MkRect(x, y, BTN_WIDTH, BTN_WIDTH), 'white')
        drw.ellipse(MkRect(x + BTN_OFF, y + BTN_OFF, BTN_WIDTH_IN, BTN_WIDTH_IN), 'gray')


def DrawDevice(display, buttons, out_path):
    img = PIL.Image.new('RGB', (400, 200), 'orange')
    drw = PIL.ImageDraw.ImageDraw(img)

    # Draw dot-matrix.
    drw.rectangle(MkRect(150 - LED_OFF, 10 - LED_OFF,
        100 + 2 * LED_OFF, 100 + 2 * LED_OFF), 'white')
    for x in range(8):
        for y in range(8):
            lx = 150 + (x * (LED_WDITH + LED_OFF))
            ly =  10 + (y * (LED_WDITH + LED_OFF))
            clr = 'red' if display[y][x] == '*' else (225, 190, 190)
            drw.ellipse(MkRect(lx, ly, LED_WDITH, LED_WDITH), clr)

    # Draw microcontroler.
    drw.rectangle(MkRect(120, 130, 160, 30), 'black')

    # Draw buttons.
    DrawButton(drw, buttons[0], 10, 90)     # Left
    DrawButton(drw, buttons[1], 60, 90)     # Right
    DrawButton(drw, buttons[3], 35, 65)     # Up
    DrawButton(drw, buttons[2], 35, 115)    # Down
    DrawButton(drw, buttons[4], 340, 90)    # Fire

    # Save result.
    img.save(out_path)


def MakeGIFAnimation(base_dir, out_name):
    imgs = [ PIL.Image.open(os.path.join(base_dir, fl)) for fl in
            sorted(os.listdir(base_dir)) if fl.endswith('.jpg') ]
    print('Number of frames : %d' % len(imgs))
    imgs[0].save(out_name, save_all=True, append_images=imgs[1:],
            optimize=True, duration=30, loop=0)
    for im in imgs:
        im.close()

    img = PIL.Image.open(out_name)
    print('Num Gif frames : %d' % img.n_frames)



if __name__ == '__main__':
    disp = [
        '********',
        '********',
        '********',
        '        ',
        '        ',
        ' *      ',
        '        ',
        '   **   ',
    ]
    btns = 'X----'
    DrawDevice(disp, btns, 'TestDrawDevice.jpg')

