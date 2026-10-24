#!/usr/bin/env python
"""Pack the extension into a signed CRX3 file and write the update manifest
Chrome polls for it

Usage: pack.py <private-key.pem> <out-dir> <base-url>
"""

import hashlib
import io
import json
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["manifest.json", "content.js", "mail.css", "popup.html", "popup.js"]
CRX_NAME = "mailbox-dark-emails.crx"


def varint(n):
    out = b""
    while n > 0x7F:
        out += bytes([n & 0x7F | 0x80])
        n >>= 7
    return out + bytes([n])


def field(number, data):
    return varint(number << 3 | 2) + varint(len(data)) + data


def openssl(*args, data=None):
    return subprocess.run(["openssl", *args], input=data, check=True, capture_output=True).stdout


def archive():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name in FILES:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, (ROOT / name).read_bytes())
    return buf.getvalue()


def main(key, out_dir, base_url):
    version = json.loads((ROOT / "manifest.json").read_text())["version"]
    zip_data = archive()
    public_key = openssl("pkey", "-in", key, "-pubout", "-outform", "DER")
    crx_id = hashlib.sha256(public_key).digest()[:16]

    # Field numbers come from Chromium's components/crx_file/crx3.proto
    signed_data = field(1, crx_id)
    signature = openssl(
        "dgst", "-sha256", "-sign", key,
        data=b"CRX3 SignedData\x00" + struct.pack("<I", len(signed_data)) + signed_data + zip_data,
    )
    header = field(2, field(1, public_key) + field(2, signature)) + field(10000, signed_data)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / CRX_NAME).write_bytes(b"Cr24" + struct.pack("<II", 3, len(header)) + header + zip_data)

    ext_id = "".join("abcdefghijklmnop"[b >> 4] + "abcdefghijklmnop"[b & 0xF] for b in crx_id)
    (out / "updates.xml").write_text(
        "<?xml version='1.0' encoding='UTF-8'?>\n"
        "<gupdate xmlns='http://www.google.com/update2/response' protocol='2.0'>\n"
        f"  <app appid='{ext_id}'>\n"
        f"    <updatecheck codebase='{base_url}/{CRX_NAME}' version='{version}' />\n"
        "  </app>\n"
        "</gupdate>\n"
    )
    print(ext_id)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
