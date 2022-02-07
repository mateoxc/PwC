# -*- coding: utf-8 -*-
#%% Pobranie danych GUS BDL umieszczonych we własnym repozytorium
import pandas as pd
url = ['https://raw.githubusercontent.com/mateoxc/PwC/main/Data/Ludnosc_os_na_km2.csv',
       'https://raw.githubusercontent.com/mateoxc/PwC/main/Data/Samochody_osobowe.csv',
       'https://raw.githubusercontent.com/mateoxc/PwC/main/Data/Scie%C5%BCki_rowerowe.csv',
       'https://raw.githubusercontent.com/mateoxc/PwC/main/Data/Wynagrodzenie.csv',
       'https://raw.githubusercontent.com/mateoxc/PwC/main/Data/Turystyka%25miejsc.csv']

df_ludnosc = pd.read_csv(url[0],delimiter = ";")
df_samochody = pd.read_csv(url[1],delimiter = ";")
df_sciezki = pd.read_csv(url[2],delimiter = ";",decimal=',')
df_wynagrodzenie = pd.read_csv(url[3],delimiter = ";",decimal=',')
df_turystyka = pd.read_csv(url[4],delimiter = ";",decimal=',')

#%% Posortowanie danych na okres od 2015 do 2019 roku
# Nie używałem danych z 2020 roku, ponieważ w niektórych 
# kategoriach zawierały duże różnice w porównaniu do lat poprzednich 

df_ludnosc.drop(df_ludnosc.iloc[:, 2:15], inplace = True, axis = 1)
df_ludnosc.drop(df_ludnosc.iloc[:, -3:], inplace = True, axis = 1)

df_samochody.drop(df_samochody.iloc[:, 2:14], inplace = True, axis = 1)
df_samochody.drop(df_samochody.iloc[:, -2:], inplace = True, axis = 1)

df_sciezki.drop(df_sciezki.iloc[:, 2:16], inplace = True, axis = 1)
df_sciezki.drop(df_sciezki.iloc[:, -2:], inplace = True, axis = 1)

df_wynagrodzenie.drop(df_wynagrodzenie.iloc[:, 2:15], inplace = True, axis = 1)
df_wynagrodzenie.drop(df_wynagrodzenie.iloc[:, -2:], inplace = True, axis = 1)

df_turystyka.drop(df_turystyka.iloc[:, 2:7], inplace = True, axis = 1)
df_turystyka.drop(df_turystyka.iloc[:, -2:], inplace = True, axis = 1)


#%% Wyliczenie srednich wartosci danych dla okresu 5 lat
df_ludnosc['Średnia_ludnosc'] = df_ludnosc.iloc[:, -5:].mean(axis=1)
df_wynagrodzenie['Średnia_wynagrodzenie'] = df_wynagrodzenie.iloc[:, -5:].mean(axis=1)
df_turystyka['Średnia_turystyka'] = df_turystyka.iloc[:, -5:].mean(axis=1)
df_samochody['Średnia_samochody'] = df_samochody.iloc[:, -5:].mean(axis=1)
df_sciezki['Średnia_sciezki'] = df_sciezki.iloc[:, -5:].mean(axis=1)


#%% Obliczenie indeksów atrakcyjności lokalizacji - IAL 

#Obliczenie atrakcyjności lokalizacji salonów
df = pd.DataFrame()
df = df_ludnosc[['Kod','Nazwa']].copy()

df['IAL_Salony'] = (1*df_ludnosc['Średnia_ludnosc']-(1/100000) *df_samochody['Średnia_samochody']+ 
             +2* df_wynagrodzenie['Średnia_wynagrodzenie']+400*df_sciezki['Średnia_sciezki'] )

#Przyporządkowanie wartsci indeksów w zakresie od 0 do 100
df.iloc[:,-1:] = df.iloc[:,-1:].apply(lambda x: 100*((x-x.min())/ (x.max()-x.min())), axis=0)

#Wartosci całkowite indeksów
df['IAL_Salony'] = pd.to_numeric(df['IAL_Salony'],downcast="integer")
df['IAL_Salony'] = df['IAL_Salony'].astype(int)

#Sortowanie wyników
df_salony = df.filter(['Kod','Nazwa','IAL_Salony'], axis=1)
df_salony=df_salony.nlargest(380, 'IAL_Salony')


#%%Obliczenie atrakcyjności lokalizacji wypożyczalni rowerów
df2 = pd.DataFrame()
df2 = df_ludnosc[['Kod','Nazwa']].copy()

df2['IAL_Wypożyczalnie'] = (1.2*df_ludnosc['Średnia_ludnosc']- (1/100000) *df_samochody['Średnia_samochody']+
                 -1*df_wynagrodzenie['Średnia_wynagrodzenie']+100* df_turystyka['Średnia_turystyka']+
                 +400*df_sciezki['Średnia_sciezki'])
#Przyporządkowanie wartsci indeksów w zakresie od 0 do 100
df2.iloc[:,-1:] = df2.iloc[:,-1:].apply(lambda x: 100*((x-x.min())/ (x.max()-x.min())), axis=0)
#Wartosci całkowite indeksów
df2['IAL_Wypożyczalnie'] = pd.to_numeric(df2['IAL_Wypożyczalnie'],downcast="integer")
df2['IAL_Wypożyczalnie'] = df2['IAL_Wypożyczalnie'].astype(int)

#Sortowanie wyników
df_wypoz = df2.filter(['Kod','Nazwa','IAL_Wypożyczalnie'], axis=1)
df_wypoz = df_wypoz.nlargest(380, 'IAL_Wypożyczalnie')


#%% Histogramy
df.hist(column='IAL_Salony')

#Zapis histogramu do pdf
'''
s = pd.Series()
ax = s.plot.hist()
ax.figure.savefig('Histogram-salony.pdf')
'''
df2.hist(column='IAL_Wypożyczalnie')

#Zapis histogramu do pdf
'''
s = pd.Series()
ax = s.plot.hist()
ax.figure.savefig('Histogram-wypożyczalnie.pdf')
'''
#%% Zapis wyników do pliku CSV
df_salony.to_csv('Wyniki_salon.csv')
df_wypoz.to_csv('Wyniki_wypozyczalnia.csv')