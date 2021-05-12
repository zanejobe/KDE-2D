# In[1]:
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

%cd "/Users/zanejobe/Dropbox/GitHub/KDE-2D/"
import density_contour

# to make saved pdf figures have real text, not outlines
matplotlib.rcParams['pdf.fonttype'] = 42 
matplotlib.rcParams['ps.fonttype'] = 42

# In[2]:

# Read into pandas DataFrames
datapath="/Users/zanejobe/Google Drive/1_GraphicLogPapers/GraphicLogML/data/"
filename="AllCores_NoBeds.csv"

df = pd.read_csv(datapath + filename)

# In[3]: Plot a P10-50-90 plot of NG vs AR

leg = ["basin plain","fan","channel","levee"]
colors = ["blue","red","yellow","black"]
ncolor = 0

for group, values in df.groupby("eodnum"): 
    #plt.scatter(np.percentile(values["ng"],10),np.percentile(values["ar"],10),color=colors[ncolor], s=25) # P10
    plt.scatter(values["ng"].median(),values["ar"].median(), color=colors[ncolor], s=25) # P50
    #plt.scatter(np.percentile(values["ng"],90),np.percentile(values["ar"],90),color=colors[ncolor], s=25) # P90
    ncolor+=1

plt.legend(leg) # This wont work if you uncomment the other plt functions in the loop
plt.xlabel("net to gross")
plt.ylabel("amalgamation ratio")
xlim=[0,1]
ylim=[0,1]
plt.xlim(xlim)
plt.ylim(ylim)

# In[4]:

xlab="Net to Gross"
ylab="Lithologic Sand Thickness Mean (m)"

figname="AllBedsTHvsGS" # specify export file name

g = sns.JointGrid("ng", "SB_mean", df, size=8, space=0)

leg = ["basin plain","fan","channel","levee"]
colors = ["blue","red","yellow","black"]
ncolor = 0

for group, values in df.groupby("eodnum"):
        # plot the marginal KDEs for x and y
        sns.kdeplot(values["ng"], ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
        sns.kdeplot(np.log10(values["SB_mean"]), ax=g.ax_marg_y, color=colors[ncolor], vertical=True, shade=False, legend=False)
    
        # plot the median values
        g.ax_joint.scatter(values["ng"].median(),np.log10(values["SB_mean"]).median(), color=colors[ncolor], s=25)
        # now plot the 2D contour map
        for level in np.array([0.9]): # or could say np.linspace(0.1, 0.9, 9)
            density_contour.bivar_kde_contour(values["ng"],np.log10(values["SB_mean"]), frac=level, ax=g.ax_joint, color=colors[ncolor], alpha=1)
        ncolor+=1

g.ax_joint.legend(leg)

g.ax_joint.grid(color='grey', linestyle='-', linewidth=0.5)  
g.ax_joint.set_xlabel(xlab) 
g.ax_joint.set_ylabel(ylab) 

xlim=[-0.5,1.5]
ylim=[-3,2]
g.ax_joint.set_xlim(xlim)
g.ax_joint.set_ylim(ylim)

ytick=np.arange(ylim[0],ylim[1],1)
g.ax_joint.set_yticks(ytick) 
yticklabel=np.arange(ylim[0],ylim[1],1) 
yticklabel=yticklabel.astype(float)
g.ax_joint.set_yticklabels(np.power(10,yticklabel)) 

# In[4]:

xlab="Sand Thickness IQR (m)"
ylab="Mud Thickness IQR (m)"

figname="AllBedsTHvsGS" # specify export file name

g = sns.JointGrid("sand_th_iqr", "mud_th_iqr", df, size=8, space=0)

leg = ["basin plain","fan","channel","levee"]
colors = ["blue","red","yellow","black"]
ncolor = 0

for group, values in df.groupby("eodnum"):
        # plot the marginal KDEs for x and y
        sns.kdeplot(np.log10(values["sand_th_iqr"]), ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
        sns.kdeplot(np.log10(values["mud_th_iqr"]), ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
    
        # plot the median values
        g.ax_joint.scatter(np.log10(values["sand_th_iqr"]).median(),np.log10(values["mud_th_iqr"]).median(), color=colors[ncolor], s=25)
        # now plot the 2D contour map
        for level in np.array([0.9]): # or could say np.linspace(0.1, 0.9, 9)
            density_contour.bivar_kde_contour(np.log10(values["sand_th_iqr"]),np.log10(values["mud_th_iqr"]), frac=level, ax=g.ax_joint, color=colors[ncolor], alpha=1)
        ncolor+=1

g.ax_joint.legend(leg)

g.ax_joint.grid(color='grey', linestyle='-', linewidth=0.5)  
g.ax_joint.set_xlabel(xlab) 
g.ax_joint.set_ylabel(ylab) 

# In[4]:

xlab="net to gross"
ylab="Lithologic Sand Thickness StDev"

figname="AllBedsTHvsGS" # specify export file name

g = sns.JointGrid("ng", "SB_std", df, size=8, space=0)

leg = ["basin plain","fan","channel","levee"]
colors = ["blue","red","yellow","black"]
ncolor = 0

for group, values in df.groupby("eodnum"):
        # plot the marginal KDEs for x and y
        sns.kdeplot(values["ng"], ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
        sns.kdeplot(np.log10(values["SB_std"]), ax=g.ax_marg_y, color=colors[ncolor], vertical=True, shade=False, legend=False)
    
        # plot the median values
        g.ax_joint.scatter(values["ng"].median(),np.log10(values["SB_std"]).median(), color=colors[ncolor], s=25)
        # now plot the 2D contour map
        for level in np.array([0.9]): # or could say np.linspace(0.1, 0.9, 9)
            density_contour.bivar_kde_contour(values["ng"],np.log10(values["SB_std"]), frac=level, ax=g.ax_joint, color=colors[ncolor], alpha=1)
        ncolor+=1

g.ax_joint.legend(leg)

g.ax_joint.grid(color='grey', linestyle='-', linewidth=0.5)  
g.ax_joint.set_xlabel(xlab) 
g.ax_joint.set_ylabel(ylab) 

# In[4]:

xlab="net to gross"
ylab="amalgamation ratio"

figname="AllBedsTHvsGS" # specify export file name

g = sns.JointGrid("ng", "ar", df, size=8, space=0)

leg = ["basin plain","fan","channel","levee"]
colors = ["blue","red","yellow","black"]
ncolor = 0

for group, values in df.groupby("eodnum"):
        # plot the marginal KDEs for x and y
        sns.kdeplot(values["ng"], ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
        sns.kdeplot(values["ar"], ax=g.ax_marg_y, color=colors[ncolor], vertical=True, shade=False, legend=False)
    
        # plot the median values
        g.ax_joint.scatter(values["ng"].median(),values["ar"].median(), color=colors[ncolor], s=25)
        # now plot the 2D contour map
        for level in np.array([0.9]): # or could say np.linspace(0.1, 0.9, 9)
            density_contour.bivar_kde_contour(values["ng"],values["ar"], frac=level, ax=g.ax_joint, color=colors[ncolor], alpha=1)
        ncolor+=1

g.ax_joint.legend(leg)

g.ax_joint.grid(color='grey', linestyle='-', linewidth=0.5)  
g.ax_joint.set_xlabel(xlab) 
g.ax_joint.set_ylabel(ylab) 

xlim=[0,1]
ylim=[0,1]
g.ax_joint.set_xlim(xlim)
g.ax_joint.set_ylim(ylim)

#ytick=np.arange(ylim[0],ylim[1],1)
#g.ax_joint.set_yticks(ytick) 
#yticklabel=np.arange(ylim[0],ylim[1],1) 
#yticklabel=yticklabel.astype(float)
#g.ax_joint.set_yticklabels(np.power(10,yticklabel)) 

#plt.savefig(figname + ".pdf", transparent=True) 
