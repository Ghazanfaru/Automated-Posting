
import httpx

from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/blogger"
]


def main():

    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json",
        scopes=SCOPES
    )

    credentials = flow.run_local_server(
        port=0,
        access_type="offline",
        prompt="consent"
    )

    print("\nOAuth authentication successful!")

    print("\nBLOGGER_REFRESH_TOKEN:")
    print(credentials.refresh_token)

    # Retrieve the user's Blogger blogs
    response = httpx.get(
        "https://www.googleapis.com/blogger/v3/users/self/blogs",
        headers={
            "Authorization": f"Bearer {credentials.token}"
        },
        timeout=30.0
    )

    response.raise_for_status()

    blogs = response.json().get("items", [])

    print("\nYour Blogger blogs:")

    for blog in blogs:
        print("---------------------------")
        print("Blog Name:", blog["name"])
        print("Blog ID:", blog["id"])
        print("Blog URL:", blog["url"])


if __name__ == "__main__":
    main()
