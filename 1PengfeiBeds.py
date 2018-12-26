
# coding: utf-8

# In[1]:
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import density_contour

# to make saved pdf figures have real text, not outlines
matplotlib.rcParams['pdf.fonttype'] = 42 
matplotlib.rcParams['ps.fonttype'] = 42

# In[2]:
############# THINGS TO MODIFY

# Read into pandas DataFrames
datapath="/Users/zanejobe/Desktop/pengfei/"
filename="Zone2and3_all.csv"

df = pd.read_csv(datapath + filename)

# In[4]:

xlab="sand (m)"
ylab="mud (m)"

# specify export file name
figname="PengfeiSandMud"

g = sns.JointGrid("ss", "ms", df, size=8, space=0)

colors = ["red", "green"]
ncolor = 0

for group, values in df.groupby("zone"):
    # plot the marginal KDEs for x and y
    sns.kdeplot(np.log10(values["ss"]), ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
    sns.kdeplot(np.log10(values["ms"]), ax=g.ax_marg_y, color=colors[ncolor], vertical=True, shade=False, legend=False)
    
    # plot the median values
    g.ax_joint.scatter(np.log10(values["ss"]).median(),np.log10(values["ms"]).median(), color=colors[ncolor], s=25)
        
    # now plot the 2D contour map
    for level in np.array([0.9]): # or could say np.linspace(0.1, 0.9, 9)
        density_contour.bivar_kde_contour(np.log10(values["ss"]),np.log10(values["ms"]), frac=level, ax=g.ax_joint, color=colors[ncolor], alpha=1)
    
    ncolor+=1

xlim=[-2,0]
ylim=[-3,1]
g.ax_joint.set_xlim(xlim)
g.ax_joint.set_ylim(ylim)

g.ax_joint.grid(color='grey', linestyle='-', linewidth=0.5)  
g.ax_joint.set_xlabel(xlab) 
g.ax_joint.set_ylabel(ylab) 

g.ax_joint.legend('23')


xtick=np.arange(xlim[0],xlim[1]+1,1)
g.ax_joint.set_xticks(xtick) 

xticklabel=np.arange(xlim[0],xlim[1]+1,1)
xticklabel=xticklabel.astype(float)
g.ax_joint.set_xticklabels(np.power(10,xticklabel)) 

ytick=np.arange(ylim[0],ylim[1]+1,1)
g.ax_joint.set_yticks(ytick) 
yticklabel=np.arange(ylim[0],ylim[1]+1,1) 
yticklabel=yticklabel.astype(float)
g.ax_joint.set_yticklabels(np.power(10,yticklabel)) 

#plt.savefig(figname + ".pdf", transparent=True)