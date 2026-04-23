import json
import os
import time
import logging
from kafka import KafkaConsumer
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Kafka-Snowflake-Consumer")

# Kafka Config
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

# Snowflake Config
SNOWFLAKE_CONFIG = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
}


# -------------------------------
# Snowflake Connection
# -------------------------------
def get_snowflake_connection():
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)


# -------------------------------
# Insert Functions
# -------------------------------
def insert_vacant(cursor, data):
    query = """
    INSERT INTO vacants (creatorUid, category, area, createdAt, creatorEmail)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        data.get("creatorUid"),
        data.get("category"),
        data.get("area"),
        data.get("createdAt"),
        data.get("creatorEmail"),
    ))


def insert_request(cursor, data):
    query = """
    INSERT INTO requests (requesterUid, requesterEmail, createdAt, vacantId)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        data.get("requesterUid"),
        data.get("requesterEmail"),
        data.get("createdAt"),
        data.get("vacantId"),
    ))


# -------------------------------
# Message Processor
# -------------------------------
def process_message(cursor, message):
    try:
        data = json.loads(message.value.decode("utf-8"))

        logger.info(f"Received: {data}")

        if data.get("type") == "vacant":
            insert_vacant(cursor, data)

        elif data.get("type") == "request":
            insert_request(cursor, data)

        else:
            logger.warning("Unknown message type")

    except Exception as e:
        logger.error(f"Error processing message: {e}")


# -------------------------------
# Main Consumer Loop
# -------------------------------
def run_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='snowflake-consumer-group',
        value_deserializer=lambda x: x
    )

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    logger.info("Consumer started...")

    try:
        for message in consumer:
            process_message(cursor, message)
            conn.commit()

    except KeyboardInterrupt:
        logger.info("Stopping consumer...")

    finally:
        cursor.close()
        conn.close()


# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    run_consumer()