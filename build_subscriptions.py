#!/usr/bin/env python3
"""build_subscriptions.py — собирает subscriptions и subs/*.txt из configs/final/*.txt.
Telegram не используется.
"""
import os
from typing import List

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FINAL_DIR = os.path.join(BASE_PATH, "configs", "final")
SUBS_DIR = os.path.join(BASE_PATH, "subs")
SUBSCRIPTIONS_PATH = os.path.join(BASE_PATH, "subscriptions")

REPO_RAW = "https://raw.githubusercontent.com/kort0881/sbornik-vless/refs/heads/main"

PROTOCOLS = ["vless", "vmess", "trojan", "ss", "hysteria", "hysteria2", "hy2", "tuic"]
CHUNK_SIZE = 1000


def read_final(proto: str) -> List[str]:
    path = os.path.join(FINAL_DIR, f"{proto}.txt")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def write_chunks(proto: str, items: List[str]) -> List[str]:
    """Пишет subs/{proto}_{NNN}.txt, возвращает raw-URL на чанки."""
    if not items:
        return []
    os.makedirs(SUBS_DIR, exist_ok=True)
    urls = []
    for i in range(0, len(items), CHUNK_SIZE):
        part = items[i:i + CHUNK_SIZE]
        part_num = i // CHUNK_SIZE + 1
        fname = f"{proto}_{part_num:03d}.txt"
        with open(os.path.join(SUBS_DIR, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(part))
        urls.append(f"{REPO_RAW}/subs/{fname}")
    return urls


def main():
    os.makedirs(SUBS_DIR, exist_ok=True)

    lines = [
        "# Автоматически сгенерированный файл подписок",
        "# Формат: блок === PROTO ===, ниже — raw-URL на чанки",
        "",
    ]
    total = 0
    for proto in PROTOCOLS:
        items = read_final(proto)
        if not items:
            continue
        urls = write_chunks(proto, items)
        lines.append(f"=== {proto.upper()} ===")
        lines.extend(urls)
        lines.append("")
        total += len(items)
        print(f"{proto:12s}: {len(items):6d} конфигов -> {len(urls)} чанк(ов)")

    with open(SUBSCRIPTIONS_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n✅ subscriptions записан: {SUBSCRIPTIONS_PATH}")
    print(f"✅ Всего конфигов: {total}")


if __name__ == "__main__":
    main()
