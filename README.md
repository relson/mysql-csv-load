# mysql-csv-load

A Python CLI tool to load data from a CSV file into a MySQL database table using **convention over configuration**.

## Features

- Parse and process CSV files efficiently using Pandas.
- **Convention over Configuration**: The database table name is automatically inferred from the CSV filename (e.g., `users.csv` will load into the `users` table).
- Environment variable support for secure database credentials.
- Global terminal command execution after installation.

---

## Installation

### From local source
Clone the repository and install it using `pip`:

```bash
git clone https://github.com/relson/mysql-csv-load.git
cd mysql-csv-load
pip install .

```

---

## Configuration

The application uses `python-dotenv` to manage database credentials. Create a `.env` file in your working directory with the following variables:

```env
MYSQL_CSV_LOAD_HOST=localhost
MYSQL_CSV_LOAD_USER=your_user
MYSQL_CSV_LOAD_PASSWORD=your_password
MYSQL_CSV_LOAD_DATABASE=your_database_name

```

---

## Usage

After installation, the package registers a global command `mysql-csv-load`. Simply provide the path to your CSV file:

```bash
mysql-csv-load path/to/your/customers.csv

```

>  **How it works:** The command above will automatically parse `customers.csv` and attempt to load its content into a MySQL table named `customers`.
