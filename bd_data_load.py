import pandas as pd
import numpy as np
import mysql.connector

#load bd data
bd = pd.read_csv('bd050125.txt', sep='\t', encoding="utf-16", names = ['CIK', 'Firm', 'reporting_file_number', 'address1', 'address2', 'city', 'state_code', 'zip_code', "drop_me"])
bd = bd.drop(['reporting_file_number','drop_me'], axis = 1)

#load nyse
nyse = pd.read_csv('nyse_members.csv')
nyse['Exchange'] = 1
nyse = nyse.rename(columns={'Account Name': 'Firm'})

#load nqx
nqx = pd.read_excel('NQXMembers-2.xlsx', names = ['Designation', 'Firm', 'Exchange', 'drop_me'])
nqx = nqx.drop('drop_me', axis =1)
nqx = nqx.drop([0,1]).reset_index(drop = True)
nqx['Exchange'] = 2

#load cboe futures
cfe = pd.read_csv('cfe.txt', sep = '/n', names = ['Firm'])
cfe['Exchange'] = 3

#use same member firms for cboe exchanges
bzx = cfe.copy()
bzx['Exchange'] = 4
byx = cfe.copy()
byx['Exchange'] = 5
edga = cfe.copy()
edga['Exchange'] = 6
cboe_edgx = cfe.copy()
cboe_edgx['Exchange'] = 7
c2 = cfe.copy()
c2['Exchange'] = 8

#load cme
cme = pd.read_csv('cme.txt', sep = '/n', names = ['Firm'])
cme['Exchange'] = 11

#load iex
iex = pd.read_csv('iex.txt', sep = '/n', names = ['Firm'])
iex['Exchange'] = 9

#load miax
miax_options = pd.read_csv('miax_options.txt', sep = '\t')
miax_options['Exchange'] = 10
miax_options = miax_options.rename(columns = {'Name ': 'Firm'})
miax_equities = pd.read_csv('miax_equities.txt', sep = '\t')
miax_equities['Exchange'] = 10
miax_equities = miax_equities.rename(columns = {'Name ': 'Firm'})

#concatenate all member dataframes
Is_A_Member_Of = [  nyse[['Firm', 'Exchange']], 
                    nqx[['Firm', 'Exchange']], 
                    cfe[['Firm', 'Exchange']], 
                    cme[['Firm', 'Exchange']], 
                    iex[['Firm', 'Exchange']], 
                    miax_options[['Firm', 'Exchange']], miax_equities[['Firm', 'Exchange']], 
                    bzx[['Firm', 'Exchange']], byx[['Firm', 'Exchange']], edga[['Firm', 'Exchange']], cboe_edgx[['Firm', 'Exchange']], c2[['Firm', 'Exchange']]]
Is_A_Member_Of = pd.concat(Is_A_Member_Of)
Is_A_Member_Of = Is_A_Member_Of.reset_index(drop=True)

#clean data
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.upper()
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace(",", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace(".", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("/", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("\xa0", " ")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("LLC", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("LP", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("THE", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("-", " ")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("INCORPORATED", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("INC", "")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("COMPANY", "CO")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.replace("  ", " ")
Is_A_Member_Of['Firm'] = Is_A_Member_Of['Firm'].str.strip()

#compare to broker dealer data to get CIK codes
bd_clean = bd.copy()
bd_clean['Firm'] = bd_clean['Firm'].str.upper()
bd_clean['Firm'] = bd_clean['Firm'].str.replace(",", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace(".", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("/", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("LLC", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("LP", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("THE", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("-", " ")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("INCORPORATED", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("INC", "")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("COMPANY", "CO")
bd_clean['Firm'] = bd_clean['Firm'].str.replace("  ", " ")
bd_clean['Firm'] = bd_clean['Firm'].str.strip()

#manually change some firm names when the firm uses aliases (so can match with bd data)
Is_A_Member_Of.loc[2,'Firm'] = 'LUCID CAPITAL MARKETS'
Is_A_Member_Of.loc[10,'Firm'] = 'MARK J MULLER EQUITIES'
Is_A_Member_Of.loc[182,'Firm'] = 'CAPITAL INSTITUTIONAL SERVICES'
Is_A_Member_Of.loc[193,'Firm'] = 'BETA CAPITAL SECURITIES'
Is_A_Member_Of.loc[229,'Firm'] = 'EDWARD D JONES & CO'
Is_A_Member_Of.loc[243,'Firm'] = 'FOLIO INVESTMENTS'
Is_A_Member_Of.loc[253,'Firm'] = 'HCWAINWRIGHT & CO'
Is_A_Member_Of.loc[282,'Firm'] = 'JONESTRADING INSTITUTIONAL SERVICES'
Is_A_Member_Of.loc[306,'Firm'] = 'PUBLIC VENTURES'
Is_A_Member_Of.loc[429,'Firm'] = "O'NEIL SECURITIES"
Is_A_Member_Of.loc[456,'Firm'] = "RJ O'BRIEN SECURITIES"
Is_A_Member_Of.loc[482,'Firm'] = "GOLDMAN SACHS & CO"
Is_A_Member_Of.loc[483,'Firm'] = "HIDDEN ROAD PARTNERS CIV US"
Is_A_Member_Of.loc[488,'Firm'] = 'MACQUARIE CAPITAL (USA)'
Is_A_Member_Of.loc[489,'Firm'] = 'MAREX CAPITAL MARKETS'
Is_A_Member_Of.loc[492,'Firm'] = 'NOMURA GLOBAL FINANCIAL PRODUCTS'
Is_A_Member_Of.loc[494,'Firm'] = "RJ O'BRIEN SECURITIES"
Is_A_Member_Of.loc[495,'Firm'] = 'RBC CAPITAL MARKETS'
Is_A_Member_Of.loc[496,'Firm'] = "RJ O'BRIEN SECURITIES"
Is_A_Member_Of.loc[497,'Firm'] = 'SANTANDER SECURITIES'
Is_A_Member_Of.loc[498,'Firm'] = 'SANTANDER SECURITIES'
Is_A_Member_Of.loc[502,'Firm'] = 'SCOTIA CAPITAL (USA)'
Is_A_Member_Of.loc[503,'Firm'] = 'TRADESTATION SECURITIES'
Is_A_Member_Of.loc[504,'Firm'] = 'WEDBUSH SECURITIES'
Is_A_Member_Of.loc[512,'Firm'] = 'TD ARRANGED SERVICES'
Is_A_Member_Of.loc[520,'Firm'] = 'BOFA SECURITIES'
Is_A_Member_Of.loc[532,'Firm'] = 'CLEAR STREET'
Is_A_Member_Of.loc[541,'Firm'] = 'DASH FINANCIAL TECHNOLOGIES'
Is_A_Member_Of.loc[558,'Firm'] = 'IMC CHICAGO'
Is_A_Member_Of.loc[612,'Firm'] = 'LEERINK PARTNERS'
Is_A_Member_Of.loc[648,'Firm'] = 'IMC CHICAGO'
Is_A_Member_Of.loc[674,'Firm'] = 'ABN AMRO SECURITIES (USA)'
Is_A_Member_Of.loc[693,'Firm'] = 'IMC CHICAGO'
Is_A_Member_Of.loc[704,'Firm'] = 'MERRILL LYNCH PIERCE FENNER & SMITH'
Is_A_Member_Of.loc[745,'Firm'] = "RJ O'BRIEN SECURITIES"
Is_A_Member_Of.loc[781,'Firm'] = "RJ O'BRIEN SECURITIES"
Is_A_Member_Of.loc[817,'Firm'] = "RJ O'BRIEN SECURITIES"
Is_A_Member_Of.loc[853,'Firm'] = "RJ O'BRIEN SECURITIES"
Is_A_Member_Of.loc[889,'Firm'] = "RJ O'BRIEN SECURITIES"

# merge the bd and member data to get CIK codes
Is_A_Member_Of = Is_A_Member_Of.merge(bd_clean, on = 'Firm', how = 'inner')
Is_A_Member_Of = Is_A_Member_Of[['CIK', 'Exchange']]
Is_A_Member_Of = Is_A_Member_Of.drop_duplicates().reset_index(drop=True)

#prepare bd data to be inserted
bd = bd.rename(columns={'Firm': 'Name'})
bd['Address'] = bd.address1 +' '+  bd.address2.fillna('') + ' ' + bd.city + ' ' + bd.state_code +' ' + bd.zip_code
bd['Address'] = bd.Address.str.replace('  ', ' ')
bd = bd[['CIK', 'Name', 'Address']]
bd = bd.fillna('unknown location')

#insert into sql
myConnection = mysql.connector.connect( 
    user='root',
    password = 'orm1Fndersine',
    host = 'localhost',
    database = 'ExchangeInfo')
cursorObject = myConnection.cursor()

#insert broker dealer data
query = "insert into Broker_Dealer values (%s, %s, %s);"
for i, row in bd.iterrows():
    values = (row[0], row[1], row[2])
    cursorObject.execute(query, values)
myConnection.commit()

#insert member data
query = "insert into Is_A_Member_Of values (%s, %s);"
for i, row in Is_A_Member_Of.iterrows():
    values = (int(row[0]), int(row[1]))
    cursorObject.execute(query, values)
myConnection.commit()

#close connections11
cursorObject.close()
myConnection.close()