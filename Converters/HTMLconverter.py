''' Statut : terminé '''
from bs4 import BeautifulSoup
from requests import get
from pandas import read_html

def htmltodf(html: str)->dict:
    '''
    This function converts an html file to a pandas DataFrame
    '''
    assert type(html) == str, 'html must be a string (path, link or html code)'
    if html[:4] == 'http':
        try:
            html = get(html, timeout=2).text
        except Exception:
            return 8
    elif html[-5:] == '.html':
        with open(html, 'r') as f:
            html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    df = {}
    for idx, table in enumerate(tables):
        df[table.get('id', f'Table {idx}')] = read_html(str(table))[0]
    return df


def dftohtml(df:dict, td_color='#808080', th_color='#FFFFFF', radius='10px', head_color='#6C7AE0', content_color1='#F8F6FF', content_color2='#FFFFFF', theme='light or dark') -> list[str]:
    
    assert theme in ['light', 'dark', 'light or dark'], 'Theme must be either "light" or "dark"'
    assert type(df) == dict, 'df must be a dictionary of DataFrames'
    assert type(td_color) == str, 'td_color must be a string'
    assert type(th_color) == str, 'th_color must be a string'
    assert type(head_color) == str, 'head_color must be a string'
    assert type(content_color1) == str, 'content_color1 must be a string'
    assert type(content_color2) == str, 'content_color2 must be a string'
    
    if type(radius) == int:
        radius = str(radius) + 'px'
    elif type(radius) == str:
        if radius[-2:] != 'px':
            radius += 'px'
    else:
        raise TypeError('radius must be an integer or string')
    
    # Default CSS styles
    if theme == 'light':
        td_color = '#808080'
        th_color = '#FFFFFF'
        radius = '10px'
        head_color = '#6C7AE0'
        content_color1 = '#F8F6FF'
        content_color2 = '#FFFFFF'

    elif theme == 'dark':
        td_color = '#808080'
        th_color = '#00AD5F'
        radius = '10px'
        head_color = '#393939'
        content_color1 = '#222'
        content_color2 = '#222'

    styles = {
        'table': {
            'font-family': 'Montserrat, sans-serif',
            'font-size': '15px',
            'color': td_color,
            'border-radius': radius,
            'border': 'transparent',
            'box-shadow': '0 0 10px rgba(0, 0, 0, .3);',
            'border-collapse': 'collapse',
            'margin-bottom': '50px',
            'width': '100%',
        },
        'th, td': {
            'padding-block': '10px',
            'text-align': 'center',
        },
        'th, caption': {
            'background-color': head_color,
            'font-weight': 'bold',
            'color': th_color,
            'font-size': '18px'
        },
        'tr:nth-child(even)': {
            'background-color': content_color1,
        },
        'tr:nth-child(odd)': {
            'background-color': content_color2,
        }
    }
    
    style = "<link href='https://fonts.cdnfonts.com/css/montserrat' rel='stylesheet'>\n<style>\n"
    for selector, properties in styles.items():
        style += f"{selector} {{\n"
        for prop, value in properties.items():
            style += f"    {prop}: {value};\n"
        style += "}\n"
    style += "</style>\n"
    html = [style]

    for table_name, table in df.items():
        table = table.fillna('')
        table_html = table.to_html(index=False, table_id=table_name)
        html += [table_html + "\n"]
    return html

if __name__ == '__main__':
    df = htmltodf('https://test.com/')
    if df == 8:
        print('Erreur de connexion')
    else:
        html = dftohtml(df, theme='dark')
        print(''.join(html))
