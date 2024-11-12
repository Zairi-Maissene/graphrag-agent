import lancedb
from .llm.llm import LLMClient

def retrieve_docs(document_id, query):
    # Connect to LanceDB (assuming local connection to the outputs/lance folder)
    db = lancedb.connect(f"graphs/{document_id}/output/lancedb")
    # Open the text unit table
    table = db.open_table("default-text_unit-text")

    embeddings = LLMClient().get_embeddings(query)
    response = (
        table.search(
            embeddings
        )
        .metric("cosine")
        .limit(20)  # Adjust the limit as needed
        .to_list()
    )
    # Extract relevant text chunks
    response = [{"text": item["text"], "distance": item["_distance"]} for item in response]

    return response