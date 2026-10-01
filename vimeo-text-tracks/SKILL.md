---
name: vimeo-text-tracks
description: Manages Vimeo text tracks (subtitles, captions) via the API. Use to list videos, upload VTT subtitle files, and set tracks as active.
tags: [vimeo, subtitles, captions, text-tracks, video]
---

# Vimeo Text Tracks Skill

## Purpose
List Vimeo videos, upload VTT subtitle/caption files, and manage text tracks via the Vimeo API using the PyVimeo SDK.

## Prerequisites
- PyVimeo SDK installed: `pip install PyVimeo`
- **Team account**: Videos are owned by user `<TEAM_OWNER_USER_ID>` (the team owner). Use `/users/<TEAM_OWNER_USER_ID>/videos` to list videos, not `/me/videos`.

## Credentials

Credentials live in `~/.config/lifelab/tokens.env`. Source it first, then read from env vars:

```bash
source ~/.config/lifelab/tokens.env
```

```python
import os
import vimeo

client = vimeo.VimeoClient(
    token=os.environ['VIMEO_ACCESS_TOKEN'],
    key=os.environ['VIMEO_CLIENT_KEY'],
    secret=os.environ['VIMEO_CLIENT_SECRET'],
)
```

## Your Task

When the user asks to manage Vimeo text tracks, follow the appropriate workflow below. All workflows use inline Python scripts.

---

## Workflow 1: List All Videos

List all videos with their IDs and existing text tracks.

```python
import os
import vimeo

client = vimeo.VimeoClient(
    token=os.environ['VIMEO_ACCESS_TOKEN'],
    key=os.environ['VIMEO_CLIENT_KEY'],
    secret=os.environ['VIMEO_CLIENT_SECRET'],
)

page = 1
while True:
    response = client.get('/users/<TEAM_OWNER_USER_ID>/videos', params={
        'per_page': 25,
        'page': page,
        'fields': 'uri,name,metadata.connections.texttracks'
    })
    data = response.json()
    for v in data['data']:
        vid = v['uri'].split('/')[-1]
        tt = v['metadata']['connections']['texttracks']['total']
        print(f"{vid}  {tt} tracks  {v['name']}")
    if data['paging']['next'] is None:
        break
    page += 1
```

### List Existing Text Tracks for a Specific Video

```python
VIDEO_ID = "YOUR_VIDEO_ID"
response = client.get(f'/videos/{VIDEO_ID}/texttracks')
for track in response.json()['data']:
    tid = track['uri'].split('/')[-1]
    print(f"  ID: {tid}  Lang: {track['display_language']} ({track['language']})  Active: {track['active']}  Source: {track['provenance']}")
```

---

## Workflow 2: Upload a VTT Subtitle File

Follow these steps in order for each video. This is the proven workflow that works.

```python
import os
import vimeo
import requests

client = vimeo.VimeoClient(
    token=os.environ['VIMEO_ACCESS_TOKEN'],
    key=os.environ['VIMEO_CLIENT_KEY'],
    secret=os.environ['VIMEO_CLIENT_SECRET'],
)

VIDEO_ID = "YOUR_VIDEO_ID"
VTT_FILE = "/path/to/subtitles.vtt"
LANGUAGE = "es"        # ISO 639-1 language code
TRACK_NAME = "Spanish" # Display name

# Step 1: Create the text track entry
response = client.post(f'/videos/{VIDEO_ID}/texttracks', data={
    'type': 'subtitles',
    'language': LANGUAGE,
    'name': TRACK_NAME
})
result = response.json()
upload_link = result['link']
track_uri = result['uri']
track_id = track_uri.split('/')[-1]
print(f"Created track {track_id}, uploading...")

# Step 2: Upload VTT file contents to the upload link
with open(VTT_FILE, 'r') as f:
    vtt_content = f.read()
requests.put(upload_link, data=vtt_content.encode('utf-8'), headers={'Content-Type': 'text/plain'})
print("VTT file uploaded")

# Step 3: Activate the text track
client.patch(track_uri, data={'active': True})
print("Track activated")

# Step 4: Verify
response = client.get(f'/videos/{VIDEO_ID}/texttracks')
for track in response.json()['data']:
    tid = track['uri'].split('/')[-1]
    print(f"  ID: {tid}  Lang: {track['display_language']}  Active: {track['active']}  Source: {track['provenance']}")
```

---

## Workflow 3: Delete a Text Track

```python
VIDEO_ID = "YOUR_VIDEO_ID"
TRACK_ID = "YOUR_TRACK_ID"

response = client.delete(f'/videos/{VIDEO_ID}/texttracks/{TRACK_ID}')
# 204 means success
print(f"Delete status: {response.status_code}")
```

---

## Batch Upload: Subtitles for Multiple Videos

When uploading subtitles to multiple videos at once:

1. List all videos (Workflow 1)
2. For each video, ask the user which VTT file to use
3. Run Workflow 2 for each video
4. Print a summary table of results

---

## Common Language Codes

| Language | Code |
|----------|------|
| English  | en   |
| Spanish  | es   |
| French   | fr   |
| German   | de   |
| Portuguese | pt |
| Chinese  | zh   |
| Japanese | ja   |
| Korean   | ko   |
| Arabic   | ar   |

---

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Proceed |
| 201 | Created | Track created, extract upload link |
| 204 | No Content | Delete succeeded |
| 400 | Bad Request | Check JSON payload format |
| 401 | Unauthorized | Token expired -- regenerate token from Vimeo app settings |
| 403 | Forbidden | Token lacks required scopes |
| 404 | Not Found | Video ID or track ID is wrong |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry after a delay |

### Common Issues

- **401 with curl but 200 with SDK**: Use the PyVimeo SDK -- it handles auth headers correctly
- **"The app didn't receive the user's credentials"**: This means curl auth failed. Switch to the SDK.
- **Upload fails silently**: Ensure the VTT file is valid WebVTT format (starts with `WEBVTT`)
- **Track not appearing**: After upload, it can take a few seconds for processing. Retry verification.
- **Wrong language**: Use ISO 639-1 two-letter codes (e.g., `es` not `spanish`)

## Notes

- Vimeo supports subtitle types: `subtitles` and `captions`
- Each video can have multiple text tracks in different languages
- Only one track per language can be active at a time
- VTT files must be valid WebVTT format
- The upload link from Step 1 is temporary -- use it promptly
- The authenticated user (`<YOUR_USER_ID>`, free account) is not the video owner; videos are owned by a team member (`<TEAM_OWNER_USER_ID>`)
