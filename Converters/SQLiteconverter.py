''' Statut : terminé '''
from sqlite3 import connect, OperationalError
from pandas import DataFrame
from os import path

def sqlitetodf(path):
    '''
    This function converts a sqlite file to a pandas DataFrame
    '''
    conn = connect(path)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    df = {}
    for table in tables:
        df[table[0]] = DataFrame(conn.execute(f'SELECT * FROM {table[0]};').fetchall())
        df[table[0]].columns = [description[0] for description in conn.execute(f'SELECT * FROM {table[0]};').description]
    conn.close()
    return df

def dftosqlite(df: dict, file_path:str):
    '''
    This function converts a pandas DataFrame to a sqlite file
    '''
    conn = connect(file_path)
    for table in df:
        try:
            df[table].to_sql(table, conn, if_exists='replace', index=False)
        except OperationalError:
            continue
    conn.close()
    return path.basename(file_path)

if __name__ == '__main__':
    df = sqlitetodf('C:/Users/flori/Documents/Projets GitHub/PyDB/test/test.db')
    print(df['genres'])
    #print(dftosqlite('C:/Users/flori/Documents/Projets GitHub/PyDB/test/render.db', df))