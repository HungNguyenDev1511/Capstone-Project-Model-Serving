import os
import random
from datetime import datetime
from time import sleep

from dotenv import load_dotenv
from postgresql_client import PostgresSQLClient

load_dotenv()

TABLE_NAME = "devices"
NUM_ROWS = 20


def main():
    pc = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Get all columns from the devices table
    try:
        columns = pc.get_columns(table_name=TABLE_NAME)
        print(columns)
    except Exception as e:
        print(f"Failed to get schema for table with error: {e}")

    # Loop over all columns and create random values
    for _ in range(NUM_ROWS):
        # Randomize values for feature columns
        feature_values = [str(random.random()) for _ in range(len(columns) - 2)]
        # Add device_id and current time
        device_id = random.randint(0, 2)
        data = [
            device_id,
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        ] + feature_values
        # Insert data
        query = f"""
            insert into {TABLE_NAME} ({",".join(columns)})
            values {tuple(data)}
        """
        pc.execute_query(query)
        sleep(2)


if __name__ == "__main__":
    main()
