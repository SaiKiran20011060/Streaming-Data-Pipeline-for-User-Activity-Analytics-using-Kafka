# Hanggout Real-Time Streaming

A real-time data streaming pipeline that listens to Firebase Firestore, processes events through Kafka, and stores data in Snowflake with Databricks integration.

## 🏗️ Architecture

```
Firebase Firestore → Kafka Producer → Kafka Broker → Kafka Consumer → Snowflake
                                                              ↓
                                                      Databricks (Analytics)
```

### Components

- **Producer**: Firebase listener that captures real-time changes and publishes to Kafka
- **Consumer**: Kafka consumer that writes events to Snowflake
- **Spark Streaming**: Stream processing with Apache Spark
- **Databricks**: Data analytics and processing with Delta Lake
- **Docker Compose**: Local Kafka & Zookeeper setup for development

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Kafka (containerized via Docker)
- Firebase Admin Account
- Snowflake Account

https://github.com/user-attachments/assets/161bb6da-99e1-4a54-a276-5bea4d3fd6c6


## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hanggout-real-time-streaming
```

### 2. Create Virtual Environment
```bash
python -m venv kafka-env
source kafka-env/bin/activate  # On Windows: kafka-env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following variables (see `.env.example` for template):

```
FIREBASE_KEY_PATH=<path-to-firebase-credentials>
SNOWFLAKE_USER=<your-snowflake-user>
SNOWFLAKE_PASSWORD=<your-snowflake-password>
SNOWFLAKE_ACCOUNT=<your-snowflake-account>
SNOWFLAKE_WAREHOUSE=<warehouse-name>
SNOWFLAKE_DATABASE=<database-name>
SNOWFLAKE_SCHEMA=<schema-name>
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=hanggout-topic
```

### 5. Add Firebase Credentials

Place your Firebase service account JSON file in the `config/` directory:
```bash
config/haang-out-61e3d-firebase-adminsdk-fbsvc-b6f4f6e9eb.json
```

⚠️ **This file is NOT included in the repository for security reasons.**

## 🐳 Docker Setup

### Start Kafka & Zookeeper

```bash
docker-compose up -d
```

This will start:
- **Zookeeper**: Port 2181
- **Kafka**: Port 9092

### Stop Services
```bash
docker-compose down
```

## 📡 Running the Application

### Start Kafka Producer (Firebase Listener)

```bash
python producer/firebase_listener.py
```

This listens to Firebase Firestore and publishes changes to Kafka.

### Start Kafka Consumer (Snowflake Writer)

```bash
python consumer/snowflake_consumer.py
```

This consumes Kafka messages and writes to Snowflake.

### Spark Streaming Processing

```bash
python consumer/spark_streaming.py
```

## 📊 Snowflake Schema

The consumer creates and maintains the following table:

```sql
CREATE TABLE vacants (
    id INTEGER AUTOINCREMENT,
    creatorUid VARCHAR,
    category VARCHAR,
    area VARCHAR,
    createdAt TIMESTAMP,
    creatorEmail VARCHAR,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

## 🔧 Databricks Integration

Setup Delta Lake tables in Databricks for analytics:

```bash
# Run the setup SQL
databricks sql execute < databricks/delta_setup.sql

# Run the notebook
databricks workspace import databricks/notebook.py
```

## 📦 Project Structure

```
├── producer/
│   ├── firebase_listener.py      # Listens to Firebase Firestore
│   └── kafka_producer.py         # Sends data to Kafka
├── consumer/
│   ├── snowflake_consumer.py     # Consumes from Kafka, writes to Snowflake
│   └── spark_streaming.py        # Spark Streaming for real-time processing
├── databricks/
│   ├── delta_setup.sql           # Delta Lake table setup
│   └── notebook.py               # Databricks notebook
├── config/
│   └── kafka_config.py           # Kafka configuration
├── data/
│   └── sample_payload.json       # Sample data payload
├── tests/
│   ├── test_producer.py          # Producer tests
│   └── test_consumer.py          # Consumer tests
├── utils/
│   └── logger.py                 # Logging utilities
├── docker-compose.yml            # Docker Compose config
└── requirements.txt              # Python dependencies
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 📝 Configuration Files

### .env (Not Included - Security)
- Contains sensitive credentials
- Firebase key path
- Snowflake credentials
- Kafka configuration
- **See `.env.example` for template**

### .gitignore
- `.env` - Environment variables
- `config/haang-out-61e3d-firebase-adminsdk-fbsvc-b6f4f6e9eb.json` - Firebase credentials
- `kafka-env/` - Virtual environment

## 🔐 Security Notes

⚠️ **IMPORTANT**: The following files are intentionally excluded from version control:

1. **`.env`** - Contains sensitive credentials (Snowflake passwords, API keys)
2. **Firebase JSON Key** - Service account credentials for Firebase

**Never commit these files to version control.**

To set up on a new machine:
1. Clone the repository
2. Copy `.env.example` to `.env`
3. Fill in the actual credentials
4. Add your Firebase service account JSON to `config/`

## 🚀 Deployment

### Local Development
Use Docker Compose and run scripts directly.

### Production Deployment
- Use managed Kafka services (Confluent Cloud, AWS MSK)
- Use Snowflake cloud
- Deploy producer/consumer as containerized services
- Use orchestration tools (Airflow, Kubernetes)

## 🐛 Troubleshooting

### Kafka Connection Issues
```bash
# Check if Kafka is running
docker ps | grep kafka

# View Kafka logs
docker logs kafka
```

### Firebase Authentication Errors
- Verify Firebase JSON credentials file path
- Check FIREBASE_KEY_PATH in `.env`
- Ensure Firebase service account has Firestore access

### Snowflake Connection Errors
- Verify Snowflake account name and credentials
- Check network connectivity to Snowflake
- Ensure warehouse is active

## 📚 Dependencies

- `firebase-admin` - Firebase SDK
- `kafka-python` - Kafka client
- `python-dotenv` - Environment variable management
- `snowflake-connector-python` - Snowflake SDK
- `pyspark` - Apache Spark (for stream processing)
- `pytest` - Testing framework

## 📖 Additional Resources

- [Kafka Documentation](https://kafka.apache.org/documentation/)
- [Firebase Firestore](https://firebase.google.com/docs/firestore)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [Databricks Delta Lake](https://docs.databricks.com/delta/)
- [Apache Spark Streaming](https://spark.apache.org/docs/latest/streaming-programming-guide.html)

## 📄 License

[Add your license here]

## 👥 Authors

- [Your Name/Team]

## 📞 Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Last Updated**: April 2026
