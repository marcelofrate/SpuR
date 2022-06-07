#Leitor SDR
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
import pandas as pd

f1 =   70000000
f2 = 6000000000
step = 10000000
f = f1
tag=0
amp=0
result=[]
mag=[]
freq=[]

def figuraDupla(tag,freq1, mag1, freq2, mag2):
    fig = plt.figure(figsize=(14, 10))
    # Adding the axes to the figure
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
    # plotting 1st dataset to the figure
    xFtemp = np.array(freq1)
    xF = np.array(freq2)
    yFtemp = np.array(mag1)
    yF = np.array(mag2)
    ax1 = ax.plot(xFtemp, yFtemp)
    # plotting 2nd dataset to the figure
    ax2 = ax.plot(xF, yF)

    # Setting Title
    ax.set_title("TAG Nº = "+tag)

    # Setting Label
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")

    # Adding Legend
    ax.legend(labels=('TEMPLATE', 'TAG LIDA, Nº: '+tag))
    # cursor
    ax.set_xlabel('Frequência')
    ax.set_ylabel('Magnitude')
    cursor = Cursor(ax, color='green', linewidth=1.3)
    plt.show()
    
def figura(freq, mag):
	xF = np.array(freq)
	yM = np.array(mag)
	fig = plt.figure(figsize=(14, 10))
	ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
	ax.plot(xF, yM)
	plt.xticks(rotation=45)
	ax.set_xlabel('Frequency (MHz)')
	ax.set_ylabel('Relative Gain (dB)')
	plt.title('Chipless RFID Reader')
	cursor = Cursor(ax, color='green', linewidth=1.2)
	plt.show()

def expDados(freq, mag):
	rfidSet = pd.DataFrame({'Freq': freq, 'Mag': mag})
	rfidSet.to_csv("/mnt/d/Compartilhada/SpuR/tag.csv", index = False)	

def calcEuc(magT, mag):
    xTemp = np.array(magT)
    xTag = np.array(mag)
    distE = np.linalg.norm(xTemp - xTag)
    return(distE)
    
def compTag(tagF,tagM):
	rfidTemp = pd.read_csv("/mnt/d/Compartilhada/SpuR/Results/BDV90.csv")
	
	#tag0
	tag0M = rfidTemp['Cod'] == 0
	tag0M = rfidTemp[tag0M]
	tag0M = tag0M['Mag']
	tag0F = rfidTemp['Cod'] == 0
	tag0F = rfidTemp[tag0F]
	tag0F = tag0F['Freq']
	
	#tag1
	tag1M = rfidTemp['Cod'] == 1
	tag1M = rfidTemp[tag1M]
	tag1M = tag1M['Mag']
	tag1F = rfidTemp['Cod'] == 1
	tag1F = rfidTemp[tag1F]
	tag1F = tag1F['Freq']
	
	#tag2
	tag2M = rfidTemp['Cod'] == 2
	tag2M = rfidTemp[tag2M]
	tag2M = tag2M['Mag']
	tag2F = rfidTemp['Cod'] == 2
	tag2F = rfidTemp[tag2F]
	tag2F = tag2F['Freq']

	#tag3
	tag3M = rfidTemp['Cod'] == 3
	tag3M = rfidTemp[tag3M]
	tag3M = tag3M['Mag']
	tag3F = rfidTemp['Cod'] == 3
	tag3F = rfidTemp[tag3F]
	tag3F = tag3F['Freq']
	
	#tag4
	tag4M = rfidTemp['Cod'] == 4
	tag4M = rfidTemp[tag4M]
	tag4M = tag4M['Mag']
	tag4F = rfidTemp['Cod'] == 4
	tag4F = rfidTemp[tag4F]
	tag4F = tag4F['Freq']

	
	#Calcula Distância Euclediana
	x0 = calcEuc(tag0M, tagM)
	x1 = calcEuc(tag1M, tagM)
	x2 = calcEuc(tag2M, tagM)
	x3 = calcEuc(tag3M, tagM)
	x4 = calcEuc(tag4M, tagM)
	
	#Verifica qual é a etiqueta

	if (x0 < x1) and (x0 < x2) and (x0 < x3) and (x0 < x4):
		tag = "0"
		figuraDupla(tag, tag0F, tag0M, tagF, tagM)
	elif (x1 < x0) and (x1 < x2) and (x1 < x3) and (x0 < x4):
		tag = "1"
		figuraDupla(tag, tag1F, tag1M, tagF, tagM)
	elif (x2 < x0) and (x2 < x1) and (x2 < x3) and (x2 < x4):
		tag = "2"
		figuraDupla(tag, tag2F, tag2M, tagF, tagM)
	elif (x3 < x0) and (x3 < x1) and (x3 < x2) and (x3 < x4):
		tag = "3"
		figuraDupla(tag, tag3F, tag3M, tagF, tagM)
	elif (x4 < x0) and (x4 < x1) and (x4 < x2) and (x4 < x3):
		tag = "4"
		figuraDupla(tag, tag4F, tag4M, tagF, tagM)
	



	
def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)

def sweeper(prob_lvl):
	global f1, f2, f, step, result, amp, mag, freq
	if prob_lvl:
		amp = (prob_lvl)
		result.append({f, amp})
		magR=truncate(amp, 4)
		mag.append(magR)
		freq.append(int(f/1000000))
		f +=step
		amp = 0
	if f> f2:
		xF=np.array(freq)
		yM=np.array(mag)
		expDados(xF, yM)
		#figura(freq, mag)
		compTag(freq, mag)
		f=f1
		#print("Resultado ", result)
		#print("Frequência", freq)
		print("Tag Nº ",tag)
		freq=[]
		mag=[]
		result=[]
	return f
