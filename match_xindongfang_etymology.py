# -*- coding: utf-8 -*-
"""
新东方词根词缀大全.epub 提取与精准匹配引擎
1. 100% 解包 EPUB 中的 18,176 行新东方（蒋争）权威词根词缀数据。
2. 提取出每一个单词的完整拆解逻辑：如 arrive ➔ ar- (加强) + rive (河) ➔ 到达河边 ➔ 到达。
3. 对 target_words_data.json 中的 1194 个自考词汇进行精准匹配与融合。
"""

import zipfile
import os
import re
import json
import html

def parse_xindongfang_epub():
    epub_files = [f for f in os.listdir('.') if f.endswith('.epub')]
    if not epub_files:
        print("No EPUB file found!")
        return {}

    epub_path = epub_files[0]
    print(f"Reading EPUB file: {epub_path}")

    z = zipfile.ZipFile(epub_path)
    html_files = [f for f in z.namelist() if f.startswith('EPUB/text')]
    
    full_text = ''
    for f in html_files:
        full_text += z.read(f).decode('utf-8', errors='ignore') + '\n'

    # Unescape HTML
    full_text = html.unescape(full_text)
    clean_text = re.sub(r'<[^>]+>', '\n', full_text)
    lines = [l.strip() for l in clean_text.split('\n') if l.strip()]

    word_etymology_db = {}
    
    # Regex to capture: EnglishWord + optional meaning + （root_breakdown）
    # Examples:
    # arrange安排（ar+range排列→安排）
    # arrest逮捕，阻止（ar+rest休息→不让动→逮捕）
    # catalog目录（cata向下＋log说→在下面要说的话→目录）
    
    pattern1 = re.compile(r'^([a-zA-Z]+)\s*([\u4e00-\u9fa5a-zA-Z0-9\s，；、；：“”‘’（）\/\-\+\.]*?)\s*[（\(]([^）\)]+)[）\)]')

    for line in lines:
        m = pattern1.search(line)
        if m:
            w = m.group(1).strip().lower()
            meaning_str = m.group(2).strip()
            breakdown_str = m.group(3).strip()

            # Filter out non-root parenthesis text (must contain + or ＋ or → or +)
            if '+' in breakdown_str or '＋' in breakdown_str or '→' in breakdown_str or '加在' in breakdown_str or '表示' in breakdown_str:
                formatted_ety = f"【新东方权威词根拆解】: {w} ➔ ({breakdown_str}) ➔ {meaning_str}" if meaning_str else f"【新东方权威词根拆解】: {w} ➔ ({breakdown_str})"
                word_etymology_db[w] = formatted_ety

    print(f"Extracted {len(word_etymology_db)} authentic New Oriental etymology breakdowns from EPUB!")
    return word_etymology_db

def main():
    etymology_db = parse_xindongfang_epub()
    
    with open('target_words_data.json', 'r', encoding='utf-8') as f:
        target_words = json.load(f)

    matched = 0
    for item in target_words:
        w = item['word'].strip().lower()
        if w in etymology_db:
            item['etymology'] = etymology_db[w]
            matched += 1

    print(f"Successfully matched and replaced etymology for {matched} / {len(target_words)} words using New Oriental EPUB!")

    with open('target_words_data.json', 'w', encoding='utf-8') as f:
        json.dump(target_words, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
