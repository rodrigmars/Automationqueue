from typing import Optional
from sqlite3 import Connection, connect


def create_tables(path_db: str) -> tuple | None:

    failed: tuple = ()

    con: Optional[Connection] = None

    print(">>>>>>>>>>>>>>>>>>>>>>>", path_db)

    try:

        con = connect(path_db)

        con.cursor().executescript("""
            BEGIN;

            CREATE TABLE IF NOT EXISTS AUTOMATE_ENTROPY_DATA_CAPTURE(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CODE TEXT NOT NULL UNIQUE,
                STATUS INTEGER NOT NULL,
                PRICE TEXT NOT NULL,
                PRODUCT_MODEL TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS AUTOMATE_ENTROPY_DATA_INTERSECTION(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CODE TEXT NOT NULL UNIQUE,
                STATUS INTEGER NOT NULL,
                PRICE TEXT NOT NULL,
                PRODUCT_MODEL TEXT NOT NULL
            );
            
            COMMIT;
            """)

    except Exception as e:
        failed = e,

    finally:
        if con:
            con.close()

        return failed if () != failed else None
