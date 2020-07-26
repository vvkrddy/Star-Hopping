
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

hmag = 20 # limiting magnitude for messiers; here all messiers will be plotted; recommended not to change
mag = 6 # limiting magnitude for Tycho-1 stars;

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
ot_ms = ms[(ms["Type"] == 'As*') | (ms["Type"] == 'LIN') | (ms["Type"] == 'mul') | (
        ms["Type"] == 'AGN')]
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
    ( (dup_ms["Type"] == 'As*') | (dup_ms["Type"] == 'LIN') | (dup_ms["Type"] == 'mul') | (dup_ms["Type"] == 'AGN')) ]
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


# reset index
gc_ms = gc_ms.reset_index(drop=True)
oc_ms = oc_ms.reset_index(drop=True)
ga_ms = ga_ms.reset_index(drop=True)
nb_ms = nb_ms.reset_index(drop=True)
ot_ms = ot_ms.reset_index(drop=True)

# ty_names=ty[(ty['Name']!='-')]
# ty_bayer=ty.dropna(subset=['Bayer'])

# full_ty = pd.concat([mag_ty,dup_ty], axis=0)
# full_ty.reset_index(drop=True)

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

mb.showwarning('Editor_GUI', "Full Screen Recommended")

#############################################################################################################################################################

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

ts_fact = 250
s_fact = 250

ax.set_xlim([xl, xr])
ax.set_ylim([yb, yt])

canvas = FigureCanvasTkAgg(fig, master=mainframe)  # A DrawingArea.
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, mainframe)
toolbar.update()

canvas.get_tk_widget().place(relx=0.0, rely=0, relheight=.99-0.02, relwidth=1)

#

#

def chart():

    # plots with +; 6+6
    # plots with ell; 2+2
    # plots with o; 6+6
    # plots 14+14+2+2

    plt.xlabel('Right Ascension (degrees)', fontsize=12)
    plt.ylabel('Declination (degrees)', fontsize=12)

    lw = 0
    plw = 1

    ax.scatter(cb['RAJ2000'], cb['DEJ2000'], color='white', s=0.1, zorder=0)
    ax.scatter(dup_cb['RAJ2000'], dup_cb['DEJ2000'], color='white', s=0.1, zorder=0)

#############################################################################################################################################################

    global ocms
    global gcms
    global gcms1
    global gams
    global nbms
    global nbms1
    global otms
    global tys
    global dtys

    ocms = ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (oc_ms['V (from SEDS)']),
               edgecolor=axbgcl, picker=1, linewidth = lw)
    ocms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(oc_ms['V (from SEDS)'], oc_ms['ID (for resolver)'], oc_ms['Common Name'])]
    gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
               zorder=2, edgecolor=axbgcl, linewidth=plw)
    gcms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m,n in zip(gc_ms['V (from SEDS)'], gc_ms['ID (for resolver)'], gc_ms['Common Name'])]
    gcms1 = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (gc_ms['V (from SEDS)']),
               edgecolor="grey",  linewidth=lw, picker=1)
    gcms1.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(gc_ms['V (from SEDS)'], gc_ms['ID (for resolver)'], gc_ms['Common Name'])]
    gams = ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (ga_ms['V (from SEDS)']),
               picker=1, linewidth = lw, edgecolor=axbgcl)
    gams.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(ga_ms['V (from SEDS)'], ga_ms['ID (for resolver)'], ga_ms['Common Name'])]
    nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (nb_ms['V (from SEDS)']),
               edgecolor=axbgcl, zorder=2, picker=1, linewidth = lw)
    nbms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(nb_ms['V (from SEDS)'], nb_ms['ID (for resolver)'], nb_ms['Common Name'])]
    nbms1 = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='black', marker="+",
               s=s_fact * 10 / 2.5 ** (nb_ms['V (from SEDS)']), edgecolor=axbgcl, linewidth=plw, picker=1)
    nbms1.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(nb_ms['V (from SEDS)'], nb_ms['ID (for resolver)'], nb_ms['Common Name'])]
    otms = ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='purple', marker="+",
               s=s_fact / 2.5 ** (ot_ms['V (from SEDS)']),
               edgecolor=axbgcl, linewidth=plw, picker=1)
    otms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(ot_ms['V (from SEDS)'], ot_ms['ID (for resolver)'], ot_ms['Common Name'])]


    # docms = ax.scatter(dup_oc_ms['RAJ2000'], dup_oc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_oc_ms['V (from SEDS)']),
    #            edgecolor=axbgcl, picker=1, linewidth = lw)
    # docms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(oc_ms['V (from SEDS)'], oc_ms['ID (for resolver)'], oc_ms['Common Name'])]
    # dgcms = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='black', marker="+", s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
    #            zorder=2, edgecolor=axbgcl, linewidth=plw)
    # dgcms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m,n in zip(gc_ms['V (from SEDS)'], gc_ms['ID (for resolver)'], gc_ms['Common Name'])]
    # dgcms1 = ax.scatter(dup_gc_ms['RAJ2000'], dup_gc_ms['DEJ2000'], color='yellow', marker="o", s=s_fact / 2.5 ** (dup_gc_ms['V (from SEDS)']),
    #            edgecolor="grey",  linewidth=lw, picker=1)
    # dgcms1.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(gc_ms['V (from SEDS)'], gc_ms['ID (for resolver)'], gc_ms['Common Name'])]
    # dgams = ax.scatter(dup_ga_ms['RAJ2000'], dup_ga_ms['DEJ2000'], color='red', marker=ell, s=s_fact / 2.5 ** (dup_ga_ms['V (from SEDS)']),
    #            picker=1, linewidth = lw, edgecolor=axbgcl)
    # dgams.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(ga_ms['V (from SEDS)'], ga_ms['ID (for resolver)'], ga_ms['Common Name'])]
    # dnbms = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='green', marker="o", s=s_fact / 2.5 ** (dup_nb_ms['V (from SEDS)']),
    #            edgecolor=axbgcl, zorder=2, picker=1, linewidth = lw)
    # dnbms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(nb_ms['V (from SEDS)'], nb_ms['ID (for resolver)'], nb_ms['Common Name'])]
    # dnbms1 = ax.scatter(dup_nb_ms['RAJ2000'], dup_nb_ms['DEJ2000'], color='black', marker="+",
    #            s=s_fact * 10 / 2.5 ** (dup_nb_ms['V (from SEDS)']), edgecolor=axbgcl, linewidth=plw, picker=1)
    # dnbms1.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(nb_ms['V (from SEDS)'], nb_ms['ID (for resolver)'], nb_ms['Common Name'])]
    # dotms = ax.scatter(dup_ot_ms['RAJ2000'], dup_ot_ms['DEJ2000'], c='purple', marker="+",
    #            s=s_fact / 2.5 ** (dup_ot_ms['V (from SEDS)']),
    #            edgecolor=axbgcl, linewidth=plw, picker=1)
    # dotms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in zip(ot_ms['V (from SEDS)'], ot_ms['ID (for resolver)'], ot_ms['Common Name'])]


    tys = ax.scatter(mag_ty['RAJ2000'], mag_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (mag_ty['V']), edgecolor=axbgcl,
                    linewidth=1 / 10)
    tys.annotation_names = [f'{n}, {b}\nV:{v}, {c}' for v,c, n, b in zip(ty['V'], ty['Constellation'], ty['Name'], ty['Bayer'])]

    # tys = ax.scatter(full_ty['RAJ2000'], full_ty['DEJ2000'], c='black', s=ts_fact / 2.5 ** (full_ty['V']), edgecolor=axbgcl,
    #                 linewidth=1 / 10)
    # tys.annotation_names = [f'{n}, {b}\nV:{v}, {c}' for v,c, n, b in zip(ty['V'], full_ty['Constellation'], full_ty['Name'], full_ty['Bayer'])]

    # # # plt.legend([red_dot, (red_dot, white_cross)], ["Attr A", "Attr A+B"])
    # lgnd= plt.legend([ocms,(gcms, gcms1),(nbms, nbms1), otms, tys ], [" Open Cluster", "Globular Cluster", "Nebula", "Other Messier", "Tycho-1 Stars"],labelspacing=5, ncol=5, borderpad=.5, loc='lower center', bbox_to_anchor=(.5,1))
    # lgnd.legendHandles[0]._sizes = [30]
    # lgnd.legendHandles[1]._sizes = [300]
    # lgnd.legendHandles[2]._sizes = [300]
    # lgnd.legendHandles[3]._sizes = [30]
    # lgnd.legendHandles[4]._sizes = [30]

    cursor = mplcursors.cursor([ocms, gcms, gcms1, gams, nbms, nbms1, otms, tys], hover=True)
    # cursor = mplcursors.cursor([ocms, gcms, gcms1, gams, nbms, nbms1, otms, docms, dgcms, dgcms1, dgams, dnbms, dnbms1, dotms, tys], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(sel.artist.annotation_names[sel.target.index]))

    # plt.savefig('6', dpi=400, format="png")

chart()

#############################################################################################################################################################




def resetchart():
    global s_fact
    s_fact = 250
    plt.cla()
    global xl
    global xr
    global yb
    global yt
    xr = 290 + 70
    xl = 0
    yb = -90
    yt = 90
    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])
    chart()
    plt.draw()
    object_entry.delete(0, END)

# def on_xlims_change(event_ax):
#     print("updated xlims: ", event_ax.get_xlim())
#     global xl
#     global xr
#     xl=event_ax.get_xlim()[0]
#     xr=event_ax.get_xlim()[0]
# def on_ylims_change(event_ax):
#     print("updated ylims: ", event_ax.get_ylim())
#     global yb
#     global yt
#     yb=event_ax.get_ylim()[0]
#     yt=event_ax.get_ylim()[1]
#
# ax.callbacks.connect('xlim_changed', on_xlims_change)
# ax.callbacks.connect('ylim_changed', on_ylims_change)

ident = np.array(ms['ID (for resolver)'])
name = np.array(ms['Common Name'])

def submit():
    inp = object_entry.get()
    inp2 = inp.split()


    if all([x.isalpha() for x in inp2]):
        inp = inp.title()
        find_res = np.array([x.find(inp) for x in name])
        pos = np.where(find_res != -1)[0]
        if len(pos) == 0:
            mb.showwarning('alert', 'Enter:\nRA DEC FoV\nOR\nName')
            return None
        rax, decx = ms['RAJ2000'][pos].values, ms['DEJ2000'][pos].values
        if len(name[pos]) > 1:
            mb.showinfo('Try again ', 'More than one object matching')
        else:
            ra = rax[0]
            dec = decx[0]
            fov = 20
            xl = ra - fov / 2 - fov / 10
            xr = ra + fov / 2 + fov / 10
            yb = dec - fov / 2 - fov / 10
            yt = dec + fov / 2 + fov / 10
            plt.cla()
            ax.set_xlim([xl, xr])
            ax.set_ylim([yb, yt])
            chart()
            plt.draw()
            object_entry.delete(0, END)
            object_entry.insert(0, name[pos][0])
            mb.showinfo('Processed')

    elif all([x.isalnum() for x in inp2]):
        if len(inp2)==3:
            ra = float(inp2[0])
            dec = float(inp2[1])
            fov = float(inp2[2])
            xl = ra - fov / 2 - fov / 10
            xr = ra + fov / 2 + fov / 10
            yb = dec - fov / 2 - fov / 10
            yt = dec + fov / 2 + fov / 10
            plt.cla()
            ax.set_xlim([xl, xr])
            ax.set_ylim([yb, yt])
            chart()
            plt.draw()
            mb.showinfo('Processed')
        else:
            inp = inp.title()
            inp = re.split('(\d+)', inp)
            print(inp)
            inp[0] = inp[0].rstrip()
            inp = inp[:2]
            inp = ' '.join(inp)
            find_res = np.array([x.find(inp) for x in ident])
            pos = np.where(find_res != -1)[0]
            if len(pos) == 0:
                mb.showinfo('Try again ', 'More than one object matching')
            else:
                rax, decx = ms['RAJ2000'][pos].values, ms['DEJ2000'][pos].values
                ra = rax[0]
                dec = decx[0]
                fov = 20
                xl = ra - fov / 2 - fov / 10
                xr = ra + fov / 2 + fov / 10
                yb = dec - fov / 2 - fov / 10
                yt = dec + fov / 2 + fov / 10
                plt.cla()
                ax.set_xlim([xl, xr])
                ax.set_ylim([yb, yt])
                chart()
                plt.draw()
                object_entry.delete(0, END)
                object_entry.insert(0, ident[pos][0])

                mb.showinfo('Processed')
    else:
        mb.showwarning('alert', 'Enter in degrees:\nRA DEC FoV\nOR\nmessierNumber FoV')

    # if len(lst) == 3 and float(lst[0]) >= 0 and float(lst[0]) < 360 and float(lst[1]) >= -90 and float(lst[1]) <= 90:
    #     ra = int(lst[0])
    #     dec = int(lst[1])
    #     fov = int(lst[2])
    #     # ra1 = ra
    #     # dec1 = dec
    #     # fov1 = fov
    #     # circ = plt.Circle((ra1, dec1), fov1 / 2, color='#00af08', zorder=-1, alpha=0.1)
    #     # circ.remove()

        # xl = ra - fov / 2 - fov / 10
        # xr = ra + fov / 2 + fov / 10
        # yb = dec - fov / 2 - fov / 10
        # yt = dec + fov / 2 + fov / 10
    #
    #     # if xr > 360:
    #     #     xr = 360
    #     #     ra -= 360
    #     #     xr -= 360
    #     #     xl -= 360
    #     plt.cla()
    #     ax.set_xlim([xl, xr])
    #     ax.set_ylim([yb, yt])
    #     # circ = plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.1)
    #     # print(circ)
    #     # ax.add_artist(circ)
    #     chart()
    #     plt.draw()
    #     mb.showinfo('Processed')
    #
    # elif len(lst) == 2 and int(lst[0]) > 0 and int(lst[0]) <= 110 and int(lst[1]) > 0:
    #     num = int(lst[0])
    #     fov = float(lst[1])
    #     ra = float(ms.iloc[[num - 1]]['RAJ2000'])
    #     dec = float(ms.iloc[[num - 1]]['DEJ2000'])
    #     xl = ra - fov / 2 - fov / 10
    #     xr = ra + fov / 2 + fov / 10
    #     yb = dec - fov / 2 - fov / 10
    #     yt = dec + fov / 2 + fov / 10
    #
    #     if xr > 360:
    #         ra -= 360
    #         xr -= 360
    #         xl -= 360
    #
    #     plt.cla()
    #     ax.set_xlim([xl, xr])
    #     ax.set_ylim([yb, yt])
    #     # ax.add_artist(plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.1))
    #     chart()
    #     plt.draw()
    #     mb.showwarning('Processed', "Press ok to close")
    # else:
    #     mb.showwarning('alert', 'Enter in degrees:\nRA DEC FoV\nOR\nmessierNumber FoV')

def misize():
    global s_fact
    global xl
    global xr
    global yb
    global yt
    xl = ax.get_xlim()[0]
    xr = ax.get_xlim()[1]
    yb = ax.get_ylim()[0]
    yt = ax.get_ylim()[1]
    plt.cla()
    print(xl,xr,yb,yt)
    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])
    s_fact *= 4
    chart()
    plt.draw()

def mdsize():
    global s_fact
    global xl
    global xr
    global yb
    global yt
    xl = ax.get_xlim()[0]
    xr = ax.get_xlim()[1]
    yb = ax.get_ylim()[0]
    yt = ax.get_ylim()[1]
    plt.cla()
    print(xl,xr,yb,yt)
    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])
    if s_fact>250:
        s_fact /= 4
    else:
        s_fact = 250
    chart()
    plt.draw()

#############################################################################################################################################################

try:
    hop_file = open("hop.pkl", "rb")
    d = pickle.load(hop_file)

except:
    d={}

def showhop():
    nl=[]
    for k,v in d.items():
        if not v == []:
            nl.append(k)
    mb.showwarning('Hops created for', nl)

print(d)

tyx=np.array(ty['RAJ2000'])
tyy=np.array(ty['DEJ2000'])
# tyx=np.array(full_ty['RAJ2000'])
# tyy=np.array(full_ty['DEJ2000'])

tree = spatial.KDTree(list(zip(tyx,tyy)))

l=[]

dict_label = Label (mainframe, text ="--<Current Hops Displayed Here>--")
dict_label.pack(side=TOP,padx=0, pady=5)

def onclick(event):
    if event.button == 1:
        global d
        global l
        xin, yin = event.xdata, event.ydata
        print(xin,yin)

        points = np.array([xin,yin])
        dist,ind = tree.query(points, k=10)
        print(dist, ind)
        # print()
        # print([ty['V'][ind].idxmin()])
        # print(ind, ty['RAJ2000'][int([ty['V'][ind].idxmin()][0])])
        global markerobj

        objra = ty['RAJ2000'][int([ty['V'][ind].idxmin()][0])]
        objde = ty['DEJ2000'][int([ty['V'][ind].idxmin()][0])]
        # objra = full_ty['RAJ2000'][int([full_ty['V'][ind].idxmin()][0])]
        # objde = full_ty['DEJ2000'][int([full_ty['V'][ind].idxmin()][0])]

        # markerobj = ax.scatter([objra],[objde], c='black', s=10000, marker='+')
        # # plt.draw()
        # # if hopobj in d.keys():
        # #     # if len(d[hopobj]) >=1:
        # #     #     if d[hopobj] == xi:
        # #             fig.canvas.mpl_disconnect(cid)
        # #             print("Hops for {} created".format(hopobject))

        global hopobj

        try:
            l.append([objra, objde])
            d[hopobj] = l
        except:
            l=[]
            d[hopobj] = []
            print("Hop started:")
        # d[ms[(ms['RAJ2000'])==l[0]]['ID (for resolver)']].append([xi,yi])

        global dict_label
        # dict_label.destroy()
        dict_label.configure(text = "Hops for '{}' :{}".format(hopobj, d[hopobj]))

# cid = fig.canvas.mpl_connect('button_press_event', onclick)

#############################################################################################################################################################

def hopstart():

    global dict_label
    global d
    global l
    global hopobj
    global cid

    l=[]

    if hop_btn['text'] == "CREATE HOP":
        print("ehlp")

        hop_btn.configure(text="FINISH HOP")
        uh["state"] = "active"

        hopobj = simpledialog.askstring("Input", "Enter the messier object towards which you would hop to",
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

            d[hopobj]=[]

            # dict_label.destroy()
            dict_label.configure(text="Hops for '{}': ".format(hopobj))

            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            print("ehlp again")
        else:

            hop_btn.configure(text="CREATE HOP")
            uh["state"] = "disabled"
            dict_label.configure(text="--<Current Hops Displayed Here>--")

    elif hop_btn['text'] == "FINISH HOP":
        hop_btn.configure(text="CREATE HOP")
        if len(d[hopobj])>0:
            hopinstr = simpledialog.askstring("Input", "Further Instruction for Hopping:",
                                            parent=widgetframe)
            d[hopobj].append(hopinstr)

        uh["state"] = "disabled"
        fig.canvas.mpl_disconnect(cid)
        dict_label.configure(text ="--<Current Hops Displayed Here>--")
        resetchart()

    print("Done")

    pickle.dump(d, open("hop.pkl", "wb"))

def undohop():
    global hopobj
    d[hopobj].pop()
    print(d)
    # global markerobj
    # markerobj.remove()
    # chart()
    # plt.draw()
    global dict_label
    # dict_label.destroy()
    dict_label.configure(text="Hops for '{}' :{}".format(hopobj, d[hopobj]))

#############################################################################################################################################################

object_label = Label ( widgetframe, text="Target" )
object_label.pack(side=LEFT,padx=0, pady=5
)

object_entry = Entry ( widgetframe, text="pos" )
object_entry.pack(side=LEFT,padx=0, pady=5
)

sub_btn=Button(widgetframe,text = 'Submit', command = submit)
sub_btn.pack(side=LEFT,padx=5, pady=5
)

hop_btn= Button ( widgetframe, text="CREATE HOP", bg="#E44021",fg="white",command = hopstart)
hop_btn.pack(side=RIGHT,padx=5, pady=5
)

uh=Button(widgetframe, text="UNDO HOP", command=undohop)
uh.pack(side=RIGHT,padx=5, pady=5
)
uh["state"] = "disabled"

rsc=Button(widgetframe, text="RESET CHART",bg="#1c91ff",fg="white", command=resetchart)
rsc.pack(side=LEFT,padx=5, pady=5
)

mdfact=Button(widgetframe, text="- MESSIER SIZE",bg="#FCC034", command=mdsize)
mdfact.pack(side=LEFT,padx=5, pady=5)

mifact=Button(widgetframe, text="+ MESSIER SIZE",bg="#FCC034", command=misize)
mifact.pack(side=LEFT,padx=5, pady=5
)

prevhops=Button(widgetframe, text="HOPS CREATED", command=showhop)
prevhops.pack(side=LEFT,padx=5, pady=5
)

# def displabel():
#     if xy.get()==1:
#         mplcursors.cursor(hover=True)
#     elif xy.get()==0:
#         mplcursors.cursor(hover=False)
# xy = IntVar()
# xyhover=Checkbutton(widgetframe, text='Label',variable=xy, onvalue=1, offvalue=0, command=displabel)
# xyhover.pack()

#############################################################################################################################################################


#############################################################################################################################################################

# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)

mainloop()