import pandas as pd
import re

data_to_exclude = [
    'Российская Федерация',
    'Центральный федеральный округ',
    'Северо-Западный федеральный округ',
    'в том числе:',
    'Южный федеральный округ',
    'Северо-Кавказский федеральный округ',
    'Приволжский федеральный округ',
    'Уральский федеральный округ',
    'Сибирский федеральный округ',
    'Дальневосточный федеральный округ',
    'Крымский федеральный округ2)',
    'Архангельская область', 
    'Тюменская область',
]

dict_to_replace ={
    'Тюменская область без автономных округов':
        'Тюменская область',
    'Ханты-Мансийский автономный округ - Югра':
        'Ханты-Мансийский АО',
    'Ямало-Ненецкий автономный округ':
        'Ямало-Ненецкий АО',
    'Архангельская область (кроме Ненецкого автономного округа)':
        'Архангельская область',
    'Республика Адыгея (Адыгея)':
        'Республика Адыгея',
    'Республика Татарстан (Татарстан)':
        'Республика Татарстан',
    'Чувашская Республика -Чувашия':
        'Чувашская Республика',
    'Кемеровская область- Кузбасс':
        'Кемеровская область'
}

dict_columns = {
    'Исследование / разработка': r'исследование и разработка',
    'Дизайн': r'дизайн',
    'Машины и оборудование': r'приобретение машин',
    'Обучение персонала': r'обучение и подготовка персонала',
    'Прочее': r'прочие затраты',
    'Инжиниринг': r'инжиниринг|виды подготовки производства',
    'Маркетинг': r'маркетинг|маркетин-говые',
    'Приобретение ПО': r'программ для ЭВМ|приобрете-ние программ-ных средств',
    'Патенты / лицензии': r'патент'
}


def prepare_data(xlsx, xlsx_sheet: int, drop_rows=data_to_exclude, 
                replacer = dict_to_replace):
    
    years = [2014, 2016, 2018, 2019, 2020, 2021, 2022]
    
    if xlsx_sheet in years:
        xlsx_sheet = xlsx_sheet % 1_000 - 6
    elif xlsx_sheet not in [8, 10, 12, 14, 15, 16]:
        raise ValueError('Invalid sheet number!')
        
    xlsx_ = pd.read_excel(xlsx, f'{xlsx_sheet}')
    xlsx_col = xlsx_.iloc[4, 2:12].values
    idx1 = xlsx_.iloc[:, 3].first_valid_index()+2
    idx2 = xlsx_.iloc[:, 1].last_valid_index()+1
    
    innov_ = (
        xlsx_
        .rename(columns={'К содержанию': 'region'})
        .set_index('region', drop=True)
        .iloc[idx1:idx2, 1:11]
        .pipe(lambda _df: _df.apply(pd.to_numeric, errors='coerce'))
        .fillna(0)
        .reset_index()
    )
    
    innov_['region'] = innov_['region'].apply(lambda row: row.strip())
    mask = ~innov_['region'].isin(drop_rows)
    innov_ = innov_.loc[mask, :].reset_index(drop=True)
    innov_['region'].replace(to_replace=replacer, inplace=True)
    
    if innov_['region'].nunique() == 85:
        pass
    else:
        raise Exception('Число регионов не равно 85!')

    return innov_, xlsx_col


def rename_columns(data, columns_, dict_columns=dict_columns):
    
    for i, col_name in enumerate(columns_):
        for key, pattern in dict_columns.items():
            m = re.search(pattern, col_name)
            ans = 1 if m else 0
            if ans:
                columns_[i] = key
                break
    data.columns = ['region', *columns_]
    data = data[['region', *dict_columns.keys()]]
    
    return data

def left_join(innov_, y_innov):

    innov_y = innov_.merge(right=y_innov, how='left', on='region')
    
    if innov_y[innov_y.isna().any(axis=1)].shape[0] > 0:
        raise Exception('NaN values after merge!')
    else:
        return innov_y