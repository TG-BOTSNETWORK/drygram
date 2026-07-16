# Media Uploads

DryGram handles file transfers asynchronously, providing automatic chunking, progress callbacks, and upload resumption capabilities.

## Basic File Upload

To upload a file and obtain a media identifier without sending a message:

```python
file_id = await client.upload("path/to/large_document.zip")
print(f"File uploaded successfully. ID: {file_id}")
```

## Resuming Interrupted Uploads

If a connection is interrupted, you can resume the upload using the byte offset that was successfully written:

```python
# Resume upload from offset 204800 bytes
resumed_id = await client.resume_upload("path/to/large_document.zip", offset=204800)
```

## Parallel Uploads Configuration

DryGram uses connection pooling to upload file chunks in parallel. You can scale this by configuring the pool size on `DryClient`:

```python
# Initializing client with 10 connection slots
client = DryClient("session_name", api_id=123, api_hash="abc")
# Chunks are dispatched concurrently over multiple connections
```
