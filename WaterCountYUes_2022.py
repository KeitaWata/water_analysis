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
    print('scraping water data...')
    page=requests.get(urlI)
    dff = pd.read_html(page.text)[0]
    dff.columns.values[1]='Yearly_water_used'
    dff.columns.values[2]='Daily_water_used_dyp'
    dff.columns.values[3]='Different_years_population'
    dff.to_csv('water.csv')
    print('water.csv was created')
    data=pd.read_csv('water.csv')


    pp = pd.merge(country, data, on='Country')
    pp['Population_growth_rate'] = pp['Population_2022']/pp['Different_years_population']
    pp['Yearly_total_2022']=pp['Daily_water_used_dyp']*pp['Population_2022']*365*0.001
    pp['rate_water'] = pp['Different_years_population']/pp['Population_2022']

    d=pp['Country']
    print('scoring the following ',len(d),' countries...')
    d=list(d)
    print(d)
    np.set_printoptions(suppress=True)

    dd_dy=pd.DataFrame(
        {
            "country": d,
            "DY_population": pp['Different_years_population'],
            "DYearly_water_used": pp['Yearly_water_used'],
            "Daily_water_used": pp['Daily_water_used_dyp'],
            })

    dd_2022=pd.DataFrame(
        {
            "country": d,
            "2022_population": pp['Population_2022'],
            'Population_growth_r':pp['Population_growth_rate'],
            "Yearly_water_u2022":pp['Yearly_total_2022'],
            "Daily_water_used_2022": np.round(pp['Daily_water_used_dyp']*pp['rate_water']),
        }
    )
    dd_dy.to_csv('result_dy.csv',index=False)
    dd_dy=pd.read_csv('result_dy.csv',index_col=0)
    dd_2022.to_csv('result_2022.csv',index=False)
    dd_2022=pd.read_csv('result_2022.csv',index_col=0)
    print(dd_dy)
    print(dd_2022)
if __name__ == "__main__":
 main()