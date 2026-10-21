from typing import Dict, List, Optional
import datetime
from google.cloud import firestore
import httpx
from bs4 import BeautifulSoup

# Hardcode project ID to avoid deployment auth issues on Agent Runtime
PROJECT_ID = "qwiklabs-gcp-03-e5805c52e198"
db = firestore.Client(project=PROJECT_ID)

COLLECTION_NAME = "content_drafts"

def add_content_draft(topic: str, platform: str, content: str, source_url: str = "", status: str = "draft") -> str:
    """Adds a new content draft to the database.

    Args:
        topic: The subject or title of the content (e.g., "AI Marketing Trends").
        platform: Target platform (e.g., "LinkedIn", "Twitter", "TikTok").
        content: The drafted content or script.
        source_url: URL of the source material, if any.
        status: The current status of the draft. Defaults to "draft". Valid values: "draft", "review", "published".

    Returns:
        A string confirming the creation and the ID of the new draft.
    """
    doc_ref = db.collection(COLLECTION_NAME).document()
    doc_ref.set({
        "topic": topic,
        "platform": platform,
        "content": content,
        "source_url": source_url,
        "status": status,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return f"Successfully added draft for '{topic}' on {platform}. Draft ID: {doc_ref.id}"


def list_content_drafts(status: Optional[str] = None, platform: Optional[str] = None) -> str:
    """Retrieves a list of content drafts, optionally filtered by status or platform.

    Args:
        status: If provided, only returns drafts with this status (e.g., "draft", "review", "published").
        platform: If provided, only returns drafts for this platform (e.g., "LinkedIn").

    Returns:
        A formatted string listing the matching drafts and their IDs, or a message if none are found.
    """
    query = db.collection(COLLECTION_NAME)
    
    if status:
        query = query.where("status", "==", status)
    if platform:
        query = query.where("platform", "==", platform)
        
    # Order by creation date descending
    query = query.order_by("created_at", direction=firestore.Query.DESCENDING)
    
    docs = query.stream()
    
    results = []
    for doc in docs:
        data = doc.to_dict()
        results.append(
            f"ID: {doc.id} | Topic: {data.get('topic', 'N/A')} | "
            f"Platform: {data.get('platform', 'N/A')} | Status: {data.get('status', 'N/A')}"
        )
        
    if not results:
        return "No drafts found matching the criteria."
        
    return "Content Drafts:\n" + "\n".join(results)


def update_draft_status(draft_id: str, new_status: str) -> str:
    """Updates the status of an existing content draft.

    Args:
        draft_id: The exact ID of the draft document in the database.
        new_status: The new status to set (e.g., "review", "published").

    Returns:
        A string confirming the update, or an error message if the draft was not found.
    """
    doc_ref = db.collection(COLLECTION_NAME).document(draft_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        return f"Error: Draft with ID '{draft_id}' not found."
        
    doc_ref.update({"status": new_status})
    return f"Successfully updated draft '{draft_id}' status to '{new_status}'."


def fetch_url_content(url: str) -> str:
    """Fetches and extracts the readable text content from a given URL.
    Use this to read articles, blog posts, or web pages before repurposing them.

    Args:
        url: The full HTTP/HTTPS URL of the web page to read.

    Returns:
        The extracted text content of the web page, or an error message if it fails.
    """
    try:
        # Use a generic User-Agent to avoid basic blocks
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text(separator="\n")
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        
        # Truncate to a reasonable length for the LLM context if it's too long
        return text[:15000]
    except Exception as e:
        return f"Failed to fetch content from {url}. Error: {str(e)}"


def find_word_synonyms(word: str) -> str:
    """Finds alternative related words (meaning similar things or often used in the same context).
    Use this to find alternative vocabulary to avoid AI clichés (e.g., 'delve', 'leverage', 'game-changer').

    Args:
        word: The English word to look up.

    Returns:
        A string containing a list of related vocabulary words.
    """
    import httpx
    
    # Using Datamuse API: ml (meaning like) gives much better practical alternatives than strictly rel_syn
    url = f"https://api.datamuse.com/words?ml={word.strip().lower()}&max=15"
    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return f"No related words found for '{word}'."
            
        synonyms = [item['word'] for item in data]
        
        return f"Alternative words for '{word}':\n" + ", ".join(synonyms)
        
    except Exception as e:
        return f"Failed to look up word '{word}'. Error: {str(e)}"
