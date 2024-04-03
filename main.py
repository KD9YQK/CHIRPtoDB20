import pyautogui
from time import sleep
from tones import tones_str

######################################
#  Configure these
######################################

m_line = [1090, 111]  # Screen location of topmost >>

next_dist = 19  # Space between >> vertically

max_line = 47  # Number of completely visible fields

# Disable TX on stations in this list
tx_off = ['ISP', 'KANEPOPO', 'KANEOEM', 'KENCOM1', 'KENCOM2', 'ANIMAL', 'WX2PA1', 'WX3PA4', 'WX4PA2', 'WX5PA3',
          'WX7PA6', 'WX1PA7', 'WX8', 'WX9', 'WX10']

# Set low power to any stations in this list
tx_low = ['GMRS 1', 'GMRS 2', 'GMRS 3', 'GMRS 4', 'GMRS 5', 'GMRS 6', 'GMRS 7', 'GMRS 8', 'GMRS 9', 'GMRS 10',
          'GMRS 11', 'GMRS 12', 'GMRS 13', 'GMRS 14', 'MURS 1', 'MURS 2', 'MURS 3', 'BLUE DOT', 'GREEN DO', 'GREENDOT']

######################################
#  End Config
######################################


class code_plug:
    Name = ""
    Frequency = ""
    Duplex = ""
    Offset = ""
    Tone = ""
    rToneFreq = ""
    cToneFreq = ""
    DtcsCode = ""
    DtcsPolarity = ""
    RxDtcsCode = ""
    CrossMode = ""
    Mode = ""
    TStep = ""
    Skip = ""
    Power = ""


plugs = []

with open('chirp.csv', 'r') as f:
    l = f.readline()
    for l in f.readlines():
        tmp = code_plug()
        s = l.split(',')
        tmp.Name = s[1]
        tmp.Frequency = s[2]
        tmp.Duplex = s[3]
        tmp.Offset = s[4]
        tmp.Tone = s[5]
        tmp.rToneFreq = s[6]
        tmp.cToneFreq = s[7]
        tmp.DtcsCode = s[8]
        tmp.DtcsPolarity = s[9]
        tmp.RxDtcsCode = s[10]
        tmp.Mode = s[12]
        tmp.Skip = s[14]
        tmp.Power = s[15]
        tmp.CrossMode = s[11]
        plugs.append(tmp)

sleep(5)  # Give some time to switch to app
ln = m_line
count = 1
reset = m_line[1]
for p in plugs:
    pyautogui.click(ln[0], ln[1], 2)
    sleep(1)

    pyautogui.write(p.Frequency)
    pyautogui.press('tab')

    if p.Duplex == '+':
        freq = str(float(p.Frequency) + float(p.Offset))
    elif p.Duplex == '-':
        freq = str(float(p.Frequency) - float(p.Offset))
    else:
        freq = p.Frequency
    pyautogui.write(freq)

    pyautogui.press('tab')
    pyautogui.write(p.Name)
    tmp = 8 - len(p.Name)
    if tmp > 0:
        pyautogui.press('tab', presses=tmp)

    # pyautogui.press('down')  # Change step to 5.0k. Not needed
    pyautogui.press('tab')

    if p.Mode == 'NFM':
        pyautogui.press('down')
    pyautogui.press('tab')
    if p.Name not in tx_low:
        pyautogui.press('down', presses=2)  # Power

    pyautogui.press('tab', presses=6)  # TX Off
    if p.Name in tx_off:
        pyautogui.press('space')

    pyautogui.press('tab')  # Channel Skip
    if p.Skip == 'S':
        pyautogui.press('space')

    pyautogui.press('tab', presses=3)  # We are at OK

    if p.Tone in ['Tone', 'TSQL', 'DTCS', 'Cross']:
        pyautogui.press('tab', presses=5)  # Tone RX
        if p.Tone == 'TSQL':
            pyautogui.press('down', presses=tones_str.index(p.cToneFreq))
        elif p.Tone == 'Tone':
            pyautogui.press('down', presses=tones_str.index(p.rToneFreq))
        elif p.Tone == 'DTCS':
            tmp = 'D' + p.DtcsCode + p.DtcsPolarity[:1]
            pyautogui.press('down', presses=tones_str.index(tmp))
        elif p.Tone == 'Cross':
            if p.CrossMode[:4] == "Tone":
                pyautogui.press('down', presses=tones_str.index(p.cToneFreq))
            else:
                tmp = 'D' + p.DtcsCode + p.DtcsPolarity[:1]
                pyautogui.press('down', presses=tones_str.index(tmp))

        pyautogui.press('tab')  # Tone TX
        # Stupid app requires an extra down key, hence every down press is +1
        if p.Tone == 'TSQL':
            pyautogui.press('down', presses=tones_str.index(p.cToneFreq)+1)
        elif p.Tone == 'Tone':
            pyautogui.press('down', presses=tones_str.index(p.rToneFreq)+1)
        elif p.Tone == 'DTCS':
            tmp = 'D' + p.DtcsCode + p.DtcsPolarity[1:]
            pyautogui.press('down', presses=tones_str.index(tmp)+1)
        elif p.Tone == 'Cross':
            if p.CrossMode[6:] == "Tone":
                pyautogui.press('down', presses=tones_str.index(p.cToneFreq)+1)
            else:
                tmp = 'D' + p.DtcsCode + p.DtcsPolarity[1:]
                pyautogui.press('down', presses=tones_str.index(tmp)+1)

        pyautogui.press('tab', presses=16)  # Squelch Mode
        if p.Tone in ['TSQL', 'DTCS', 'Cross']:
            pyautogui.press('down')

        pyautogui.press('tab', presses=8)  # We are at OK

    pyautogui.press('space')
    sleep(.5)
    #  If we are at bottom of screen, scroll and start back at top
    count += 1
    if count > 47:
        ln[1] = reset
        pyautogui.click(1910, 980)
        count = 1
        sleep(1)
    else:
        ln[1] = ln[1] + next_dist
