
## Supported Platforms

The API currently integrates with:

- Discord
- Bluesky
- Blogger

Each platform is implemented independently using a common publishing interface.

## Architecture

- FastAPI handles incoming HTTP requests.
- Pydantic validates request data.
- Individual platform classes handle third-party API communication.
- The central posting service executes integrations concurrently.
- Failures are isolated so one platform does not prevent publishing attempts on others.
- Environment variables store API credentials.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure your `.env` file using `.env.example`.

Start the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

Open Swagger documentation:

http://localhost:4000/docs

## Example Request

POST `/posting`

```json
{
  "message": "Check out our latest business platform https://example.com"
}
```

## Example Response

```json
{
  "success": true,
  "results": [
    {
      "platform": "Discord",
      "status": "success",
      "posted_url": "https://discord.com/example",
      "public_access": false,
      "date": "2026-11-23",
      "time": "00:30:00",
      "error": null
    },
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/example",
      "public_access": true,
      "date": "2026-11-23",
      "time": "00:30:00",
      "error": null
    },
    {
      "platform": "Blogger",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": "2026-11-23",
      "time": "00:30:00",
      "error": "Example API error"
    }
  ]
}
```