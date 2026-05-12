#!/usr/bin/env python3
"""
Build script for the blog.

Usage:
    python3 build.py

Requires:
    pip install markdown

What it does:
    - Reads every *.md file in posts/ (files starting with _ are skipped)
    - Parses front matter (title and date fields)
    - Converts the markdown body to HTML
    - Writes posts/{slug}.html for each post
    - Regenerates index.html with posts sorted newest first

File naming: use lowercase-hyphenated names, e.g. my-first-post.md
The filename (without .md) becomes the URL slug.
"""

import sys
from pathlib import Path
from datetime import datetime

try:
    import markdown as md_lib
except ImportError:
    print("Missing dependency. Run:  pip install markdown")
    sys.exit(1)

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
SITE_URL = "https://smarmelling.com"


# ── helpers ──────────────────────────────────────────────────────────────────

def parse_front_matter(text):
    """Return (meta_dict, body) from a --- delimited front matter block."""
    text = text.lstrip("﻿")  # strip BOM
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, text[end + 4:].strip()


def format_date(date_str):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%b %d, %Y")
        except ValueError:
            continue
    return date_str


def format_rfc822(date_str):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%a, %d %b %Y 00:00:00 +0000")
        except ValueError:
            continue
    return date_str


# ── HTML templates ────────────────────────────────────────────────────────────

def post_html(title, date_formatted, content_html, slug):
    post_url = f"{SITE_URL}/posts/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>&lt;matteo&gt; — {title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <div class="container">
    <div class="site-name">
      <a href="../index.html">&lt;matteo&gt;</a>
    </div>
    <div class="post-header">
      <h1 class="post-heading">{title}</h1>
      <p class="post-meta">{date_formatted}</p>
    </div>
    <div class="prose">
      {content_html}
    </div>
    <div class="comments">
      <div id="disqus_thread"></div>
      <script>
        var disqus_config = function () {{
          this.page.url = "{post_url}";
          this.page.identifier = "{slug}";
        }};
        (function() {{
          var d = document, s = d.createElement('script');
          s.src = 'https://smarmelling.disqus.com/embed.js';
          s.setAttribute('data-timestamp', +new Date());
          (d.head || d.body).appendChild(s);
        }})();
      </script>
      <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
    </div>
  </div>
</body>
</html>
"""


INTRO = (
    "I wanted to give you a chance, but you failed to seize it. Because you have tried to "
    "shoot something political, unaware that the walls have fallen. Now it’s come again "
    "the time to open everything. Biascica, open everything! "
    '<a href="https://www.youtube.com/watch?v=t-hoaBtejII">(Boris season 3, ep. 13)</a>'
)


def index_html(posts):
    if posts:
        items = "\n".join(
            f'      <li class="post-item">\n'
            f'        <a href="posts/{p["slug"]}.html" class="post-link">\n'
            f'          <span class="post-title">{p["title"]}</span>\n'
            f'          <span class="post-date">{p["date_formatted"]}</span>\n'
            f'        </a>\n'
            f'      </li>'
            for p in posts
        )
        post_list = f'    <ul class="post-list">\n{items}\n    </ul>'
    else:
        post_list = '    <p class="no-posts">No posts yet.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>&lt;matteo&gt;</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <link rel="alternate" type="application/rss+xml" title="matteo" href="{SITE_URL}/feed.xml">
</head>
<body>
  <div class="container">
    <div class="site-name"><a href="index.html">&lt;matteo&gt;</a></div>
    <p class="intro">{INTRO}</p>
    <p class="more-link"><a href="more.html">more</a></p>
    <p class="more-link"><a href="feed.xml">rss</a></p>
{post_list}
  </div>
</body>
</html>
"""


def feed_xml(posts):
    items = "\n".join(
        f"  <item>\n"
        f"    <title>{p['title']}</title>\n"
        f"    <link>{SITE_URL}/posts/{p['slug']}.html</link>\n"
        f"    <guid>{SITE_URL}/posts/{p['slug']}.html</guid>\n"
        f"    <pubDate>{format_rfc822(p['date'])}</pubDate>\n"
        f"  </item>"
        for p in posts
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>matteo</title>
    <link>{SITE_URL}</link>
    <description>matteo's blog</description>
{items}
  </channel>
</rss>
"""


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    POSTS_DIR.mkdir(exist_ok=True)
    converter = md_lib.Markdown(extensions=["fenced_code", "tables"])
    posts = []

    for md_file in sorted(POSTS_DIR.glob("*.md")):
        if md_file.name.startswith("_"):
            continue

        text = md_file.read_text(encoding="utf-8")
        meta, body = parse_front_matter(text)

        title = meta.get("title", "").strip()
        date_str = meta.get("date", "").strip()

        if not title or not date_str:
            print(f"  skip  {md_file.name}  (missing title or date in front matter)")
            continue

        converter.reset()
        content = converter.convert(body)
        slug = md_file.stem
        date_fmt = format_date(date_str)

        out = POSTS_DIR / f"{slug}.html"
        out.write_text(post_html(title, date_fmt, content, slug), encoding="utf-8")
        print(f"  built  posts/{slug}.html")

        posts.append({"slug": slug, "title": title, "date": date_str, "date_formatted": date_fmt})

    posts.sort(key=lambda p: p["date"], reverse=True)

    (ROOT / "index.html").write_text(index_html(posts), encoding="utf-8")
    n = len(posts)
    print(f"  wrote  index.html  ({n} post{'s' if n != 1 else ''})")

    (ROOT / "feed.xml").write_text(feed_xml(posts), encoding="utf-8")
    print(f"  wrote  feed.xml")


if __name__ == "__main__":
    main()
