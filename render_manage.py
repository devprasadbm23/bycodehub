"""
render_manage.py

Utility to manage Render service env vars and trigger deploys via the Render API.

Usage examples:
  # Set a single env var
  RENDER_API_KEY=xxxx python render_manage.py --service-id <service-id> --set DATABASE_URL "postgresql://..."

  # Load env vars from a .env file and upsert them
  RENDER_API_KEY=xxxx python render_manage.py --service-id <service-id> --set-file .env.local

  # Trigger a manual deploy
  RENDER_API_KEY=xxxx python render_manage.py --service-id <service-id> --deploy

Notes:
- The script reads the API key from the `RENDER_API_KEY` environment variable (or `--api-key`).
- You must provide the Render service ID (found in Render dashboard URL or API responses).
- This tool does not store secrets in the repo; supply API key via env var or secure secret manager.
"""

import os
import sys
import json
import argparse
from typing import Dict, Optional

try:
    import requests
except ImportError:
    print("Missing dependency 'requests'. Install with: pip install requests")
    sys.exit(1)

RENDER_API_BASE = "https://api.render.com/v1"


def headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def get_env_vars(service_id: str, api_key: str):
    url = f"{RENDER_API_BASE}/services/{service_id}/env-vars"
    r = requests.get(url, headers=headers(api_key))
    r.raise_for_status()
    return r.json()


def create_env_var(service_id: str, api_key: str, key: str, value: str):
    url = f"{RENDER_API_BASE}/services/{service_id}/env-vars"
    payload = {"key": key, "value": value}
    r = requests.post(url, headers=headers(api_key), data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def update_env_var(service_id: str, api_key: str, env_var_id: str, value: str):
    url = f"{RENDER_API_BASE}/services/{service_id}/env-vars/{env_var_id}"
    payload = {"value": value}
    r = requests.patch(url, headers=headers(api_key), data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def set_env_var(service_id: str, api_key: str, key: str, value: str):
    # Fetch existing env vars and either update or create
    envs = get_env_vars(service_id, api_key)
    existing = next((e for e in envs if e.get("key") == key), None)
    if existing:
        print(f"Updating env var {key}")
        return update_env_var(service_id, api_key, existing["id"], value)
    else:
        print(f"Creating env var {key}")
        return create_env_var(service_id, api_key, key, value)


def trigger_deploy(service_id: str, api_key: str) -> Dict:
    url = f"{RENDER_API_BASE}/services/{service_id}/deploys"
    payload = {}  # Render accepts empty body for manual deploys
    r = requests.post(url, headers=headers(api_key), data=json.dumps(payload))
    r.raise_for_status()
    return r.json()


def load_env_file(path: str) -> Dict[str, str]:
    result = {}
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            result[k.strip()] = v.strip().strip('"').strip("'")
    return result


def main():
    p = argparse.ArgumentParser(description="Manage Render env vars and trigger deploys")
    p.add_argument("--service-id", required=True, help="Render service ID (not name)")
    p.add_argument("--api-key", help="Render API key (or use RENDER_API_KEY env var)")
    p.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"), help="Set a single env var")
    p.add_argument("--set-file", metavar="FILE", help="Load env vars from a .env-style file and upsert them")
    p.add_argument("--deploy", action="store_true", help="Trigger a manual deploy for the service")

    args = p.parse_args()
    api_key = args.api_key or os.environ.get("RENDER_API_KEY")
    if not api_key:
        print("Error: Render API key is required. Set RENDER_API_KEY or provide --api-key")
        sys.exit(2)

    service_id = args.service_id

    try:
        if args.set:
            key, value = args.set
            resp = set_env_var(service_id, api_key, key, value)
            print("OK:", json.dumps(resp, indent=2))

        if args.set_file:
            envs = load_env_file(args.set_file)
            for k, v in envs.items():
                try:
                    resp = set_env_var(service_id, api_key, k, v)
                    print(f"Upserted {k}")
                except Exception as ex:
                    print(f"Failed to set {k}: {ex}")

        if args.deploy:
            resp = trigger_deploy(service_id, api_key)
            print("Deploy triggered:", json.dumps(resp, indent=2))

        if not (args.set or args.set_file or args.deploy):
            print("No action requested. Use --set, --set-file, or --deploy. See --help.")

    except requests.HTTPError as http_err:
        print(f"HTTP error: {http_err} - {http_err.response.text if http_err.response is not None else ''}")
        sys.exit(3)
    except Exception as e:
        print("Error:", e)
        sys.exit(4)


if __name__ == "__main__":
    main()
