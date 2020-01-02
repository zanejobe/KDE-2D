import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import math

import density_contour





datapath="/Users/zanejobe/Dropbox/1 PointLomaRosieCABR/Compilation_Database/Digitize/PLdata/PointLomaShp_2019/"
filename="aaPLData_Thickness_ThinningRate_Distance_Lithology_Element.txt"
df = pd.read_csv(datapath + filename, header=1, names=['th', 'tr', 'dist', 'lith', 'el']) 

# drop rows with NaNs for thickness
df = df[np.isfinite(df['th'])]
# and now the same for thinning rate
df = df[np.isfinite(df['tr'])]
# and get rid of the datum "garbage bed" that has an element number=10
df=df[df.el != 10] # the != means "not equal to"

# make some log10 columns to make plotting easier
df['logth']=np.log10(df.th)
df['logtr']=np.log10(df.tr)
df['logdist']=np.log10(df.dist)






xlab="thinning rate (cm/m) (data is m/m, but xticklabels are adjusted to cm/m)"
ylab="thickness (m)"
# thinning rate is x axis
# thickness is y axis

colors = ["black", "xkcd:yellowish" , "xkcd:greenish", "xkcd:cerulean"]
ncolor = 0






g = sns.JointGrid("logtr", "logth", df, size=10, space=0)
for el, values in df.groupby("el"):
    # plot the marginal KDEs for x and y
    sns.kdeplot(values["logtr"], ax=g.ax_marg_x, color=colors[ncolor], shade=False, legend=False)
    sns.kdeplot(values["logth"], ax=g.ax_marg_y, color=colors[ncolor], vertical=True, shade=False, legend=False)
    # plot the median values
    g.ax_joint.scatter(values["logtr"].median(),values["logth"].median(), color=colors[ncolor], s=25)
    g.ax_joint.text(values["logtr"].median(),values["logth"].median(),'n='+ str(len(values["logth"])))
    # now plot the 2D contour map
    
    
    
    
    # NOT WORKING
    density_contour.bivar_kde_contour(values["logtr"], values["logth"],frac=0.9,color=colors[ncolor])
    #g.plot_joint(sns.kdeplot) # this should work but it's not either
    
    
    # ARE THERE ISSUES WITH THE NEGATIVE NUMBERS? AXIS CALL? WHERE ARE THEY PLOTTING
    
    
    
    ncolor+=1
    print(el)

xlim=[-6,-1]
ylim=[-3,0]

g.fig.suptitle('Cabrillo Lobe Elements')
g.ax_joint.legend('1234',loc='lower right') #not the best way, but it works
g.ax_joint.set_xlim(xlim)
g.ax_joint.set_ylim(ylim)
g.ax_joint.grid(color='grey', linestyle='-', linewidth=0.5)  
g.ax_joint.set_xlabel(xlab) 
g.ax_joint.set_ylabel(ylab) 
xtick=np.arange(xlim[0],xlim[1]+1,1)
g.ax_joint.set_xticks(xtick) 
xticklabel=np.arange(xlim[0]+2,xlim[1]+3,1) # add 2 (i.e., 100 in log space) to each to convert m/m to cm/m
xticklabel=xticklabel.astype(float)
g.ax_joint.set_xticklabels(np.power(10,xticklabel)) 
ytick=np.arange(ylim[0],ylim[1]+1,1)
g.ax_joint.set_yticks(ytick) 
yticklabel=np.arange(ylim[0],ylim[1]+1,1) 
yticklabel=yticklabel.astype(float)
g.ax_joint.set_yticklabels(np.power(10,yticklabel));

