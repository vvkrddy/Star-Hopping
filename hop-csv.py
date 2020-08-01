import pickle
import pandas as pd

hop_file = open("hop.pkl", "rb")
d = pickle.load(hop_file)
ms = pd.read_csv('messier_objects.csv', low_memory=False)
ty = pd.read_csv('tycho-1.csv', low_memory=False)
ty['Bayer'] = ty['Bayer'].fillna('-')
# print(d)

for key, value in d.items():
    print(key, value)

column_names =  list(range(1,11,1))
column_names.append('Instruction')
column_names.insert(0,"Messier")
print(column_names)

df = pd.DataFrame(columns = column_names)
messier = list(d.keys())
df['Messier']=messier
print(df)



for i in range(len(messier)):
    for j in range(len(d[messier[i]])-2):
#         print(i,j)
        df[j+1][df.index[df['Messier'] == messier[i]]] = ','.join(str(v) for v in d[messier[i]][j])
        df[j+1][df.index[df['Messier'] == messier[i]]] = df[j+1][df.index[df['Messier'] == messier[i]]].astype(str)+','+(ty['Name'][ty.index[ty["RAJ2000"]==d[messier[i]][j][0]]].values)
        df[j+1][df.index[df['Messier'] == messier[i]]] = df[j+1][df.index[df['Messier'] == messier[i]]].astype(str)+','+(ty['Bayer'][ty.index[ty["RAJ2000"]==d[messier[i]][j][0]]].values)
#         df[j+1][df.index[df['Messier'] == messier[i]]] = df[j+1][df.index[df['Messier'] == messier[i]]].astype(str)+','+(ty['V'][ty.index[ty["V"]==d[messier[i]][j][0]]].values)

#     messier_coord=[float(ms['RAJ2000'][ms.index[ms['ID (for resolver)']==messier[i]]]), float(ms['DEJ2000'][ms.index[ms['ID (for resolver)']==messier[i]]])]
# #     df[len(d[messier[i]])][df.index[df['Messier'] == messier[i]]] = ','.join(str(v) for v in messier_coord)
    df[len(d[messier[i]])-1][df.index[df['Messier'] == messier[i]]] = ','.join(str(v) for v in d[messier[i]][-2]) +','+ messier[i]
    if d[messier[i]][-1] == None or d[messier[i]][-1] =='':
        df['Instruction'][df.index[df['Messier'] == messier[i]]] = '-'
    else:
        df['Instruction'][df.index[df['Messier'] == messier[i]]] = d[messier[i]][-1]
print(df)
df.sort_values(by=['Messier'], inplace=True)

df.to_csv("hops.csv", index=False)