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
############# THINGS TO MODIFY

# Read into pandas DataFrames
datapath="/Users/zanejobe/Google Drive/1_GraphicLogPapers/GraphicLogML/data/"
filename="AllBeds.csv"

df = pd.read_csv(datapath + filename)

# In[3]:

leg = ["basin plain mud","basin plain sand","fan mud","fan sand","channel mud","channel sand","levee mud","levee sand"]
colors = ["blue",        "cyan",           "red",    "magenta","yellow",      "gold",       "black",     "grey"]
ncolor = 0

for group0, values0 in df.groupby("eodnum"):
    for group, values in values0.groupby("snd_shl"): 
        plt.scatter(np.log2(values["mean_gs_mm"]).median(),np.log10(values["th"]).median(), color=colors[ncolor], s=25)
        plt.text(np.log2(values["mean_gs_mm"]).median(),np.log10(values["th"]).median(),leg[ncolor])
        ncolor+=1

plt.xlabel("mean grain size (psi)")
plt.ylabel("thickness (log10[m])")
xlim=[-10,-2]
ylim=[-2,0]
plt.xlim(xlim)
plt.ylim(ylim)
plt.xticks(np.arange(xlim[0],xlim[1]+1))
plt.yticks(np.arange(ylim[0],ylim[1]+1))

# In[4]:

xlab="mean grain size (psi)"
ylab="thickness (log10[m])"

# specify export file name
figname="AllBedsTHvsGS"

g = sns.JointGrid("mean_gs_mm", "th", df, size=8, space=0)

leg={"basin plain sand","basin plain mud","fan sand","fan mud","channel sand","channel mud","levee sand","levee mud"}
colors = ["blue",        "cyan",           "red",    "magenta","yellow",      "gold",       "black",     "grey"]
ncolor = 0

for group0, values0 in df.groupby("eodnum"):
    for group, values in values0.groupby("snd_shl"): 
        # plot the marginal KDEs for x and y
        sns.kdeplot(np.log2(values["mean_gs_mm"]), ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
        sns.kdeplot(np.log10(values["th"]), ax=g.ax_marg_y, color=colors[ncolor], vertical=True, shade=False, legend=False)
    
        # plot the median values
        g.ax_joint.scatter(np.log2(values["mean_gs_mm"]).median(),np.log10(values["th"]).median(), color=colors[ncolor], s=25)
        print('t') # error testing
        # now plot the 2D contour map
        for level in np.array([0.9]): # or could say np.linspace(0.1, 0.9, 9)
            density_contour.bivar_kde_contour(np.log2(values["mean_gs_mm"]), np.log10(values["th"]), frac=level, ax=g.ax_joint, color=colors[ncolor], alpha=1)
        
        ncolor+=1
        print(group0) # error testing
        print(group) # error testing

g.ax_joint.legend(leg) # THIS ISNT LABELING THINGS RIGHT

g.ax_joint.grid(color='grey', linestyle='-', linewidth=0.5)  
g.ax_joint.set_xlabel(xlab) 
g.ax_joint.set_ylabel(ylab) 

xlim=[-11,0]
ylim=[-4,1]
g.ax_joint.set_xlim(xlim)
g.ax_joint.set_ylim(ylim)

ytick=np.arange(ylim[0],ylim[1],1)
g.ax_joint.set_yticks(ytick) 
yticklabel=np.arange(ylim[0],ylim[1],1) 
yticklabel=yticklabel.astype(float)
g.ax_joint.set_yticklabels(np.power(10,yticklabel)) 

#plt.savefig(figname + ".pdf", transparent=True) 
