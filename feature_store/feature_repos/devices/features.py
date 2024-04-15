from datetime import timedelta

from data_sources import device_stats_batch_source, device_stats_stream_source
from entities import device
from feast import FeatureView, Field
from feast.stream_feature_view import stream_feature_view
from feast.types import Float32, Int32
from pyspark.sql import DataFrame

device_stats_view = FeatureView(
    name="device_stats",
    description="device features",
    entities=[device],
    ttl=timedelta(days=36500),
    schema=[
        Field(name="feature_5", dtype=Float32),
        Field(name="feature_3", dtype=Float32),
        Field(name="feature_1", dtype=Float32),
        Field(name="feature_8", dtype=Float32),
        Field(name="feature_6", dtype=Float32),
        Field(name="feature_0", dtype=Float32),
        Field(name="feature_4", dtype=Float32),
    ],
    online=True,
    source=device_stats_batch_source,
)


@stream_feature_view(
    entities=[device],
    ttl=timedelta(days=36500),
    mode="spark",
    schema=[
        Field(name="feature_5", dtype=Float32),
        Field(name="feature_3", dtype=Float32),
        Field(name="feature_1", dtype=Float32),
        Field(name="feature_8", dtype=Float32),
        Field(name="feature_6", dtype=Float32),
        Field(name="feature_0", dtype=Float32),
        Field(name="feature_4", dtype=Float32),
    ],
    timestamp_field="created",
    online=True,
    source=device_stats_stream_source,
)
def device_stats_stream(df: DataFrame):
    from pyspark.sql.functions import col

    return (
        df.withColumn("new_feature_5", col("feature_5") + 1.0)
        .withColumn("new_feature_3", col("feature_3") + 1.0)
        .withColumn("new_feature_1", col("feature_1") + 1.0)
        .withColumn("new_feature_8", col("feature_8") + 1.0)
        .withColumn("new_feature_6", col("feature_6") + 1.0)
        .withColumn("new_feature_0", col("feature_0") + 1.0)
        .withColumn("new_feature_4", col("feature_4") + 1.0)
        .drop(
            "feature_5",
            "feature_3",
            "feature_1",
            "feature_8",
            "feature_6",
            "feature_0",
            "feature_4",
        )
        .withColumnRenamed("new_feature_5", "feature_5")
        .withColumnRenamed("new_feature_3", "feature_3")
        .withColumnRenamed("new_feature_1", "feature_1")
        .withColumnRenamed("new_feature_8", "feature_8")
        .withColumnRenamed("new_feature_6", "feature_6")
        .withColumnRenamed("new_feature_0", "feature_0")
        .withColumnRenamed("new_feature_4", "feature_4")
    )
