# Media Downloads

DryGram allows downloading files from Telegram servers directly into binary memory buffers, saving them to files, or streaming them in chunks.

## Basic Download

To download a file directly:

```python
file_bytes = await client.download("file_id_string")
with open("downloaded_image.jpg", "wb") as f:
    f.write(file_bytes)
```

## Chunked File Streaming

For very large files, download chunks using the stream generator to prevent high memory utilization:

```python
async for chunk in client.stream("large_file_id_string"):
    # Process each chunk asynchronously
    print(f"Downloaded chunk of {len(chunk)} bytes")
```

## Resuming Downloads

If a download fails midway, you can request remaining bytes starting from the saved file offset:

```python
# Resume download from offset 102400 bytes
remaining_bytes = await client.resume_download("large_file_id_string", offset=102400)
```
