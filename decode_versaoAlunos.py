
#Importe todas as bibliotecas
from suaBibSignal import signalMeu
import peakutils
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time, os
from tkinter import messagebox, Tk, ttk, Label
from tkinter.filedialog import askopenfilename

def todB(s):
    sdB=10*np.log10(s)
    return(sdB)

def loadsound():
    window=Tk()
    window.title('Escolha o método de áudio')
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    
    def recordmic():
        global som
        messagebox.showinfo('Gravando', 'Som gravado')
        audio=sd.rec(int(T * fs))
        sd.wait()
        window.destroy()
        som=audio

    def loadsoundfile():
        global som
        file=askopenfilename(initialdir=os.getcwd(), title='Selecione o arquivo de áudio a ser identificado', filetypes=[('Sound Files', '.wav'), ('Sound Files', '.mp4'), ('Sound Files', '.ogg')])
        window.destroy()
        som=file
    
    Column1=ttk.Button(window, text='Carregar um arquivo', command=loadsoundfile)
    Column2=ttk.Button(window, text='Gravar meu microfone', command=recordmic)
    Column1.grid(row=3, column=2, padx=25, pady=10)
    Column2.grid(row=3, column=4, padx=25, pady=10)

    window.mainloop()

def get_freq1(freq):
    freqs=[1209, 1336, 1477, 1633]
    for f in freqs:
        if int(freq) in range(f-50, f+50):
            return_freq=f
    return return_freq

def get_freq2(freq):
    freqs=[697, 770, 852, 941]
    for f in freqs:
        if int(freq) in range(f-50, f+50):
            return_freq=f
    return return_freq

def getsymbol(freq1, freq2):
    tabela={'1':(1209, 697), '2':(1336, 697), '3':(1477, 697), 'A':(1633, 697),
            '4':(1209, 770), '5':(1336, 770), '6':(1477, 770), 'B':(1633, 770),
            '7':(1209, 852), '8':(1336, 852), '9':(1477, 852), 'C':(1633, 852),
            'X':(1209, 941), '0':(1336, 941), '#':(1477, 941), 'D':(1633, 941)}
    for symbol, freqs in tabela.items():
        if freq1==freqs[0] and freq2==freqs[1]:
            return symbol

def resultado(freq1, freq2):
    freq1=get_freq1(freq1)
    freq2=get_freq2(freq2)
    symbol=getsymbol(freq1, freq2)
    window=Tk()
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    subtitulo=Label(window, text='O símbolo correspondete a este som é:', padx=50, pady=10)
    resultado=ttk.Label(window, text=symbol, padding=5)
    resultado.config(font=("Calibri", 44))
    subtitulo.grid(column=0, row=0)
    resultado.grid(column=0, row=1)
    window.mainloop()

def main():
    global som
    signal=signalMeu()

    sd.default.samplerate=fs
    sd.default.channels=1
    
    loadsound()
    recording=sd.playrec(som)
    sd.wait()
    
    plt.plot(t, recording)
    plt.title("Som gravado")
    plt.show()
    
    x, y=signal.calcFFT(recording, fs)
    signal.plotFFT(recording, fs)
    index=peakutils.indexes(y, thres=0.2, min_dist=10)
    for freq in x[index]:
        if int(freq) in range(1100, 1700):
            freq1=get_freq1(freq)
        if int(freq) in range(500, 1000):
            freq2=get_freq2(freq)
    resultado(freq1, freq2)

if __name__=='__main__':
    fs=44100 
    T=1
    t=np.linspace(-T,T,T*fs)
    som=None
    main()
    # resultado(1300, 900)
