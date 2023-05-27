''' Statut : En cours de développement '''

from pandas import DataFrame, read_excel, ExcelWriter
from os import path

def dftoexcel(df:dict, file_path:str) -> None:
    '''
    This function converts a pandas DataFrame to an excel file
    :param df: a dict of pandas DataFrame
    :param file_path: the path of the excel file
    '''
    if type(df) != dict:
        raise TypeError('df must be a dict of pandas DataFrame')
    try:
        writer = ExcelWriter(file_path)
        for sheet in df:
            df[sheet].to_excel(writer, sheet_name=sheet)
        writer.close()
    except Exception as e:
        print(e)
        return 2
    return path.basename(file_path)

def exceltodf(path:str) -> DataFrame:
    '''
    This function converts an excel file to a pandas DataFrame
    '''
    return read_excel(path, sheet_name=None, header=None, index_col=None, engine='openpyxl')

if __name__ == '__main__':
    df = exceltodf('C:/Users/flori/Documents/Projets GitHub/PyDB/test/test.xlsx')
    print(dftoexcel(df, 'C:/Users/flori/Documents/Projets GitHub/PyDB/uploads/output.xlsx'))