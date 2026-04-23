from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("KafkaConsumer") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host.docker.internal:9092") \
    .option("subscribe", "vacancies-topic,requests-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert to readable format
df = df.selectExpr("CAST(topic AS STRING)", "CAST(value AS STRING)")

query = df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

query.awaitTermination()