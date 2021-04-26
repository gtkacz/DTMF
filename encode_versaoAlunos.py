import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import sys, os, logging
from suaBibSignal import signalMeu
from tkinter import Tk, Button, RAISED, Label
from functools import partial
from datetime import datetime

def todB(s):
    #converte intensidade em Db, caso queiram ...
    sdB=10*np.log10(s)
    return(sdB)

def dialPad():
    global digit
    window=Tk()
    window.title("Dial Pad")
    window.resizable(False, False)
    buttons=[['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['X','0','#','D']]

    def buttonClicked(buttonVal):
        global digit
        digit=buttonVal
        window.destroy()

    for r in range(4):
        for c in range(4):
            button=Button(window,
                            relief=RAISED,
                            padx=10,
                            text=buttons[r][c],
                            command=partial(buttonClicked, buttons[r][c]))
            button.grid(row=r, column=c)
            
    w=140 # width for the Tk window
    h=103 # height for the Tk window

    # get screen width and height
    ws=window.winfo_screenwidth() # width of the screen
    hs=window.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk window window
    x=(ws/2) - (w/2)
    y=(hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    window.mainloop()

def tabelaDTMF(digit):
    tabela={'1':(1209, 697), '2':(1336, 697), '3':(1477, 697), 'A':(1633, 697),
            '4':(1209, 770), '5':(1336, 770), '6':(1477, 770), 'B':(1633, 770),
            '7':(1209, 852), '8':(1336, 852), '9':(1477, 852), 'C':(1633, 852),
            'X':(1209, 941), '0':(1336, 941), '#':(1477, 941), 'D':(1633, 941)}
    return tabela[str(digit)]
    
def getfilename(type):
    time=datetime.now().strftime("%Y-%m-%d at %Hhrs %Mmin %Ss")
    if type=='log':
        filename=f'emissão ({time}).log'
    elif type=='som':
        filename=f'emissão ({time}).wav'
    return filename

def main():
    global digit

    print('Inicializando encoder')
    logging.basicConfig(filename=getfilename('log'), level=logging.INFO, format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    logging.info('Inicializando encoder')
    signal=signalMeu()
    
    print('Aguardando usuário')
    logging.info('Aguardando usuário')
    dialPad()
    
    print(f'Gerando tons base referentes ao símbolo: {digit}')
    logging.info(f'Gerando tons base referentes ao símbolo: {digit}')
    freq1, freq2=tabelaDTMF(digit)
    
    print('Executando as senoides (emitindo o som)')
    logging.info('Executando as senoides (emitindo o som)')
    fs=44100
    F=1
    T=1
    t=np.linspace(-T, T, T*fs)
    sd.default.samplerate=fs
    sd.default.channels=1
    
    x1, y1=signal.generateSin(freq1, 1, T, fs)
    x2, y2=signal.generateSin(freq2, 1, T, fs)
    y3=y1+y2
    
    print(f'Gerando tom referente ao símbolo: {digit}')
    logging.info(f'Gerando tom referente ao símbolo: {digit}')
    sd.play(y3)
    
    print('Plotando os gráficos')
    logging.info('Plotando os gráficos')
    plt.figure()
    plt.plot(t[:300], y1[:300], alpha=0.5, label= (f'{freq1}Hz'))
    plt.plot(t[:300], y2[:300], 'g', alpha=0.5, label=(f'{freq2}Hz'))
    plt.plot(t[:300], y3[:300], 'k', alpha=0.75, label=(f'Soma de {freq1}Hz e {freq2}Hz'))
    plt.legend()
    plt.title(f'Frequências do símbolo {digit}')
    plt.grid(True)
    plt.show()
    
    sd.wait()
    
    filename=getfilename('som')
    print(f'Salvando o som em: {filename}')
    logging.info(f'Salvando o som em: {filename}')
    sf.write(filename, y3, fs) 

if __name__=='__main__':
    digit=None
    main()
