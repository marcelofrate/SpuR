#SpuR - An Spectral Signature Writer System in Chipless Tags Using Software Defined Radio (SDR)
#Reader - Module
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np
import pandas as pd
import sys
from tkinter import *
from tkinter import messagebox

f1 =    70000000
f2 =  6000000000
step =   1000000
f = f1
tag=1
amp=0
result=[]
mag=[]
freq=[]

def figuraDupla(tag,freq1, mag1, freq2, mag2):
    fig = plt.figure(figsize=(10, 7))
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
    ax.set_title("Tag Identificada Nº = "+tag)

    # Setting Label
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")

    # Adding Legend
    ax.legend(labels=('BD', 'Tag lida, Nº: '+tag))
    # cursor
    ax.set_xlabel('Frequency (MHz)')
    ax.set_ylabel('Magnitude (dBm)')
    cursor = Cursor(ax, color='green', linewidth=1.2)
    plt.ylim(-45, 0)
    plt.xlim(0, 6000)
    plt.grid()
    plt.savefig('/mnt/d/SpuR/Tag_Read_'+str(tag)+'.png', transparent=False)
    plt.show()
    
def figura(freq, mag):
	xF = np.array(freq)
	yM = np.array(mag)
	fig = plt.figure(figsize=(10, 7))
	ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
	ax.plot(xF, yM)
	plt.xticks(rotation=45)
	ax.set_xlabel('Frequency (MHz)')
	ax.set_ylabel('Magnitude')
	plt.title('Chipless RFID Reader')
	cursor = Cursor(ax, color='green', linewidth=1.2)
	plt.ylim(-45, 0)
	plt.xlim(1000, 6000)
	plt.grid()
	plt.show()

def expDados(freq, mag):
	rfidSet = pd.DataFrame({'Freq': freq, 'Mag': mag})
	rfidSet.to_csv('/mnt/d/SpuR/Tag_Read_'+str(tag)+'.csv', index = False)	

def calcEuc(magT, mag):
    xTemp = np.array(magT)
    xTag = np.array(mag)
    distE = np.linalg.norm(xTemp - xTag)
    return(distE)
    
def compTag(tagF,tagM):
	rfidTemp = pd.read_csv("/mnt/d/SpuR/BD/BD.csv")
	
	#Tag1
	tag1M = rfidTemp['Cod'] == 1
	tag1M = rfidTemp[tag1M]
	tag1M = tag1M['Mag']
	tag1F = rfidTemp['Cod'] == 1
	tag1F = rfidTemp[tag1F]
	tag1F = tag1F['Freq']
	
	#Tag2
	tag2M = rfidTemp['Cod'] == 2
	tag2M = rfidTemp[tag2M]
	tag2M = tag2M['Mag']
	tag2F = rfidTemp['Cod'] == 2
	tag2F = rfidTemp[tag2F]
	tag2F = tag2F['Freq']

	#Tag3
	tag3M = rfidTemp['Cod'] == 3
	tag3M = rfidTemp[tag3M]
	tag3M = tag3M['Mag']
	tag3F = rfidTemp['Cod'] == 3
	tag3F = rfidTemp[tag3F]
	tag3F = tag3F['Freq']
	
	#Tag4
	tag4M = rfidTemp['Cod'] == 4
	tag4M = rfidTemp[tag4M]
	tag4M = tag4M['Mag']
	tag4F = rfidTemp['Cod'] == 4
	tag4F = rfidTemp[tag4F]
	tag4F = tag4F['Freq']
	
	#Calcula Distância Euclediana
	x1 = calcEuc(tag1M, tagM)
	x2 = calcEuc(tag2M, tagM)
	x3 = calcEuc(tag3M, tagM)
	x4 = calcEuc(tag4M, tagM)
	
#Verifica qual é a etiqueta
	if (x1 < x2) and (x1 < x3) and (x1 < x4):
		tag = "1"
		figuraDupla(tag, tag1F, tag1M, tagF, tagM)
	elif (x2 < x1) and (x2 < x3) and (x2 < x4):
		tag = "2"
		figuraDupla(tag, tag2F, tag2M, tagF, tagM)
	elif (x3 < x1) and (x3 < x2) and (x3 < x4):
		tag = "3"
		figuraDupla(tag, tag3F, tag3M, tagF, tagM)
	elif (x4 < x1) and (x4 < x2) and (x4 < x3):
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
		compTag(freq, mag)
		f=f1
		print("Tag Nº ",tag)
		expDados(xF, yM)
		freq=[]
		mag=[]
		result=[]
	return f
