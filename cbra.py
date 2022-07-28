# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:21:52 2022

@author: Mrunmay Junagade
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics as ST

#%% Read input
infile=r'G:\My Drive\Research\Cables\cbra\input.csv'
outfile=r'G:\My Drive\Research\Cables\cbra\out.xlsx'
inp=pd.read_csv(infile)
out=pd.read_excel(outfile)

#create average SOG data 

inp=inp.drop(columns=['MMSI','BaseDateTime','LAT','LON','Heading','COG','Status','CallSign'])
inp=inp.drop_duplicates()

#%% Vessel Types

#by type
l=(inp.VesselType)
l=l.sort_values(ascending=True)
l.dropna(inplace=True)
l=l.unique()
g=['luls']*len(l)
typecount=np.zeros(len(l))

for i in range(0,len(l)):
    typecount[i]=inp.VesselType.value_counts()[l[i]]
    j=str(l[i])
    g[i]=j

plt.figure(figsize=(16, 6), dpi=80)
plt.bar(g,typecount,label='Vessel Counts w.r.t DWT')
plt.xlabel('Vessel Type')
plt.ylabel('Vessel Counts')
plt.grid()   

#by DWT
k=(inp.DWT)
k=k.sort_values(ascending=True)
k=k.unique()

typecount2=np.zeros(len(k))

for i in range(0,len(k)):
    typecount2[i]=inp.DWT.value_counts()[k[i]]
    
plt.figure()
plt.plot(k[1:len(k)],typecount2[1:len(k)],'r--',label='Vessel Counts w.r.t DWT')
plt.xlabel('DWT')
plt.ylabel('Vessel Counts')
plt.grid()   


#%% Filter Inputs

mp=pd.Series(inp.AverageMileage).unique()
mp.sort()

#filter for Na values in lengths
inp=inp.sort_values(by=['AverageMileage'],ascending=True)
inp=inp.sort_values(by=['Length'],ascending=True)
inp=inp.reset_index(drop=True)
inp=inp.dropna(subset=['Length','Width','Draft'])

# #filter for Vessel Types
# VT=[1003,1004,1005,1016]
# inp=inp[inp['VesselType'].isin(VT)]


#%% Create Subset for mileage points

BigData=[None]*len(mp)
for i in range(0,len(mp)):
    a=inp[inp['AverageMileage']==mp[i]]
    BigData[i]=a
    

#%% Define Function to median percentile of Vessel Size - function to find DWT which includes 90% if vessels

for i in range(0,len(BigData)):
    m=BigData[i]
    DWT=np.percentile(m.DWT,50)
    out.Median_DWT[i]=DWT
    AW=(0.0913*(DWT*1000)**0.6452)/1000
    out.Strike_Depth[i]=1.3496*AW**0.3076
    out.Vessel_count_total[i]=len(BigData[i])*6
    out.Vship[i]=(sum(BigData[i].SOG)/len(BigData[i].SOG))*1.852
    m=m[m['DWT']>=DWT]
    BigData[i]=m
    out.Vessel_count_selected[i]=len(BigData[i])*6
    out.Pstrike[i]=out.Pwd[i]*out.Ptraffic[i]*len(BigData[i])*6*out.Dship[i]*out.Pincident[i]/(out.Vship[i]*8760)
    out.Recurrence[i]=1/out.Pstrike[i]
 
