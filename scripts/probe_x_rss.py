#!/usr/bin/env python3
"""Diagnostic only: test public X-to-RSS feeds without credentials or scraping X."""
import datetime
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

URLS = [
    ("RSSHub user", "https://rsshub.app/twitter/user/MENASTREAM"),
    ("RSSHub list", "https://rsshub.app/twitter/list/AfrOsint1/2111744614570905970"),
    ("Nitter tiekoetter", "https://nitter.tiekoetter.com/MENASTREAM/rss"),
    ("Nitter netbub", "https://nitter.netbub.com/MENASTREAM/rss"),
    ("Nitter meowing", "https://nitter.meowing.monster/MENASTREAM/rss"),
]
def check(name, url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AfrOSINT-Feed-Diagnostics/1.0", "Accept": "application/rss+xml, application/atom+xml, application/xml"})
        with urllib.request.urlopen(req, timeout=12) as res:
            body = res.read(750000)
            status = res.status
        root = ET.fromstring(body)
        entries = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        post_links = [e.findtext("link") or e.findtext("{http://www.w3.org/2005/Atom}link") for e in entries]
        print(f"{name}: HTTP {status}; XML={root.tag}; entries={len(entries)}; valid_links={sum(bool(x) for x in post_links)}")
        return bool(entries)
    except (urllib.error.URLError, TimeoutError, ET.ParseError, ValueError, OSError) as e:
        print(f"{name}: UNAVAILABLE ({type(e).__name__}: {str(e)[:150]})")
        return False

if __name__ == "__main__":
    print("AES free X feed availability check:", datetime.datetime.now(datetime.timezone.utc).isoformat())
    successes = sum(check(name, url) for name, url in URLS)
    print(f"RESULT: {successes}/{len(URLS)} endpoints returned at least one parseable post.")
    print("Diagnostic only. A successful one-time probe does not prove long-term reliability.")
