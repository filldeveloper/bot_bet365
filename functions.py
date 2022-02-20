from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from selenium.webdriver.common.by import By
from time import sleep

def outer_html(element):
    html_content = element.get_attribute('outerHTML')
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()

    return text


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Call function to create database
def main():
    database = 'bet365.db'

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS results (
                                    id integer PRIMARY KEY,
                                    date text NOT NULL,
                                    result text NOT NULL,
                                    hour_result text NOT NULL,
                                    championship text NOT NULL,
                                    unique_key text UNIQUE NOT NULL
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


def feed_table(dados):
    database = 'bet365.db'
    conn = create_connection(database)

    sql = f"""INSERT INTO results
            (date, result, hour_result, championship, unique_key) 
            VALUES
            (?,?,?,?,?)"""

    cur = conn.cursor()
    cur.execute(sql, dados)
    conn.commit()
    cur.close()
    conn.close()
    return cur.lastrowid

def get_results(chrome, index):
    sleep(1)
    last_results = chrome.find_elements(
    By.XPATH, f'/html/body/app-root/app-horarios/main/section/div[2]/div/app-tabela-futebol/table/tbody/tr[{index}]'
    )
    sleep(0.5)
    return last_results
# if __name__ == '__main__':
#     main()