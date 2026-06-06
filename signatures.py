SIGNATURES = [
    {
        "name": "PNG",
        "extensions": [".png"],
        "signature": b"\x89PNG\r\n\x1a\n",
        "offset": 0
    },
    {
        "name": "JPEG",
        "extensions": [".jpg", ".jpeg"],
        "signature": b"\xff\xd8\xff",
        "offset": 0
    },
]


def identify(data):
    matches = []

    for filetype in SIGNATURES:
        sig = filetype["signature"]
        offset = filetype.get("offset", 0)

        if data[offset:offset + len(sig)] == sig:
            matches.append(filetype)

    return matches