''' Status: En cours de développement '''
from json import dumps
from pandas import read_json

def jsontodf(json:str)->dict:
    '''
    This function converts json data to a dict of pandas DataFrames
    '''
    if not isinstance(json, str):
        return 3
    
    df = {"Table 1": read_json(json)}
    return df


def dftojson(df: dict)->list[str]:
    '''
    This function converts a pandas DataFrame to a JSON object
    :param df: dict of pandas DataFrames
    :return: JSON object
    '''
    temp = []
    for _, value in df.items():
        temp.append(value.to_json(orient='records', indent=4))
    return temp

if __name__ == '__main__':
    df = jsontodf('C:/Users/flori/Documents/Projets GitHub/PyDB/test/test.json')
    print(df)
    json = dftojson(df)
    print(json)