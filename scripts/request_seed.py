import requests
import json

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

STUDENT_ID = "23P31A42G3"
GITHUB_REPO_URL = "https://github.com/JallaShalini/pki-2fa-microservice"


def request_seed(student_id: str, github_repo_url: str, api_url: str):
    # 1. Read student public key
    with open("student_public.pem", "r") as f:
        public_key = f.read()

    # 2. Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # 3. Send POST request
    response = requests.post(
        api_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=15
    )

    # 4. Handle response
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    data = response.json()

    if "encrypted_seed" not in data:
        raise Exception(f"Unexpected response: {data}")

    # 5. Save encrypted seed
    with open("encrypted_seed.txt", "w") as f:
        f.write(data["encrypted_seed"])

    print("✅ Encrypted seed saved to encrypted_seed.txt")


if __name__ == "__main__":
    request_seed(STUDENT_ID, GITHUB_REPO_URL, API_URL)

