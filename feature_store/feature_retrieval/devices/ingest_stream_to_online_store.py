import os

import constants
import pandas as pd
from feast import FeatureStore
from feast.data_source import PushMode
from feast.infra.contrib.spark_kafka_processor import SparkProcessorConfig
from feast.infra.contrib.stream_processor import get_stream_processor_object
from pyspark.sql import SparkSession

# Configure the SparkSession
# See https://spark.apache.org/docs/3.1.2/structured-streaming-kafka-integration.html#deploying for notes on why we need this environment variable.
os.environ[
    "PYSPARK_SUBMIT_ARGS"
] = "--packages=org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 pyspark-shell"
spark = SparkSession.builder.master("local").appName("feast-spark").getOrCreate()
spark.conf.set("spark.sql.shuffle.partitions", 5)

# Initialize the feature store
store = FeatureStore(repo_path=constants.REPO_PATH)


# If we want to further process features
# along with Spark, define it here
def preprocess_fn(rows: pd.DataFrame):
    print(f"[INFO] df columns: {rows.columns}")
    print(f"[INFO] df size: {rows.size}")
    print(f"[INFO]df preview:\n{rows.head()}")
    return rows


# Define ingestion config
ingestion_config = SparkProcessorConfig(
    mode="spark",
    source="kafka",
    spark_session=spark,
    processing_time="30 seconds",
    query_timeout=15,
)
# Initialize the stream view from our feature store
sfv = store.get_stream_feature_view("device_stats_stream")
# Initialize the processor
processor = get_stream_processor_object(
    config=ingestion_config,
    fs=store,
    sfv=sfv,
    preprocess_fn=preprocess_fn,
)
# Start to ingest
query = processor.ingest_stream_feature_view()

# You can push feature to offline store via the following commands
# query = processor.ingest_stream_feature_view(PushMode.OFFLINE)

# , and use this below command to stop ingestion job
# query.stop()
