def serialize_document(doc):
    """Convert a Beanie document to a dict with ObjectId converted to str."""
    if hasattr(doc, "dict"):
        # For Beanie/Pydantic models, use their dict method
        doc_dict = doc.dict()
        # Convert ObjectId to str
        if "_id" in doc_dict:
            doc_dict["_id"] = str(doc_dict["_id"])
        return doc_dict
    elif isinstance(doc, list):
        # Handle lists of documents
        return [serialize_document(item) for item in doc]
    elif isinstance(doc, dict):
        # Handle dictionaries that might contain ObjectId
        return {k: serialize_document(v) for k, v in doc.items()}
    else:
        # Return the value as is if it's not a document
        return doc
