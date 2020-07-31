"""
author: vivek reddy
"""

# packages
from tkinter import *
import pickle
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
from svgpath2mpl import parse_path
import pandas as pd
import mplcursors
import tkinter.messagebox as mb
import re
from tkinter import simpledialog
from scipy import spatial
import ast

# #

ng = pd.read_csv('NGC.csv', low_memory=False)
ms = pd.read_csv('messier_objects.csv', low_memory=False)
cb = pd.read_csv('constellation_borders.csv', low_memory=False)
ty = pd.read_csv('tycho-1.csv', low_memory=False)

ell = parse_path(
    """M 490.60742,303.18917 A 276.31408,119.52378 28.9 0 1 190.94051,274.29027 276.31408,119.52378 28.9 0 1 6.8010582,36.113705 276.31408,119.52378 28.9 0 1 306.46799,65.012613 276.31408,119.52378 28.9 0 1 490.60742,303.18917 Z""")
ell.vertices -= ell.vertices.mean(axis=0)

# #

mag = 6  # limiting the magnitude for Tycho-1 stars;
mag_ty = ty[(ty['V'] <= mag)]  # Tycho

dup_ng = ng.copy(deep=True)  # NGC
dup_ms = ms.copy(deep=True)  # Messier
dup_ty = mag_ty.copy(deep=True)  # Tycho
dup_cb = cb.copy(deep=True)  # Constellation borders
dup_ng['RAJ2000'] -= 360  # NGC transform
dup_ms['RAJ2000'] -= 360  # Messier transform
dup_ty['RAJ2000'] -= 360  # Tycho transform
dup_cb['RAJ2000'] -= 360  # Constellation borders transform

# sorting objects in messier_objects.csv and NGC.csv according to type
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
ot_ms = ms[(ms["TYPE"] == 'As*') | (ms["TYPE"] == 'LIN') | (ms["TYPE"] == 'mul') | (
        ms["TYPE"] == 'AGN')]
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
    ((dup_ms["TYPE"] == 'As*') | (dup_ms["TYPE"] == 'LIN') | (dup_ms["TYPE"] == 'mul') | (dup_ms["TYPE"] == 'AGN'))]
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
mag_ty = mag_ty.reset_index(drop=True)

# ty_names=ty[(ty['Name']!='-')] # tycho-1 stars with names
# ty_bayer=ty.dropna(subset=['Bayer']) # tycho-1 stars with bayer designations

# full_ty = pd.concat([mag_ty,dup_ty], axis=0) # combining tycho-1 and the transformed catalogue into one dataframe
# full_ty.reset_index(drop=True)

# #

# tkinter
root = Tk()
root.wm_title("Editor _ Star Hopping")
root.configure(bg='black')
root.geometry("1200x700+200+200")
mainframe = Frame(root, relief=RAISED, borderwidth=1)
mainframe.place(relx=0, rely=.1, relwidth=1, relheight=0.9)
widgetframe = Frame(root, padx=1, pady=1)
widgetframe.place(relx=0.0, y=0, relwidth=1, relheight=0.1)
mb.showwarning('Editor_GUI', "Full Screen Recommended")

# #

# axis limits for initial plot
xr = 360
xl = 0
yb = -90
yt = 90

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.set_aspect(1)
axbgcl = "grey"  # axis background color
fig.patch.set_facecolor('slategrey')


def axclr():
    ax.set_facecolor('gainsboro')
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', color="#838383", zorder=0, alpha=.4)
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black', zorder=0, alpha=0.2)
axclr()

ts_fact = 150
s_fact = 150
ax.set_xlim([xl, xr])
ax.set_ylim([yb, yt])
canvas = FigureCanvasTkAgg(fig, master=mainframe)  # A DrawingArea.
canvas.draw()
toolbar = NavigationToolbar2Tk(canvas, mainframe)
toolbar.update()
canvas.get_tk_widget().place(relx=0.0, rely=0, relheight=.99 - 0.02, relwidth=1)

# stick figures
file = open('constellation_lines_simplified.dat')
lines = file.readlines()[56::]
cond = np.where([x.isalpha() for x in lines])[0]
constellation = [lines[i] for i in cond]
find_res = np.array([x.find('[') for x in lines])
pos = np.where(find_res != -1)[0]
points = [lines[i].strip('\n') for i in pos]
points = [ast.literal_eval(items) for items in points]

ra = ty['RAJ2000']
dec = ty['DEJ2000']
hip = ty['HIP']
hip = [x for x in hip]

def draw_sticks():
    for i in range(len(points)):
        lst = points[i]
        ra_line = []
        dec_line = []
        for items in lst:
            index = hip.index(float(items))
            if len(ra_line) != 0:
                if abs(ra[index] - ra_line[-1]) > 300 and -75 < dec[index] < 75:
                    if ra_line[-1] > 300:
                        pred_slope = (dec[index] - dec_line[-1]) / 360 + (ra[index] - ra_line[-1])
                        ra_line.append(0)
                        dec_line.append(dec_line[-1] + pred_slope * (360 - ra_line[-1]))
                        new_dec = dec_line[-1] + pred_slope * (360 - ra_line[-1])
                        ra_line = []
                        dec_line = []
                        ra_line.append(0)
                        dec_line.append(new_dec)
                        ax.plot(ra_line, dec_line, '-', color="green", linewidth=np.power(100, 1 / 5), alpha=0.2,
                                zorder=0)
                    elif ra_line[-1] < 60:
                        pred_slope = (dec[index] - dec_line[-1]) / (ra[index] - ra_line[-1]) - 360
                        ra_line.append(0)
                        dec_line.append(dec_line[-1] + pred_slope * (-ra_line[-1]))
                        new_dec = dec_line[-1] + pred_slope * (-ra_line[-1])
                        q = ax.plot(ra_line, dec_line, '-', color="green", linewidth=np.power(100, 1 / 5), alpha=0.1,
                                    zorder=0)
                        ra_line = []
                        dec_line = []
                        ra_line.append(360)
                        dec_line.append(new_dec)
                else:
                    ra_line.append(ra[index])
                    dec_line.append(dec[index])
            else:
                ra_line.append(ra[index])
                dec_line.append(dec[index])
        ax.plot(ra_line, dec_line, '-', color="green", linewidth=np.power(100, 1 / 5), alpha=0.2, zorder=0)

def chart():
    plt.xlabel('Right Ascension (degrees)', fontsize=12)
    plt.ylabel('Declination (degrees)', fontsize=12)
    lw = 0
    plw = 1
    ax.scatter(cb['RAJ2000'], cb['DEJ2000'], color='white', s=0.1, zorder=0)
    ax.scatter(dup_cb['RAJ2000'], dup_cb['DEJ2000'], color='white', s=0.1, zorder=0)
    global ocms
    global gcms
    global gcms1
    global gams
    global nbms
    global nbms1
    global otms
    global tys
    global dtys

    ocms = ax.scatter(oc_ms['RAJ2000'], oc_ms['DEJ2000'], color='yellow', marker="o",
                      s=s_fact / np.power(100, 1 / 5) ** (oc_ms['V (from SEDS)']),
                      edgecolor=axbgcl, picker=1, linewidth=lw)
    ocms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in
                             zip(oc_ms['V (from SEDS)'], oc_ms['ID (for resolver)'], oc_ms['Common Name'])]
    gcms = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='black', marker="+",
                      s=s_fact / np.power(100, 1 / 5) ** (gc_ms['V (from SEDS)']),
                      zorder=2, edgecolor=axbgcl, linewidth=plw)
    gcms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in
                             zip(gc_ms['V (from SEDS)'], gc_ms['ID (for resolver)'], gc_ms['Common Name'])]
    gcms1 = ax.scatter(gc_ms['RAJ2000'], gc_ms['DEJ2000'], color='yellow', marker="o",
                       s=s_fact / np.power(100, 1 / 5) ** (gc_ms['V (from SEDS)']),
                       edgecolor="grey", linewidth=lw, picker=1)
    gcms1.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in
                              zip(gc_ms['V (from SEDS)'], gc_ms['ID (for resolver)'], gc_ms['Common Name'])]
    gams = ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ell,
                      s=s_fact / np.power(100, 1 / 5) ** (ga_ms['V (from SEDS)']),
                      picker=1, linewidth=lw, edgecolor=axbgcl)
    gams.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in
                             zip(ga_ms['V (from SEDS)'], ga_ms['ID (for resolver)'], ga_ms['Common Name'])]
    nbms = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='green', marker="o",
                      s=s_fact / np.power(100, 1 / 5) ** (nb_ms['V (from SEDS)']),
                      edgecolor=axbgcl, zorder=2, picker=1, linewidth=lw)
    nbms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in
                             zip(nb_ms['V (from SEDS)'], nb_ms['ID (for resolver)'], nb_ms['Common Name'])]
    nbms1 = ax.scatter(nb_ms['RAJ2000'], nb_ms['DEJ2000'], color='black', marker="+",
                       s=s_fact * 10 / np.power(100, 1 / 5) ** (nb_ms['V (from SEDS)']), edgecolor=axbgcl,
                       linewidth=plw, picker=1)
    nbms1.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in
                              zip(nb_ms['V (from SEDS)'], nb_ms['ID (for resolver)'], nb_ms['Common Name'])]
    otms = ax.scatter(ot_ms['RAJ2000'], ot_ms['DEJ2000'], c='purple', marker="+",
                      s=s_fact / np.power(100, 1 / 5) ** (ot_ms['V (from SEDS)']),
                      edgecolor=axbgcl, linewidth=plw, picker=1)
    otms.annotation_names = [f'{m}\nV:{v}\n{n}' for v, m, n in
                             zip(ot_ms['V (from SEDS)'], ot_ms['ID (for resolver)'], ot_ms['Common Name'])]

    tys = ax.scatter(mag_ty['RAJ2000'], mag_ty['DEJ2000'], c='black', s=ts_fact / np.power(100, 1 / 5) ** (mag_ty['V']),
                     edgecolor=axbgcl,
                     linewidth=1 / 10)
    tys.annotation_names = [f'{n}, {b}\nV:{v}, {c}' for v, c, n, b in
                            zip(mag_ty['V'], mag_ty['Constellation'], mag_ty['Name'], mag_ty['Bayer'])]

    # lgnd= plt.legend([ocms,(gcms, gcms1),(nbms, nbms1), otms, tys ], [" Open Cluster", "Globular Cluster", "Nebula", "Other Messier", "Tycho-1 Stars"],labelspacing=5, ncol=5, borderpad=.5, loc='lower center', bbox_to_anchor=(.5,1))
    # lgnd.legendHandles[0]._sizes = [30]
    # lgnd.legendHandles[1]._sizes = [300]
    # lgnd.legendHandles[2]._sizes = [300]
    # lgnd.legendHandles[3]._sizes = [30]
    # lgnd.legendHandles[4]._sizes = [30]

    cursor = mplcursors.cursor([ocms, gcms, gcms1, gams, nbms, nbms1, otms, tys], hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(sel.artist.annotation_names[sel.target.index]))
    # plt.savefig('fig', format="png")

chart()

# #

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
    axclr()
    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])
    xy.set(0)
    chart()
    plt.draw()
    object_entry.delete(0, END)

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
            axclr()
            ax.set_xlim([xl, xr])
            ax.set_ylim([yb, yt])
            if xy.get() == 1:
                draw_sticks()
            chart()
            plt.draw()
            object_entry.delete(0, END)
            object_entry.insert(0, name[pos][0])
            mb.showinfo('Processed')
    elif all([x.isalnum() for x in inp2]):
        if len(inp2) == 3:
            ra = float(inp2[0])
            dec = float(inp2[1])
            fov = float(inp2[2])
            xl = ra - fov / 2 - fov / 10
            xr = ra + fov / 2 + fov / 10
            yb = dec - fov / 2 - fov / 10
            yt = dec + fov / 2 + fov / 10
            plt.cla()
            axclr()
            ax.set_xlim([xl, xr])
            ax.set_ylim([yb, yt])
            if xy.get() == 1:
                draw_sticks()
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
                axclr()
                ax.set_xlim([xl, xr])
                ax.set_ylim([yb, yt])
                if xy.get() == 1:
                    draw_sticks()
                chart()
                plt.draw()
                object_entry.delete(0, END)
                object_entry.insert(0, ident[pos][0])
                mb.showinfo('Processed')
    else:
        mb.showwarning('alert', 'Enter in degrees:\nRA DEC FoV\nOR\nmessierNumber FoV')

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
    axclr()
    print(xl, xr, yb, yt)
    if xy.get() == 1:
        draw_sticks()
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
    axclr()
    print(xl, xr, yb, yt)
    if xy.get() == 1:
        draw_sticks()
    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])
    if s_fact > 250:
        s_fact /= 4
    else:
        s_fact = 250
    chart()
    plt.draw()

# #

try:
    hop_file = open("hop.pkl", "rb")
    d = pickle.load(hop_file)
except:
    d = {}
def showhop():
    nl = []
    for k, v in d.items():
        if not v == []:
            nl.append(k)
    mb.showwarning('Hops created for', nl)
# print(d)
tyx = np.array(mag_ty['RAJ2000'])
tyy = np.array(mag_ty['DEJ2000'])
# tyx=np.array(full_ty['RAJ2000'])
# tyy=np.array(full_ty['DEJ2000'])
tree = spatial.KDTree(list(zip(tyx, tyy)))
dict_label = Label(mainframe, text="--<Current Hops Displayed Here>--")
dict_label.pack(side=TOP, padx=0, pady=5)
def onclick(event):
    if event.button == 1:
        global d
        global l
        global hopobj
        xin, yin = event.xdata, event.ydata
        # print(xin, yin)
        point = np.array([xin, yin])
        ind = tree.query_ball_point(point, .5)
        print(ind)
        if not ind == []:
            objra = mag_ty['RAJ2000'][mag_ty['V'][ind].idxmin()]
            objde = mag_ty['DEJ2000'][mag_ty['V'][ind].idxmin()]
            l.append([objra, objde])
            d[hopobj] = l
            print("asd")
        global dict_label
        dict_label.configure(text="Hops for '{}' :{}".format(hopobj, d[hopobj]))

# #

def hopstart():
    global dict_label
    global d
    global l
    global hopobj
    global cid

    l = []
    print(ms['ID (for resolver)'].values)
    if hop_btn['text'] == "CREATE HOP":

        hop_btn.configure(text="FINISH HOP", bg="red")
        uh["state"] = "active"
        while True:
            hopobj = simpledialog.askstring("Input", "Enter the messier object towards which you would hop to",
                                            parent=widgetframe)
            if hopobj == None:
                hop_btn.configure(text="CREATE HOP", bg="SpringGreen2")
                uh["state"] = "disabled"
                dict_label.configure(text="--<Current Hops Displayed Here>--")
                break
            try:
                hopobj = hopobj.strip()
                messier = hopobj.capitalize()[0]+' '+hopobj.capitalize()[1:].strip()
            except:
                messier = hopobj.strip()
            if messier in ms['ID (for resolver)'].values:
                hopobj = messier
                d[hopobj] = []
                dict_label.configure(text="Hops for '{}': ".format(hopobj))
                cid = fig.canvas.mpl_connect('button_press_event', onclick)
                break
            elif messier == '' or messier not in ms['ID (for resolver)'].values:
                continue


    elif hop_btn['text'] == "FINISH HOP":
        hop_btn.configure(text="CREATE HOP", bg="SpringGreen2")
        if len(d[hopobj]) > 0:
            hopinstr = simpledialog.askstring("Input", "Further Instruction for Hopping:",
                                              parent=widgetframe)
            d[hopobj].append(hopinstr)
        uh["state"] = "disabled"
        fig.canvas.mpl_disconnect(cid)
        dict_label.configure(text="--<Current Hops Displayed Here>--")
        resetchart()
        print("Done button")
        d = {key: value for key, value in d.items() if value != []}
        messier = list(d.keys())
        for i in range(len(messier)):
            messier_coord = [float(ms['RAJ2000'][ms.index[ms['ID (for resolver)'] == messier[i]]]),
                             float(ms['DEJ2000'][ms.index[ms['ID (for resolver)'] == messier[i]]])]
            if not d[messier[i]][-2] == messier_coord:
                d[messier[i]].insert(-1, messier_coord)
        pickle.dump(d, open("hop.pkl", "wb"))

def undohop():
    global hopobj
    try:
        d[hopobj].pop()
    except:
        None
    print(d)
    global dict_label
    dict_label.configure(text="Hops for '{}' :{}".format(hopobj, d[hopobj]))

# #

object_label = Label(widgetframe, text="Target")
object_label.pack(side=LEFT, padx=0, pady=5)
object_entry = Entry(widgetframe, text="pos")
object_entry.pack(side=LEFT, padx=0, pady=5)
sub_btn = Button(widgetframe, text='Submit', command=submit)
sub_btn.pack(side=LEFT, padx=5, pady=5)
hop_btn = Button(widgetframe, text="CREATE HOP", bg="SpringGreen2", fg="black", command=hopstart)
hop_btn.pack(side=RIGHT, padx=5, pady=5)
uh = Button(widgetframe, text="UNDO HOP", command=undohop)
uh.pack(side=RIGHT, padx=5, pady=5)
uh["state"] = "disabled"
prevhops = Button(widgetframe, text="HOPS CREATED", command=showhop)
prevhops.pack(side=RIGHT, padx=5, pady=5)
rsc = Button(widgetframe, text="RESET CHART", bg="#1c91ff", fg="white", command=resetchart)
rsc.pack(side=LEFT, padx=5, pady=5)
mdfact = Button(widgetframe, text="- MESSIER SIZE", bg="#FCC034", command=mdsize)
mdfact.pack(side=LEFT, padx=5, pady=5)
mifact = Button(widgetframe, text="+ MESSIER SIZE", bg="#FCC034", command=misize)
mifact.pack(side=LEFT, padx=5, pady=5)
def sticks():
    if xy.get() == 1:
        xl = ax.get_xlim()[0]
        xr = ax.get_xlim()[1]
        yb = ax.get_ylim()[0]
        yt = ax.get_ylim()[1]
        plt.cla()
        axclr()
        ax.set_xlim([xl, xr])
        ax.set_ylim([yb, yt])
        draw_sticks()
        chart()
        plt.draw()
    elif xy.get() == 0:
        draw_sticks()
        xl = ax.get_xlim()[0]
        xr = ax.get_xlim()[1]
        yb = ax.get_ylim()[0]
        yt = ax.get_ylim()[1]
        plt.cla()
        axclr()
        ax.set_xlim([xl, xr])
        ax.set_ylim([yb, yt])
        chart()
        plt.draw()
xy = IntVar()
xyhover = Checkbutton(widgetframe, text='Show Constellation Sticks', variable=xy, onvalue=1, offvalue=0, command=sticks)
xyhover.pack(side=LEFT)
mainloop()
