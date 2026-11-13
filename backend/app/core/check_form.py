import re


def check_form_email(email: str) -> bool:
    if not email or len(email) > 254:
        return False

    pattern = (
        r"[a-zA-Z0-9._%+-]+"
        r"@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?[.])+"
        r"[a-zA-Z]{2,}"
    )

    if not re.fullmatch(pattern, email):
        return False

    local_part = email.split("@", 1)[0]
    if ".." in local_part or local_part.startswith(".") or local_part.endswith("."):
        return False

    return True