# Necessary imports
import matplotlib.pyplot as plt
import pandas as pd
from svgpath2mpl import parse_path

# hy = pd.read_csv('hygfull.csv')
# n1 = pd.read_csv('NOMAD_1.csv')
# n2 = pd.read_csv('NOMAD_2.csv')
# n3 = pd.read_csv('NOMAD_3.csv')
# n = pd.concat([n1, n2, n3], ignore_index=True)

ng = pd.read_csv('NGC.csv')
ms = pd.read_csv('messier_objects.csv')
cb = pd.read_csv('constellation_borders.csv')
ty = pd.read_csv('tycho_1.csv')

# svg paths for custom markers
ga = parse_path(
    """M 490.60742,303.18917 A 276.31408,119.52378 28.9 0 1 190.94051,274.29027 276.31408,119.52378 28.9 0 1 6.8010582,36.113705 276.31408,119.52378 28.9 0 1 306.46799,65.012613 276.31408,119.52378 28.9 0 1 490.60742,303.18917 Z""")
ga.vertices -= ga.vertices.mean(axis=0)
cl = parse_path(
    """M 541.64941,265.49102 A 270.8247,265.49102 0 0 1 270.82471,530.98205 270.8247,265.49102 0 0 1 0,265.49102 270.8247,265.49102 0 0 1 270.82471,0 270.8247,265.49102 0 0 1 541.64941,265.49102 Z""")
cl.vertices -= cl.vertices.mean(axis=0)
pn = parse_path(
    """M 488,240 H 256 V 8 c 0,-4.418 -3.582,-8 -8,-8 -4.418,0 -8,3.582 -8,8 V 240 H 8 c -4.418,0 -8,3.582 -8,8 0,4.418 3.582,8 8,8 h 232 v 232 c 0,4.418 3.582,8 8,8 4.418,0 8,-3.582 8,-8 V 256 h 232 c 4.418,0 8,-3.582 8,-8 0,-4.418 -3.582,-8 -8,-8 z""")
pn.vertices -= pn.vertices.mean(axis=0)

# function with telescope parameters; m: magnification of telescope; afov: apparent field of view of eyepiece; D: aperture size in mm;
def func1(ra, dec, m, afov, d):
    fov = afov / m  # true field of view based on magnification and apparent fov of eye piece
    mag = 2 + 5 * np.log10(d)  # limiting visual magnitude based of aperture

    #     x=np.pi/180
    # cos(A) = sin(Decl.1)sin(Decl.2) + cos(Decl.1)cos(Decl.2)cos(RA.1 - RA.2); formula for the angular seperation
    # distance of each object from user input of ra, dec
    #     ng["distance"]=np.arccos(np.sin(dec*x)*np.sin(ng["_DEJ2000"]*x)+np.cos(dec*x)*np.cos(ng["_DEJ2000"]*x)*np.cos(ra*x-ng["_RAJ2000"]*x))*(180/np.pi)
    #     ms["distance"]=np.arccos(np.sin(dec*x)*np.sin(ms["DEJ2000"]*x)+np.cos(dec*x)*np.cos(ms["DEJ2000"]*x)*np.cos(ra*x-ms["RAJ2000"]*x))*(180/np.pi)
    #     ty["distance"]=np.arccos(np.sin(dec*x)*np.sin(ty["_DEJ2000"]*x)+np.cos(dec*x)*np.cos(ty["_DEJ2000"]*x)*np.cos(ra*x-ty["_RAJ2000"]*x))*(180/np.pi)

    # sorting objects under the user input of limiting magnitude;
    # also duplicating the the objects and transforming them so they are repeated to the left of y-axis
    mag_ng = ng[(ng["mag"] <= mag)]
    mag_ms = ms[(ms['V'] <= mag)]
    mag_ty = ty[(ty['V'] <= mag)]
    dup_ng = mag_ng.copy(deep=True)
    dup_ms = mag_ms.copy(deep=True)
    dup_ty = mag_ty.copy(deep=True)
    dup_ng['_RAJ2000'] -= 360
    dup_ms['RAJ2000'] -= 360
    dup_ty['_RAJ2000'] -= 360

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_aspect('equal')

    # breathing space aroung the fov circle in the plot
    xl = ra - fov / 2 - fov / 10
    xr = ra + fov / 2 + fov / 10
    yb = dec - fov / 2 - fov / 10
    yt = dec + fov / 2 + fov / 10

    # sorting objects in messier_objects.csv according to objects
    cl_ms = ms[(ms["OTYPE_3"] == 'OpC') | (ms["OTYPE_3"] == 'GlC') | (ms["OTYPE_3"] == 'Cl*')]
    pn_ms = ms[(ms["OTYPE_3"] == 'PN')]
    ga_ms = ms[
        (ms["OTYPE_3"] == 'G') | (ms["OTYPE_3"] == 'Sy2') | (ms["OTYPE_3"] == 'IG') | (ms["OTYPE_3"] == 'GiG') | (
                    ms["OTYPE_3"] == 'GiP') | (ms["OTYPE_3"] == 'SyG') | (ms["OTYPE_3"] == 'SBG') | (
                    ms["OTYPE_3"] == 'BiC') | (ms["OTYPE_3"] == 'H2G')]
    re_ms = ms[
        (ms["OTYPE_3"] == 'HII') | (ms["OTYPE_3"] == 'As*') | (ms["OTYPE_3"] == 'LIN') | (ms["OTYPE_3"] == 'mul') | (
                    ms["OTYPE_3"] == 'RNe') | (ms["OTYPE_3"] == 'AGN')]
    # duplicated data sort by object type
    dup_cl_ms = dup_ms[(dup_ms["OTYPE_3"] == 'OpC') | (dup_ms["OTYPE_3"] == 'GlC') | (dup_ms["OTYPE_3"] == 'Cl*')]
    dup_pn_ms = dup_ms[(dup_ms["OTYPE_3"] == 'PN')]
    dup_ga_ms = dup_ms[(dup_ms["OTYPE_3"] == 'G') | (dup_ms["OTYPE_3"] == 'Sy2') | (dup_ms["OTYPE_3"] == 'IG') | (
                dup_ms["OTYPE_3"] == 'GiG') | (dup_ms["OTYPE_3"] == 'GiP') | (dup_ms["OTYPE_3"] == 'SyG') | (
                                   ms["OTYPE_3"] == 'SBG') | (dup_ms["OTYPE_3"] == 'BiC') | (
                                   dup_ms["OTYPE_3"] == 'H2G')]
    dup_re_ms = dup_ms[(dup_ms["OTYPE_3"] == 'HII') | (dup_ms["OTYPE_3"] == 'As*') | (dup_ms["OTYPE_3"] == 'LIN') | (
                dup_ms["OTYPE_3"] == 'mul') | (dup_ms["OTYPE_3"] == 'RNe') | (dup_ms["OTYPE_3"] == 'AGN')]

    print(f"Observing RA: {ra} deg, DEC: {dec} deg, Calculated FoV: {fov} deg, Calculated Limiting Magnitude: {mag}")

    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', color="#838383")
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='white')
    ax.set_facecolor('#dbdbdb')

    # if user input ra is nearer to 360 deg, the region near 0 is plotted; here the duplicated and transformed data from above is useful
    if xr > 360:
        ra -= 360
        xr -= 360
        xl -= 360

    # scatter messier
    ax.scatter(cl_ms['RAJ2000'], cl_ms['DEJ2000'], color='yellow', marker=cl, s=cl_ms['V'] * 1000 / fov, zorder=2,
               edgecolor="black", linewidth=40 / fov)
    ax.scatter(pn_ms['RAJ2000'], pn_ms['DEJ2000'], color='black', marker=pn4, s=pn_ms['V'] * 4000 / fov, zorder=2)
    # ax.scatter(pn_ms['RAJ2000'], pn_ms['DEJ2000'], color='green', marker=cl, s=pn_ms['V'] * 1000 / fov, zorder=3)
    ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ga, s=ga_ms['V'] * 1000 / fov, zorder=2)
    ax.scatter(re_ms['RAJ2000'], re_ms['DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=re_ms['V'] * 10 / fov)

    # scatter ngc
    ax.scatter(mag_ng['_RAJ2000'], mag_ng['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=mag_ng['mag'] * 1000 / fov)
    ax.scatter(dup_ng['_RAJ2000'], dup_ng['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=dup_ng['mag'] * 1000 / fov)

    # scatter tycho
    ax.scatter(mag_ty['_RAJ2000'], mag_ty['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=mag_ty['V'] * 1000 / fov)
    ax.scatter(dup_ty['_RAJ2000'], dup_ty['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=dup_ty['V'] * 1000 / fov)

    # constellation borders
    for i in cb['Constellation'].unique():
        ax.scatter(cb[(cb['Constellation'] == i)]['RAJ2000'], cb[(cb['Constellation'] == i)]['DEJ2000'], color='blue',
                   s=20 / fov)

    # test markers
    #     ax.scatter([10],[40],marker= cl, s=1000)
    #     ax.scatter([0],[20+10],marker= cl, s=1000)
    #     ax.scatter([0],[20+10],marker= pn4, s=4000)
    #     ax.scatter([20],[50],marker= ga, s=10000)
    #     ax.scatter([20],[0], edgecolor='white',s=10000, linewidth=200/fov, color='black')
    #     ax.scatter([20],[40],marker=pl, s=10000, edgecolor='black', linewidth=0)
    #     ax.scatter([0],[50],marker=cp, s=10000, edgecolor='black', linewidth=0, alpha=0.5)
    #     ax.scatter([0],[60],marker=pn4, s=100, linewidth=2/fov)

    ax.add_artist(plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.1))

    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])

    ax.set_yticklabels([round(y, 2) for y in ax.get_yticks()])
    ax.set_xticklabels([(x + 360) if x < 0 else round(x, 2) for x in ax.get_xticks()])

    plt.xlabel('Right Ascension (degrees)', fontsize=16)
    plt.ylabel('Declination (degrees)', fontsize=16)

    cluster = mlines.Line2D([], [], color='yellow', marker=cl, linestyle='None',
                              markersize=20, label='Clusters', markeredgecolor="black", markeredgewidth=1)
    plantary_neb = mlines.Line2D([], [], color='green', marker=cl, linestyle='None',
                              markersize=20, label='Planetory Nebula')
    planetary_neb2 = mlines.Line2D([], [], color='black', marker=pn4, linestyle='None',
                              markersize=20, label='Planetory Nebula')
    galaxy = mlines.Line2D([], [], color='Red', marker=ga, linestyle='None',
                              markersize=20, label='Galaxies')
    rest = mlines.Line2D([], [], color='Black', marker=cl, linestyle='None',
                              markersize=20, label='Rest', markeredgecolor="white", markeredgewidth=1)
    plt.legend(handles=[cluster,planetary_neb2, galaxy, rest], labelspacing=5, ncol=4, borderpad=1, loc='lower center')

    #     cst_names=cb['Constellation'].unique()
    #     cbcx=[]
    #     cbcy=[]
    #     for i in cst_names:
    #         cbcx.append((cb[(cb['Constellation']==i)]['RAJ2000'].min()+cb[(cb['Constellation']==i)]['RAJ2000'].max())/2)
    #         cbcy.append((cb[(cb['Constellation']==i)]['DEJ2000'].min()+cb[(cb['Constellation']==i)]['DEJ2000'].max())/2)

    #     for i, txt in enumerate(cst_names):
    #         ax.annotate(txt, (cbcx[i], cbcy[i]), xytext=(0, 0), textcoords='offset points', horizontalalignment='center', verticalalignment='center')
    #         print(txt)
    plt.show()
# func1(299, 20, 20, 50, 100)

# Use the following function to enter any limiting magnitude and fov values
# mag is the limiting magnitude
def func2(ra, dec, mag, fov):
    #     x=np.pi/180
    # cos(A) = sin(Decl.1)sin(Decl.2) + cos(Decl.1)cos(Decl.2)cos(RA.1 - RA.2); formula for the angular seperation
    # distance of each object from user input of ra, dec
    #     ng["distance"]=np.arccos(np.sin(dec*x)*np.sin(ng["_DEJ2000"]*x)+np.cos(dec*x)*np.cos(ng["_DEJ2000"]*x)*np.cos(ra*x-ng["_RAJ2000"]*x))*(180/np.pi)
    #     ms["distance"]=np.arccos(np.sin(dec*x)*np.sin(ms["DEJ2000"]*x)+np.cos(dec*x)*np.cos(ms["DEJ2000"]*x)*np.cos(ra*x-ms["RAJ2000"]*x))*(180/np.pi)
    #     ty["distance"]=np.arccos(np.sin(dec*x)*np.sin(ty["_DEJ2000"]*x)+np.cos(dec*x)*np.cos(ty["_DEJ2000"]*x)*np.cos(ra*x-ty["_RAJ2000"]*x))*(180/np.pi)

    # sorting objects under the user input of limiting magnitude;
    # also duplicating the the objects and transforming them so they are repeated to the left of y-axis
    mag_ng = ng[(ng["mag"] <= mag)]
    mag_ms = ms[(ms['V'] <= mag)]
    mag_ty = ty[(ty['V'] <= mag)]
    dup_ng = mag_ng.copy(deep=True)
    dup_ms = mag_ms.copy(deep=True)
    dup_ty = mag_ty.copy(deep=True)
    dup_ng['_RAJ2000'] -= 360
    dup_ms['RAJ2000'] -= 360
    dup_ty['_RAJ2000'] -= 360

    fig, ax = plt.subplots(figsize=(20, 15))
    ax.set_aspect('equal')

    # breathing space around the fov circle in the plot
    xl = ra - fov / 2 - fov / 10
    xr = ra + fov / 2 + fov / 10
    yb = dec - fov / 2 - fov / 10
    yt = dec + fov / 2 + fov / 10

    # sorting objects in messier_objects.csv according to objects
    cl_ms = ms[(ms["OTYPE_3"] == 'OpC') | (ms["OTYPE_3"] == 'GlC') | (ms["OTYPE_3"] == 'Cl*')]
    pn_ms = ms[(ms["OTYPE_3"] == 'PN')]
    ga_ms = ms[
        (ms["OTYPE_3"] == 'G') | (ms["OTYPE_3"] == 'Sy2') | (ms["OTYPE_3"] == 'IG') | (ms["OTYPE_3"] == 'GiG') | (
                ms["OTYPE_3"] == 'GiP') | (ms["OTYPE_3"] == 'SyG') | (ms["OTYPE_3"] == 'SBG') | (
                ms["OTYPE_3"] == 'BiC') | (ms["OTYPE_3"] == 'H2G')]
    re_ms = ms[
        (ms["OTYPE_3"] == 'HII') | (ms["OTYPE_3"] == 'As*') | (ms["OTYPE_3"] == 'LIN') | (ms["OTYPE_3"] == 'mul') | (
                ms["OTYPE_3"] == 'RNe') | (ms["OTYPE_3"] == 'AGN')]
    # duplicated data sort by object type
    dup_cl_ms = dup_ms[(dup_ms["OTYPE_3"] == 'OpC') | (dup_ms["OTYPE_3"] == 'GlC') | (dup_ms["OTYPE_3"] == 'Cl*')]
    dup_pn_ms = dup_ms[(dup_ms["OTYPE_3"] == 'PN')]
    dup_ga_ms = dup_ms[(dup_ms["OTYPE_3"] == 'G') | (dup_ms["OTYPE_3"] == 'Sy2') | (dup_ms["OTYPE_3"] == 'IG') | (
            dup_ms["OTYPE_3"] == 'GiG') | (dup_ms["OTYPE_3"] == 'GiP') | (dup_ms["OTYPE_3"] == 'SyG') | (
                               ms["OTYPE_3"] == 'SBG') | (dup_ms["OTYPE_3"] == 'BiC') | (
                               dup_ms["OTYPE_3"] == 'H2G')]
    dup_re_ms = dup_ms[(dup_ms["OTYPE_3"] == 'HII') | (dup_ms["OTYPE_3"] == 'As*') | (dup_ms["OTYPE_3"] == 'LIN') | (
            dup_ms["OTYPE_3"] == 'mul') | (dup_ms["OTYPE_3"] == 'RNe') | (dup_ms["OTYPE_3"] == 'AGN')]

    print(f"Observing RA: {ra} deg, DEC: {dec} deg, FoV: {fov} deg, Limiting Magnitude: {mag}")

    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', color="#838383")
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='white')
    ax.set_facecolor('#dbdbdb')

    # if user input ra is nearer to 360 deg, the region near 0 is plotted; here the duplicated and transformed data from above is useful
    if xr > 360:
        ra -= 360
        xr -= 360
        xl -= 360

    # scatter messier
    ax.scatter(cl_ms['RAJ2000'], cl_ms['DEJ2000'], color='yellow', marker=cl, s=cl_ms['V'] * 1000 / fov, zorder=2,
               edgecolor="black", linewidth=40 / fov)
    ax.scatter(pn_ms['RAJ2000'], pn_ms['DEJ2000'], color='black', marker=pn, s=pn_ms['V'] * 4000 / fov, zorder=2)
    # ax.scatter(pn_ms['RAJ2000'], pn_ms['DEJ2000'], color='green', marker=cl, s=pn_ms['V'] * 1000 / fov, zorder=3)
    ax.scatter(ga_ms['RAJ2000'], ga_ms['DEJ2000'], color='red', marker=ga, s=ga_ms['V'] * 1000 / fov, zorder=2)
    ax.scatter(re_ms['RAJ2000'], re_ms['DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=re_ms['V'] * 10 / fov)

    # scatter ngc
    ax.scatter(mag_ng['_RAJ2000'], mag_ng['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=mag_ng['mag'] * 1000 / fov)
    ax.scatter(dup_ng['_RAJ2000'], dup_ng['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=dup_ng['mag'] * 1000 / fov)

    # scatter tycho
    ax.scatter(mag_ty['_RAJ2000'], mag_ty['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=mag_ty['V'] * 1000 / fov)
    ax.scatter(dup_ty['_RAJ2000'], dup_ty['_DEJ2000'], c='black', edgecolor="white", linewidth=40 / fov, label='Stars',
               s=dup_ty['V'] * 1000 / fov)

    # constellation borders
    # for i in cb['Constellation'].unique():
    #     ax.scatter(cb[(cb['Constellation'] == i)]['RAJ2000'], cb[(cb['Constellation'] == i)]['DEJ2000'], color='blue',s=20 / fov)

    # test markers
    #     ax.scatter([10],[40],marker= cl, s=1000)
    #     ax.scatter([0],[20+10],marker= cl, s=1000)
    #     ax.scatter([0],[20+10],marker= pn4, s=4000)
    #     ax.scatter([20],[50],marker= ga, s=10000)
    #     ax.scatter([20],[0], edgecolor='white',s=10000, linewidth=200/fov, color='black')
    #     ax.scatter([20],[40],marker=pl, s=10000, edgecolor='black', linewidth=0)
    #     ax.scatter([0],[50],marker=cp, s=10000, edgecolor='black', linewidth=0, alpha=0.5)
    #     ax.scatter([0],[60],marker=pn4, s=100, linewidth=2/fov)

    ax.add_artist(plt.Circle((ra, dec), fov / 2, color='#00af08', zorder=-1, alpha=0.1))

    ax.set_xlim([xl, xr])
    ax.set_ylim([yb, yt])

    ax.set_yticklabels([round(y, 2) for y in ax.get_yticks()])
    ax.set_xticklabels([(x + 360) if x < 0 else round(x, 2) for x in ax.get_xticks()])

    plt.xlabel('Right Ascension (degrees)', fontsize=16)
    plt.ylabel('Declination (degrees)', fontsize=16)

    cst_names = cb['Constellation'].unique()
    cbcx = []
    cbcy = []

    cluster = mlines.Line2D([], [], color='yellow', marker=cl, linestyle='None',
                              markersize=20, label='Clusters', markeredgecolor="black", markeredgewidth=1)
    plantary_neb = mlines.Line2D([], [], color='green', marker=cl, linestyle='None',
                              markersize=20, label='Planetory Nebula')
    planetary_neb2 = mlines.Line2D([], [], color='black', marker=pn4, linestyle='None',
                              markersize=20, label='Planetory Nebula')
    galaxy = mlines.Line2D([], [], color='Red', marker=ga, linestyle='None',
                              markersize=20, label='Galaxies')
    rest = mlines.Line2D([], [], color='Black', marker=cl, linestyle='None',
                              markersize=20, label='Rest', markeredgecolor="white", markeredgewidth=1)
    plt.legend(handles=[cluster,planetary_neb2, galaxy, rest], labelspacing=5, ncol=4, borderpad=1, loc='lower center')

    # naming constellations
    # for i in cst_names:
    #     cbcx.append((cb[(cb['Constellation'] == i)]['RAJ2000'].min() + cb[(cb['Constellation'] == i)]['RAJ2000'].max()) / 2)
    #     cbcy.append((cb[(cb['Constellation'] == i)]['DEJ2000'].min() + cb[(cb['Constellation'] == i)]['DEJ2000'].max()) / 2)

    # for i, txt in enumerate(cst_names):
    #     ax.annotate(txt, (cbcx[i], cbcy[i]), xytext=(0, 0), textcoords='offset points', horizontalalignment='center', verticalalignment='center')
    plt.show()
func2(300, 20, 4, 100)

