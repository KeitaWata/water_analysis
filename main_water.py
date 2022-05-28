import requests,re
import pandas as pd
import subprocess as sp
import numpy as np

def main():
    url='https://www.worldometers.info/world-population/population-by-country/'
    print('scraping population...')
    page=requests.get(url)
    df = pd.read_html(page.text)[0]
    df.columns.values[1]='Country'
    df.columns.values[2]='Population_2022'
    df.to_csv('pop.csv')
    print('pop.csv was created')
    country= pd.read_csv('pop.csv')
    


    urlI='https://www.worldometers.info/water/'
    print('scraping population...')
    page=requests.get(urlI)
    dff = pd.read_html(page.text)[0]
    dff.columns.values[1]='Yearly_water_used'
    dff.columns.values[2]='Daily_water_used_dyp'
    dff.columns.values[3]='Different_years_population'
    dff.to_csv('popd.csv')
    print('popd.csv was created')
    data=pd.read_csv('popd.csv')

    pp = pd.merge(country, data, on='Country')

    d=pp['Country']
    print('scoring the following ',len(d),' countries...')
    d=list(d)
    print(d)

    dd=pd.DataFrame(
        {
            "country": d,
            "Yearly_water": pp['Yearly_water_used'],
            "Different_Y_population": pp['Different_years_population'],
            "2022_population": pp['Population_2022'],
            "Daily_water_DYP": pp['Daily_water_used_dyp'],
            "Daily_water_2022": round(pp['Yearly_water_used']*1000/pp['Population_2022']/365),
            })
    dd.to_csv('result.csv',index=False)
    dd=pd.read_csv('result.csv',index_col=0)
    print(dd)
if __name__ == "__main__":
 main()