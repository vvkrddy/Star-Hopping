
from tkinter import *
import pickle
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import numpy as np
from svgpath2mpl import parse_path
import pandas as pd
import tkinter.font as font
import mplcursors
import tkinter.messagebox as mb
import scipy.spatial
import re
from tkinter import simpledialog
from scipy import spatial


###############################################################################################################################################################

ng = pd.read_csv('NGC.csv', low_memory=False)
ms = pd.read_csv('messier_objects.csv', low_memory=False)
cb = pd.read_csv('constellation_borders.csv', low_memory=False)
ty = pd.read_csv('tycho-1.csv', low_memory=False)

ell = parse_path(
    """M 490.60742,303.18917 A 276.31408,119.52378 28.9 0 1 190.94051,274.29027 276.31408,119.52378 28.9 0 1 6.8010582,36.113705 276.31408,119.52378 28.9 0 1 306.46799,65.012613 276.31408,119.52378 28.9 0 1 490.60742,303.18917 Z""")
ell.vertices -= ell.vertices.mean(axis=0)



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
gc_ms = ms[(ms["Type"] == 'GlC')]
gc_ng = ng[(ng["Type"] == 'GlC')]
# open clusters
oc_ms = ms[(ms["Type"] == 'OpC') | (ms["Type"] == 'Cl*')]
oc_ng = ng[(ng["Type"] == 'OpC') | (ng["Type"] == 'C+N')]
# galaxies
ga_ms = ms[(ms["Type"] == 'G') | (ms["Type"] == 'Sy2') | (ms["Type"] == 'IG') | (ms["Type"] == 'GiG') | (
        ms["Type"] == 'GiP') | (ms["Type"] == 'SyG') | (ms["Type"] == 'SBG') | (ms["Type"] == 'BiC') | (
                   ms["Type"] == 'H2G')]
ga_ng = ng[(ng["Type"] == 'Gal')]
# nebula and supernova remnant
nb_ms = ms[(ms["Type"] == 'PN') | (ms["Type"] == 'RNe') | (ms["Type"] == 'HII') | (ms["Type"] == 'SNR')]
nb_ng = ng[(ng["Type"] == 'PN') | (ng["Type"] == 'Nb') | (ng["Type"] == 'Kt')]
# other messiers
ot_ms = ms[(ms["Type"] == 'HII') | (ms["Type"] == 'As*') | (ms["Type"] == 'LIN') | (ms["Type"] == 'mul') | (
        ms["Type"] == 'AGN') | (ms["Type"] == 'SNR')]
# other ngc; stars
ot_ng = ng[(ng["Type"] == 'D+?') | (ng["Type"] == 'C+N') | (ng["Type"] == 'Kt') | (
        ng["Type"] == '*?') | (ng["Type"] == 'Ast') | (ng["Type"] == 'Str')]

# duplicated data sort by object type
# globular clusters
dup_gc_ms = dup_ms[(dup_ms["Type"] == 'GlC')]
dup_gc_ng = dup_ng[(dup_ng["Type"] == 'GlC')]
# open clusters
dup_oc_ms = dup_ms[(dup_ms["Type"] == 'OpC') | (dup_ms["Type"] == 'Cl*')]
dup_oc_ng = dup_ng[(dup_ng["Type"] == 'OpC') | (dup_ng["Type"] == 'C+N')]
# galaxies
dup_ga_ms = dup_ms[
    (dup_ms["Type"] == 'G') | (dup_ms["Type"] == 'Sy2') | (dup_ms["Type"] == 'IG') | (dup_ms["Type"] == 'GiG') | (
            dup_ms["Type"] == 'GiP') | (dup_ms["Type"] == 'SyG') | (dup_ms["Type"] == 'SBG') | (
            dup_ms["Type"] == 'BiC') | (
            dup_ms["Type"] == 'H2G')]
dup_ga_ng = dup_ng[(dup_ng["Type"] == 'Gal')]
# nebula and supernova remnant
dup_nb_ms = dup_ms[
    (dup_ms["Type"] == 'PN') | (dup_ms["Type"] == 'RNe') | (dup_ms["Type"] == 'HII') | (dup_ms["Type"] == 'SNR')]
dup_nb_ng = dup_ng[(dup_ng["Type"] == 'PN') | (dup_ng["Type"] == 'Nb') | (dup_ng["Type"] == 'Kt')]
# other messiers
dup_ot_ms = dup_ms[
    (dup_ms["Type"] == 'HII') | (dup_ms["Type"] == 'As*') | (dup_ms["Type"] == 'LIN') | (dup_ms["Type"] == 'mul') | (
            dup_ms["Type"] == 'AGN') | (dup_ms["Type"] == 'SNR')]
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

# order by the mag value
gc_ms.sort_values(by=['V (from SEDS)'], inplace=True)
gc_ng.sort_values(by=['V'], inplace=True)
oc_ms.sort_values(by=['V (from SEDS)'], inplace=True)
oc_ng.sort_values(by=['V'], inplace=True)
ga_ms.sort_values(by=['V (from SEDS)'], inplace=True)
ga_ng.sort_values(by=['V'], inplace=True)
nb_ms.sort_values(by=['V (from SEDS)'], inplace=True)
nb_ng.sort_values(by=['V'], inplace=True)
ot_ms.sort_values(by=['V (from SEDS)'], inplace=True)
ot_ng.sort_values(by=['V'], inplace=True)

dup_gc_ms.sort_values(by=['V (from SEDS)'], inplace=True)
dup_gc_ng.sort_values(by=['V'], inplace=True)
dup_oc_ms.sort_values(by=['V (from SEDS)'], inplace=True)
dup_oc_ng.sort_values(by=['V'], inplace=True)
dup_ga_ms.sort_values(by=['V (from SEDS)'], inplace=True)
dup_ga_ng.sort_values(by=['V'], inplace=True)
dup_nb_ms.sort_values(by=['V (from SEDS)'], inplace=True)
dup_nb_ng.sort_values(by=['V'], inplace=True)
dup_ot_ms.sort_values(by=['V (from SEDS)'], inplace=True)
dup_ot_ng.sort_values(by=['V'], inplace=True)

mag_ty.sort_values(by=['V'], inplace=True)
dup_ty.sort_values(by=['V'], inplace=True)

tynames=ty[ty['Name']!='-']

#############################################################################################################################################################

# tkinter
root = Tk()
root.wm_title("Editor _ Star Hopping")
root.configure(bg='black')
root.geometry("1000x600+400+400")

mainframe = Frame(root, relief=RAISED, borderwidth=1)
mainframe.place( relx = 0, rely = .1, relwidth=1, relheight=0.9)
widgetframe = Frame(root, padx=1, pady=1)
widgetframe.place( relx = 0.0, y = 0, relwidth=1, relheight=0.1)

#########################################################################################https://opensource.com/article/18/5/how-kill-process-stop-program-linux#:~:text=Simply%20execute%20xkill%20in%20a,window%20you%20want%20to%20close.####################################################################

# axis limits for opening plot
xr = 290 + 70
xl = 0
yb = -90
yt = 90

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.set_aspect(1)
axbgcl="grey" # axis background color
fig.patch.set_facecolor('slategrey')
ax.set_facecolor('gainsboro')
ax.set_axisbelow(True)
ax.minorticks_on()
ax.grid(which='major', color="#838383", zorder=0, alpha=.4)
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black', zorder=0, alpha=0.2)

ts_fact = 100
s_fact = 1000 # messiers and ngcs are exaggerated in size

ax.set_xlim([xl, xr])
ax.set_ylim([yb, yt])


def chart():

    # plots with +; 6+6
    # plots with ell; 2+2
    # plots with o; 6+6
    # plots 14+14+2+2

    plt.xlabel('Right Ascension (degrees)', fontsize=12)
    plt.ylabel('Declination (degrees)', fontsize=12)


    lw = 0
    plw = 1



    ocms = ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
               edgecolor=axbgcl, picker=1, linewidth = lw)
    # abc.set_visible(False)
    gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
               zorder=2, edgecolor=axbgcl, linewidth=plw)
    gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
               edgecolor="grey",  linewidth=lw, picker=1)
    gams = ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ms['V (from SEDS)']),
               picker=1, linewidth = lw, edgecolor=axbgcl)
    nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (nb_ms['V (from SEDS)']),
               edgecolor=axbgcl, zorder=2, picker=1, linewidth = lw)
    nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='black', marker="+",
               s=s_fact * 10 / 2.5 ** (nb_ms['V (from SEDS)']), edgecolor=axbgcl, linewidth=plw, picker=1)
    otms = ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='purple', marker="+",
               s=s_fact / 2.5 ** (ot_ms['V (from SEDS)']),
               edgecolor=axbgcl, linewidth=plw, picker=1)



    docms = ax.scatter(dup_oc_ms['RAJ2000'], dup_oc_ms['DEJ2000'], color='yellow', marker="o",
               s=s_fact / 2.5 ** (dup_oc_ms['V (from SEDS)']), edgecolor=axbgcl, picker=1, linewidth = lw)
    dgcms = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='black', marker="+",
               s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
               zorder=2, edgecolor=axbgcl, linewidth=plw, picker=1)
    dgcms = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='yellow', marker="o",
               s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']), edgecolor="grey", linewidth=lw, picker=1)
    dgams = ax.scatter(dup_ga_ms['RAJ2000'], dup_ga_ms['DEJ2000'], color='red', marker=ell,
               s=s_fact / 2.5 ** (dup_ga_ms['V (from SEDS)']), linewidth = lw,
               picker=1)
    dnbms = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='green', marker="o",
               s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),edgecolor=axbgcl,
               zorder=2, picker=1, linewidth = lw)
    dnbms = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='black', marker="+",
               s=s_fact * 10 / 2.5 ** (dup_nb_ms['V (from SEDS)']), edgecolor=axbgcl,
               picker=1, linewidth =  plw)
    dotms = ax.scatter(dup_ot_ms['RAJ2000'], dup_ot_ms['DEJ2000'], c='purple', marker="+",
               s=s_fact / 2.5 ** (dup_ot_ms['V (from SEDS)']), edgecolor=axbgcl, linewidth=plw,picker=1)


    ty = ax.scatter(mag_ty['RAJ2000'], mag_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (mag_ty['V']), edgecolor=axbgcl,
                    linewidth=1/10, zorder=2)
    dty = ax.scatter(dup_ty['RAJ2000'], dup_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (dup_ty['V']), edgecolor=axbgcl,
                    linewidth=1/10, zorder=2)

    ax.scatter(cb['RAJ2000'], cb['DEJ2000'], color='white', s=0.1, zorder=0)
    ax.scatter(dup_cb['RAJ2000'], dup_cb['DEJ2000'], color='white', s=0.1, zorder=0)



    # plt.savefig('6', dpi=400, format="png")


    # m=np.arange(1,20,1)
    # x=np.ones(19)*150
    # y=np.zeros(19)
    # ax.scatter(x,y,s=10000/2.5**m[::-1], edgecolor=axbgcl)


    #
    #
    #
    # ocng = ax.scatter(oc_ng['RAJ2000'], oc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (oc_ng['V']), zorder=2,
    #            edgecolor=axbgcl)
    # gcng = ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ng['V']), zorder=3,
    #            edgecolor=axbgcl)
    # gcng = ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (gc_ng['V']), zorder=2,
    #            edgecolor="grey")
    # gang = ax.scatter(ga_ng['RAJ2000'], ga_ng['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ng['V']), zorder=2)
    # nbng = ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (nb_ng['V']), zorder=3, edgecolor=axbgcl)
    # nbng = ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='black', marker="+", s=s_fact * 10 / 2.5 ** (nb_ng['V']), zorder=2)
    # otng = ax.scatter(ot_ng['RAJ2000'], ot_ng['DEJ2000'], c='blue', marker="+",
    #            edgecolor=axbgcl)
    #
    #
    #
    # docng = ax.scatter(dup_oc_ng['RAJ2000'], dup_oc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_oc_ng['V']),
    #            zorder=2, edgecolor=axbgcl)
    # dgcng = ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (dup_gc_ng['V']),
    #            zorder=3, edgecolor=axbgcl)
    # dgcng = ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_gc_ng['V']),
    #            zorder=2, edgecolor="grey")
    # dgang = ax.scatter(dup_ga_ng['RAJ2000'], dup_ga_ng['DEJ2000'], color='red', marker=ell,   s=s_fact / 2.5 ** (dup_ga_ng['V']))
    # dnbng = ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (dup_nb_ng['V']),
    #            zorder=3, edgecolor=axbgcl)
    # dnbng = ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='black', marker="+", s=s_fact * 10 / 2.5 ** (dup_nb_ng['V']),
    #            zorder=2, edgecolor=axbgcl)
    # dotng = ax.scatter(dup_ot_ng['RAJ2000'], dup_ot_ng['DEJ2000'], c='blue', marker="+", edgecolor=axbgcl,
    #            s=s_fact / 2.5 ** (dup_ot_ng['V']))
    # ocms = ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="+", s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
    #            zorder=2,
    #            edgecolor=axbgcl, picker=1)
    # gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
    #            zorder=3, edgecolor=axbgcl, linewidth=1,picker=1)
    # gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='yellow', marker="+", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
    #            zorder=2,
    #            edgecolor="grey",  linewidth=1, picker=1)
    # gams = ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ms['V (from SEDS)']),
    #            zorder=2, picker=1)
    # nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='green', marker="+", s=s_fact / 2.5 ** (nb_ms['V (from SEDS)']),
    #            edgecolor=axbgcl, zorder=3, picker=1)
    # nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='black', marker="+",
    #            s=s_fact * 10 / 2.5 ** (nb_ms['V (from SEDS)']), edgecolor=axbgcl, linewidth=1, zorder=2, picker=1)
    # otms = ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='purple', marker="+",
    #            s=s_fact / 2.5 ** (ot_ms['V (from SEDS)']),
    #            edgecolor=axbgcl, linewidth=1, picker=1)
    #
    #
    #
    # docms = ax.scatter(dup_oc_ms['RAJ2000'], dup_oc_ms['DEJ2000'], color='yellow', marker="+",
    #            s=s_fact / 2.5 ** (dup_oc_ms['V (from SEDS)']),
    #            zorder=2, edgecolor=axbgcl, picker=1)
    # dgcms = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='black', marker="+",
    #            s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
    #            zorder=3, edgecolor=axbgcl, linewidth=1, picker=1)
    # dgcms = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='yellow', marker="+",
    #            s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
    #            zorder=2, edgecolor="grey", linewidth=1, picker=1)
    # dgams = ax.scatter(dup_ga_ms['RAJ2000'], dup_ga_ms['DEJ2000'], color='red', marker="+",
    #            s=s_fact / 2.5 ** (dup_ga_ms['V (from SEDS)']),
    #            zorder=2, picker=1)
    # dnbms = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='green', marker="+",
    #            s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),edgecolor=axbgcl,
    #            zorder=3, picker=1)
    # dnbms = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='black', marker="+",
    #            s=s_fact * 10 / 2.5 ** (dup_nb_ms['V (from SEDS)']), edgecolor=axbgcl, linewidth=1,
    #            zorder=2, picker=1)
    # dotms = ax.scatter(dup_ot_ms['RAJ2000'], dup_ot_ms['DEJ2000'], c='purple', marker="+",
    #            s=s_fact / 2.5 ** (dup_ot_ms['V (from SEDS)']), edgecolor=axbgcl, linewidth=1,picker=1)
    #
    #
    #
    # ocng = ax.scatter(oc_ng['RAJ2000'], oc_ng['DEJ2000'], color='yellow', marker="+", s=s_fact / 2.5 ** (oc_ng['V']), zorder=2,
    #            edgecolor=axbgcl)
    # gcng = ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ng['V']), zorder=3,
    #            edgecolor=axbgcl, linewidth=1)
    # gcng = ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='yellow', marker="+", s=s_fact / 2.5 ** (gc_ng['V']), zorder=2,
    #            edgecolor="grey")
    # gang = ax.scatter(ga_ng['RAJ2000'], ga_ng['DEJ2000'], color='red', marker="+", s=s_fact / 2.5 ** (ga_ng['V']), zorder=2)
    # nbng = ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='green', marker="+", s=s_fact / 2.5 ** (nb_ng['V']), zorder=3, edgecolor=axbgcl)
    # nbng = ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='black', marker="+", s=s_fact * 10 / 2.5 ** (nb_ng['V']), zorder=2, linewidth=1)
    # otng = ax.scatter(ot_ng['RAJ2000'], ot_ng['DEJ2000'], c='blue', marker="+", linewidth=1, s=s_fact / 2.5 ** (ot_ng['V']),
    #            edgecolor=axbgcl)
    #
    #
    #
    # docng = ax.scatter(dup_oc_ng['RAJ2000'], dup_oc_ng['DEJ2000'], color='yellow', marker="+", s=s_fact / 2.5 ** (dup_oc_ng['V']),
    #            zorder=2, edgecolor=axbgcl)
    # dgcng = ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (dup_gc_ng['V']),
    #            zorder=3, edgecolor=axbgcl, linewidth=1)
    # dgcng = ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='yellow', marker="+", s=s_fact / 2.5 ** (dup_gc_ng['V']),
    #            zorder=2, edgecolor="grey")
    # dgang = ax.scatter(dup_ga_ng['RAJ2000'], dup_ga_ng['DEJ2000'], color='red', marker="+",   s=s_fact / 2.5 ** (dup_ga_ng['V']))
    # dnbng = ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='green', marker="+", s=s_fact / 2.5 ** (dup_nb_ng['V']),
    #            zorder=3, edgecolor=axbgcl)
    # dnbng = ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='black', marker="+", s=s_fact * 10 / 2.5 ** (dup_nb_ng['V']),
    #            zorder=2, linewidth=1, edgecolor=axbgcl)
    # dotng = ax.scatter(dup_ot_ng['RAJ2000'], dup_ot_ng['DEJ2000'], c='blue', marker="+", edgecolor=axbgcl, linewidth=1,
    #            s=s_fact / 2.5 ** (dup_ot_ng['V']))

chart()

# ts_fact = 100
# s_fact = 10000
# #
# ax.set_xlim([xl, xr])
# ax.set_ylim([yb, yt])
#
# ocms = ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
#            zorder=2,
#            edgecolor="grey", picker=1)
# gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
#            zorder=3, edgecolor="grey", linewidth=1,picker=1)
# gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
#            zorder=2,
#            edgecolor="grey",  linewidth=1, picker=1)
# gams = ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ms['V (from SEDS)']),
#            zorder=2, edgecolor="grey",  picker=1)
# nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (nb_ms['V (from SEDS)']),
#            edgecolor="grey", zorder=3, picker=1)
# nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='black', marker="+",
#            s=s_fact * 10 / 2.5 ** (nb_ms['V (from SEDS)']), edgecolor="grey", linewidth=1, zorder=2, picker=1)
# otms = ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='purple', marker="+",
#            s=s_fact / 2.5 ** (ot_ms['V (from SEDS)']),
#            edgecolor="grey", linewidth=1, picker=1)
# docms = ax.scatter(dup_oc_ms['RAJ2000'], dup_oc_ms['DEJ2000'], color='yellow', marker="o",
#            s=s_fact / 2.5 ** (dup_oc_ms['V (from SEDS)']),
#            zorder=2, edgecolor="grey", picker=1)
# dgcms = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='black', marker="+",
#            s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
#            zorder=3, edgecolor="grey", linewidth=1, picker=1)
# dgcms = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='yellow', marker="o",
#            s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
#            zorder=2, edgecolor="grey", linewidth=1, picker=1)
# dgams = ax.scatter(dup_ga_ms['RAJ2000'], dup_ga_ms['DEJ2000'], color='red', marker=ell,
#            s=s_fact / 2.5 ** (dup_ga_ms['V (from SEDS)']),
#            zorder=2,edgecolor="grey",  picker=1)
# dnbms = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='green', marker="o",
#            s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),edgecolor="grey",
#            zorder=3, picker=1)
# dnbms = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='black', marker="+",
#            s=s_fact * 10 / 2.5 ** (dup_nb_ms['V (from SEDS)']), edgecolor="grey", linewidth=1,
#            zorder=2, picker=1)
# dotms = ax.scatter(dup_ot_ms['RAJ2000'], dup_ot_ms['DEJ2000'], c='purple', marker="+",
#            s=s_fact / 2.5 ** (dup_ot_ms['V (from SEDS)']), edgecolor="grey", linewidth=1,picker=1)
#
# ocng = ax.scatter(oc_ng['RAJ2000'], oc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (oc_ng['V']), zorder=2,
#            edgecolor="grey")
# gcng = ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ng['V']), zorder=3,
#            edgecolor="grey", linewidth=1)
# gcng = ax.scatter(gc_ng['RAJ2000'], gc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (gc_ng['V']), zorder=2,
#            edgecolor="grey")
# gang = ax.scatter(ga_ng['RAJ2000'], ga_ng['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ng['V']), zorder=2)
# nbng = ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (nb_ng['V']), zorder=3, edgecolor="grey")
# nbng = ax.scatter(nb_ng['RAJ2000'], nb_ng['DEJ2000'], color='black', marker="+", s=s_fact * 10 / 2.5 ** (nb_ng['V']), zorder=2, linewidth=1)
# otng = ax.scatter(ot_ng['RAJ2000'], ot_ng['DEJ2000'], c='blue', marker="+", linewidth=1, s=s_fact / 2.5 ** (ot_ng['V']),
#            edgecolor="grey")
# docng = ax.scatter(dup_oc_ng['RAJ2000'], dup_oc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_oc_ng['V']),
#            zorder=2, edgecolor="grey")
# dgcng = ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (dup_gc_ng['V']),
#            zorder=3, edgecolor="grey", linewidth=1)
# dgcng = ax.scatter(dup_gc_ng['RAJ2000'], dup_gc_ng['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_gc_ng['V']),
#            zorder=2, edgecolor="grey")
# dgang = ax.scatter(dup_ga_ng['RAJ2000'], dup_ga_ng['DEJ2000'], color='red', marker=ell,   s=s_fact / 2.5 ** (dup_ga_ng['V']))
# dnbng = ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (dup_nb_ng['V']),
#            zorder=3, edgecolor="grey")
# dnbng = ax.scatter(dup_nb_ng['RAJ2000'], dup_nb_ng['DEJ2000'], color='black', marker="+", s=s_fact * 10 / 2.5 ** (dup_nb_ng['V']),
#            zorder=2, linewidth=1)
# dotng = ax.scatter(dup_ot_ng['RAJ2000'], dup_ot_ng['DEJ2000'], c='blue', marker="+", edgecolor="grey", linewidth=1,
#            s=s_fact / 2.5 ** (dup_ot_ng['V']))
#
# ty = ax.scatter(mag_ty['RAJ2000'], mag_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (mag_ty['V']), edgecolor="grey",
#                 linewidth=1/10)
# dty = ax.scatter(dup_ty['RAJ2000'], dup_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (dup_ty['V']), edgecolor="grey",
#                 linewidth=1/10)
# ax.scatter(cb['RAJ2000'], cb['DEJ2000'], color='white', s=0.1, zorder=0)
# ax.scatter(dup_cb['RAJ2000'], dup_cb['DEJ2000'], color='white', s=0.1, zorder=0)

#############################################################################################################################################################

canvas = FigureCanvasTkAgg(fig, master=mainframe)  # A DrawingArea.
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, mainframe)
toolbar.update()

canvas.get_tk_widget().place(relx=0.0, rely=0, relheight=.99-0.02, relwidth=1)

#############################################################################################################################################################


def resetchart():
    plt.cla()
    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])
    chart()
    plt.draw()
    object_entry.delete(0, END)

def submit():
    text = object_entry.get()
    lst = text.split()
    print(lst)

    if len(lst) == 3 and float(lst[0]) >= 0 and float(lst[0]) < 360 and float(lst[1]) >= -90 and float(lst[1]) <= 90:
        ra = int(lst[0])
        dec = int(lst[1])
        fov = int(lst[2])
        # ra1 = ra
        # dec1 = dec
        # fov1 = fov
        # circ = plt.Circle((ra1, dec1), fov1 / 2, color='#00af08', zorder=-1, alpha=0.1)
        # circ.remove()

        xl = ra - fov / 2 - fov / 10
        xr = ra + fov / 2 + fov / 10
        yb = dec - fov / 2 - fov / 10
        yt = dec + fov / 2 + fov / 10

        if xr > 360:
            ra -= 360
            xr -= 360
            xl -= 360
        plt.cla()
        ax.set_xlim([xl, xr])
        ax.set_ylim([yb, yt])
        # circ = plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.1)
        # print(circ)
        # ax.add_artist(circ)
        chart()
        plt.draw()
        mb.showinfo('Processed')

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

        plt.cla()
        ax.set_xlim([xl, xr])
        ax.set_ylim([yb, yt])
        # ax.add_artist(plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.1))
        chart()
        plt.draw()
        mb.showwarning('Processed', "Press ok to close")
    else:
        mb.showwarning('alert', 'Enter in degrees:\nRA DEC FoV\nOR\nmessierNumber FoV')

    # # s_fact = int(text_box2.text)
    # # ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o",
    # #            s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
    # #            zorder=4,
    # #            edgecolor="grey", linewidth=.004 * oc_ms['V (from SEDS)'])
    # # ax.draw()
#############################################################################################################################################################
try:
    hop_file = open("hop.pkl", "rb")
    d = pickle.load(hop_file)

except:
    d={}

print(d)

count = 1

tyx=np.array(ty['RAJ2000'])
tyy=np.array(ty['DEJ2000'])
# dtyx=np.array(dup_ty['RAJ2000'])
# dtyy=np.array(dup_ty['DEJ2000'])

tree = spatial.KDTree(list(zip(tyx,tyy)))

l=[]

dict_label = Label (mainframe, text ="--<Current Hops Displayed Here>--")
dict_label.pack(side=TOP,padx=0, pady=5
    )

# dict_label.attributes('-topmost', 'true')


def onclick(event):
    # if event.button == 1:
    # global xi, yi
    global d
    global l
    global count
    xin, yin = event.xdata, event.ydata
    print(xin,yin)

    points = np.array([xin,yin])
    dist,ind = tree.query(points, k=500)
    # print()
    # print([ty['V'][ind].idxmin()])
    # print(ind, ty['RAJ2000'][int([ty['V'][ind].idxmin()][0])])
    global markerobj

    objra = ty['RAJ2000'][int([ty['V'][ind].idxmin()][0])]
    objde = ty['DEJ2000'][int([ty['V'][ind].idxmin()][0])]
    markerobj = ax.scatter([objra],[objde], c='black', s=10000, marker='+')
    plt.draw()
    # if hopobj in d.keys():
    #     # if len(d[hopobj]) >=1:
    #     #     if d[hopobj] == xi:
    #             fig.canvas.mpl_disconnect(cid)
    #             print("Hops for {} created".format(hopobject))

    global hopobj

    try:
        l.append([objra, objde])
        d[hopobj] = l
    except:
        l=[]
        d[hopobj] = []
        print("Hop started:")
    # d[ms[(ms['RAJ2000'])==l[0]]['ID (for resolver)']].append([xi,yi])

    print(d)

    global dict_label
    # dict_label.destroy()
    dict_label.configure(text = "Hops for '{}' :{}".format(hopobj, d[hopobj]))

# def undohop():
#     print("yo")

# cid = fig.canvas.mpl_connect('button_press_event', onclick)


# def on_key_press(event):
#    if event.key == 'shift':
#        shift_is_held = True
#
# def on_key_release(event):
#    if event.key == 'shift':
#        shift_is_held = False
#
# fig.canvas.mpl_connect('key_press_event', on_key_press)
# fig.canvas.mpl_connect('key_release_event', on_key_release)

# def on_pick(event):
#     index=event.ind
#     print(index)



#############################################################################################################################################################

def hopstart():
    global dict_label
    global d
    global l
    global hopobj
    global cid

    if hop_btn['text'] == "CREATE HOP":
        print("ehlp")

        hop_btn.configure(text="FINISH HOP", bg='slategrey', fg='white')
        uh["state"] = "active"

        hopobj = simpledialog.askstring("Input", "Enter a messier number towards which you would hop to",
                                        parent=widgetframe)
        if not hopobj==None and not hopobj=='':

            messier = hopobj.capitalize()[0]+' '+hopobj.capitalize()[1:].strip()

            # validation and resolver
            while True:
                if not messier in ms['ID (for resolver)'].values:
                    hopobj = simpledialog.askstring("Input", "Enter a messier towards which you would hop to",
                                                    parent=widgetframe)
                    messier = hopobj.capitalize()[0] + ' ' + hopobj.capitalize()[1:].strip()
                else:
                    break

            hopobj = messier

            # dict_label.destroy()
            dict_label.configure(text="Hops for '{}' :".format(hopobj))

            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            print("hello")
        else:
            hop_btn.configure(text="CREATE HOP", bg='grey', fg='black')
            uh["state"] = "disabled"
            dict_label.configure(text="--<Current Hops Displayed Here>--")

    elif hop_btn['text'] == "FINISH HOP":
        hop_btn.configure(text="CREATE HOP", bg='grey', fg='black')
        uh["state"] = "disabled"
        fig.canvas.mpl_disconnect(cid)
        dict_label.configure(text ="--<Current Hops Displayed Here>--")

    print("Done")
    l = []


    pickle.dump(d, open("hop.pkl", "wb"))

    resetchart()

# def hopfinish():
#     fig.canvas.mpl_disconnect(cid)
#     print("Done")
#     global l
#     l=[]
#     global dict_label
#     dict_label.destroy()
#
#     global d
#
#     pickle.dump(d, open("hop.pkl", "wb"))
#
#     resetchart()



# def info():
#     mb.showinfo("Instructions:", "Enter:\nRA DEC FoV\n Messier Number\nCommon Name")



def undohop():
    global hopobj
    d[hopobj].pop()
    print(d)
    global markerobj
    markerobj.remove()
    chart()
    plt.draw()
    global dict_label
    # dict_label.destroy()
    dict_label.configure(text="Hops for '{}' :{}".format(hopobj, d[hopobj]))


# def resizex():
#     global s_fact
#     global ts_fact
#     s_fact = s_factx.get()
#     ts_fact = ts_factx.get()
#     plt.cla()
#     ax.set_xlim([xl, xr])
#     ax.set_ylim([yb, yt])
#     chart()
#     plt.draw()

#############################################################################################################################################################


object_label = Label ( widgetframe, text="Target" )
object_label.pack(side=LEFT,padx=0, pady=5
)

#
# target_info = Button(widgetframe,text="i",command = info, relief=RAISED)
# # target_info["border"]="0"
# target_info.pack(side=LEFT,padx=0, pady=5
# )
# myFont = font.Font(size=1)
# target_info['font'] = myFont

object_entry = Entry ( widgetframe, text="pos" )
object_entry.pack(side=LEFT,padx=0, pady=5
)

sub_btn=Button(widgetframe,text = 'Submit', command = submit)
sub_btn.pack(side=LEFT,padx=5, pady=5
)

hop_btn= Button ( widgetframe, text="CREATE HOP", command = hopstart)
hop_btn.pack(side=RIGHT,padx=5, pady=5
)

# fin_btn= Button ( widgetframe, text="FINISH HOP", command = hopfinish)
# fin_btn.pack(side=RIGHT,padx=5, pady=5
# )
uh=Button(widgetframe, text="UNDO HOP", command=undohop)
uh.pack(side=RIGHT,padx=5, pady=5
)
uh["state"] = "disabled"

# s_factx = Scale(widgetframe, from_=10000, to=20000)
# s_factx.set(10000)
# s_factx.pack(side=LEFT,padx=5, pady=5
# )
# ts_factx = Scale(widgetframe, from_=100, to=10000)
# ts_factx.set(100)
# ts_factx.pack(side=LEFT,padx=5, pady=5
# )
# subfact=Button ( widgetframe, text="resize", command = resizex)
# subfact.pack(side=LEFT,padx=5, pady=5
# )

rsc=Button(widgetframe, text="RESET CHART", command=resetchart)
rsc.pack(side=LEFT,padx=5, pady=5
)

# def xyh():
#     if xy.get()==1:
#         mplcursors.cursor(hover=True)
#     elif xy.get()==0:
#         mplcursors.cursor(hover=False)
# xy = IntVar()
# xyhover=Checkbutton(widgetframe, text='Hellow',variable=xy, onvalue=1, offvalue=0, command=xyh)
# xyhover.pack()

#############################################################################################################################################################

#############################################################################################################################################################

# def tycho1():
#     ts_fact = 100
#     xr = 290 + 70
#     xl = 0
#     yb = -90
#     yt = 90
#
#
#
#     plt.cla()
#
#     ax.scatter(mag_ty['RAJ2000'], mag_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (mag_ty['V']), edgecolor="grey",
#                linewidth=1 / 10)
#
#     ax.scatter(dup_ty['RAJ2000'], dup_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (dup_ty['V']), edgecolor="grey",
#                linewidth=1 / 10)
#     ax.scatter(cb['RAJ2000'], cb['DEJ2000'], color='white', s=0.1, zorder=0)
#     ax.scatter(dup_cb['RAJ2000'], dup_cb['DEJ2000'], color='white', s=0.1, zorder=0)
#     ax.set_xlim([xl, xr])
#     ax.set_ylim([yb, yt])
#     plt.draw()

# def toggle():
#     '''
#     use
#     t_btn.config('text')[-1]
#     to get the present state of the toggle button
#     '''
#     if tycho1_btn.config('relief')[-1] == SUNKEN:
#         tycho1_btn.config(relief=RAISED)
#         tycho1()
#         print("yo")
#     else:
#         tycho1_btn.config(relief=SUNKEN)
#         chart()
#         print("yo agia")

# tycho1_btn=Button ( root, text="Tycho", command = toggle, relief=SUNKEN )
# tycho1_btn.pack(side=RIGHT)


# object_label.grid(row=0, column=0)
# object_entry.grid(row=0, column=1)

#############################################################################################################################################################

# mplcursors.cursor(hover=True)


#############################################################################################################################################################



# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)
#
#
# canvas.mpl_connect("key_press_event", on_key_press)

#############################################################################################################################################################

# hover to get label
# annot1 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot1.set_visible(False)
#
# def update_annot1(ind):
#
#     pos = ocms.get_offsets()[ind["ind"][0]]
#     annot1.xy = pos
#     annot1.set_text(oc_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot1.get_bbox_patch().set_alpha(0.4)
#
# def hover1(event):
#     vis = annot1.get_visible()
#     if event.inaxes == ax:
#         cont, ind = ocms.contains(event)
#         if cont:
#             update_annot1(ind)
#             annot1.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot1.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot2 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot2.set_visible(False)
#
# def update_annot2(ind):
#
#     pos = gcms.get_offsets()[ind["ind"][0]]
#     annot2.xy = pos
#     annot2.set_text(gc_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot2.get_bbox_patch().set_alpha(0.4)
#
# def hover2(event):
#     vis = annot2.get_visible()
#     if event.inaxes == ax:
#         cont, ind = gcms.contains(event)
#         if cont:
#             update_annot2(ind)
#             annot2.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot2.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot3 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot3.set_visible(False)
#
# def update_annot3(ind):
#
#     pos = gams.get_offsets()[ind["ind"][0]]
#     annot3.xy = pos
#     annot3.set_text(ga_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot3.get_bbox_patch().set_alpha(0.4)
#
# def hover3(event):
#     vis = annot3.get_visible()
#     if event.inaxes == ax:
#         cont, ind = gams.contains(event)
#         if cont:
#             update_annot3(ind)
#             annot3.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot3.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot4 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot4.set_visible(False)
#
# def update_annot4(ind):
#
#     pos = nbms.get_offsets()[ind["ind"][0]]
#     annot4.xy = pos
#     annot4.set_text(nb_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot4.get_bbox_patch().set_alpha(0.4)
#
# def hover4(event):
#     vis = annot4.get_visible()
#     if event.inaxes == ax:
#         cont, ind = nbms.contains(event)
#         if cont:
#             update_annot4(ind)
#             annot4.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot4.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot5 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot5.set_visible(False)
#
# def update_annot5(ind):
#
#     pos = otms.get_offsets()[ind["ind"][0]]
#     annot5.xy = pos
#     annot5.set_text(ot_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot5.get_bbox_patch().set_alpha(0.4)
#
# def hover5(event):
#     vis = annot5.get_visible()
#     if event.inaxes == ax:
#         cont, ind = otms.contains(event)
#         if cont:
#             update_annot5(ind)
#             annot5.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot5.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot6 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot6.set_visible(False)
#
# def update_annot6(ind):
#
#     pos = docms.get_offsets()[ind["ind"][0]]
#     annot6.xy = pos
#     annot6.set_text(dup_oc_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot6.get_bbox_patch().set_alpha(0.4)
#
# def hover6(event):
#     vis = annot6.get_visible()
#     if event.inaxes == ax:
#         cont, ind = docms.contains(event)
#         if cont:
#             update_annot6(ind)
#             annot6.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot6.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot7 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot7.set_visible(False)
#
# def update_annot7(ind):
#
#     pos = dgcms.get_offsets()[ind["ind"][0]]
#     annot7.xy = pos
#     annot7.set_text(dup_gc_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot7.get_bbox_patch().set_alpha(0.4)
#
# def hover7(event):
#     vis = annot7.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dgcms.contains(event)
#         if cont:
#             update_annot7(ind)
#             annot7.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot7.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot8 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot8.set_visible(False)
#
# def update_annot8(ind):
#
#     pos = dgams.get_offsets()[ind["ind"][0]]
#     annot8.xy = pos
#     annot8.set_text(dup_ga_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot8.get_bbox_patch().set_alpha(0.4)
#
# def hover8(event):
#     vis = annot8.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dgams.contains(event)
#         if cont:
#             update_annot8(ind)
#             annot8.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot8.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot9 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot9.set_visible(False)
#
# def update_annot9(ind):
#
#     pos = dnbms.get_offsets()[ind["ind"][0]]
#     annot9.xy = pos
#     annot9.set_text(dup_nb_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot9.get_bbox_patch().set_alpha(0.4)
#
# def hover9(event):
#     vis = annot9.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dnbms.contains(event)
#         if cont:
#             update_annot9(ind)
#             annot9.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot9.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot10 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot10.set_visible(False)
#
# def update_annot10(ind):
#
#     pos = dotms.get_offsets()[ind["ind"][0]]
#     annot10.xy = pos(points)
#     annot10.set_text(dup_ot_ms.iloc[ind["ind"][0]]['Constellation'])
#     annot10.get_bbox_patch().set_alpha(0.4)
#
# def hover10(event):
#     vis = annot10.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dotms.contains(event)
#         if cont:
#             update_annot10(ind)
#             annot10.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot10.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot11 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot11.set_visible(False)
#
# def update_annot11(ind):
#
#     pos = ocng.get_offsets()[ind["ind"][0]]
#     annot11.xy = pos
#     annot11.set_text(oc_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot11.get_bbox_patch().set_alpha(0.4)
#
# def hover11(event):
#     vis = annot11.get_visible()
#     if event.inaxes == ax:
#         cont, ind = ocng.contains(event)
#         if cont:
#             update_annot11(ind)
#             annot11.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot11.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot12 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot12.set_visible(False)
#
# def update_annot12(ind):
#
#     pos = gcng.get_offsets()[ind["ind"][0]]
#     annot12.xy = pos
#     annot12.set_text(gc_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot12.get_bbox_patch().set_alpha(0.4)
#
# def hover12(event):
#     vis = annot12.get_visible()
#     if event.inaxes == ax:
#         cont, ind = gcng.contains(event)
#         if cont:
#             update_annot12(ind)
#             annot12.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot12.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot13 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot13.set_visible(False)
#
# def update_annot13(ind):
#
#     pos = gang.get_offsets()[ind["ind"][0]]
#     annot13.xy = pos
#     annot13.set_text(ga_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot13.get_bbox_patch().set_alpha(0.4)
#
# def hover13(event):
#     vis = annot13.get_visible()
#     if event.inaxes == ax:
#         cont, ind = gang.contains(event)
#         if cont:
#             update_annot13(ind)
#             annot13.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot13.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot14 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot14.set_visible(False)
#
# def update_annot14(ind):
#
#     pos = nbng.get_offsets()[ind["ind"][0]]
#     annot14.xy = pos
#     annot14.set_text(nb_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot14.get_bbox_patch().set_alpha(0.4)
#
# def hover14(event):
#     vis = annot14.get_visible()
#     if event.inaxes == ax:
#         cont, ind = nbng.contains(event)
#         if cont:
#             update_annot14(ind)
#             annot14.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot14.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot15 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot15.set_visible(False)
#
# def update_annot15(ind):
#
#     pos = otng.get_offsets()[ind["ind"][0]]
#     annot15.xy = pos
#     annot15.set_text(ot_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot15.get_bbox_patch().set_alpha(0.4)
#
# def hover15(event):
#     vis = annot15.get_visible()
#     if event.inaxes == ax:
#         cont, ind = otng.contains(event)
#         if cont:
#             update_annot15(ind)
#             annot15.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot15.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot16 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot16.set_visible(False)
#
# def update_annot16(ind):
#
#     pos = docng.get_offsets()[ind["ind"][0]]
#     annot16.xy = pos
#     annot16.set_text(dup_oc_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot16.get_bbox_patch().set_alpha(0.4)
#
# def hover16(event):
#     vis = annot16.get_visible()
#     if event.inaxes == ax:
#         cont, ind = docng.contains(event)
#         if cont:
#             update_annot16(ind)
#             annot16.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot16.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot17 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot17.set_visible(False)
#
# def update_annot17(ind):
#
#     pos = dgcng.get_offsets()[ind["ind"][0]]
#     annot17.xy = pos
#     annot17.set_text(dup_gc_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot17.get_bbox_patch().set_alpha(0.4)
#
# def hover17(event):
#     vis = annot17.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dgcng.contains(event)
#         if cont:
#             update_annot17(ind)
#             annot17.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot17.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot18 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot18.set_visible(False)
#
# def update_annot18(ind):
#
#     pos = dgang.get_offsets()[ind["ind"][0]]
#     annot18.xy = pos
#     annot18.set_text(dup_ga_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot18.get_bbox_patch().set_alpha(0.4)
#
# def hover18(event):
#     vis = annot18.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dgang.contains(event)
#         if cont:
#             update_annot18(ind)
#             annot18.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot18.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot19 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot19.set_visible(False)
#
# def update_annot19(ind):
#
#     pos = dnbng.get_offsets()[ind["ind"][0]]
#     annot19.xy = pos
#     annot19.set_text(dup_nb_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot19.get_bbox_patch().set_alpha(0.4)
#
# def hover19(event):
#     vis = annot19.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dnbng.contains(event)
#         if cont:
#             update_annot19(ind)
#             annot19.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot19.set_visible(False)
#                 fig.canvas.draw_idle()
#
# annot20 = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot20.set_visible(False)
#
# def update_annot20(ind):
#
#     pos = dotng.get_offsets()[ind["ind"][0]]
#     annot20.xy = pos
#     annot20.set_text(dup_ot_ng.iloc[ind["ind"][0]]['Constellation'])
#     annot20.get_bbox_patch().set_alpha(0.4)
#
# def hover20(event):
#     vis = annot20.get_visible()
#     if event.inaxes == ax:
#         cont, ind = dotng.contains(event)
#         if cont:
#             update_annot20(ind)
#             annot20.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot20.set_visible(False)
#                 fig.canvas.draw_idle()
#
#
# canvas.mpl_connect("motion_notify_event", hover1)
# canvas.mpl_connect("motion_notify_event", hover2)
# canvas.mpl_connect("motion_notify_event", hover3)
# canvas.mpl_connect("motion_notify_event", hover4)
# canvas.mpl_connect("motion_notify_event", hover5)
# canvas.mpl_connect("motion_notify_event", hover6)
# canvas.mpl_connect("motion_notify_event", hover7)
# canvas.mpl_connect("motion_notify_event", hover8)
# canvas.mpl_connect("motion_notify_event", hover9)
# canvas.mpl_connect("motion_notify_event", hover10)
# canvas.mpl_connect("motion_notify_event", hover11)
# canvas.mpl_connect("motion_notify_event", hover12)
# canvas.mpl_connect("motion_notify_event", hover13)
# canvas.mpl_connect("motion_notify_event", hover14)
# canvas.mpl_connect("motion_notify_event", hover15)
# canvas.mpl_connect("motion_notify_event", hover16)
# canvas.mpl_connect("motion_notify_event", hover17)
# canvas.mpl_connect("motion_notify_event", hover18)
# canvas.mpl_connect("motion_notify_event", hover19)
# canvas.mpl_connect("motion_notify_event", hover20)
#



#############################################################################################################################################################

# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)

mainloop()
# plt.savefig(6,dpi=400, format="png")
