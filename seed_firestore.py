import datetime
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-e5805c52e198"
db = firestore.Client(project=PROJECT_ID)
COLLECTION_NAME = "content_drafts"

seed_data = [
    {
        "topic": "Why SEO is Dead in 2026",
        "platform": "TikTok",
        "content": "Visual: Pointing to a graph going down.\nVoiceover: Stop writing SEO articles immediately. AI search just killed the traditional blog...",
        "source_url": "https://example.com/ai-search-trends",
        "status": "draft",
        "created_at": firestore.SERVER_TIMESTAMP
    },
    {
        "topic": "3 Ways to use AI for Market Research",
        "platform": "LinkedIn",
        "content": "Most founders still use surveys for market research.\n\nHere's why you should use AI sentiment analysis instead:\n\n1. It's real-time.\n2. It's unfiltered.\n3. It's free.\n\nStop asking people what they want. Watch what they actually complain about.",
        "source_url": "",
        "status": "review",
        "created_at": firestore.SERVER_TIMESTAMP
    }
]

def seed():
    print(f"Seeding '{COLLECTION_NAME}' in project {PROJECT_ID}...")
    for data in seed_data:
        doc_ref = db.collection(COLLECTION_NAME).document()
        doc_ref.set(data)
        print(f"Added: {data['topic']} (ID: {doc_ref.id})")
    print("Done seeding.")

if __name__ == "__main__":
    seed()
