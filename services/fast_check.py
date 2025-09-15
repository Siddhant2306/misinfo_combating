from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv

load_dotenv()

fact_check_api_key = os.getenv("FACT_CHECK_API_KEY")

service = build("factchecktools", "v1alpha1", developerKey=fact_check_api_key)

def search_claims(query: str, language="en"):
    result = service.claims().search(query=query, languageCode=language).execute()
    claims_output = []

    if "claims" in result:
        for claim in result["claims"]:
            claim_obj = {
                "text": claim.get("text", ""),
                "claimReview": []
            }
            if "claimReview" in claim:
                for review in claim["claimReview"]:
                    claim_obj["claimReview"].append({
                        "textualRating": review.get("textualRating", ""),
                        "publisher": {
                            "name": review.get("publisher", {}).get("name", "")
                        },
                        "url": review.get("url", "")
                    })
            claims_output.append(claim_obj)

    # replace later with Gemini API call
    gemini_analysis = "Based on verified sources, this claim needs further context."

    result_json = {
        "claims": claims_output,
        "gemini_analysis": gemini_analysis
    }

    # Save output to file 
    output_file = "factcheck_output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_json, f, indent=2, ensure_ascii=False)

    return result_json


if __name__ == "__main__":
    query = "COVID vaccines contain microchips"
    output = search_claims(query)
    print(json.dumps(output, indent=2))
