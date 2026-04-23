import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os
import time
from kafka_producer import send_to_kafka

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()
firebase_path = os.getenv("FIREBASE_KEY_PATH")

if not firebase_path:
    raise ValueError("FIREBASE_KEY_PATH not found in .env")

# -------------------------------
# INIT FIREBASE
# -------------------------------
cred = credentials.Certificate(firebase_path)

firebase_admin.initialize_app(cred)

db = firestore.client()

print("🔥 Firebase initialized successfully")


# -------------------------------
# VACANTS LISTENER
# -------------------------------
def vacants_listener(col_snapshot, changes, read_time):
    print("📡 Vacants snapshot received")

    for change in changes:
        data = change.document.to_dict()

        print("Change Type:", change.type.name, data)

        if change.type.name in ["ADDED", "MODIFIED"]:
            payload = {
                "type": "vacant",
                "creatorUid": data.get("creatorUid"),
                "category": data.get("category"),
                "area": data.get("area"),
                "createdAt": str(data.get("createdAt")),
                "creatorEmail": data.get("creatorEmail")
            }

            print("🚀 Sending Vacant:", payload)
            send_to_kafka(payload)


# -------------------------------
# REQUESTS LISTENER
# -------------------------------
def requests_listener(col_snapshot, changes, read_time):
    print("📡 Requests snapshot received")

    for change in changes:
        data = change.document.to_dict()

        print("Change Type:", change.type.name, data)

        if change.type.name in ["ADDED", "MODIFIED"]:
            payload = {
                "type": "request",
                "requesterUid": data.get("requesterUid"),
                "requesterEmail": data.get("requesterEmail"),
                "createdAt": str(data.get("createdAt")),
                "vacantId": data.get("vacantId")
            }

            print("🚀 Sending Request:", payload)
            send_to_kafka(payload)


# -------------------------------
# ATTACH LISTENERS
# -------------------------------
vacants_ref = db.collection("vacants")
requests_ref = db.collection("requests")

vacants_watch = vacants_ref.on_snapshot(vacants_listener)
requests_watch = requests_ref.on_snapshot(requests_listener)

print("🔥 Listening to Firebase (vacants & requests)...")

# Keep alive
while True:
    time.sleep(5)