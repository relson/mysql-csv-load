# mysql-csv-load

[Ler em Português do Brasil](README.pt-BR.md)

This is a simple Python script to load data from a CSV file into a MySQL database table.

## Features

- Reads a CSV file specified as a command-line argument.
- Creates a table in the MySQL database with the same name as the CSV file (without the extension).
- The table columns are created dynamically based on the CSV file header.
- Inserts the data from the CSV file into the newly created table.

## How to use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/relson/mysql-csv-load.git
   cd mysql-csv-load
   ```

2. **(Optional) Create and activate a virtual environment:**

   It's recommended to use a virtual environment to manage dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database credentials:**

   Create a `.env` file in the root directory of the project with your MySQL credentials. You can use the `.env.example` file as a template.

   ```
   MYSQL_CSV_LOAD_HOST=localhost
   MYSQL_CSV_LOAD_USER=root
   MYSQL_CSV_LOAD_PASSWORD=root
   MYSQL_CSV_LOAD_DATABASE=m
   ```

4. **Run the script:**

   Run the script from the command line, passing the path to your CSV file as an argument:

   ```bash
   python main.py path/to/your/file.csv
   ```

   For example:

   ```bash
   python main.py examples/customer_data.csv
   ```

   The script will create a table called `customer_data` (if it doesn't already exist) and insert the data from the CSV file into it.

## Example

Suppose you have a `products.csv` file with the following content:

```csv
ID,Name,Price
1,Product A,19.99
2,Product B,29.99
3,Product C,39.99
```

When running the command:

```bash
python main.py products.csv
```

The script will:

1. Connect to your MySQL database.
2. Create a table called `products` with the columns `ID`, `Name`, and `Price`.
3. Insert the 3 rows of data from the CSV file into the `products` table.

## Requirements

- Python 3.x
- pandas
- mysql-connector-python

You can install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

## TODO

- ~Use a .env file, to load the credentials~
- Create a pip package
