from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import urlopen

import streamlit as st

from app.core.config import get_settings


def fetch_health_status(base_url: str) -> tuple[bool, str]:
    health_url = f"{base_url.rstrip('/')}/health"
    try:
        with urlopen(health_url, timeout=3) as response:
            payload = json.loads(response.read().decode("utf-8"))
        service = payload.get("service", "FastAPI")
        status = payload.get("status", "unknown")
        return status == "ok", f"{service} is {status}"
    except URLError as exc:
        return False, f"FastAPI is unavailable at {health_url}: {exc.reason}"
    except TimeoutError:
        return False, f"FastAPI did not respond within 3 seconds at {health_url}"
    except json.JSONDecodeError:
        return False, f"FastAPI returned an invalid health response at {health_url}"


def main() -> None:
    settings = get_settings()

    st.set_page_config(
        page_title=settings.app_name,
        layout="wide",
    )

    st.sidebar.title("Navigation")
    st.sidebar.radio(
        "Sections",
        ["Overview", "Resume Match", "Cover Letter", "Interview Prep"],
        index=0,
    )

    st.title(settings.app_name)
    st.write(
        "A local-first AI platform for resume parsing, job matching, and career preparation."
    )

    is_healthy, message = fetch_health_status(settings.fastapi_base_url)
    if is_healthy:
        st.success(message)
    else:
        st.warning(message)


if __name__ == "__main__":
    main()
