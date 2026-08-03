# -*- coding: utf-8 -*-
"""
多本 EPUB 词根词缀书籍级联匹配引擎
优先级策略：
Priority 1: 新东方词根词缀大全.epub (保持原 303 个匹配)
Priority 2: 英语万词速成_词根+词缀记忆法.epub (全量补充匹配)
Priority 3: 为什么用背300词根词缀就够了.epub & 用得上的200词根词缀就够了.epub (进一步补充匹配)
"""

import zipfile
import os
import re
import json
import html

def extract_epub_text(epub_filename):
    if not os.path.exists(epub_filename):
        return ""
    z = zipfile.ZipFile(epub_filename)
    html_files = [f for f in z.namelist() if f.endswith(('.html', '.xhtml', '.htm'))]
    full_text = ''
    for f in html_files:
        full_text += z.read(f).decode('utf-8', errors='ignore') + '\n'
    full_text = html.unescape(full_text)
    clean_text = re.sub(r'<[^>]+>', '\n', full_text)
    return clean_text

def parse_wanci_epub(filename):
    text = extract_epub_text(filename)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    db = {}
    pattern = re.compile(r'^([a-zA-Z]+)\s*([\u4e00-\u9fa5a-zA-Z0-9\s，；、；：“”‘’（）\/\-\+\.]*?)\s*[（\(]([^）\)]+)[）\)]')

    for line in lines:
        m = pattern.search(line)
        if m:
            w = m.group(1).strip().lower()
            meaning_str = m.group(2).strip()
            breakdown_str = m.group(3).strip()

            if '+' in breakdown_str or '＋' in breakdown_str or '→' in breakdown_str or '=' in breakdown_str:
                formatted_ety = f"【万词速成词根拆解】: {w} ➔ ({breakdown_str}) ➔ {meaning_str}" if meaning_str else f"【万词速成词根拆解】: {w} ➔ ({breakdown_str})"
                db[w] = formatted_ety
    return db

def parse_generic_epub(filename, source_tag):
    text = extract_epub_text(filename)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    db = {}
    pattern = re.compile(r'^([a-zA-Z]+)\s*([\u4e00-\u9fa5a-zA-Z0-9\s，；、；：“”‘’（）\/\-\+\.]*?)\s*[（\(]([^）\)]+)[）\)]')

    for line in lines:
        m = pattern.search(line)
        if m:
            w = m.group(1).strip().lower()
            meaning_str = m.group(2).strip()
            breakdown_str = m.group(3).strip()

            if '+' in breakdown_str or '＋' in breakdown_str or '→' in breakdown_str or '=' in breakdown_str:
                formatted_ety = f"【{source_tag}词根拆解】: {w} ➔ ({breakdown_str}) ➔ {meaning_str}" if meaning_str else f"【{source_tag}词根拆解】: {w} ➔ ({breakdown_str})"
                db[w] = formatted_ety
    return db

def main():
    epub_files = [f for f in os.listdir('.') if f.endswith('.epub')]
    print("Found EPUB files:", epub_files)

    wanci_file = [f for f in epub_files if '万词' in f]
    b300_file = [f for f in epub_files if '300' in f]
    y200_file = [f for f in epub_files if '200' in f]

    wanci_db = parse_wanci_epub(wanci_file[0]) if wanci_file else {}
    b300_db = parse_generic_epub(b300_file[0], "300词根") if b300_file else {}
    y200_db = parse_generic_epub(y200_file[0], "200词根") if y200_file else {}

    print(f"Loaded 万词速成 DB size: {len(wanci_db)}")
    print(f"Loaded 300词根 DB size: {len(b300_db)}")
    print(f"Loaded 200词根 DB size: {len(y200_db)}")

    with open('target_words_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    p1_xindongfang = 0
    p2_wanci = 0
    p3_other = 0

    for item in data:
        w = item['word'].strip().lower()
        ety = item.get('etymology', '')

        if '新东方' in ety:
            p1_xindongfang += 1
        elif w in wanci_db:
            item['etymology'] = wanci_db[w]
            p2_wanci += 1
        elif w in b300_db:
            item['etymology'] = b300_db[w]
            p3_other += 1
        elif w in y200_db:
            item['etymology'] = y200_db[w]
            p3_other += 1

    total_matched = p1_xindongfang + p2_wanci + p3_other
    total_unmatched = len(data) - total_matched

    print("\n================== 词根拆解匹配统计 ==================")
    print(f"1. 新东方词根词缀大全 (优先): {p1_xindongfang} 个词")
    print(f"2. 英语万词速成新增匹配: {p2_wanci} 个词")
    print(f"3. 300/200 词根精选新增匹配: {p3_other} 个词")
    print(f"--------------------------------------------------")
    print(f"已成功匹配词根拆解词数: {total_matched} / {len(data)} ({(total_matched/len(data))*100:.1f}%)")
    print(f"未匹配词根拆解词数: {total_unmatched} 个词")
    print("====================================================\n")

    with open('target_words_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
