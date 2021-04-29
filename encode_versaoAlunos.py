import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import sys, os, logging
from suaBibSignal import signalMeu
from tkinter import Tk, Button, RAISED, ttk, StringVar
from functools import partial
from datetime import datetime

def todB(s):
    #converte intensidade em Db, caso queiram ...
    sdB=10*np.log10(s)
    return(sdB)

def dialPad():
    global digit, quer_log, quer_arquivo
    window=Tk()
    window.title("Dial Pad")
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    buttons=[['1','2','3','A'],
            ['4','5','6','B'],
            ['7','8','9','C'],
            ['X','0','#','D']]

    def buttonClicked(buttonVal):
        global digit
        digit=buttonVal
        window.destroy()
        
    def quer_salvar_log():
        global quer_log
        quer_log=True
            
    def quer_salvar_som():
        global quer_arquivo
        quer_arquivo=True

    for r in range(4):
        for c in range(4):
            button=ttk.Button(window,
                            text=buttons[r][c],
                            command=partial(buttonClicked, buttons[r][c]))
            button.grid(row=r, column=c)
            
    querlog_var = StringVar(value=0)
    querarquivo_var = StringVar(value=0)

    querlog = ttk.Checkbutton(window, text='Quero salvar o log', command=quer_salvar_log, variable=querlog_var)
    querarquivo = ttk.Checkbutton(window, text='Quero salvar o arquivo de som', command=quer_salvar_som, variable=querarquivo_var)
    
    querlog.grid(column=4, row=1)
    querarquivo.grid(column=4, row=2)
    
    # w=140 # width for the Tk window
    # h=103 # height for the Tk window

    # get screen width and height
    ws=window.winfo_screenwidth() # width of the screen
    hs=window.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk window window
    # x=(ws/2) - (w/2)
    # y=(hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    # window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    window.mainloop()

def tabelaDTMF(digit):
    tabela={'1':(1209, 697), '2':(1336, 697), '3':(1477, 697), 'A':(1633, 697),
            '4':(1209, 770), '5':(1336, 770), '6':(1477, 770), 'B':(1633, 770),
            '7':(1209, 852), '8':(1336, 852), '9':(1477, 852), 'C':(1633, 852),
            'X':(1209, 941), '0':(1336, 941), '#':(1477, 941), 'D':(1633, 941)}
    return tabela[str(digit)]
    
def getfilename(type, symbol):
    time=datetime.now().strftime("%Y-%m-%d at %Hhrs %Mmin %Ss")
    if type=='log':
        filename=f'Emissão referente ao símbolo {symbol} de ({time}).log'
    elif type=='som':
        filename=f'Emissão referente ao símbolo {symbol} de ({time}).wav'
    return filename

def info(string):
    global quer_log
    print(string)
    if quer_log==True:
        logging.info(string)

def main():
    global digit
    global quer_log
    global quer_arquivo

    info('Inicializando encoder')
    signal=signalMeu()
    
    info('Aguardando usuário')
    dialPad()
    
    if quer_log==True:
        logging.basicConfig(filename=getfilename('log', digit), level=logging.INFO, format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    
    info(f'Gerando tons base referentes ao símbolo: {digit}')
    freq1, freq2=tabelaDTMF(digit)
    
    info('Executando as senoides (emitindo o som)')
    fs=44100
    F=1
    T=1
    t=np.linspace(0, 2*T, T*fs)
    sd.default.samplerate=fs
    sd.default.channels=1
    
    x1, y1=signal.generateSin(freq1, F, T, fs)
    x2, y2=signal.generateSin(freq2, F, T, fs)
    y3=y1+y2
    
    info(f'Gerando tom referente ao símbolo: {digit}')
    sd.play(y3)
    
    info('Plotando os gráficos')
    plt.figure()
    plt.plot(t[:300], y1[:300], 'b--', alpha=0.5, label= (f'{freq1}Hz'))
    plt.plot(t[:300], y2[:300], 'g--', alpha=0.5, label=(f'{freq2}Hz'))
    plt.plot(t[:300], y3[:300], 'k', alpha=0.75, label=(f'Soma de {freq1}Hz e {freq2}Hz'))
    plt.legend()
    plt.title(f'Frequências do símbolo {digit}')
    plt.grid(True)
    plt.autoscale(enable=True, axis='both', tight=True)
    plt.show()
    
    sd.wait()
    
    if quer_arquivo==True:
        filename=getfilename('som', digit)
        info(f'Salvando o arquivo de som em: {filename}')
        sf.write(filename, y3, fs) 

if __name__=='__main__':
    digit=None
    quer_log=False
    quer_arquivo=False
    main()
