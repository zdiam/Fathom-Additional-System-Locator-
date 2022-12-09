
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
import pandas as pd
import os
import numpy as np



#gui interface
def import_csv_data():
    global j
    csv_file_path = askopenfilename()
    print(csv_file_path)
    j.set(csv_file_path)
    df = pd.read_csv(csv_file_path)
#gui for entering the file path of the .csv file
root = tk.Tk()
root.geometry('450x400')
root.title('Enter File')
tk.Label(root, text='File Path').place(x = 15, y = 65)
tk.Label(root, text='*Resave .csv file after export before use to avoid encoding error*').place(x = 15, y = 40)
j = tk.StringVar()

entry = tk.Entry(root, textvariable=j).place(x = 15, y = 90)
tk.Button(root, text='.csv File Location',command=import_csv_data).place(x = 75, y = 90)
tk.Button(root, text='Input GPM and Maximum Velocity',command=root.destroy).place(x = 15, y = 190)
root.mainloop()
#end of gui for .csv file which leads into next gui for paramter info due to root.destroy

#gui for paramater info entering
root = Tk()
root.geometry('450x450')
root.title('Fathom Additional System Advisor')

def info():
    list_of_lists = [[f'{gpm.get()}',],
                    [f'{velocity.get()}',]],


entry1_text = Label(root, text = 'Enter Additional GPM')
entry2_text = Label(root, text = 'Enter Maximum Velocity Allowed (ft/s)')

entry1_text.place(x = 15, y = 30)
entry2_text.place(x = 15, y = 90)

gpm = StringVar()
velocity = StringVar()

gpm_entry = Entry(root, textvariable = gpm, width = "15")
velocity_entry = Entry(root, textvariable = velocity, width = "15")

gpm_entry.place(x = 15, y = 60)
velocity_entry.place(x = 15, y = 120)


register = Button(root,text = "Run", width = "10", height = "2", command=root.destroy, bg = "lightgreen")
register.place(x = 15, y = 240)

root.mainloop()
#end of gui

chw = pd.read_csv (j.get(), error_bad_lines=False)
#reads .csv from string entered into 1st gui



chw.rename(columns={chw.columns[0]:'Info'}, inplace=True)
#Rename the 1st column for easier future searches

#Locate the start of the pipe output table info
chwp = chw.loc[chw['Info'].str.contains('Pipe Output Table',na=False)]
chwp


#Find the amount of pipes modeled from the output data 
chwpa = chw.loc[chw['Info'].str.contains('Number Of Pipes=',na=False)]
chwpa.set_index('Info')
chwpa = chwpa.loc [: , 'Info']
str(chwpa)
#Produces with a string with the number of pipes


import re
nop = re.findall(r'= \d+', str(chwpa))
nop = re.findall(r'\d+', str(nop))
nop = ''.join(nop)
nop = float(nop)
nop
#Extracts the number of pipes to an integer value to use for the location. This seems a little obtuse and there is probably a better way to do it



chwpn = chwp.index[0]

#Extracts the row to start pulling pipe info from


chwpn = chwpn.astype(float)
#Data type changes

pipes = chw.loc[(int(chwpn)+2):((int(chwpn)+3)+int(nop)-1)]
pipes.columns = pipes.iloc[0]

#Find information on pipe outputs from all the pulled data above

pipes = pipes.loc[(int(chwpn)+3):((int(chwpn)+3)+int(nop)-1)]
pipes = pipes[['Pipe','Pipe Nominal Size','Vol. Flow Rate (gal/min)','Velocity  (feet/sec)']]


pipesA = pipes['Pipe']
pipesB = pipes['Pipe Nominal Size'].str.extract('(\d+\.*\d*)')
pipesC = pipes['Vol. Flow Rate (gal/min)'].str.extract('(\d+\.*\d*)')
pipesD = pipes['Velocity  (feet/sec)'].str.extract('(\d+\.*\d*)')
#Extract values from each column that are not numbers besides the pipe column incase they are named. This will round down any 1/n" pipe due to Fathom displaying this as "x-1/y". 
# This is acceptable since only smaller pipe is manufactured at such intervals. It may be worthwhile to adjust this if the application were to expand outside of adding new buildings to a system.



pipes = pd.concat([pipesA,pipesB,pipesC,pipesD,],axis =1, ignore_index=True)
pipes.columns= ['Pipe Name','Pipe Size (in.)','Vol. Flow Rate (gal./min.)','Velocity (ft./s.)']

#Merge all columns back together after filtering out letters


pipesfloat = pipes[['Pipe Size (in.)','Vol. Flow Rate (gal./min.)','Velocity (ft./s.)']].apply(pd.to_numeric)
pipesfloat.astype(float)
#Data type changes for non pipe name column

pipesno = pipes['Pipe Name']
#Pull the pipe name out and readd to system where all other values are floats
pipes = pd.concat([pipesno,pipesfloat], axis =1 )

pipes['ID'] = pipes['Pipe Size (in.)']
pipes['ID']= pipes['ID'].replace({1.0:1.049,2.0: 2.067, 3.0:3.068, 4.0: 4.026, 5.0:5.047, 6.0: 6.065, 8.0: 7.981, 10.0:10.020, 12.0 : 11.938, 16.0 : 15.0, 18.0 : 16.876, 20.0 : 18.812, 24.0 : 22.624, 32.0: 30.624 , 34.0: 32.624, 36.0 : 34.5, 42.0 : 40.5}) 
#Use ID FROM _______ https://www.engineersedge.com/fluid_flow/steel-pipe-schedule-40.htm



ps= gpm.get()
#Entered additional gpm from gui #2

pipes['New Combined GPM'] = pipes['Vol. Flow Rate (gal./min.)'].add(int(ps))
#Create a new column which is the combination of the existing flow rates from the .csv import and the additonal gpm from gui#2

# Q = V * A == Flow rate is equal to Velocity times Cross Sectional Area
cSA = (3.14*((pipes['ID']/2)**2))#Circle Cross Section Area formula
cSA = (3.85*pipes['New Combined GPM']/cSA) # 1 gal/min == 3.85 in^3/s
cSA = cSA/12 # Convert the output velocity from in to ft


cc = pd.concat([pipes,cSA], axis = 1, ignore_index=False)
#Add cSA (the new velocity of the pipe from the new combined gpm)

cc = cc.loc[cc['Vol. Flow Rate (gal./min.)'] > 0] #Remove all values that are 0. Negatives will also be removed.

cc.rename( columns={0 :'New Velocity'}, inplace=True )



ve = float(velocity.get())
#Gets the max allowed velocity entered into gui#2

pl = cc.loc[cc['New Velocity'] < float(ve)]
pl = pl.loc[pl['New Velocity']!= 0]
#Locates values of the new velocity that are less than the allowed max. Also removes 0 values incase they are missed by any other filter to remove null pipes

plcsv = pl[['Pipe Name','New Velocity']].copy()



xs= j.get()
xy = gpm.get()

filepath = (xs)
#Setup save path to be the initial file location of the .csv file and the gpm added to the system
filepath = filepath.replace('csv', xy+'gpm.csv')
plcsv.to_csv (filepath,index=None)