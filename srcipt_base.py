from typhoon.api import hil 
from typhoon.api.schematic_editor import model
from pathlib import Path 
import pytest
import logging
import matplotlib.pyplot as plt 
import numpy as np 
from fpdf import FPDF
import os



# setando o logging do script atual
logger = logging.getLogger(__name__)

# armazeando o diretorio pai do script atual e defindo-o como pai
dirpath = Path(__file__).parent

# armazenando o caminho ate o esquematico a ser compilado e executado a partir do diretorio pai
sch = str(dirpath/".."/"Schematics"/"schematic_5.tse")

# setando o caminho do arquivo que sera compilado para ser usado
cpd = model.get_compiled_model_file(sch)



# carregando o esquematico
model.load(filename=sch)


# set_component_property(component, property, value)
#model.set_component_property('Grid Simulator1', 'Vb', 220)




# compilando o esquematico
model.compile()

# carregando no dispositivo hil
hil.load_model(file=cpd, vhil_device=True)


def generate_pdf_report(file_name, time, voltage, power_p, power_q):
    
    pdf = FPDF()
    pdf.add_page()
    
    # ----- Gráfico de Corrente e Tensao -----
    plt.figure(figsize=(8, 4))
    plt.plot(time, voltage, label='Tensao(V)', color='red' )
    plt.ylim(200, 500)
    plt.axhline(y=0, linewidth=0.7, color="black")
    plt.grid(True, which='both', linestyle='--', linewidth=0.7)
    plt.legend()
    plt.savefig("current_voltage.png", dpi=150, bbox_inches="tight")
    plt.close()
    
    pdf.image("current_voltage.png", x=20, w=170)
    pdf.ln(10)  # quebra de linha no PDF
      
    # ----- Gráfico de Potencias Ativa e Reativa -----
    plt.figure(figsize=(8, 4))
    plt.plot(time, power_p, label="Ativa(W)", color='blue')
    plt.plot(time, power_q, label='Reativa(var)', color='red')
    plt.ylim(-3500,3500)
    plt.axhline(y=0, linewidth=0.7, color="black")
    plt.grid(True, which='both', linestyle='--', linewidth=0.7)
    plt.legend()
    plt.savefig("power.png", dpi=150, bbox_inches="tight")
    plt.close()
    
    pdf.image("power.png", x=20, w=170)
    
    # ----- Salvar PDF -----
    pdf.output(file_name)
    
    # limpar imagens temporárias
    os.remove("current_voltage.png")
    os.remove("power.png")
    
    





# decimation, numberOfChannels, numberOfSamples
captureSettings = [300,3,1000]

# triggerType, triggerSource, threshold, edge, triggerOffset
triggerSettings = ['Forced']

# signals for capturing
channelSettings = ['VAB', 'POWER_P', 'POWER_Q']

capturedDataBuffer = []

if hil.start_capture(
    captureSettings,
    triggerSettings,
    channelSettings,
    dataBuffer = capturedDataBuffer,
    fileName = r'C:\captured_signals\captured_singal6.csv',
    ):
    
    hil.start_simulation()
    
    while hil.capture_in_progress():
        pass
    
    # unpack data from data buffer
    # singalNames = list with the names of the singals
    # yDataMatrix = 'numpy.ndarray' matrix with data values
    # xData = 'numpy.array' wiht time data
    (signalName, signals, tempo) = capturedDataBuffer[0]
    
    VAB = signals[0].tolist()
    POWER_P = signals[1].tolist()
    POWER_Q = signals[2].tolist()
    t = tempo.tolist()
    
else:
    print('unable to start capture process')
        

hil.stop_simulation()

generate_pdf_report('relatorio1.pdf', t, VAB,POWER_P, POWER_Q)
