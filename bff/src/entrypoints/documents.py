# TODO Projects.create
# ## Important Notes
# When frontend is ready, this endpoint should be rewritten.
# 
# **Current Behavior:**
# - Creates document metadata in database
# - Uploads file directly to S3
# - Returns complete document object
# 
# **Future Implementation:**
# - Use `POST /documents/` for metadata only
# - Use `GET /documents/{document_id}/get-upload-url` for file upload (when frontend is ready)
# 
# **Flow should be like this:**
# - client send document metadata;
# - document creates in DB and mark as "not completed" (or something else);
# - client get response with all metadata including document_id;
# - client make GET request to /{document_id}/get-upload-url and get direct link for S3 uploading;
# - client make PUT request to this link with file content;
# - after uploading is completed, S3 push message to a queue;
# - documents service read this message and mark document as completed;
# - if document is not marked as completed for upload link expiring time - responsible user should be notified"""
