import os
import pickle
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pymongo import MongoClient

# Gmail API setup
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_PICKLE_FILE = "token.pickle"
CREDENTIALS_FILE = "credentials.json"  # Download this from Google Cloud Console

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "gmail_db"
COLLECTION_NAME = "emails"


def get_gmail_service():
    """
    Creates and returns an authenticated Gmail API service instance.
    Uses token.pickle for storing/retrieving credentials to avoid manual login.
    """
    creds = None

    # Load existing token if it exists
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, "rb") as token:
            creds = pickle.load(token)

    # If credentials don't exist or are invalid, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This will open a browser window for authorization (only once)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PICKLE_FILE, "wb") as token:
            pickle.dump(creds, token)

    # Create and return the Gmail API service
    return build("gmail", "v1", credentials=creds)


def connect_to_mongodb():
    """Connects to MongoDB and returns the collection object."""
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


def get_unprocessed_emails(service, mongodb_collection):
    """
    Fetches emails from Gmail that haven't been processed yet.
    Uses a unique ID based on message ID and timestamp to track processed messages.
    """
    # Get list of message IDs already in MongoDB
    processed_message_ids = set(
        doc["gmail_id"] for doc in mongodb_collection.find({}, {"gmail_id": 1})
    )

    # Query Gmail for messages
    results = service.users().messages().list(userId="me", maxResults=50).execute()
    messages = results.get("messages", [])

    unprocessed_emails = []

    for message in messages:
        message_id = message["id"]

        # Skip already processed messages
        if message_id in processed_message_ids:
            continue

        # Get full message details
        msg = service.users().messages().get(userId="me", id=message_id).execute()

        # Create a unique identifier that includes the message ID and received time
        internal_date = int(msg["internalDate"]) / 1000  # Convert to seconds
        datetime_obj = datetime.fromtimestamp(internal_date)
        unique_id = f"{message_id}_{int(internal_date)}"

        # Extract email information (simplified for the skeleton)
        headers = msg["payload"]["headers"]
        subject = next(
            (
                header["value"]
                for header in headers
                if header["name"].lower() == "subject"
            ),
            "No Subject",
        )
        sender = next(
            (header["value"] for header in headers if header["name"].lower() == "from"),
            "Unknown",
        )

        # Create email document
        email_doc = {
            "gmail_id": message_id,
            "unique_id": unique_id,
            "subject": subject,
            "sender": sender,
            "date": datetime_obj,
            "processed_at": datetime.now(),
            "snippet": msg.get("snippet", ""),
            # Add more fields as needed
        }

        unprocessed_emails.append(email_doc)

    return unprocessed_emails


def process_and_store_emails():
    """Main function to process emails and store them in MongoDB."""
    # Get authenticated Gmail service
    gmail_service = get_gmail_service()

    # Connect to MongoDB
    mongo_collection = connect_to_mongodb()

    # Create a unique index on unique_id to prevent duplicates
    mongo_collection.create_index("unique_id", unique=True)

    # Get unprocessed emails
    new_emails = get_unprocessed_emails(gmail_service, mongo_collection)

    # Store emails in MongoDB
    if new_emails:
        try:
            mongo_collection.insert_many(new_emails, ordered=False)
            print(f"Successfully stored {len(new_emails)} new emails.")
        except Exception as e:
            print(f"Error storing emails: {e}")
    else:
        print("No new emails to process.")


if __name__ == "__main__":
    process_and_store_emails()
