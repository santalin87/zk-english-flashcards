# -*- coding: utf-8 -*-
"""
Spoonfed_Chinese.apkg 真实 Anki 共享牌组精准匹配与融合引擎
1. 从用户提取的 Spoonfed_Chinese.apkg 数据库读取 7,335 条原装 Anki 句库。
2. 针对 target_words_data.json 中的 1194 个自考核心词汇，进行全词词组匹配 (\bword\b)。
3. 优先选择最简短、最地道、句长最短的 Anki 原装例句 + 完美中文翻译。
4. 全量覆盖并重构 target_words_data.json。
"""

import json
import sqlite3
import zipfile
import tempfile
import os
import re

def main():
    print("Extracting and reading Spoonfed_Chinese.apkg...")
    apkg_path = 'Spoonfed_Chinese.apkg'
    if not os.path.exists(apkg_path):
        print(f"Error: {apkg_path} not found!")
        return

    tmpdir = tempfile.mkdtemp()
    with zipfile.ZipFile(apkg_path, 'r') as z:
        z.extractall(tmpdir)

    db_path = os.path.join(tmpdir, 'collection.anki21')
    if not os.path.exists(db_path):
        db_path = os.path.join(tmpdir, 'collection.anki2')

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT flds FROM notes")
    rows = cur.fetchall()

    anki_pairs = []
    for r in rows:
        fields = r[0].split('\x1f')
        if len(fields) >= 3:
            eng = fields[0].strip()
            # Clean HTML tags if any
            eng_clean = re.sub(r'<[^>]+>', '', eng).strip()
            chn = fields[2].strip()
            chn_clean = re.sub(r'<[^>]+>', '', chn).strip()
            
            if eng_clean and chn_clean:
                anki_pairs.append((eng_clean, chn_clean))

    print(f"Loaded {len(anki_pairs)} authentic Anki Spoonfed sentence pairs!")

    # Load target words data
    with open('target_words_data.json', 'r', encoding='utf-8') as f:
        target_words = json.load(f)

    matched_count = 0

    for item in target_words:
        w = item['word'].strip()
        pattern = re.compile(rf'\b{re.escape(w)}\b', re.IGNORECASE)

        candidates = []
        for eng, chn in anki_pairs:
            if pattern.search(eng):
                # Calculate sentence length (word count)
                word_count = len(eng.split())
                # Prefer concise sentences (4 to 10 words)
                score = word_count
                if 4 <= word_count <= 8:
                    score -= 5 # Bonus for optimal 4-8 word length
                candidates.append((score, eng, chn))

        if candidates:
            # Sort by best score (shortest / most natural)
            candidates.sort(key=lambda x: x[0])
            best_score, best_eng, best_chn = candidates[0]

            item['sentence'] = best_eng
            item['translation'] = best_chn
            matched_count += 1

    print(f"Successfully matched and replaced {matched_count} / {len(target_words)} words using authentic Spoonfed Anki sentences!")

    with open('target_words_data.json', 'w', encoding='utf-8') as f:
        json.dump(target_words, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
