import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#############################################################################################################################################################
cb = pd.read_csv('constellation_borders.csv', low_memory=False)
#############################################################################################################################################################

dup_cb = cb.copy(deep=True)  # Constellation borders
dup_cb['RAJ2000'] -= 360  # Constellation borders transform



#############################################################################################################################################################
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.set_aspect(1)

# plot borders
# ax.scatter(cb['RAJ2000'], cb['DEJ2000'], color='grey', s=0.1, zorder=0)
# ax.scatter(dup_cb['RAJ2000'], dup_cb['DEJ2000'], color='grey', s=0.1, zorder=0)

ax.set_xlim([-400,400])
ax.set_ylim([-90,90])

cst_names=cb['Constellation'].unique()
cbcx=[]
cbcy=[]
for i in cst_names:
    cbcx.append((cb[(cb['Constellation']==i)]['RAJ2000'].min()+cb[(cb['Constellation']==i)]['RAJ2000'].max())/2)
    cbcy.append((cb[(cb['Constellation']==i)]['DEJ2000'].min()+cb[(cb['Constellation']==i)]['DEJ2000'].max())/2)
dup_cbcx=np.array(cbcx)-360

for i, txt in enumerate(cst_names):
    p=ax.annotate(txt, (cbcx[i], cbcy[i]), xytext=(0, 0), textcoords='offset points', horizontalalignment='center', verticalalignment='center', fontsize=4)
for i, txt in enumerate(cst_names):
    p=ax.annotate(txt, (dup_cbcx[i], cbcy[i]), xytext=(0, 0), textcoords='offset points', horizontalalignment='center', verticalalignment='center', fontsize=4)

plt.show()
