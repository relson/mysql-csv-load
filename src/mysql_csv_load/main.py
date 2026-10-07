import argparse
import csv
import os
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


DEFAULT_BATCH_SIZE = 1_000


def _quote_identifier(identifier: str) -> str:
    return f"`{identifier.replace('`', '``')}`"


def import_csv(
    csv_file: Path, table_name: str, cursor, connection, batch_size: int
) -> int:
    csv.field_size_limit(sys.maxsize)
    table = _quote_identifier(table_name)
    imported = 0

    with csv_file.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        columns = next(reader, None)
        if not columns:
            raise ValueError("The CSV file is empty or has no header.")
        if any(not column.strip() for column in columns):
            raise ValueError("The CSV header contains empty column names.")
        if len(set(columns)) != len(columns):
            raise ValueError("The CSV header contains duplicate column names.")

        quoted_columns = [_quote_identifier(column) for column in columns]
        create_table = ", ".join(f"{column} TEXT" for column in quoted_columns)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({create_table})")
        connection.commit()

        column_list = ", ".join(quoted_columns)
        placeholders = ", ".join(["%s"] * len(columns))
        insert = f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"
        batch = []

        for record_number, row in enumerate(reader, start=2):
            if len(row) != len(columns):
                raise ValueError(
                    f"CSV record {record_number} has {len(row)} columns; "
                    f"the header has {len(columns)}."
                )

            batch.append(tuple(row))
            if len(batch) == batch_size:
                cursor.executemany(insert, batch)
                connection.commit()
                imported += len(batch)
                batch.clear()

                if imported % 100_000 == 0:
                    print(f"{imported:,} records imported", file=sys.stderr)

        if batch:
            cursor.executemany(insert, batch)
            connection.commit()
            imported += len(batch)

    return imported


def run(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Import a CSV file into a MySQL table in batches."
    )
    parser.add_argument("csv_file", type=Path, help="path to the CSV file")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"rows per batch (default: {DEFAULT_BATCH_SIZE})",
    )
    args = parser.parse_args(argv)

    if args.batch_size < 1:
        parser.error("--batch-size must be greater than zero.")

    load_dotenv()
    table_name = os.path.splitext(args.csv_file.name)[0]
    db_host = os.getenv("MYSQL_CSV_LOAD_HOST")
    db_user = os.getenv("MYSQL_CSV_LOAD_USER")
    db_password = os.getenv("MYSQL_CSV_LOAD_PASSWORD")
    db_name = os.getenv("MYSQL_CSV_LOAD_DATABASE")
    db_port_env = os.getenv("MYSQL_CSV_LOAD_PORT")
    db_port = (
        int(db_port_env)
        if db_port_env and db_port_env.strip().isdigit()
        else 3306
    )

    if not db_host or not db_user or not db_name:
        parser.error(
            "MYSQL_CSV_LOAD_HOST, MYSQL_CSV_LOAD_USER, and "
            "MYSQL_CSV_LOAD_DATABASE must be set."
        )

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
        )
    except mysql.connector.Error as error:
        parser.error(f"Could not connect to MySQL: {error}")

    try:
        cursor = connection.cursor()
        try:
            imported = import_csv(
                args.csv_file, table_name, cursor, connection, args.batch_size
            )
        finally:
            cursor.close()
    except (mysql.connector.Error, OSError, csv.Error, ValueError) as error:
        connection.rollback()
        parser.error(
            f"Import failed: {error}. Previously committed batches remain "
            "in the database."
        )
    finally:
        connection.close()

    print(
        f"Successfully imported {imported:,} records into table '{table_name}'."
    )
