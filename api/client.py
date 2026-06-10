import requests

from config import BASE_URL, HEADERS


class ZafronixAPIError(RuntimeError):
    pass


class ZafronixRateLimitError(ZafronixAPIError):
    pass


class ZafronixClient:
    def get(self, endpoint, params=None):
        url = f"{BASE_URL}/{endpoint}"
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=30,
        )

        retry_after = response.headers.get("Retry-After")
        rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")

        if response.status_code == 429 or rate_limit_remaining == "0":
            details = [
                f"GET {url} hit the API rate limit",
                f"HTTP {response.status_code} {response.reason}",
            ]

            if retry_after:
                details.append(f"Retry-After: {retry_after} seconds")

            raise ZafronixRateLimitError(". ".join(details))

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError as exc:
            content_type = response.headers.get("Content-Type", "unknown")
            body_preview = response.text.strip().replace("\n", " ")[:300]

            details = [
                f"GET {url} returned HTTP {response.status_code} {response.reason}",
                f"Content-Type: {content_type}",
            ]

            if retry_after:
                details.append(f"Retry-After: {retry_after}")

            if rate_limit_remaining is not None:
                details.append(f"X-RateLimit-Remaining: {rate_limit_remaining}")

            details.append(f"Body: {body_preview or '<empty>'}")

            raise ZafronixAPIError(
                "API returned a non-JSON response. " + " | ".join(details)
            ) from exc

        if not response.ok:
            error = data.get("error", "unknown_error") if isinstance(data, dict) else "unknown_error"
            message = data.get("message", data) if isinstance(data, dict) else data
            request_id = data.get("request_id") if isinstance(data, dict) else None

            details = [
                f"GET {url} returned HTTP {response.status_code} {response.reason}",
                f"error={error}",
                f"message={message}",
            ]

            if request_id:
                details.append(f"request_id={request_id}")

            raise ZafronixAPIError("API request failed. " + " | ".join(details))

        return data
