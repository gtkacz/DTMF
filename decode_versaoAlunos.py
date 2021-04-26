
#Importe todas as bibliotecas
from suaBibSignal import signalMeu
import peakutils
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time, os
from scipy import signal
from scipy.fftpack import fft, fftshift
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from functools import partial

def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def loadsound():
    window = Tk()
    window.title("Escolha o método de áudio")
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    
    def recordmic():
        global som
        messagebox.showinfo('Gravando', 'Estamos gravando!')
        audio = sd.rec(int(T * fs))
        sd.wait()
        window.destroy()
        som=audio

    def loadsoundfile():
        global som
        file=askopenfilename(initialdir=os.getcwd(), title="Selecione o arquivo de áudio a ser identificado", filetypes=[("Sound Files", ".wav"), ("Sound Files", ".mp4"), ("Sound Files", ".ogg")])
        window.destroy()
        som=file
    
    Column1=Button(window, text="Carregar um arquivo", command=loadsoundfile)
    Column2=Button(window, text="Gravar meu microfone", command=recordmic)
    Column1.grid(row=3, column=2, padx=25, pady=10)
    Column2.grid(row=3, column=4, padx=25, pady=10)

    window.mainloop()

def main():
    global som
    signal = signalMeu()

    sd.default.samplerate = fs
    sd.default.channels = 1
    
    loadsound()
    
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(inicio,fim,numPontos)
    # plot do gravico áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) . 
       
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(y, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.4, min_dist=50)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    fs = 44100 
    T  = 1
    t  = np.linspace(-T,T,T*fs)
    som=None
    main()
