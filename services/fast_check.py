import re
import json
from .base_fact import get_factcheck_service
from googleapiclient.errors import HttpError


# Initialize service once
factcheck_service = get_factcheck_service()

# Fact check search function
def search_claims(prompt: str, language="en"):
    # 1️⃣ Clean the prompt
    clean_prompt = re.sub(r"[^\x00-\x7F]+", "", prompt).strip()
    if len(clean_prompt) > 200:
        clean_prompt = clean_prompt[:200]  # API prefers short claims

    print("Query being sent:", clean_prompt)
    print("Type:", type(clean_prompt))

    # 2️⃣ Call Fact Check Tools API with query parameter
    try:
        result = factcheck_service.claims().search(
            query=clean_prompt,  # just the string
            languageCode=language
        ).execute()
    except HttpError as e:
        print("Fact Check API error:", e)
        return []  # return empty list if API fails

    # 3️⃣ Process results
    claims_output = []
    if "claims" in result:
        for claim in result["claims"]:
            claim_obj = {
                "text": claim.get("text", ""),
                "claimReview": []
            }
            for review in claim.get("claimReview", []):
                claim_obj["claimReview"].append({
                    "textualRating": review.get("textualRating", ""),
                    "publisher": {
                        "name": review.get("publisher", {}).get("name", "")
                    },
                    "url": review.get("url", "")
                })
            claims_output.append(claim_obj)
            print("Web-Search:")
            print(json.dumps(claim_obj, indent=4, ensure_ascii=False))
            print("-" * 50) 
            
    return claims_output;
