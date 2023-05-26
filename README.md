# PyDB
*"Unlock the potential of your data with PyDB!"*

<img width="100%" alt="image" src="https://github.com/Flo-Devv/PyDB/assets/129592338/8cbe23d9-8e7f-4b64-9a26-2a4236ab2f00">

## Introduction

Pydb is a powerful Python library that allows you to seamlessly convert popular table languages into various other formats, including Excel, JSON, SQLite, CSV, and HTML. With Pydb, you can easily transform and manipulate your data by utilizing a middle state, represented by DataFrames (df), which enables efficient data analysis, storage, and presentation.

## Features

- Convert tables between popular formats: Excel, JSON, SQLite, CSV, and HTML.
- Utilize the middle state, represented by DataFrames (df), for data manipulation and transformation operations.
- Preserve data integrity and maintain formatting during conversion.
- Seamlessly integrate Pydb into your existing Python projects.
- Enjoy the benefits of an intuitive and easy-to-use API.

## Web Application

An interactive web application is also available, providing a user-friendly interface to utilize the power of PyDB. Visit [website](https://pydb-9cawl.ondigitalocean.app/) to access the web application and explore its features.

## Usage

To use PyDB in your Python project, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/pydb.git`
2. Navigate to the project directory: `cd PyDB`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Import Pydb into your Python script:

```python
from Converters import*
```

5. Convert your data to the middle state (DataFrame) using the appropriate functions. See the examples below:

```python
# Example: Convert an HTML table to a DataFrame
df = htmltodf('input.html')

# Example: Convert a SQLite table to a DataFrame
df = sqlite_to_df('input.db')

# Example: Convert a DataFrame to HTML
html = dftohtml(df, **style)
 
# Example: Convert a DataFrame to JSON
dftojson(df, 'output.json')
```

Please refer to the documentation for more detailed information on the available methods and their parameters.

## Contributing

Contributions to Pydb are more than welcome! If you'd like to contribute, please follow these guidelines:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push the branch to your fork: `git push origin my-new-feature`
5. Submit a pull request.
