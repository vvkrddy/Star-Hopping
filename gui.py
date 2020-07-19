import mpld3
from mpld3 import plugins
from mpld3.utils import get_id
import numpy as np
import collections
import matplotlib.pyplot as plt
import pandas as pd
from svgpath2mpl import parse_path
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
import pylab
import tkinter as tk
import tkinter.messagebox as mb
import mplcursors
import pickle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = tk.Tk()
root.withdraw()
root.wm_title("Embedding in Tk")



# ##############################################################################################################################################################

ng = pd.read_csv('NGC.csv', low_memory=False)
ms = pd.read_csv('messier_objects.csv', low_memory=False)
cb = pd.read_csv('constellation_borders.csv', low_memory=False)
ty = pd.read_csv('tycho-1.csv', low_memory=False)

ell = parse_path(
    """M 490.60742,303.18917 A 276.31408,119.52378 28.9 0 1 190.94051,274.29027 276.31408,119.52378 28.9 0 1 6.8010582,36.113705 276.31408,119.52378 28.9 0 1 306.46799,65.012613 276.31408,119.52378 28.9 0 1 490.60742,303.18917 Z""")
ell.vertices -= ell.vertices.mean(axis=0)

df = pd.DataFrame(ms)
ident = np.array(df['ID (for resolver)'])
name = np.array(df['Common Name'])

#############################################################################################################################################################

hmag = 20
mag = 6

mag_ng = ng[(ng["V"] <= hmag)]
mag_ms = ms[(ms['V (from SEDS)'] <= hmag)]
mag_ty = ty[(ty['V'] <= mag)]  # Tycho
dup_ng = mag_ng.copy(deep=True)  # NGC
dup_ms = mag_ms.copy(deep=True)  # Messier
dup_ty = mag_ty.copy(deep=True)  # Tycho
dup_cb = cb.copy(deep=True)  # Constellation borders
dup_ng['RAJ2000'] -= 360  # NGC transform
dup_ms['RAJ2000'] -= 360  # Messier transform
dup_ty['RAJ2000'] -= 360  # Tycho transfor9
dup_cb['RAJ2000'] -= 360  # Constellation borders transform

# sorting objects in messier_objects.csv and NGC.csv according to objects
# globular clusters
gc_ms = ms[(ms["TYPE"] == 'GlC')]
gc_ng = ng[(ng["Type"] == 'GlC')]
# open clusters
oc_ms = ms[(ms["TYPE"] == 'OpC') | (ms["TYPE"] == 'Cl*')]
oc_ng = ng[(ng["Type"] == 'OpC') | (ng["Type"] == 'C+N')]
# galaxies
ga_ms = ms[(ms["TYPE"] == 'G') | (ms["TYPE"] == 'Sy2') | (ms["TYPE"] == 'IG') | (ms["TYPE"] == 'GiG') | (
        ms["TYPE"] == 'GiP') | (ms["TYPE"] == 'SyG') | (ms["TYPE"] == 'SBG') | (ms["TYPE"] == 'BiC') | (
                   ms["TYPE"] == 'H2G')]
ga_ng = ng[(ng["Type"] == 'Gal')]
# nebula and supernova remnant
nb_ms = ms[(ms["TYPE"] == 'PN') | (ms["TYPE"] == 'RNe') | (ms["TYPE"] == 'HII') | (ms["TYPE"] == 'SNR')]
nb_ng = ng[(ng["Type"] == 'PN') | (ng["Type"] == 'Nb') | (ng["Type"] == 'Kt')]
# other messiers
ot_ms = ms[(ms["TYPE"] == 'HII') | (ms["TYPE"] == 'As*') | (ms["TYPE"] == 'LIN') | (ms["TYPE"] == 'mul') | (
        ms["TYPE"] == 'AGN') | (ms["TYPE"] == 'SNR')]
# other ngc; stars
ot_ng = ng[(ng["Type"] == 'D+?') | (ng["Type"] == 'C+N') | (ng["Type"] == 'Kt') | (
        ng["Type"] == '*?') | (ng["Type"] == 'Ast') | (ng["Type"] == 'Str')]

# duplicated data sort by object type
# globular clusters
dup_gc_ms = dup_ms[(dup_ms["TYPE"] == 'GlC')]
dup_gc_ng = dup_ng[(dup_ng["Type"] == 'GlC')]
# open clusters
dup_oc_ms = dup_ms[(dup_ms["TYPE"] == 'OpC') | (dup_ms["TYPE"] == 'Cl*')]
dup_oc_ng = dup_ng[(dup_ng["Type"] == 'OpC') | (dup_ng["Type"] == 'C+N')]
# galaxies
dup_ga_ms = dup_ms[
    (dup_ms["TYPE"] == 'G') | (dup_ms["TYPE"] == 'Sy2') | (dup_ms["TYPE"] == 'IG') | (dup_ms["TYPE"] == 'GiG') | (
            dup_ms["TYPE"] == 'GiP') | (dup_ms["TYPE"] == 'SyG') | (dup_ms["TYPE"] == 'SBG') | (
            dup_ms["TYPE"] == 'BiC') | (
            dup_ms["TYPE"] == 'H2G')]
dup_ga_ng = dup_ng[(dup_ng["Type"] == 'Gal')]
# nebula and supernova remnant
dup_nb_ms = dup_ms[
    (dup_ms["TYPE"] == 'PN') | (dup_ms["TYPE"] == 'RNe') | (dup_ms["TYPE"] == 'HII') | (dup_ms["TYPE"] == 'SNR')]
dup_nb_ng = dup_ng[(dup_ng["Type"] == 'PN') | (dup_ng["Type"] == 'Nb') | (dup_ng["Type"] == 'Kt')]
# other messiers
dup_ot_ms = dup_ms[
    (dup_ms["TYPE"] == 'HII') | (dup_ms["TYPE"] == 'As*') | (dup_ms["TYPE"] == 'LIN') | (dup_ms["TYPE"] == 'mul') | (
            dup_ms["TYPE"] == 'AGN') | (dup_ms["TYPE"] == 'SNR')]
# other ngc; stars
dup_ot_ng = dup_ng[
    (dup_ng["Type"] == 'D+?') | (dup_ng["Type"] == 'C+N') | (dup_ng["Type"] == 'Kt') | (
            dup_ng["Type"] == '*?') | (dup_ng["Type"] == 'Ast') | (dup_ng["Type"] == 'Str')]

# dropping rows with missing mag values
gc_ms = gc_ms.dropna(subset=['V (from SEDS)'])
gc_ng = gc_ng.dropna(subset=['V'])
oc_ms = oc_ms.dropna(subset=['V (from SEDS)'])
oc_ng = oc_ng.dropna(subset=['V'])
ga_ms = ga_ms.dropna(subset=['V (from SEDS)'])
ga_ng = ga_ng.dropna(subset=['V'])
nb_ms = nb_ms.dropna(subset=['V (from SEDS)'])
nb_ng = nb_ng.dropna(subset=['V'])
ot_ms = ot_ms.dropna(subset=['V (from SEDS)'])
ot_ng = ot_ng.dropna(subset=['V'])

dup_gc_ms = dup_gc_ms.dropna(subset=['V (from SEDS)'])
dup_gc_ng = dup_gc_ng.dropna(subset=['V'])
dup_oc_ms = dup_oc_ms.dropna(subset=['V (from SEDS)'])
dup_oc_ng = dup_oc_ng.dropna(subset=['V'])
dup_ga_ms = dup_ga_ms.dropna(subset=['V (from SEDS)'])
dup_ga_ng = dup_ga_ng.dropna(subset=['V'])
dup_nb_ms = dup_nb_ms.dropna(subset=['V (from SEDS)'])
dup_nb_ng = dup_nb_ng.dropna(subset=['V'])
dup_ot_ms = dup_ot_ms.dropna(subset=['V (from SEDS)'])
dup_ot_ng = dup_ot_ng.dropna(subset=['V'])

mag_ty = mag_ty.dropna(subset=['V'])
dup_ty = dup_ty.dropna(subset=['V'])

#############################################################################################################################################################
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.set_aspect(1)
# fig = pylab.gcf()
# fig.canvas.set_window_title('Editor _ Star Hopping')
plt.gcf().canvas.set_window_title('Editor _ Star Hopping')
fig.patch.set_facecolor('seashell')
ax.set_facecolor('gainsboro')
ax.set_axisbelow(True)
ax.minorticks_on()
ax.grid(which='major', color="#838383", zorder=0, alpha=.4)
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black', zorder=0, alpha=0.2)

# xl = ra- fov / 2 - fov / 10
# xr = ra + fov / 2 + fov / 10
# yb = dec - fov / 2 - fov / 10
# yt = dec + fov / 2 + fov/ 10
#
# # if xr>360:
# #     ra-=360
# #     xr-=360
# #     xl-=360
#
# ax.set_xlim([xl,xr])
# ax.set_ylim([yb,yt])

# ax.set_yticklabels([round(y,2) for y in ax.get_yticks()])
# ax.set_xticklabels([(x+360) if x<0 and (x+360)>0 else x+720 if (x+360)<0  else round(x,2) if x>0 and x<360 else x%360 for x in ax.get_xticks()])

ts_fact = 100
s_fact = 10000

ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
           zorder=2,
           edgecolor="grey", linewidth=.004 * oc_ms['V (from SEDS)'])
ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
           zorder=3,
           edgecolor="grey", linewidth=1)
ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
           zorder=2,
           edgecolor="grey", linewidth=1)
ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ms['V (from SEDS)']),
           zorder=2)
ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (nb_ms['V (from SEDS)']),
           zorder=3)
ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='black', marker="+",
           s=s_fact * 10 / 2.5 ** (nb_ms['V (from SEDS)']), zorder=2)
ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='red', marker="+", linewidth=1,
           s=s_fact / 2.5 ** (ot_ms['V (from SEDS)']),
           edgecolor="grey")
ax.scatter(dup_oc_ms['RAJ2000'], dup_oc_ms['DEJ2000'], color='yellow', marker="o",
           s=s_fact / 2.5 ** (dup_oc_ms['V (from SEDS)']),
           zorder=2, edgecolor="grey", linewidth=.004 * oc_ms['V (from SEDS)'])
ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='black', marker="+",
           s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
           zorder=3, edgecolor="grey", linewidth=1)
ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='yellow', marker="o",
           s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
           zorder=2, edgecolor="grey", linewidth=1)
ax.scatter(dup_ga_ms['RAJ2000'], dup_ga_ms['DEJ2000'], color='red', marker=ell,
           s=s_fact / 2.5 ** (dup_ga_ms['V (from SEDS)']),
           zorder=2)
ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='green', marker="o",
           s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),
           zorder=3)
ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='black', marker="+",
           s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),
           zorder=2)
ax.scatter(dup_ot_ms['RAJ2000'], dup_ot_ms['DEJ2000'], c='red', marker="+", edgecolor="grey", linewidth=1,
           s=s_fact / 2.5 ** (dup_ot_ms['V (from SEDS)']))
#
# ax.scatter(oc_ng['RAJ2000'], oc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (oc_ng['V']), zorder=2,
#            edgecolor="grey", linewidth=1)
# ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ng['V']), zorder=3,
#            edgecolor="grey", linewidth=1)
# ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (gc_ng['V']), zorder=2,
#            edgecolor="grey", linewidth=1)
# ax.scatter(ga_ng['RAJ2000'], ga_ng['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ng['V']), zorder=2)
# ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (nb_ng['V']), zorder=3)
# ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (nb_ng['V']), zorder=2)
# ax.scatter(ot_ng['RAJ2000'], ot_ng['DEJ2000'], c='blue', marker="+", linewidth=1, s=s_fact / 2.5 ** (ot_ng['V']),
#            edgecolor="grey")
# ax.scatter(dup_oc_ng['RAJ2000'], dup_oc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_oc_ng['V']),
#            zorder=2, edgecolor="grey", linewidth=1)
# ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (dup_gc_ng['V']),
#            zorder=3, edgecolor="grey", linewidth=1)
# ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_gc_ng['V']),
#            zorder=2, edgecolor="grey", linewidth=1)
# ax.scatter(dup_ga_ng['RAJ2000'], dup_ga_ng['DEJ2000'], color='red', marker=ell,   s=s_fact / 2.5 ** (dup_ga_ng['V']),
#            zorder=2)
# ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (dup_nb_ng['V']),
#            zorder=3)
# ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (dup_nb_ng['V']),
#            zorder=2)
# ax.scatter(dup_ot_ng['RAJ2000'], dup_ot_ng['DEJ2000'], c='blue', marker="+", edgecolor="grey", linewidth=1,
#            s=s_fact / 2.5 ** (dup_ot_ng['V']))

#

# ocm=ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']), zorder=3,
#            edgecolor="grey", linewidth=1)
# gcm=ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']), zorder=3,
#            edgecolor="grey", linewidth=1)
# gam=ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (ga_ms['V (from SEDS)']), zorder=3)
# nbm=ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (nb_ms['V (from SEDS)']), zorder=3)
# otm=ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='red', marker="+", linewidth=1, s=s_fact / 2.5 ** (ot_ms['V (from SEDS)']),
#            edgecolor="grey")
# dgcm=ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
#            zorder=3, edgecolor="grey", linewidth=1)
# docm=ax.scatter(dup_oc_ms['RAJ2000'], dup_oc_ms['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (dup_oc_ms['V (from SEDS)']),
#            zorder=3, edgecolor="grey", linewidth=1)
# dgam=ax.scatter(dup_ga_ms['RAJ2000'], dup_ga_ms['DEJ2000'], color='red', marker="+",
#            s=s_fact / 2.5 ** (dup_ga_ms['V (from SEDS)']),
#            zorder=2)
# dnbm=ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),
#            zorder=3)
# dotm=ax.scatter(dup_ot_ms['RAJ2000'], dup_ot_ms['DEJ2000'], c='red', marker="+", edgecolor="grey", linewidth=1,
#            s=s_fact / 2.5 ** (dup_ot_ms['V (from SEDS)']))
# ax.scatter([0],[0], c='red', marker="+", edgecolor="grey", linewidth=1,
#            s=s_fact / 2.5 ** (1.6))
#
# ax.scatter(oc_ng['RAJ2000'], oc_ng['DEJ2000'], color='blue', marker="+", s=s_fact / 2.5 ** (oc_ng['V']), zorder=2,
#            edgecolor="grey", linewidth=.004 * oc_ng['V'])
# ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='blue', marker="+", s=s_fact / 2.5 ** (gc_ng['V']), zorder=2,
#            edgecolor="grey", linewidth=.004 * gc_ng['V'])
# ax.scatter(ga_ng['RAJ2000'], ga_ng['DEJ2000'], color='blue', marker="+", s=s_fact / 2.5 ** (ga_ng['V']), zorder=2)
# ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='blue', marker="+", s=s_fact / 2.5 ** (nb_ng['V']), zorder=2)
# ax.scatter(ot_ng['RAJ2000'], ot_ng['DEJ2000'], c='blue', marker="+", linewidth=1, s=s_fact / 2.5 ** (ot_ng['V']),
#            edgecolor="grey")
# ax.scatter(dup_oc_ng['RAJ2000'], dup_oc_ng['DEJ2000'], color='blue', marker="+", s=s_fact / 2.5 ** (dup_oc_ng['V']),
#            zorder=2, edgecolor="grey", linewidth=.004 * oc_ng['V'])
# ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='blue', marker="+", s=s_fact / 2.5 ** (dup_gc_ng['V']),
#            zorder=2, edgecolor="grey", linewidth=.004 * gc_ng['V'])
# ax.scatter(dup_ga_ng['RAJ2000'], dup_ga_ng['DEJ2000'], color='blue', marker="+",   s=s_fact / 2.5 ** (dup_ga_ng['V']),
#            zorder=2)
# ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='blue', marker="+", s=s_fact / 2.5 ** (dup_nb_ng['V']),
#            zorder=3)
# ax.scatter(dup_ot_ng['RAJ2000'], dup_ot_ng['DEJ2000'], c='blue', marker="+", edgecolor="grey", linewidth=1,
#            s=s_fact / 2.5 ** (dup_ot_ng['V']))


# scatter tycho, constellation borders
#
mt = ax.scatter(mag_ty['RAJ2000'], mag_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (mag_ty['V']), edgecolor="grey",
                linewidth=1/10)
mt.set_color = "yellow"

dt = ax.scatter(dup_ty['RAJ2000'], dup_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (dup_ty['V']), edgecolor="grey",
                linewidth=1/10)
ax.scatter(cb['RAJ2000'], cb['DEJ2000'], color='white', s=0.1, zorder=0)
ax.scatter(dup_cb['RAJ2000'], dup_cb['DEJ2000'], color='white', s=0.1, zorder=0)

# mplcursors.cursor(highlight=True)



#
# cst_names=cb['Constellation'].unique()
# cbcx=[]
# cbcy=[]
# for i in cst_names:
#     cbcx.append((cb[(cb['Constellation']==i)]['RAJ2000'].min()+cb[(cb['Constellation']==i)]['RAJ2000'].max())/2)
#     cbcy.append((cb[(cb['Constellation']==i)]['DEJ2000'].min()+cb[(cb['Constellation']==i)]['DEJ2000'].max())/2)
# dup_cbcx=np.array(cbcx)-360
#
# for i, txt in enumerate(cst_names):
#     p=ax.annotate(txt, (cbcx[i], cbcy[i]), xytext=(0, 0), textcoords='offset points', horizontalalignment='center', verticalalignment='center', fontsize=7)
# for i, txt in enumerate(cst_names):
#     p=ax.annotate(txt, (dup_cbcx[i], cbcy[i]), xytext=(0, 0), textcoords='offset points', horizontalalignment='center', verticalalignment='center', fontsize=7)


# axcolor = 'lightgoldenrodyellow'
# axfontsi = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
#
# sfontsi = Slider(axfontsi, 'Constellation Name Size', 0, 100, valinit=5, valstep=5)
#
# def update(val):
#     fontsi = sfontsi.val
#     for i, txt in enumerate(cst_names):
#         ax.annotate(txt, (cbcx[i], cbcy[i]), xytext=(0, 0), textcoords='offset points', horizontalalignment='center', verticalalignment='center', fontsize=fontsi)
#     print()
#     plt.draw()
#
# sfontsi.on_changed(update)
#
# resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
# button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
#
# def reset(event):
#     sfontsi.reset()
# button.on_clicked(reset)
#

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

count = 1
#############################################################################################################################################################
# text box for ra, dec or messier number
posbox = plt.axes([0.5, 0.9, 0.2, 0.04])
# si = plt.axes([0.5, 0.7, 0.2, 0.04    ])
text_box1 = TextBox(posbox, '<RA DEC FoV> or <messierNumber FoV> or <commonNameOfMessier>:')
# text_box2 = TextBox(si, '<RA DEC FoV> or <messierNumber FoV>:')
def pos(text):
    lst = text_box1.text.split()

    if len(lst) == 3 and int(lst[0]) >= 0 and int(lst[0]) < 360 and int(lst[1]) >= -90 and int(lst[1]) <= 90:
        ra = int(lst[0])
        dec = int(lst[1])
        fov = int(lst[2])
        xl = ra - fov / 2 - fov / 10
        xr = ra + fov / 2 + fov / 10
        yb = dec - fov / 2 - fov / 10
        yt = dec + fov / 2 + fov / 10

        if xr > 360:
            ra -= 360
            xr -= 360
            xl -= 360

        ax.set_xlim([xl, xr])
        ax.set_ylim([yb, yt])
        # ax.add_artist(plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.01))
        # plt.draw()
    elif len(lst) == 2 and int(lst[0]) > 0 and int(lst[0]) <= 110 and int(lst[1]) > 0:
        num = int(lst[0])
        fov = float(lst[1])
        ra = float(ms.iloc[[num - 1]]['RAJ2000'])
        dec = float(ms.iloc[[num - 1]]['DEJ2000'])
        xl = ra - fov / 2 - fov / 10
        xr = ra + fov / 2 + fov / 10
        yb = dec - fov / 2 - fov / 10
        yt = dec + fov / 2 + fov / 10

        if xr > 360:
            ra -= 360
            xr -= 360
            xl -= 360

        ax.set_xlim([xl, xr])
        ax.set_ylim([yb, yt])
        # ax.add_artist(plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.1))
    elif all([x.isalpha() for x in lst]):
        text = text.title()
        find_res = np.array([x.find(text) for x in name])
        pos = np.where(find_res != -1)[0]
        if len(pos) == 0:
            mb.showinfo('alert', 'Bad things happened!')
        else:
            ra, dec = df['RAJ2000'][pos].values, df['DEJ2000'][pos].values
            # print(name[pos], ra, dec)
            fov = 5
            xl = ra - fov / 2 - fov / 10
            xr = ra + fov / 2 + fov / 10
            yb = dec - fov / 2 - fov / 10
            yt = dec + fov / 2 + fov / 10

            if xr > 360:
                ra -= 360
                xr -= 360
                xl -= 360

            ax.set_xlim([xl, xr])
            ax.set_ylim([yb, yt])

    elif all([x.isalnum() for x in lst]):
        text = text.title()
        text = re.split('(\d+)', text)
        text[0] = text[0].rstrip()
        text = text[:2]
        text = ' '.join(text)
        find_res = np.array([x.find(text) for x in ident])
        pos = np.where(find_res != -1)[0]
        if len(pos) == 0:
            mb.showinfo('alert', 'Bad things happened!')
        else:
            ra, dec = df['RAJ2000'][pos].values, df['DEJ2000'][pos].values
            fov = 5
            xl = ra - fov / 2 - fov / 10
            xr = ra + fov / 2 + fov / 10
            yb = dec - fov / 2 - fov / 10
            yt = dec + fov / 2 + fov / 10

            if xr > 360:
                ra -= 360
                xr -= 360
                xl -= 360

            ax.set_xlim([xl, xr])
            ax.set_ylim([yb, yt])

    else:
        mb.showinfo('alert', 'Bad things happened!')
    # s_fact = int(text_box2.text)
    # ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o",
    #            s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
    #            zorder=4,
    #            edgecolor="grey", linewidth=.004 * oc_ms['V (from SEDS)'])
    # ax.draw()
    fig.canvas.draw()

    # global count
    # plt.savefig("file{}.png".format(count) , dpi=400)
    # count+=1
    mb.showinfo('Processed', "Ok to close")


text_box1.on_submit(pos)
# text_box2.on_submit(pos)

#
resetax = plt.axes([0.7 + 0.1, 0.9, 0.05, 0.04])
button = Button(resetax, 'Reset', color='yellow', hovercolor='0.975')


def reset(event):
    xl = 0
    xr = 260+100
    yb = -90
    yt = 90
    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])
    plt.draw()
    text_box1.set_val(" ")
button.on_clicked(reset)
#############################################################################################################################################################


# def sizz(text):
#     s_fact = int(text)
#     ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='yellow', marker="o",
#                s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
#                zorder=2,
#                edgecolor="grey", linewidth=.004 * oc_ms['V (from SEDS)'])
#     plt.draw()
#
#


#############################################################################################################################################################

# axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor='yellow')
# samp = Slider(axamp, 'Amp', 100, 100000, valinit=10000)
# def update(val):
#     s_fact=samp.val
#     print(s_fact)
#
#     ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o",
#                s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']), zorder=2,
#                edgecolor="grey", linewidth=.004 * oc_ms['V (from SEDS)'])
#     ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='black', marker="+",
#                s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']), zorder=3,
#                edgecolor="grey", linewidth=.004 * gc_ms['V (from SEDS)'])
#     ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='yellow', marker="o",
#                s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']), zorder=2,
#                edgecolor="grey", linewidth=.004 * gc_ms['V (from SEDS)'])
#     ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ms['V (from SEDS)']),
#                zorder=2)
#     ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='green', marker="o",
#                s=s_fact / 2.5 ** (nb_ms['V (from SEDS)']), zorder=3)
#     ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='black', marker="+",
#                s=s_fact * 10 / 2.5 ** (nb_ms['V (from SEDS)']), zorder=2)
#     ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='red', marker="+", linewidth=1,
#                s=s_fact / 2.5 ** (ot_ms['V (from SEDS)']),
#                edgecolor="grey")
#     ax.scatter(dup_oc_ms['RAJ2000'], dup_oc_ms['DEJ2000'], color='yellow', marker="o",
#                s=s_fact / 2.5 ** (dup_oc_ms['V (from SEDS)']),
#                zorder=2, edgecolor="grey", linewidth=.004 * oc_ms['V (from SEDS)'])
#     ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='black', marker="+",
#                s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
#                zorder=3, edgecolor="grey", linewidth=.004 * gc_ms['V (from SEDS)'])
#     ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='yellow', marker="o",
#                s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
#                zorder=2, edgecolor="grey", linewidth=.004 * gc_ms['V (from SEDS)'])
#     ax.scatter(dup_ga_ms['RAJ2000'], dup_ga_ms['DEJ2000'], color='red', marker=ell,
#                s=s_fact / 2.5 ** (dup_ga_ms['V (from SEDS)']),
#                zorder=2)
#     ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='green', marker="o",
#                s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),
#                zorder=3)
#     ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='black', marker="+",
#                s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),
#                zorder=2)
#     ax.scatter(dup_ot_ms['RAJ2000'], dup_ot_ms['DEJ2000'], c='red', marker="+", edgecolor="grey", linewidth=1,
#                s=s_fact / 2.5 ** (dup_ot_ms['V (from SEDS)']))
#     fig.canvas.draw_idle()
#
# samp.on_changed(update)

#############################################################################################################################################################


#############################################################################################################################################################
# work in progress
try:
    hop_file = open("hop.pkl", "rb")
    d = pickle.load(hop_file)
except:
    d={}


print(d)

count = 1
def onclick(event):
    # global xi, yi
    global d
    global l
    global count
    xi, yi = event.xdata, event.ydata

    if 'x{}'.format(count) in d.keys():
        if len(d['x{}'.format(count)]) >=1:
            if d['x{}'.format(count)][-1][0] == xi:
                fig.canvas.mpl_disconnect(cid)
                print("Hops for M{} created".format(count))
                count += 1


    try:
        l.append([xi, yi])
        d['x{}'.format(count)] = l
    except:
        l=[]
        d['x{}'.format(count)] = []
        print("Hop started:")
    # d[ms[(ms['RAJ2000'])==l[0]]['ID (for resolver)']].append([xi,yi])

    print(d)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

resetax = plt.axes([0.7 + 0.1, 0.1, 0.05, 0.04])
hopbutton = Button(resetax, 'Hop', color='yellow', hovercolor='0.975')

def hop(event):
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

hopbutton.on_clicked(hop)

# plt.gcf().text(0.02, 0.5, "ell", fontsize=14)


#############################################################################################################################################################
# plt.savefig("file4.png", dpi=400)
#
# mpld3.show()
plt.show()

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

root.mainloop()

