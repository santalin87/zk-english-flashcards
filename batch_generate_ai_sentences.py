# -*- coding: utf-8 -*-
"""
AI 全量极简例句生成引擎
AI 核心法则：
1. 每条例句控制在 4-8 个单词。
2. 绝对不包含生僻词、长难句、分句或 ... 截断碎片。
3. 语境必须生活化、高频化，帮助第一眼死磕记住目标单词。
"""

import json
import re

def generate_ai_simple_sentence(word, meaning):
    w = word.strip()
    m_clean = re.sub(r'^[a-z]+\.\s*', '', meaning).split(';')[0].split(',')[0].split('；')[0].strip()
    
    # Analyze POS
    pos = ""
    if meaning.startswith("v.") or "vt." in meaning or "vi." in meaning:
        pos = "verb"
    elif meaning.startswith("n.") or "n. " in meaning:
        pos = "noun"
    elif meaning.startswith("adj.") or "a." in meaning:
        pos = "adj"
    elif meaning.startswith("adv."):
        pos = "adv"
    elif meaning.startswith("prep."):
        pos = "prep"
    elif meaning.startswith("conj."):
        pos = "conj"

    # Direct custom high-frequency templates
    if pos == "verb":
        if w.endswith("ing"):
            s = f"He is {w} now."
            t = f"他现在正在{m_clean}。"
        elif w.endswith("ed"):
            s = f"They {w} together yesterday."
            t = f"他们昨天一起{m_clean}了。"
        else:
            s = f"Never {w} your dream." if "放弃" in m_clean or "改变" in m_clean else f"Please {w} the door carefully."
            if "放弃" in m_clean:
                s = f"Never {w} your dream."
                t = f"永远不要{m_clean}你的梦想。"
            elif "相信" in m_clean or "接受" in m_clean or "感谢" in m_clean:
                s = f"I {w} your good advice."
                t = f"我{m_clean}你的好建议。"
            elif "增加" in m_clean or "减少" in m_clean or "提高" in m_clean:
                s = f"We must {w} our efficiency."
                t = f"我们必须{m_clean}我们的效率。"
            else:
                s = f"We should {w} every day."
                t = f"我们应该每天{m_clean}。"

    elif pos == "noun":
        if "人" in m_clean or "家" in m_clean or "员" in m_clean or "师" in m_clean:
            s = f"He is a famous {w}."
            t = f"他是一位著名的{m_clean}。"
        elif "地方" in m_clean or "室" in m_clean or "馆" in m_clean or "场" in m_clean:
            s = f"We arrived at the {w}."
            t = f"我们到达了{m_clean}。"
        elif "时间" in m_clean or "天" in m_clean or "月" in m_clean or "年" in m_clean:
            s = f"It was a memorable {w}."
            t = f"那是一个值得纪念的{m_clean}。"
        else:
            s = f"This is a useful {w}."
            t = f"这是一个实用的{m_clean}。"

    elif pos == "adj":
        if "好" in m_clean or "美" in m_clean or "大" in m_clean or "重要" in m_clean:
            s = f"It is a very {w} idea."
            t = f"这是一个非常{m_clean}的主意。"
        elif "难" in m_clean or "坏" in m_clean or "危险" in m_clean:
            s = f"Be careful with this {w} task."
            t = f"对待这项{m_clean}的任务要小心。"
        else:
            s = f"She looks very {w} today."
            t = f"她今天看起来非常{m_clean}。"

    elif pos == "adv":
        s = f"She spoke very {w}."
        t = f"她说话非常{m_clean}。"

    elif pos == "prep":
        s = f"Walk {w} the quiet street."
        t = f"沿着安静的街道{m_clean}行走。"

    else:
        s = f"Keep {w} in mind always."
        t = f"始终把{m_clean}记在心里。"

    return s, t

def run_ai_sentence_upgrade():
    with open('target_words_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Import manually curated AI sentences
    from ai_simplify_all_sentences import AI_SIMPLE_SENTENCES

    upgraded = 0
    for item in data:
        w = item['word']
        orig_s = item.get('sentence', '')
        orig_t = item.get('translation', '')
        m = item.get('meaning', '')

        # Check if hand-curated
        if w.lower() in AI_SIMPLE_SENTENCES:
            new_s, new_t = AI_SIMPLE_SENTENCES[w.lower()]
        else:
            # Audit original sentence: if it's longer than 9 words OR has '...' OR has punctuation fragments
            words_list = orig_s.replace('...', '').strip().split()
            if len(words_list) > 9 or '...' in orig_s or not orig_s.endswith(('.', '!', '?')) or not orig_s[0].isupper():
                new_s, new_t = generate_ai_simple_sentence(w, m)
            else:
                new_s, new_t = orig_s, orig_t

        if new_s != orig_s or new_t != orig_t:
            item['sentence'] = new_s
            item['translation'] = new_t
            upgraded += 1

    with open('target_words_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"AI Sentence Engine successfully upgraded {upgraded} / {len(data)} words in target_words_data.json!")

if __name__ == '__main__':
    run_ai_sentence_upgrade()
