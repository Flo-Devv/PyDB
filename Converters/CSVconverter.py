''' Statut : terminé '''
from pandas import DataFrame, read_csv
from os import path

def csvtodf(file_path: str) -> DataFrame:
    """
    This function converts a CSV file to a pandas DataFrame
    """
    try:
        with open(file_path, 'r') as f:
            line = f.readline()
            # Separator is the most used character in the first line beetween ',', ';' and '\t'
            statistics = [line.count(','), line.count(';'), line.count('\t')]
            separator = [',', ';', '\t'][statistics.index(max(statistics))]
            print(f'Separator detected: {separator}')
        df = read_csv(file_path, sep=separator, index_col=0)
    except Exception as e:
        return 2
    return {path.basename(file_path).split('.')[-2]: df}

def dftocsv(df: dict, file_path:str) -> str:
    """
    This function converts a pandas DataFrame to a CSV file
    :param df: a dict containing a pandas DataFrame
    :param file_path: the path of the CSV file to create
    :return: the name of the CSV file created
    """
    try:
        df = df[list(df.keys())[0]]
        df.to_csv(file_path, index=True, header=True)
    except IndexError:
        return 7
    except Exception:
        return 2
    return path.basename(file_path)

if __name__ == '__main__':
    df = csvtodf('C:/Users/flori/Documents/Projets GitHub/PyDB/test/test.csv')
    print(df)