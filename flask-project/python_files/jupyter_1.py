import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

colnames=['symboling', 'normalized-losses', 'company', 'fuel-type', 'aspiration', 'num-of-doors', 'body-style', 
         'drive-wheels', 'engine-location', 'wheel-base', 'length', 'width', 'height', 'curb-weight', 
          'engine-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'bore', 'stroke', 'compression-ratio', 
          'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg', 'price'] 


data = pd.read_csv("./DATA1/imports-85.data", sep=',', names=colnames, header=None)
for i in colnames:
    data.loc[data[i] == '?', i] = np.nan
del data['symboling']


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


data[['city-mpg']] = round(data[['city-mpg']] / 2.352, 2)
data[['highway-mpg']] = round(data[['highway-mpg']] / 2.352, 2)
data.rename(columns={'city-mpg': 'city-km/l'}, inplace = True)
data.rename(columns={'highway-mpg': 'highway-km/l'}, inplace = True)
data['horsepower'] = pd.to_numeric(data['horsepower'])
data['peak-rpm'] = pd.to_numeric(data['peak-rpm'])

tables, titles = [data.to_html(classes='data')], data.columns.values

    

'''
# Scatter plot of mean of price
data['price'] = data1 = data['price'].fillna(data['price'][0]).astype('int64')
mean = data['price'].fillna(data['price'][0]).astype('int64').mean()
min_value = min(data1)
max_value = max(data1)
plt.title("Price Dataset")
plt.ylim(min_value - 10000, max_value + 10000)
plt.scatter(x=data.index, y=data['price'])
plt.hlines(y=mean, xmin=0, xmax=len(data1)) # average
plt.hlines(y=min(data1), xmin=0, xmax=len(data), colors='r') # lowest
plt.hlines(y=max(data1), xmin=0, xmax=len(data), colors='g') # highest
figfile = io.BytesIO()
plt.savefig(figfile, format='jpeg')
plt.clf()
'''
# lets calculate mean of wheel-base for drive-wheels
tables1, titles1 = [data.pivot_table(index=["drive-wheels"], values = ['wheel-base'], aggfunc = 'mean').to_html(classes='data')], \
    data.pivot_table(index=["drive-wheels"], values = ['wheel-base'], aggfunc = 'mean').columns.values


# lets calculate mean of horsepower, city-km/l and highway-km/l for engine-type

tables2, titles2 = [data.pivot_table(index=["engine-type"], values = ['horsepower', 'city-km/l', 'highway-km/l'], \
                 aggfunc = 'mean', fill_value = 0).round(2).to_html(classes='data')], \
                     data.pivot_table(index=["engine-type"], values = ['horsepower', 'city-km/l', 'highway-km/l'], \
                 aggfunc = 'mean', fill_value = 0).round(2).columns.values

'''
# Medians of length, width, height and curb-weight
d = {'length': data['length'].median(), 
     'width': data['width'].median(),
     'height': data['height'].median(),
     'curb-weight': data['curb-weight'].median()}
print('   MEDIANs')
for i in range(len(d)):
    print(list(d.keys())[i],':', list(d.values())[i])
print('\n\n')
# Medians compared to body-style
'''
tables3, titles3 = [data.pivot_table(index=["body-style"], values = ['length', 'width', 'height', 'curb-weight'], \
                 aggfunc = 'median', fill_value = 0).to_html(classes='data')], \
                    data.pivot_table(index=["body-style"], values = ['length', 'width', 'height', 'curb-weight'], \
                 aggfunc = 'median', fill_value = 0).columns.values


# Standard deviation of price and normalized-losses	for different companies' cars
tables4, titles4 = [data.pivot_table(index=["company"], values = ['price', 'normalized-losses'], \
                 aggfunc = 'std', fill_value = 0).round(2).replace(0, 'undefined', regex=True).to_html(classes='data')], \
                     data.pivot_table(index=["company"], values = ['price', 'normalized-losses'], \
                 aggfunc = 'std', fill_value = 0).round(2).replace(0, 'undefined', regex=True).columns.values

'''
# body_style information
body_style = data['body-style'].value_counts().to_dict()
plt.bar(range(len(body_style)), body_style.values(), align = 'center')
plt.xticks(range(len(body_style)), body_style.keys()) 
# plt.savefig("body_style.png")
figfile = io.BytesIO()
plt.savefig(figfile, format='jpeg')
plt.clf()


# correlation between a pair of features
# sns.heatmap(data.iloc[:].corr(), vmin = -1, vmax = 1, cmap="YlGnBu")


# normalized-losses information
data.dropna(subset = ['normalized-losses'], inplace = True)
data[['normalized-losses']] = data[['normalized-losses']].astype('int64')
d = dict()
for i in set(data['company']): # making dictionary without values
    d[i] = 0
for j in range(len(data['company'])): # adding values to the dictionary
    d[list(data['company'])[j]] += list(data['normalized-losses'])[j]
for k in d.values(): # fingind average of values
    d[list(d.keys())[list(d.values()).index(k)]] //= list(data['company']).count(list(d.keys())[list(d.values()).index(k)])
myexplode = [0.2 if i == max(d.values()) else i * 0 for i in d.values()]
plt.pie(d.values(), labels=d.keys(), explode = myexplode, autopct='%1.1f%%')
# plt.savefig("normalized_losses.png")
figfile = io.BytesIO()
plt.savefig(figfile, format='jpeg')
plt.clf()


# rereading the data bc we deleted NaN rows for normalized-losses column
data = pd.read_csv("./DATA1/imports-85.data", sep=',', names=colnames, header=None)
for i in colnames:
    data.loc[data[i] == '?', i] = np.nan


# engine aspiration compared to engine type
labels = list(set(data['engine-type']))
first_lable, second_lable = list(set(data['aspiration']))[0], list(set(data['aspiration']))[1] # turbo, std
turbo, std = [], []
d = dict()
for j in set(data['engine-type']):
    d[j] = [0, 0]
for i in range(len(data['engine-type'])):
    if list(data['aspiration'])[i] == 'turbo':
        ind = 0
    else: ind = 1
    d[list(data['engine-type'])[i]][ind] += 1
for i in d.values():
    turbo.append(i[0])
    std.append(i[1])
x = np.arange(len(set(data['engine-type'])))  # the location of the lable
width = 0.35  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, turbo, width, label = first_lable)
rects2 = ax.bar(x + width/2, std, width, label = second_lable)
# # Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of engines of certain type')
ax.set_title('Types of engines')
ax.set_xticks(x, labels)
ax.legend()
ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
fig.tight_layout()
# plt.savefig("engine.png")
figfile = io.BytesIO()
plt.savefig(figfile, format='jpeg')
plt.clf()
'''