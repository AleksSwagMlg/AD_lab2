from datetime import datetime
import urllib.request
import pandas as pd
import os

def download_files():
    for i in range(1,26):
        url='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean'.format(i)
        wp = urllib.request.urlopen(url)
        text = wp.read()

        now = datetime.now()
        date_and_time_time = now.strftime("%d%m%Y%H%M%S")

        out = open('NOAA_ID_'+'obl_{}'.format(i)+'_'+date_and_time_time+'.csv','wb')
        out.write(text)
        out.close()

def read_files_to_dataframe(directory_path):
    global dataframe
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):  # переконайтеся, що зчитуєте лише потрібні файли
            parts = filename.split("_")
            i = int(parts[3])
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path, header=1, names=headers)
            df = df.drop(df.loc[df['VHI'] == -1].index)  # видалення рядків зі значенням -1 у стовбці 'VHI'
            df['area'] = i  # додавання стовбця з індексами регіонів
            df['area'].replace({
                1: "Вінницька",
                2: "Волинська",
                3: "Дніпропетровська",
                4: "Донецька",
                5: "Житомирська",
                6: "Закарпатська",
                7: "Запорізька",
                8: "Івано-Франківська",
                9: "Київська",
                10: "Кіровоградська",
                11: "Луганська",
                12: "Львівська",
                13: "Миколаївська",
                14: "Одеська",
                15: "Полтавська",
                16: "Рівенська",
                17: "Сумська",
                18: "Тернопільська",
                19: "Харківська",
                20: "Херсонська",
                21: "Хмельницька",
                22: "Черкаська",
                23: "Чернівецька",
                24: "Чернігівська",
                25: "Республіка Крим"
            }, inplace=True)  # заміна індексів регіонів на нові
            dataframe = pd.concat([dataframe, df])  # додавання даних з поточного файлу до загального фрейму
            #os.remove(filename)
    return dataframe

def get_vhi_for_area_year(area, year):
    vhi_series = dataframe[(dataframe["area"] == area) & (dataframe["Year"] == year)]["VHI"]
    vhi_min = vhi_series.min()
    vhi_max = vhi_series.max()
    return print("Ряд VHI для області {} за рік {}:".format(area, year)), \
           print(vhi_series), \
           print("Мінімальне значення VHI:", vhi_min), \
           print("Максимальне значення VHI:", vhi_max)

def find_extreme_drought_years(region, percentage):
    region_data = dataframe[dataframe["area"] == region]
    years = region_data["Year"].unique()
    extreme_drought_years = []
    for year in years:
        year_data = region_data[region_data["Year"] == year]
        affected_area_percentage = (year_data["VHI"] <= 15).mean() * 100
        if affected_area_percentage >= percentage:
            extreme_drought_years.append(year)
    return print("Роки з екстримальними посухами, в регіоні {} вищими за {} відсвотків: ".format(region, percentage), extreme_drought_years)

def find_moderate_drought_years(region, percentage):
    region_data = dataframe[dataframe["area"] == region]
    years = region_data["Year"].unique()
    moderate_drought_years = []
    for year in years:
        year_data = region_data[region_data["Year"] == year]
        affected_area_percentage = ((year_data["VHI"] > 15) & (year_data["VHI"] <= 35)).mean() * 100
        if affected_area_percentage >= percentage:
            moderate_drought_years.append(year)
    return print("Роки з екстримальними посухами, в регіоні {} вищими за {} відсвотків: ".format(region, percentage), moderate_drought_years)

dataframe = pd.DataFrame()
#download_files()
read_files_to_dataframe(r"C:\Users\Новая надежда\PycharmProjects\pythonProject")

get_vhi_for_area_year("Донецька", "1984")  #Ряд VHI для області за рік, пошук екстремумів (min та max);

find_extreme_drought_years("Донецька", 8) #Ряд VHI за всі роки для області, виявити роки з екстремальнимипосухами,
                                          #які торкнулися більше вказаного відсотка області;

find_moderate_drought_years("Донецька", 40) #Аналогічно для помірних посух

print(dataframe)