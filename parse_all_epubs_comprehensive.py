# -*- coding: utf-8 -*-
"""
全量 4 本电子书词根词缀级联匹配引擎
包含电子书：
1. 新东方词根词缀大全.epub (Priority 1)
2. 英语万词速成_词根+词缀记忆法.epub (Priority 2)
3. 为什么用背300词根词缀就够了.epub (Priority 3)
4. 用得上的200词根词缀就够了.epub (Priority 4)
"""

import zipfile
import os
import re
import json
import html

def extract_epub_clean_lines(epub_filename):
    if not os.path.exists(epub_filename):
        return []
    z = zipfile.ZipFile(epub_filename)
    html_files = [f for f in z.namelist() if f.endswith(('.html', '.xhtml', '.htm'))]
    full_text = ''
    for f in html_files:
        full_text += z.read(f).decode('utf-8', errors='ignore') + '\n'
    full_text = html.unescape(full_text)
    clean_text = re.sub(r'<[^>]+>', '\n', full_text)
    return [l.strip() for l in clean_text.split('\n') if l.strip()]

def parse_xindongfang(filename):
    lines = extract_epub_clean_lines(filename)
    db = {}
    pattern = re.compile(r'^([a-zA-Z]+)\s*([\u4e00-\u9fa5a-zA-Z0-9\s，；、；：“”‘’（）\/\-\+\.]*?)\s*[（\(]([^）\)]+)[）\)]')

    for line in lines:
        m = pattern.search(line)
        if m:
            w = m.group(1).strip().lower()
            meaning_str = m.group(2).strip()
            breakdown_str = m.group(3).strip()

            if '+' in breakdown_str or '＋' in breakdown_str or '→' in breakdown_str:
                formatted = f"【新东方词根拆解】: {w} ➔ ({breakdown_str}) ➔ {meaning_str}" if meaning_str else f"【新东方词根拆解】: {w} ➔ ({breakdown_str})"
                db[w] = formatted
    return db

def parse_wanci(filename):
    lines = extract_epub_clean_lines(filename)
    db = {}
    
    # Pattern A: stem＋stem→word（meaning）
    # Examples: act＋ive→active（inclined to action...）
    pattern_a = re.compile(r'([a-zA-Z\s\＋\+\-\(\)〈〉]+)[→➔]\s*([a-zA-Z]+)\s*[（\(]([^）\)]+)[）\)]')
    
    # Pattern B: word （breakdown）
    pattern_b = re.compile(r'^([a-zA-Z]+)\s*([\u4e00-\u9fa5]*)\s*[（\(]([a-zA-Z0-9\+\-＋\s→\＝]+)[）\)]')

    for line in lines:
        ma = pattern_a.search(line)
        if ma:
            breakdown_raw = ma.group(1).strip()
            w = ma.group(2).strip().lower()
            meaning_raw = ma.group(3).strip()
            if ('+' in breakdown_raw or '＋' in breakdown_raw) and len(w) > 2:
                db[w] = f"【万词速成拆解】: {w} ➔ ({breakdown_raw}) ➔ {meaning_raw}"
            continue

        mb = pattern_b.search(line)
        if mb:
            w = mb.group(1).strip().lower()
            m_str = mb.group(2).strip()
            b_str = mb.group(3).strip()
            if ('+' in b_str or '＋' in b_str) and len(w) > 2:
                db[w] = f"【万词速成拆解】: {w} ➔ ({b_str}) ➔ {m_str}" if m_str else f"【万词速成拆解】: {w} ➔ ({b_str})"

    return db

def parse_300_200(filename, source_name):
    lines = extract_epub_clean_lines(filename)
    db = {}
    pattern = re.compile(r'([a-zA-Z]+)\s*([\u4e00-\u9fa5a-zA-Z0-9\s，；、；：“”‘’\/\-\+\.]*?)\s*[（\(]([^）\)]+)[）\)]')

    for line in lines:
        m = pattern.search(line)
        if m:
            w = m.group(1).strip().lower()
            meaning_str = m.group(2).strip()
            breakdown_str = m.group(3).strip()

            if ('+' in breakdown_str or '＋' in breakdown_str or '→' in breakdown_str) and len(w) > 2:
                db[w] = f"【{source_name}拆解】: {w} ➔ ({breakdown_str}) ➔ {meaning_str}" if meaning_str else f"【{source_name}拆解】: {w} ➔ ({breakdown_str})"
    return db

def main():
    epub_files = [f for f in os.listdir('.') if f.endswith('.epub')]
    print("Detected EPUB files:", epub_files)

    xindongfang_file = [f for f in epub_files if '新东方' in f]
    wanci_file = [f for f in epub_files if '万词' in f]
    b300_file = [f for f in epub_files if '300' in f]
    y200_file = [f for f in epub_files if '200' in f]

    db_xdf = parse_xindongfang(xindongfang_file[0]) if xindongfang_file else {}
    db_wanci = parse_wanci(wanci_file[0]) if wanci_file else {}
    db_300 = parse_300_200(b300_file[0], "300词根") if b300_file else {}
    db_200 = parse_300_200(y200_file[0], "200词根") if y200_file else {}

    print(f"\nExtracted databases:")
    print(f" - 新东方词根词缀库: {len(db_xdf)} 词")
    print(f" - 英语万词速成库: {len(db_wanci)} 词")
    print(f" - 背300词根词缀库: {len(db_300)} 词")
    print(f" - 用得上200词根库: {len(db_200)} 词")

    with open('target_words_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    p1_xdf = 0
    p2_wanci = 0
    p3_300 = 0
    p4_200 = 0

    unmatched_words = []

    for item in data:
        w = item['word'].strip().lower()
        ety = item.get('etymology', '')

        if '新东方' in ety:
            p1_xdf += 1
        elif w in db_wanci:
            item['etymology'] = db_wanci[w]
            p2_wanci += 1
        elif w in db_300:
            item['etymology'] = db_300[w]
            p3_300 += 1
        elif w in db_200:
            item['etymology'] = db_200[w]
            p4_200 += 1
        else:
            unmatched_words.append(w)

    total_matched = p1_xdf + p2_wanci + p3_300 + p4_200
    total_unmatched = len(unmatched_words)

    print("\n================== 4本电子书级联匹配统计报告 ==================")
    print(f"1. 新东方词根词缀大全 (Priority 1): {p1_xdf} 个词")
    print(f"2. 英语万词速成 (Priority 2 新增): {p2_wanci} 个词")
    print(f"3. 背300词根就够了 (Priority 3 新增): {p3_300} 个词")
    print(f"4. 用得上200词根 (Priority 4 新增): {p4_200} 个词")
    print(f"--------------------------------------------------")
    print(f"全书库重构覆盖总数: {total_matched} / {len(data)} ({(total_matched/len(data))*100:.1f}%)")
    print(f"尚待进一步补充/未匹配词数: {total_unmatched} 个词")
    print("===============================================================\n")

    with open('target_words_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
