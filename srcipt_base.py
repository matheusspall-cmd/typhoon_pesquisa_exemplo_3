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
sch = str(dirpath/".."/"Schematics"/"schematic_2.tse")

# setando o caminho do arquivo que sera compilado para ser usado
cpd = model.get_compiled_model_file(sch)




# carregando o esquematico
model.load(filename=sch)

# compilando o esquematico
model.compile()

# carregando no dispositivo hil
hil.load_model(file=cpd, vhil_device=True)



def generate_pdf_report(file_name, time, voltage):
    
    pdf = FPDF()
    pdf.add_page()
    
    plt.figure()
    plt.plot(time, voltage)
    plt.xlabel("time")
    plt.ylabel("voltage")
    plt.title("V x t")
    plt.ylim(-500,500)
    plt.axhline(y=0,linewidth=0.7)
    plt.grid(True, which='both', linestyle='--', linewidth=0.7)
    plt.savefig("image.png", dpi=150, bbox_inches="tight")
    plt.close()
    
    pdf.image('image.png',x=20,w=170)
    pdf.output(file_name)
    
    os.remove('image.png')
    
    





# decimation, numberOfChannels, numberOfSamples
captureSettings = [300,1,1000]

# triggerType, triggerSource, threshold, edge, triggerOffset
triggerSettings = ['Forced']

# signals for capturing
channelSettings = ['Probe1']

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
    # xDara = 'numpy.array' wiht time data
    (signalName, tensao, tempo) = capturedDataBuffer[0]
    
    v = tensao[0].tolist()
    t = tempo.tolist()
    
else:
    print('unable to start capture process')
        

hil.stop_simulation()

generate_pdf_report('relatorio2.pdf',t,v)




    
    
