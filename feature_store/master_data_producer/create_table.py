import os

from dotenv import load_dotenv
from postgresql_client import PostgresSQLClient

load_dotenv()


def main():
    pc = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Create devices table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS devices (
            device_id INT,
            created TIMESTAMP,
            feature_5 FLOAT,
            feature_3 FLOAT,
            feature_1 FLOAT,
            feature_8 FLOAT,
            feature_6 FLOAT,
            feature_0 FLOAT,
            feature_4 FLOAT
        );
    """
    try:
        pc.execute_query(create_table_query)
    except Exception as e:
        print(f"Failed to create table with error: {e}")


if __name__ == "__main__":
    main()
