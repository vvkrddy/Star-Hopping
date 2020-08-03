#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:42:35 2020

@author: sahyadri
"""


from astroquery.vizier import Vizier
from astroquery.simbad import Simbad
import requests
from bs4 import BeautifulSoup
import numpy as np
from astropy.table import Table, vstack
from astropy.io import ascii
from astropy import units as u
from astropy.coordinates import SkyCoord, get_constellation
import pandas as pd
import glob, os

print('Downloading constellation_borders.csv...')
# This loads all the catalogs by the keyword "constellation"
catalogue_list = Vizier.find_catalogs("Constellation")
Vizier.ROW_LIMIT = -1
# Following table contains the relevant data
catalog = Vizier.get_catalogs("VI/49")[1]
catalog.remove_columns(['cst', 'type'])
coords = SkyCoord(catalog['RAJ2000'], catalog['DEJ2000'], unit="deg")
const = coords.get_constellation()
const = ['Bootes' if x == 'Boötes' else x for x in const]  # fixing for the unicode problem
catalog.add_column(const, name="Constellation", index=2)
catalog.write("constellation_borders.csv", format="csv", overwrite="True")
print('Done - Constellation borders\n')

print('Downloading messier_objects.csv...')

#Download magnitdue data from astropixels/SEDS
page = requests.get("http://astropixels.com/messier/messiercat.html")
soup = BeautifulSoup(page.content,'html.parser')
table = soup.find_all('tbody')[0]
rows = table.find_all('tr')
mag = []
for items in rows:
    mag.append(items.find_all('td')[3].get_text())

# The next three lines are to simplify the output table
Simbad.reset_votable_fields()
Simbad.remove_votable_fields('coordinates')
# These are all the columns added to the table
Simbad.add_votable_fields('otype(3)', 'ra(d;A;ICRS;J2000;2000)', 'dec(d;D;ICRS;J2000;2000)', 'flux(B)', 'flux(V)')
# This asks the SIMBAD database to list all objects from the messier catalog
result_table = Simbad.query_catalog("Messier")
result_table['FLUX_V'].name = 'V'
result_table['OTYPE_3'] = np.array([x.decode('utf8') for x in result_table['OTYPE_3']])
result_table['MAIN_ID'] = np.array([x.decode('utf8') for x in result_table['MAIN_ID']])
result_table['RA_d_A_ICRS_J2000_2000'].name = "RAJ2000"
result_table['DEC_d_D_ICRS_J2000_2000'].name = "DEJ2000"
result_table['B-V'] = result_table['FLUX_B'] - result_table['V']
result_table.remove_column('FLUX_B')
result_table.rename_column('OTYPE_3', 'TYPE')

coords = SkyCoord(result_table['RAJ2000'], result_table['DEJ2000'], unit="deg")
const = coords.get_constellation()
const = ['Bootes' if x == 'Boötes' else x for x in const]  # fixing for the unicode problem
const_abr = coords.get_constellation(short_name="True")
result_table.add_column(const, name="Constellation", index=2)

m = ['M {}'.format(i + 1) for i in range(len(const))]
result_table.add_column(m, name='ID (for resolver)', index=0)

otype = result_table['TYPE']
internal_id = ['{}_{}_M{}'.format(otype[i], const_abr[i], str(i + 1)) for i in range(len(const))]
result_table.add_column(internal_id, name="Internal ID Number", index=0)

#Adding common names of the messier objects
link = requests.get('https://en.wikipedia.org/wiki/Messier_object')
soup = BeautifulSoup(link.content,'html.parser')
table = soup.find_all('table',attrs={"class":"wikitable sortable"})[0]
names = []    
name_rows = table.find_all('td')[1::9]
for items in name_rows:
    if items.get_text()=='–\n':
        names.append('-')
    else:
        names.append(items.get_text().strip('\n'))
nURL = 'https://en.wikipedia.org/wiki/Messier_object'
npage = requests.get(nURL)
nsoup = BeautifulSoup(npage.content, 'html.parser')
ngc=[]
for i in range(23,1013,9):
    ngc.append(nsoup.find_all('td')[i].get_text().strip())
result_table.add_column(names,name="Common Name",index=3)
result_table.add_column(mag,name="V (from SEDS)",index=8)
result_table.add_column(ngc, name="NGC", index=2)
messier_table = result_table

result_table.write("messier_objects.csv", format="csv", overwrite="True")# creates a csv file

Simbad.reset_votable_fields()  # renders the prev changes to simbad class temporary.
print('Done - Messier objects\n')

print('Downloading NGC.csv...')

v = Vizier(columns=['Name', 'Type', 'mag','RA (deg)', 'Dec (deg)'])  # Columns added to table
v.ROW_LIMIT = -1
result_table = v.get_catalogs("VII/118/ngc2000")[0]

# Changing the type and name - making more uniform.
result_table['Name'] = np.array(['IC ' + x[1:] if x[0] == 'I' else 'NGC ' + x for x in result_table['Name']])
result_table['Type'] = np.array([
                                    'Gal' if x == 'Gx' else 'OpC' if x == 'OC' else 'GlC' if x == 'Gb' else 'PN' if x == 'Pl' else 'Str' if x == '*' or x == 'D*' or x == '***' else '-' if x == '' or x == '-' or x == '?' else x
                                    for x in result_table['Type']])
result_table['Name'] = [" ".join(x.split()) for x in result_table['Name']]

# Adding constellation names
coords = SkyCoord(result_table['_RAJ2000'], result_table['_DEJ2000'], unit="deg")
const = coords.get_constellation()
const = ['Bootes' if x == 'Boötes' else x for x in const]  # fixing for the unicode problem
const_abr = coords.get_constellation(short_name="True")
result_table.add_column(const, name="Constellation", index=2)

result_table.add_column(np.zeros(len(result_table)), name="Messier")
ngc_desig=[]
for x in messier_table['NGC']:
    ngc_desig.append(x.split(',')[0].strip())
    try:
        ngc_desig.append(x.split(',')[1].strip())
    except:
        None
for x in ngc_desig:
    for i in range(len(result_table)):
        if x == result_table['Name'][i]:
            result_table['Messier'][i]=1
            
# Adding an internal id number
otype = result_table['Type']
internal_id = [
    '{}_{}_{}'.format(otype[i], const_abr[i], result_table['Name'][i]) if otype[i] != '-' else 'notype_{}_{}'.format(
        const_abr[i], result_table['Name'][i]) for i in range(len(const))]
result_table.add_column(internal_id, name="Internal ID Number", index=0)
result_table.rename_column('mag', 'V')
result_table.rename_column('_RAJ2000', 'RAJ2000')
result_table.rename_column('_DEJ2000', 'DEJ2000')
result_table.write("NGC.csv", format="csv", overwrite="True")

# Cross-reference catalogue for NGC
v = Vizier(columns=['Object', 'Name'])
v.ROW_LIMIT = -1
v.TIMEOUT = 1000
cross_catalog = v.get_catalogs('VII/118/names')[0]

cross_catalog['Name'] = [
    'IC {}'.format(x.split()[1]) if len(x.split()) == 2 and x.split()[0] == "I" else 'IC {}'.format(
        x.split()[0][1:]) if len(x.split()) == 1 and x[0] == "I" else 'NGC {}'.format(x) for x in cross_catalog['Name']]
name = np.array([len(x.split()) for x in cross_catalog['Name']])
index = np.array(np.where(name == 1)[0])
cross_catalog['Name'][index] = ['NGC 6603', 'NGC 7092', 'NGC 1432', 'NGC 5866']  # manual editing
cross_catalog.write("DsCrossCatalog.csv", format='csv', overwrite="True")

# Adding common names of some NGC objects
ccat = pd.read_csv('DsCrossCatalog.csv')
ccat = pd.DataFrame(ccat)
ccat = ccat.groupby('Name')['Object'].apply(lambda x: ', '.join(x)).reset_index()
ntable = pd.read_csv('NGC.csv')
ntable = pd.DataFrame(ntable)
ntable.insert(2, "Common Name", np.zeros(len(ntable['RAJ2000'])))
ntable['Common Name'] = ntable.Name.map(ccat.set_index('Name').Object, na_action="ignore")
ntable['Common Name'] = ntable['Common Name'].fillna('-')

#Changing the coordinates of messier objects to refernece SIMBAD for uniformity
#find_res = np.array([x.find('M') for x in ntable['Common Name']])
#pos = np.where(find_res!=-1)[0]
#rd = [x for x in ntable['Name'][pos]]
#Simbad.TIME_OUT = -1
#Simbad.reset_votable_fields()
#Simbad.ROW_LIMIT = 100000
#Simbad.remove_votable_fields('coordinates')
#Simbad.add_votable_fields('ra(d;A;ICRS;J2000;2000)', 'dec(d;D;ICRS;J2000;2000)')
#names = np.array(rd)
#radec = Simbad.query_objects(names)
#ra = [x for x in radec['RA_d_A_ICRS_J2000_2000']]
#dec = [x for x in radec['DEC_d_D_ICRS_J2000_2000']]
#Simbad.reset_votable_fields()
#pos = [x for x in pos]

#ntable.loc[pos,'RAJ2000'] = ra
#ntable.loc[pos,'DEJ2000'] = dec

ntable.to_csv('NGC.csv')
ntable = Table.read('NGC.csv')
ntable.remove_columns(['col0'])
ntable.write('NGC.csv', format='csv', overwrite="True")

print('Done - NGC')

# Download the star name file
# kaggle.api.authenticate()
# kaggle.api.dataset_download_files('ecotner/named-stars/IAU-CSN.csv', path='/home/sahyadri/Desktop/Star-Hopping', unzip=True)

# CROSS CATALOG
v = Vizier(columns=['HD', 'TYC', 'HIP', 'Vmag', 'Fl', 'Bayer', 'Cst'])
v.ROW_LIMIT = -1
v.TIMEOUT = 1000
cross_catalog = v.get_catalogs('IV/27A/catalog')[0]
bayer_const = ['{} {}'.format(x['Bayer'], x['Cst']) if len(x['Bayer'])!=0 else '{} {}'.format(x['Fl'], x['Cst']) for x in cross_catalog]
cross_catalog.remove_columns("Bayer")
cross_catalog['BayerConst'] = bayer_const
cross_catalog.write("CrossCatalog.csv", format='csv', overwrite="True")

ccat = pd.read_csv('CrossCatalog.csv')
ccat = pd.DataFrame(ccat)
ccat["HIP"].fillna("0", inplace=True)
miss_index = np.where(ccat['HIP'] == '0')[0]
hd_missing = np.array(ccat['HD'][miss_index])
hip = []  # will containt all missing values
for items in hd_missing:
    ident_table = np.array(Simbad.query_objectids("HD " + str(items)))
    ident_table = np.array([x[0].decode('utf8') for x in ident_table])
    if any(['HIP' in x.split()[0] for x in ident_table]):
        ind = np.where(['HIP' in x.split()[0] for x in ident_table])[0]
        hip.append(ident_table[ind][0].split()[1])
    else:
        hip.append('0')
        
cross_catalog['HIP'][miss_index] = hip
cross_catalog.write("CrossCatalog.csv", format='csv', overwrite="True")

print('Tycho-1 Catalogue: ')

run_count = 0
run = True
last_id = 0

# first iteration downloads upto 6 magnitude (cannot skip)
# later prompts for user input to continue in increments of 3 upto 12 mag
minV = ''
maxV = 6

while run:

    #     MinVm = input('(INT ONLY) Input minimum value of Vmag (skippable) ',)
    #     MaxVmag = float(input('(INT ONLY) Input maximum value of Vmag (MAX 12)',))

    #     if type(MaxVmag)!=float:
    #         print("invalid entry")
    #         continue
    #     elif MaxVmag>12:
    #         print("Input a number less than or equal to 12 for tycho-1")
    #         continue

    if minV != '':
        minV = int(minV)
    run_count += 1
    if minV == '':
        filter_input = "<{}".format(maxV)
    else:
        filter_input = "{}..{}".format(minV, maxV)

    print("Downloading upto {} mag ...".format(maxV))

    # Query
    v = Vizier(columns=['HIP', 'TYC', 'HD', '_RAJ2000', '_DECJ2000', '+Vmag', 'B-V'],
               column_filters={"Vmag": "{}".format(filter_input)})
    v.ROW_LIMIT = 1000000000
    v.TIMEOUT = 1000
    catalog_stars = v.get_catalogs("I/239/tyc_main")[0]
    catalog_stars['Vmag'].name = "V"

    # Adding constellation names
    coords = SkyCoord(catalog_stars['_RAJ2000'], catalog_stars['_DEJ2000'], unit="deg")
    const = coords.get_constellation()
    const = ['Bootes' if x == 'Boötes' else x for x in const]  # fixing for the unicode problem
    const_abr = coords.get_constellation(short_name="True")

    catalog_stars.add_column(const, name="Constellation", index=0)

    # adding internal id
    internal_id = ["Str_{}_{:08d}".format(const_abr[i], i + last_id + 1) for i in range(len(catalog_stars['_RAJ2000']))]
    catalog_stars.add_column(internal_id, name="Internal ID Number", index=0)

    catalog_stars.rename_column('_RAJ2000', 'RAJ2000')
    catalog_stars.rename_column('_DEJ2000', 'DEJ2000')

    catalog_stars.write("tycho_{}.csv".format(run_count), format="csv", overwrite="True")
    last_id = last_id + len(catalog_stars['RAJ2000'])

    # Adding common names to the stars
    names_table = pd.read_csv('IAU-CSN.csv')
    names_table = pd.DataFrame(names_table)
    ttable = pd.read_csv('tycho_{}.csv'.format(run_count), dtype={"Name": "string"})
    ttable = pd.DataFrame(ttable)
    names_table["HIP"] = np.array([x if x != '-' else 0 for x in names_table["HIP"]])
    ttable.insert(1, "Name", np.zeros(len(ttable['TYC'])))
    names_table["HIP"] = pd.to_numeric(names_table['HIP'], errors='coerce')
    ttable['Name'] = ttable.HIP.map(names_table.set_index('HIP').Name)
    ttable['Name']= ttable['Name'].fillna('-')
    ttable.to_csv('tycho_{}.csv'.format(run_count))

    # The cross cataloguing part
    ccat = pd.read_csv('CrossCatalog.csv')
    ccat = pd.DataFrame(ccat)
    ccat["HIP"].fillna("0", inplace=True)
    ttable = pd.read_csv('tycho_{}.csv'.format(run_count), dtype={"Name": "string"})
    ttable = pd.DataFrame(ttable)
    ccat = ccat.loc[~ccat.HIP.duplicated(keep='first')]
    ttable.insert(4, "Bayer", np.zeros(len(ttable['RAJ2000'])))
    ttable['Bayer'] = ttable.HIP.map(ccat.set_index('HIP').BayerConst, na_action="ignore")
    ttable['Bayer']= ttable['Bayer'].fillna('')
    if maxV==6:
        ttable['Bayer']=np.where(ttable.Bayer=='',ttable.HD.map(ccat.set_index('HD').BayerConst, na_action="ignore"),ttable.Bayer)
        ttable['Bayer']=ttable['Bayer'].fillna('')
    del ttable['Unnamed: 0']
    if run_count == 1:
        ttable.to_csv('tycho-1.csv', index=False)
    else:
        ttable.to_csv('tycho-1.csv', mode='a', header=False, index=False)

    # below is where the +3 increment takes places
    minV = maxV
    maxV += 3

    while True:
        if (maxV <= 12):
            if maxV == 12:
                maxV = 10.5
            status = input("Download upto {} mag? (y/n)".format(maxV))
            if status == "n":
                run = False
                break
            elif status == "y":
                run = True
                break
            else:
                print("invalid answer")
        else:
            run = False
            break
for file in glob.glob("tycho_*.csv"):
    os.remove(file)

# os.rename('tycho-1.csv','tycho-1_{}.csv'.format(maxV)) # final file will be tycho-1_{maximum_magnitude}.csv

print("Done")

# Tycho-2 Catalogue from 10.5 mag to 12 mag
print('Tycho-2 Catalogue - from Vmag 10.5 to 12')
print('NOTE: Large file, may take some time.')  # user is warned of large file size

run = True
while run:

    tycho2 = input("Would you like to download Tycho-2 Catalogue from 10.5 to 12?(y/n)")
    # only if user accepts, the download takes place
    if (tycho2 == 'y'):
        print('Downloading...')
        # The catalogue download
        v = Vizier(columns=['HIP', '_RAJ2000', 'DECJ2000', 'BTmag', '+VTmag'], column_filters={"VTmag": "10.2..12.3"})
        v.ROW_LIMIT = -1
        v.TIMEOUT = 1000
        catalog_stars = v.get_catalogs("I/259/tyc2")[0]
        vmag = catalog_stars['VTmag'] - 0.09 * (catalog_stars['BTmag'] - catalog_stars['VTmag'])
        catalog_stars.add_column(vmag, name='Vmag', index=5)
        catalog_stars['Vmag'].name = "V"
        catalog_stars['V'].sort()

        # Filtering
        v = np.array([x if x != '--' else 0 for x in catalog_stars['V']])
        ind1 = np.where(v > 12)[0]
        ind2 = np.where(v < 10.5)[0]
        ind = np.concatenate((ind1, ind2))
        catalog_stars.remove_rows(ind)

        # adding constellation names
        coords = SkyCoord(catalog_stars['_RAJ2000'], catalog_stars['_DEJ2000'], unit="deg")
        const = coords.get_constellation()
        const = ['Bootes' if x == 'Boötes' else x for x in const]  # fixing for the unicode problem
        const_abr = coords.get_constellation(short_name="True")
        bv = np.array(catalog_stars['BTmag']) - np.array(catalog_stars['VTmag'])
        catalog_stars.add_column(bv, name='BT-VT', index=6)
        catalog_stars.remove_columns(['BTmag', 'VTmag'])
        # adding internal id and saving
        internal_id = ["Str_{}_{:08d}".format(const_abr[i], i + last_id + 1) for i in
                       range(len(catalog_stars['_RAJ2000']))]
        catalog_stars.add_column(internal_id, name="Internal ID Number", index=0)
        catalog_stars.add_column(const, name="Constellation", index=1)

        catalog_stars.rename_column('_RAJ2000', 'RAJ2000')
        catalog_stars.rename_column('_DEJ2000', 'DEJ2000')

        catalog_stars.write("tycho-2.csv", format="csv", overwrite="True", fast_writer=True)
        break
    elif (tycho2 == 'n'):
        break
    else:
        print("Invalid choice")

# os.remove('DsCrossCatalog.csv')
# os.remove('CrossCatalog.csv')

print('Done')
