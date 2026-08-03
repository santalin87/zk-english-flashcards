import json, sys, time, re

sys.path.append(r'd:\User\Documents\自考英语')
from prep_1_500_data import selected_1_500

with open(r'd:\User\Documents\自考英语\target_words_data.json', 'r', encoding='utf-8') as f:
    target_1200 = json.load(f)

full_dataset = []

# Dict of custom rich sentences for first 117 words
custom_sentences = {}
for item in selected_1_500:
    w, ipa, meaning, phonics, phrase, etym, sent, trans = item
    custom_sentences[w.lower()] = (sent, trans)
    full_dataset.append({
        "row": len(full_dataset) + 1,
        "word": w,
        "ipa": ipa,
        "meaning": meaning,
        "phonics": phonics,
        "phrase": phrase,
        "etymology": etym,
        "sentence": sent,
        "translation": trans
    })

def generate_etymology(word, meaning, phrase):
    w_lower = word.lower().strip()
    etym = f"核心词汇 ➔ 音节拆解 ➔ 【{phrase}】"
    if w_lower.startswith('re') and len(w_lower) > 3:
        etym = f"re- (重新/向后) + {w_lower[2:]} ➔ 重复执行或向后反作用 ➔ {meaning}"
    elif w_lower.startswith('un') and len(w_lower) > 3:
        etym = f"un- (否定/无) + {w_lower[2:]} ➔ 表达相反否定含义 ➔ {meaning}"
    elif w_lower.startswith('dis') and len(w_lower) > 4:
        etym = f"dis- (剥夺/相反) + {w_lower[3:]} ➔ 相反或分开状态 ➔ {meaning}"
    elif w_lower.startswith('sub') and len(w_lower) > 4:
        etym = f"sub- (在……下方) + {w_lower[3:]} ➔ 处于下层或次级 ➔ {meaning}"
    elif w_lower.startswith('trans') and len(w_lower) > 5:
        etym = f"trans- (跨越/转变) + {w_lower[5:]} ➔ 跨越形式转变 ➔ {meaning}"
    elif w_lower.startswith('in') and len(w_lower) > 4:
        etym = f"in- (在内/使成为) + {w_lower[2:]} ➔ 进入或使处于某种状态 ➔ {meaning}"
    elif w_lower.startswith('con') and len(w_lower) > 4:
        etym = f"con- (共同/一起) + {w_lower[3:]} ➔ 共同聚集或加强 ➔ {meaning}"
    elif w_lower.startswith('ex') and len(w_lower) > 3:
        etym = f"ex- (向外/出来) + {w_lower[2:]} ➔ 由内向外伸展脱离 ➔ {meaning}"
    elif w_lower.endswith('tion') or w_lower.endswith('sion'):
        etym = f"{w_lower[:-4]} + -tion/-sion (抽象名词后缀) ➔ 表达动作或结果 ➔ {meaning}"
    elif w_lower.endswith('able') or w_lower.endswith('ible'):
        etym = f"{w_lower[:-4]} + -able/-ible (形容词: 能……的) ➔ 具备某能力的 ➔ {meaning}"
    elif w_lower.endswith('ment'):
        etym = f"{w_lower[:-4]} + -ment (名词后缀) ➔ 行为过程或结果 ➔ {meaning}"
    elif w_lower.endswith('ive'):
        etym = f"{w_lower[:-3]} + -ive (形容词后缀) ➔ 具有某种性质特征的 ➔ {meaning}"
    return etym

for item in target_1200:
    w_lower = item['word'].lower().strip()
    if w_lower not in custom_sentences:
        etym = item.get('etymology') or generate_etymology(item['word'], item['meaning'], item['phrase'])
        sent = item.get('sentence', f"She bit her lower lip.")
        trans = item.get('translation', f"她咬了咬下唇。")
        full_dataset.append({
            "row": len(full_dataset) + 1,
            "word": item['word'],
            "ipa": item['ipa'],
            "meaning": item['meaning'],
            "phonics": item['phonics'],
            "phrase": item['phrase'],
            "etymology": etym,
            "sentence": sent,
            "translation": trans
        })

# Comprehensive Root and Suffix Database (44 Core Roots & Affixes)
root_dataset = [
    {
        "id": 1,
        "affix": "re-",
        "type": "前缀 (Prefix)",
        "meaning": "重新、向后、重复、再次",
        "explanation": "放置在词根前，表示动作的重复执行、重新开始或向相反方向反作用。",
        "examples": "realize (实现), recently (最近), receive (收到), record (记录), report (报告), research (研究), result (结果), return (返回), review (复习)"
    },
    {
        "id": 2,
        "affix": "un-",
        "type": "前缀 (Prefix)",
        "meaning": "否定、无、相反、解除",
        "explanation": "附加于形容词或动词前，表达相反否定含义或解除某种状态。",
        "examples": "unusual (不寻常的), understand (理解), unit (单元), university (大学), until (直到)"
    },
    {
        "id": 3,
        "affix": "dis-",
        "type": "前缀 (Prefix)",
        "meaning": "剥夺、分开、相反、消除",
        "explanation": "表示分离、剥夺或与原动作/状态相反的含义。",
        "examples": "discuss (讨论), discover (发现), disease (疾病), distance (距离), dislike (不喜欢)"
    },
    {
        "id": 4,
        "affix": "sub-",
        "type": "前缀 (Prefix)",
        "meaning": "在……下方、次级、下层",
        "explanation": "表示位置处于下方、下层，或等级处于次要、附属地位。",
        "examples": "subway (地铁), subject (主题/科目), substance (物质), substitute (替代)"
    },
    {
        "id": 5,
        "affix": "trans-",
        "type": "前缀 (Prefix)",
        "meaning": "跨越、转变、贯穿、传输",
        "explanation": "表示从一处跨越到另一处、形态或性质的转变。",
        "examples": "transfer (转移), translate (翻译), transport (运输), transform (转变)"
    },
    {
        "id": 6,
        "affix": "in- / im- / en-",
        "type": "前缀 (Prefix)",
        "meaning": "进入、在内、使成为某种状态",
        "explanation": "表示进入内部、处于某种状态或使事物具备某种性质。",
        "examples": "instead (代替), institute (研究所), interest (兴趣), invite (邀请), industry (工业)"
    },
    {
        "id": 7,
        "affix": "con- / com- / co-",
        "type": "前缀 (Prefix)",
        "meaning": "共同、一起、聚集、加强",
        "explanation": "表示多方共同参与、聚集在一起或对动作概念起加强作用。",
        "examples": "consider (考虑), continue (继续), control (控制), connect (连接), condition (条件)"
    },
    {
        "id": 8,
        "affix": "ex-",
        "type": "前缀 (Prefix)",
        "meaning": "向外、出来、超出、前任",
        "explanation": "表示由内向外伸展脱离、超出范围或前任身份。",
        "examples": "exercise (锻炼), extreme (极端), examine (检查), expect (期望), express (表达)"
    },
    {
        "id": 9,
        "affix": "pre-",
        "type": "前缀 (Prefix)",
        "meaning": "在……之前、预先",
        "explanation": "表示时间或空间上的提前、预先准备。",
        "examples": "prevent (预防/阻止), prepare (准备), present (呈现/礼物), predict (预测)"
    },
    {
        "id": 10,
        "affix": "pro-",
        "type": "前缀 (Prefix)",
        "meaning": "向前、推进、支持",
        "explanation": "表示向前方延伸、促使发展或赞同支持。",
        "examples": "produce (生产), project (项目), progress (进步), promise (许诺), protect (保护)"
    },
    {
        "id": 11,
        "affix": "inter-",
        "type": "前缀 (Prefix)",
        "meaning": "在……之间、相互",
        "explanation": "表示两者或多者之间的相互作用与联系。",
        "examples": "interact (互动), international (国际的), internet (互联网), interview (面试/采访)"
    },
    {
        "id": 12,
        "affix": "anti-",
        "type": "前缀 (Prefix)",
        "meaning": "反对、对抗、抗击",
        "explanation": "表示对抗、抵制或相反作用。",
        "examples": "antibiotic (抗生素), antibody (抗体), social-anti (反社会的)"
    },
    {
        "id": 13,
        "affix": "de-",
        "type": "前缀 (Prefix)",
        "meaning": "向下、离开、彻底除去",
        "explanation": "表示向下降低、离开或彻底剥夺。",
        "examples": "decline (下降), decrease (减少), decide (决定), defend (防御)"
    },
    {
        "id": 14,
        "affix": "mis-",
        "type": "前缀 (Prefix)",
        "meaning": "错误、坏、不当",
        "explanation": "表示错误的动作或不当的状态。",
        "examples": "mislead (误导), mistake (错误), misunderstand (误解)"
    },
    {
        "id": 15,
        "affix": "over-",
        "type": "前缀 (Prefix)",
        "meaning": "过度、超越、在……上方",
        "explanation": "表示超出正常限度或覆盖在上方。",
        "examples": "overcome (克服), overlook (忽略/俯瞰), overseas (海外的), overall (总体的)"
    },
    {
        "id": 16,
        "affix": "under-",
        "type": "前缀 (Prefix)",
        "meaning": "在……下方、不足、隐蔽",
        "explanation": "表示位置处于下方、程度不足或隐蔽进行。",
        "examples": "understand (理解), undergo (经历), underline (下划线/强调)"
    },
    {
        "id": 17,
        "affix": "fore-",
        "type": "前缀 (Prefix)",
        "meaning": "预先、在前的",
        "explanation": "表示时间提前或位置靠前。",
        "examples": "forecast (预测), forehead (额头), foresee (预见)"
    },
    {
        "id": 18,
        "affix": "auto-",
        "type": "前缀 (Prefix)",
        "meaning": "自动、自己",
        "explanation": "表示依靠自身力量运转或与自己相关的。",
        "examples": "automatic (自动的), biography-auto (自传)"
    },
    {
        "id": 19,
        "affix": "bio-",
        "type": "前缀 (Prefix)",
        "meaning": "生命、生物",
        "explanation": "表示与生命、生物学相关的。",
        "examples": "biology (生物学), biography (传记), antibiotic (抗生素)"
    },
    {
        "id": 20,
        "affix": "tele-",
        "type": "前缀 (Prefix)",
        "meaning": "远距离、电视/电话",
        "explanation": "表示跨越长距离的传输与通信。",
        "examples": "telephone (电话), television (电视), telescope (望远镜)"
    },
    {
        "id": 21,
        "affix": "-tion / -sion",
        "type": "后缀 (Suffix)",
        "meaning": "抽象名词后缀（表达动作、状态或结果）",
        "explanation": "附着在动词后，将其转化为表达该动作过程、状态或具体结果的抽象名词。",
        "examples": "action (行动), activity (活动), condition (条件), decision (决定), direction (方向), education (教育), question (问题), situation (情况)"
    },
    {
        "id": 22,
        "affix": "-able / -ible",
        "type": "后缀 (Suffix)",
        "meaning": "形容词后缀（能……的、易……的、值得……的）",
        "explanation": "附着在动词或名词后，构成表示具有某能力或值得做某事的形容词。",
        "examples": "capable (有能力的), comfortable (舒适的), valuable (有价值的), possible (可能的), acceptable (可接受的)"
    },
    {
        "id": 23,
        "affix": "-ment",
        "type": "后缀 (Suffix)",
        "meaning": "名词后缀（行为、过程、机构或结果）",
        "explanation": "附着在动词后，构成表示行为过程、组织机构或具体结果的名词。",
        "examples": "argument (争论), development (发展), environment (环境), government (政府), improvement (改善), movement (运动)"
    },
    {
        "id": 24,
        "affix": "-ive",
        "type": "后缀 (Suffix)",
        "meaning": "形容词后缀（具有某种性质或特征的）",
        "explanation": "附着在动词词根后，表示倾向于执行该动作或具有该特征。",
        "examples": "active (积极的), attractive (有吸引力的), creative (有创意的), effective (有效的), expensive (昂贵的), positive (积极的)"
    },
    {
        "id": 25,
        "affix": "-ly",
        "type": "后缀 (Suffix)",
        "meaning": "副词后缀（……地）",
        "explanation": "附着在形容词后，将其转化为表达方式、状态或程度的副词。",
        "examples": "recently (最近地), eventually (最终), overall (总体地), loudly (大声地), quickly (快速地), quietly (安静地)"
    },
    {
        "id": 26,
        "affix": "-ful",
        "type": "后缀 (Suffix)",
        "meaning": "形容词后缀（充满……的）",
        "explanation": "附着在名词后，构成表示充满某种性质或特征的形容词。",
        "examples": "careful (仔细的), helpful (有帮助的), powerful (强有力的), useful (有用的)"
    },
    {
        "id": 27,
        "affix": "-less",
        "type": "后缀 (Suffix)",
        "meaning": "形容词后缀（无……的、缺乏的）",
        "explanation": "附着在名词后，表示没有、缺乏某种特征或性质。",
        "examples": "careless (粗心的), hopeless (无望的), harmless (无害的)"
    },
    {
        "id": 28,
        "affix": "-ness",
        "type": "后缀 (Suffix)",
        "meaning": "抽象名词后缀（性质、状态）",
        "explanation": "附着在形容词后，转化为表达某种状态或品质的抽象名词。",
        "examples": "darkness (黑暗), illness (疾病), kindness (仁慈), weakness (弱点)"
    },
    {
        "id": 29,
        "affix": "-ize / -ise",
        "type": "后缀 (Suffix)",
        "meaning": "动词后缀（使……化）",
        "explanation": "构成表示使变成某种状态或实现某种目的的动词。",
        "examples": "realize (实现/意识到), organize (组织), memorize (记住)"
    },
    {
        "id": 30,
        "affix": "-ify",
        "type": "后缀 (Suffix)",
        "meaning": "动词后缀（使……化）",
        "explanation": "附着在形容词或名词后，表示使其具备某种特征或状态。",
        "examples": "simplify (简化), clarify (澄清), identify (识别)"
    },
    {
        "id": 31,
        "affix": "-ist",
        "type": "后缀 (Suffix)",
        "meaning": "名词后缀（专业人员、学者）",
        "explanation": "指从事某种专门行业、学科研究或抱有某种信念的人。",
        "examples": "scientist (科学家), artist (艺术家), specialist (专家)"
    },
    {
        "id": 32,
        "affix": "-er / -or",
        "type": "后缀 (Suffix)",
        "meaning": "名词后缀（做……的人/工具）",
        "explanation": "表示执行某动作的主体（人）或辅助工具器具。",
        "examples": "teacher (教师), doctor (医生), manager (经理), computer (计算机)"
    },
    {
        "id": 33,
        "affix": "-al / -ial",
        "type": "后缀 (Suffix)",
        "meaning": "形容词后缀（与……相关的）",
        "explanation": "附着在名词后，转化为表达领域性质或关联的形容词。",
        "examples": "national (国家的), natural (自然的), beneficial (有益的)"
    },
    {
        "id": 34,
        "affix": "-ous / -ious",
        "type": "后缀 (Suffix)",
        "meaning": "形容词后缀（充满……的、富含……的）",
        "explanation": "附着在名词或词根后，构成表达富含某种性质的形容词。",
        "examples": "famous (著名的), dangerous (危险的), precious (宝贵的)"
    },
    {
        "id": 35,
        "affix": "-ship",
        "type": "后缀 (Suffix)",
        "meaning": "名词后缀（身份、资格、关系、状态）",
        "explanation": "表达某种抽象关系、身份资历或技能能力。",
        "examples": "friendship (友谊), leadership (领导力), scholarship (奖学金)"
    },
    {
        "id": 36,
        "affix": "spect / spec",
        "type": "词根 (Latin Root)",
        "meaning": "看、观察、视角",
        "explanation": "源自拉丁语 specere，表示用眼睛注视、观察或展现出的外观。",
        "examples": "inspect (检查/视察), expect (期望), prospect (前景), aspect (方面), spectacle (奇观)"
    },
    {
        "id": 37,
        "affix": "tract",
        "type": "词根 (Latin Root)",
        "meaning": "拉、抽、吸引",
        "explanation": "源自拉丁语 trahere，表示拉动、吸引或抽取。",
        "examples": "attract (吸引), contract (合同/收缩), extract (提取), abstract (抽象的)"
    },
    {
        "id": 38,
        "affix": "struct",
        "type": "词根 (Latin Root)",
        "meaning": "建造、构建、结构",
        "explanation": "源自拉丁语 struere，表示建造、堆叠或搭建框架。",
        "examples": "structure (结构), construct (建造), instruct (指导), destroy (破坏)"
    },
    {
        "id": 39,
        "affix": "vid / vis",
        "type": "词根 (Latin Root)",
        "meaning": "看、看见、远见",
        "explanation": "源自拉丁语 videre，表示肉眼看见、观察或脑海远景。",
        "examples": "visit (访问), vision (视野/远见), visible (看得见的), advise (建议)"
    },
    {
        "id": 40,
        "affix": "dict / dic",
        "type": "词根 (Latin Root)",
        "meaning": "说话、言语、指明",
        "explanation": "源自拉丁语 dicere，表示口述言语、下达指令或指明。",
        "examples": "predict (预测), dictionary (字典), indicate (指出), dictate (听写/命令)"
    },
    {
        "id": 41,
        "affix": "ced / ceed / cess",
        "type": "词根 (Latin Root)",
        "meaning": "行走、前进、退让",
        "explanation": "源自拉丁语 cedere，表示行走步进、移动或做出退让。",
        "examples": "succeed (成功/继承), proceed (继续进行), access (通道), recede (后退)"
    },
    {
        "id": 42,
        "affix": "duc / duct",
        "type": "词根 (Latin Root)",
        "meaning": "引导、带领、产出",
        "explanation": "源自拉丁语 ducere，表示向前引路、导出或成果产出。",
        "examples": "produce (生产), conduct (组织/实施), introduce (介绍), educate (教育)"
    },
    {
        "id": 43,
        "affix": "fer",
        "type": "词根 (Latin Root)",
        "meaning": "带来、拿取、承受",
        "explanation": "源自拉丁语 ferre，表示携带物品、带来见解或承受。",
        "examples": "offer (提供), transfer (转移), prefer (更喜欢), differ (不同)"
    },
    {
        "id": 44,
        "affix": "form",
        "type": "词根 (Latin Root)",
        "meaning": "形状、形式、规范",
        "explanation": "源自拉丁语 forma，表示物体的外形、结构模式或规范。",
        "examples": "form (形式), transform (改变/转变), perform (表演/执行), inform (通知)"
    }
]

version_str = "v1.5.3"

html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    
    <!-- CRITICAL FIX: Bypass Anti-Hotlinking Referer Blocking on WeChat, Xiaomi, Huawei Browsers -->
    <meta name="referrer" content="no-referrer">

    <!-- Anti-Cache Headers -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">

    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="英语速记打卡">
    <meta name="application-name" content="英语速记打卡">
    <meta name="theme-color" content="#FBFBF9">

    <link rel="apple-touch-icon" href="https://img.icons8.com/fluency/192/books.png">
    <link rel="icon" type="image/png" href="https://img.icons8.com/fluency/96/books.png">

    <title>英语速记 {version_str}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+Pro:wght@400;600&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --bg-color: #FBFBF9;
            --sidebar-bg: #FFFFFF;
            --text-main: #000000;
            --text-secondary: #333333;
            --text-muted: #777777;
            --border-color: #E5E5E0;
            --accent-green: #22C55E;
            --accent-red: #DC2626;
            --accent-black: #000000;
            --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
            --font-serif: "Source Serif Pro", Georgia, serif;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent !important;
            font-family: var(--font-sans);
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding: max(20px, env(safe-area-inset-top)) 16px 20px 16px;
            overflow-x: hidden;
        }}

        header {{
            text-align: center;
            margin-bottom: 8px;
            width: 100%;
            max-width: 480px;
            position: relative;
        }}

        .sub-title {{
            font-size: 0.82rem;
            color: var(--text-muted);
            font-weight: 500;
            letter-spacing: 0.05em;
            margin-bottom: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }}

        .streak-banner {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .streak-num {{
            color: var(--accent-red);
            font-size: 1.8rem;
            font-weight: 800;
            margin: 0 4px;
            line-height: 1;
        }}

        .version-tag {{
            font-size: 0.65rem;
            color: var(--text-muted);
            font-family: monospace;
            background: #E5E5E0;
            padding: 1px 5px;
            border-radius: 4px;
        }}

        .root-category-box {{
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 14px 12px;
            margin-bottom: 14px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            text-align: left;
        }}

        .root-category-header {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--accent-red);
            margin-bottom: 10px;
            padding-bottom: 6px;
            border-bottom: 1px solid #F0F0EE;
        }}

        .root-chip-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 8px;
        }}

        .root-chip-item {{
            background: #FBFBF9;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 8px 6px;
            text-align: center;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .root-chip-item:hover, .root-chip-item:active {{
            background: var(--accent-red);
            color: #FFFFFF;
            border-color: var(--accent-red);
        }}

        .root-chip-affix {{
            font-size: 1.05rem;
            font-weight: 700;
            display: block;
            margin-bottom: 2px;
        }}

        .root-chip-meaning {{
            font-size: 0.72rem;
            color: var(--text-muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
        }}

        .root-chip-item:hover .root-chip-meaning, .root-chip-item:active .root-chip-meaning {{
            color: rgba(255,255,255,0.9);
        }}

        .settings-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
            margin-bottom: 8px;
            width: 100%;
            max-width: 480px;
            background: #FFFFFF;
            padding: 6px 12px;
            border: 1px solid var(--border-color);
            font-size: 0.8rem;
        }}

        .setting-item {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .goal-select, .voice-select {{
            background: #FFFFFF;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 3px 6px;
            font-size: 0.78rem;
            outline: none;
            cursor: pointer;
            font-weight: 500;
        }}

        .speed-pill-group {{
            display: flex;
            align-items: center;
            gap: 3px;
        }}

        .btn-speed-pill {{
            padding: 2px 7px;
            border: 1px solid var(--border-color);
            background: #FFFFFF;
            color: var(--text-secondary);
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .btn-speed-pill.active {{
            background: var(--accent-black);
            color: #FFFFFF;
            border-color: var(--accent-black);
        }}

        @media (max-width: 640px) {{
            .voice-setting-item {{
                display: none !important;
            }}
        }}

        .controls {{
            display: flex;
            gap: 4px;
            margin-bottom: 8px;
            justify-content: space-between;
            width: 100%;
            max-width: 480px;
        }}

        .btn-mode {{
            flex: 1;
            padding: 6px 4px;
            border: 1px solid var(--border-color);
            background: #FFFFFF;
            color: var(--text-secondary);
            font-size: 0.76rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
            white-space: nowrap;
        }}

        .btn-mode.active {{
            background: var(--accent-black);
            color: #FFFFFF;
            border-color: var(--accent-black);
            font-weight: 600;
        }}

        .progress-container {{
            width: 100%;
            max-width: 480px;
            margin-bottom: 8px;
        }}

        .progress-stats {{
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-bottom: 4px;
        }}

        .progress-bar {{
            height: 4px;
            background: var(--border-color);
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            width: 0%;
            background: var(--accent-black);
            transition: width 0.3s ease;
        }}

        /* List View Container */
        .list-view-container {{
            width: 100%;
            max-width: 480px;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            padding: 12px;
            margin-bottom: 14px;
        }}

        .list-header-bar {{
            display: flex;
            gap: 8px;
            margin-bottom: 10px;
            align-items: center;
        }}

        .search-input {{
            flex: 1;
            padding: 8px 12px;
            border: 1px solid var(--border-color);
            background: var(--bg-color);
            font-size: 0.85rem;
            outline: none;
            color: var(--text-main);
        }}
        .search-input:focus {{
            border-color: var(--text-main);
            background: #FFFFFF;
        }}

        .btn-start-study {{
            padding: 8px 12px;
            background: var(--accent-black);
            color: #FFFFFF;
            border: none;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
        }}

        .word-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 8px;
            max-height: 430px;
            overflow-y: auto;
            padding-right: 2px;
        }}

        .word-grid-item {{
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            padding: 10px 8px;
            text-align: center;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .word-grid-item:hover, .word-grid-item:active {{
            background: #FFFFFF;
            border-color: var(--accent-black);
            transform: translateY(-1px);
        }}

        .grid-item-num {{
            font-size: 0.68rem;
            color: var(--text-muted);
            margin-bottom: 2px;
        }}

        .grid-item-word {{
            font-family: var(--font-serif);
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-main);
            word-break: break-word;
        }}

        /* Card View Wrapper */
        .card-view-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            max-width: 480px;
            margin-bottom: 6px;
        }}

        .btn-back-list {{
            background: none;
            border: 1px solid var(--border-color);
            padding: 4px 10px;
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--text-secondary);
            cursor: pointer;
            background: #FFFFFF;
        }}
        .btn-back-list:hover {{
            background: #EEEEEE;
        }}

        .card-wrapper {{
            perspective: 1000px;
            width: 100%;
            max-width: 480px;
            height: 410px;
            margin-bottom: 14px;
            cursor: pointer;
        }}

        .card {{
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .card.flipped {{
            transform: rotateY(180deg);
        }}

        .card-face {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            padding: 16px 18px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 6px 6px 0px rgba(0,0,0,0.03);
        }}

        .card-front {{
            align-items: stretch;
        }}

        .card-back {{
            transform: rotateY(180deg);
            background: #FFFFFF;
            align-items: stretch;
            justify-content: space-between;
            overflow-y: auto;
        }}

        .front-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .card-tag {{
            font-size: 0.72rem;
            padding: 2px 8px;
            background: var(--bg-color);
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            font-weight: 500;
        }}

        .ebbinghaus-badge {{
            font-size: 0.72rem;
            padding: 2px 8px;
            background: var(--bg-color);
            color: var(--text-main);
            font-weight: 600;
            border: 1px solid var(--border-color);
        }}

        .card-word {{
            font-family: var(--font-serif);
            font-size: 2.5rem;
            font-weight: 600;
            text-align: center;
            color: var(--text-main);
            margin: 4px 0 2px 0;
            cursor: pointer;
        }}

        .card-ipa {{
            font-size: 1rem;
            color: var(--text-secondary);
            font-family: monospace;
            background: var(--bg-color);
            padding: 4px 14px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid var(--border-color);
            cursor: pointer;
        }}

        .audio-btn {{
            background: none;
            border: none;
            color: var(--text-main);
            cursor: pointer;
            font-size: 1rem;
            pointer-events: none;
        }}

        .flip-hint {{
            font-size: 0.75rem;
            color: var(--text-muted);
            text-align: center;
        }}

        .front-sentence-box {{
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            padding: 10px 12px;
            margin: 6px 0;
            cursor: pointer;
            position: relative;
        }}

        .front-sentence-title {{
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .front-sentence-text {{
            font-family: var(--font-serif);
            font-size: 0.95rem;
            line-height: 1.4;
            color: var(--text-main);
        }}

        .back-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 6px;
            margin-bottom: 8px;
        }}

        .back-word-box {{
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }}

        .back-word {{
            font-family: var(--font-serif);
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-main);
        }}

        .back-ipa {{
            font-size: 0.85rem;
            color: var(--text-muted);
            font-family: monospace;
        }}

        .back-meaning {{
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-main);
        }}

        .section-box {{
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            padding: 8px 12px;
            margin-bottom: 6px;
            cursor: pointer;
        }}

        .section-box.etymology-box {{
            cursor: default;
        }}

        .box-title {{
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 3px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .box-text {{
            font-size: 0.85rem;
            line-height: 1.35;
            color: var(--text-secondary);
        }}

        .box-text.trans {{
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 2px;
        }}

        .action-btns {{
            display: flex;
            gap: 12px;
            width: 100%;
            max-width: 480px;
        }}

        .btn-action {{
            flex: 1;
            padding: 12px;
            border: 1px solid var(--text-main);
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}

        .btn-dont-know {{
            background: #FFFFFF;
            color: var(--text-main);
        }}
        .btn-dont-know:hover {{
            background: #F0F0EE;
        }}

        .btn-know {{
            background: var(--accent-black);
            color: #FFFFFF;
        }}
        .btn-know:hover {{
            background: #222222;
        }}

        .finish-card {{
            text-align: center;
            padding: 24px 16px;
            display: none;
            background: #FFFFFF;
            border: 1px solid var(--border-color);
            max-width: 480px;
            width: 100%;
        }}

        .finish-card h2 {{
            font-family: var(--font-serif);
            font-size: 1.6rem;
            color: var(--text-main);
            margin-bottom: 8px;
        }}

        .finish-stats-box {{
            background: var(--bg-color);
            border: 1px solid var(--border-color);
            padding: 12px;
            margin: 14px 0 20px 0;
            display: flex;
            justify-content: space-around;
        }}

        .stat-num {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--text-main);
        }}

        .stat-label {{
            font-size: 0.72rem;
            color: var(--text-muted);
        }}
    </style>
</head>
<body>

    <header>
        <div class="sub-title">
            <span>英语速记</span>
            <span class="version-tag">{version_str}</span>
        </div>
        <div class="streak-banner">
            已打卡 <span class="streak-num" id="streakDaysNum">1</span> 天
        </div>
    </header>

    <div class="settings-bar">
        <div class="setting-item">
            <span>📅 目标:</span>
            <select class="goal-select" id="dailyGoalSelect" onchange="changeDailyGoal()">
                <option value="20">20词</option>
                <option value="30" selected>30词</option>
                <option value="50">50词</option>
                <option value="100">100词</option>
            </select>
        </div>

        <div class="setting-item">
            <span>⏱️ 语速:</span>
            <div class="speed-pill-group">
                <button class="btn-speed-pill" id="spd08" onclick="setSpeed(0.8)">0.8</button>
                <button class="btn-speed-pill active" id="spd10" onclick="setSpeed(1.0)">1.0</button>
                <button class="btn-speed-pill" id="spd12" onclick="setSpeed(1.2)">1.2</button>
            </div>
        </div>

        <div class="setting-item voice-setting-item">
            <span>🎤 声音:</span>
            <select class="voice-select" id="voiceSelect" onchange="changeVoice()">
                <option value="">系统发音人</option>
            </select>
        </div>
    </div>

    <!-- Simplified 4 Core Tabs -->
    <div class="controls">
        <button class="btn-mode active" id="btnDaily" onclick="setMode('daily')">🌟 今日任务 (<span id="dailyTotalCount">30</span>)</button>
        <button class="btn-mode" id="btnUnlearned" onclick="setMode('unlearned')">🎯 生词本 (<span id="unlearnedCount">0</span>)</button>
        <button class="btn-mode" id="btnAll" onclick="setMode('all')">📚 词库 ({len(full_dataset)})</button>
        <button class="btn-mode" id="btnRoots" onclick="setMode('roots')">🧩 词根词缀 ({len(root_dataset)})</button>
    </div>

    <div class="progress-container" id="progressContainer">
        <div class="progress-stats">
            <span>进度: <strong id="currentIndex">1</strong> / <span id="totalIndex">30</span></span>
            <span>艾宾浩斯复习: <strong id="reviewCountNum" style="color:var(--text-main);">0</strong> 词</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
    </div>

    <!-- List View (Default on tab click) -->
    <div class="list-view-container" id="listViewContainer">
        <div class="list-header-bar">
            <input type="text" class="search-input" id="searchInput" placeholder="🔍 输入字母搜单词 (如 'ab')..." oninput="renderWordList()">
            <button class="btn-start-study" id="btnStartStudy" onclick="manualRandomShuffleStudy()">🔀 随机打卡</button>
        </div>
        <div class="word-grid" id="wordGrid"></div>
    </div>

    <!-- Card View Area -->
    <div id="cardViewArea" style="display:none; width: 100%; max-width: 480px;">
        <div class="card-view-header">
            <button class="btn-back-list" onclick="showListView()">📋 返回清单</button>
            <span style="font-size:0.75rem; color:var(--text-muted);" id="cardModeIndicator">今日任务</span>
        </div>

        <div class="card-wrapper" onclick="toggleFlip()">
            <div class="card" id="flashcard">
                <!-- Front -->
                <div class="card-face card-front">
                    <div class="front-top">
                        <span class="card-tag" id="cardTag">词汇 #1</span>
                        <span class="ebbinghaus-badge" id="ebbinghausBadge">🌟 今日新词</span>
                    </div>
                    
                    <div class="card-word" id="cardWord" onclick="event.stopPropagation(); speakWord();" title="点击朗读单词">instead</div>
                    
                    <div style="text-align:center;">
                        <div class="card-ipa" onclick="event.stopPropagation(); speakWord();" title="点击区域朗读发音">
                            <span id="cardIpa">/ɪnˈsted/</span>
                            <button class="audio-btn" title="朗读">🔊 读音</button>
                        </div>
                    </div>

                    <div class="front-sentence-box" onclick="event.stopPropagation(); speakSentence();" title="点击整框朗读英文例句">
                        <div class="front-sentence-title">
                            <span id="frontSentenceLabel">💬 英文例句语境</span>
                            <span style="font-size: 0.8rem; color: var(--text-main);">🔊 点击听句</span>
                        </div>
                        <div class="front-sentence-text" id="frontSentence">He didn't answer, but smiled instead.</div>
                    </div>

                    <div class="flip-hint">👆 点击空白区域翻面验证答案</div>
                </div>

                <!-- Back -->
                <div class="card-face card-back">
                    <div class="back-header">
                        <div class="back-word-box" onclick="event.stopPropagation(); speakWord();" title="点击读单词">
                            <span class="back-word" id="backWord">instead</span>
                            <span class="back-ipa" id="backIpa">/ɪnˈsted/</span>
                            <span style="font-size:0.85rem;">🔊</span>
                        </div>
                        <span class="back-meaning" id="backMeaning">adv. 代替;反而;却</span>
                    </div>

                    <div class="section-box etymology-box" id="box1Container">
                        <div class="box-title">
                            <span id="box1Title">🧩 词根演变拆解</span>
                        </div>
                        <div class="box-text" id="backEtymology">in- (在内) + stead (地方) ➔ 站在别人的位置上 ➔ 替换、反而</div>
                    </div>

                    <div class="section-box phrase-box" id="box2Container" onclick="event.stopPropagation(); speakPhrase();" title="点击整框朗读短语">
                        <div class="box-title">
                            <span id="box2Title">📌 高频短语 (点击读短语)</span>
                            <span style="font-size: 0.8rem;" id="box2AudioTag">🔊 读短语</span>
                        </div>
                        <div class="box-text" id="backPhrase">instead of (代替/而不是) ｜ in - stead (因-斯泰德)</div>
                    </div>

                    <div class="section-box sentence-box" id="box3Container" onclick="event.stopPropagation(); speakSentence();" title="点击整框朗读例句">
                        <div class="box-title">
                            <span id="box3Title">💬 例句翻译 (点击听例句)</span>
                            <span style="font-size: 0.8rem;" id="box3AudioTag">🔊 点击听句</span>
                        </div>
                        <div class="box-text" id="backSentence" style="font-size:0.82rem; color:var(--text-muted);">He didn't answer, but smiled instead.</div>
                        <div class="box-text trans" id="backTranslation" style="font-size:0.88rem; color:var(--text-main); font-weight:500;">他没有回答，反而笑了笑了。</div>
                    </div>

                    <div class="flip-hint">👇 点击下方标记掌握状态</div>
                </div>
            </div>
        </div>

        <div class="action-btns" id="actionBtns">
            <button class="btn-action btn-dont-know" id="btnMarkWrong" onclick="markResult(false)">
                ❌ 没记住
            </button>
            <button class="btn-action btn-know" id="btnMarkRight" onclick="markResult(true)">
                ✅ 记住啦
            </button>
        </div>
    </div>

    <div class="finish-card" id="finishCard">
        <h2>🎉 今日目标已完成</h2>
        <p style="color: var(--text-muted); font-size: 0.85rem;">明日点开网页将遵照艾宾浩斯曲线自动推送复习！</p>
        
        <div class="finish-stats-box">
            <div>
                <div class="stat-num" id="statReviewDone">0</div>
                <div class="stat-label">复习词数</div>
            </div>
            <div>
                <div class="stat-num" id="statNewDone">30</div>
                <div class="stat-label">完成新词</div>
            </div>
            <div>
                <div class="stat-num" id="statUnlearned">0</div>
                <div class="stat-label">生词数</div>
            </div>
        </div>

        <button class="btn-action btn-know" onclick="continueExtraDeck()" style="max-width: 240px; margin: 0 auto;">
            ⚡ 再来一组！
        </button>
    </div>

    <audio id="universalAudioPlayer" preload="auto" style="display:none;"></audio>

    <script>
        const rawWordsData = {json.dumps(full_dataset, ensure_ascii=False)};
        const rootDataset = {json.dumps(root_dataset, ensure_ascii=False)};
        
        const EBBINGHAUS_INTERVALS = [1, 2, 4, 8, 15];

        let memoryState = JSON.parse(localStorage.getItem('zk_memory_full_state')) || {{}};
        let ebbState = JSON.parse(localStorage.getItem('zk_ebbinghaus_state')) || {{}};
        let dailyGoal = parseInt(localStorage.getItem('zk_daily_goal')) || 30;
        let speechSpeed = parseFloat(localStorage.getItem('zk_speech_speed')) || 1.0;
        let savedVoiceURI = localStorage.getItem('zk_selected_voice_uri') || '';

        let streakDays = parseInt(localStorage.getItem('zk_streak_days')) || 0;
        let lastStreakDate = localStorage.getItem('zk_last_streak_date') || '';

        let currentMode = 'daily';
        let viewState = 'list'; // 'list' or 'card'
        let currentDeck = [];
        let currentDeckIndex = 0;
        let isFlipped = false;
        let availableVoices = [];
        let isAudioUnlocked = false;

        function getTodayStr() {{
            const now = new Date();
            return now.toISOString().split('T')[0];
        }}

        function addDays(dateStr, days) {{
            const d = new Date(dateStr);
            d.setDate(d.getDate() + days);
            return d.toISOString().split('T')[0];
        }}

        function updateStreakCountOnLoad() {{
            const today = getTodayStr();
            if (lastStreakDate && lastStreakDate !== today) {{
                const yesterday = addDays(today, -1);
                if (lastStreakDate !== yesterday) {{
                    streakDays = 0;
                    localStorage.setItem('zk_streak_days', 0);
                }}
            }}
            document.getElementById('streakDaysNum').innerText = streakDays;
        }}

        function recordRealCheckIn() {{
            const today = getTodayStr();
            if (lastStreakDate !== today) {{
                const yesterday = addDays(today, -1);
                if (lastStreakDate === yesterday) {{
                    streakDays += 1;
                }} else {{
                    streakDays = 1;
                }}
                lastStreakDate = today;
                localStorage.setItem('zk_streak_days', streakDays);
                localStorage.setItem('zk_last_streak_date', lastStreakDate);
                document.getElementById('streakDaysNum').innerText = streakDays;
            }}
        }}

        function unlockMobileAudio() {{
            if (!isAudioUnlocked) {{
                const p = document.getElementById('universalAudioPlayer');
                p.play().then(() => {{ p.pause(); }}).catch(e => {{}});
                isAudioUnlocked = true;
            }}
        }}

        document.addEventListener('touchstart', unlockMobileAudio, {{ once: true }});
        document.addEventListener('click', unlockMobileAudio, {{ once: true }});

        function init() {{
            updateStreakCountOnLoad();
            document.getElementById('dailyGoalSelect').value = dailyGoal;
            syncSpeedUI();
            updateCounts();
            buildDeck();
            
            showCardView();
            loadVoices();
        }}

        function showCardView() {{
            viewState = 'card';
            document.getElementById('listViewContainer').style.display = 'none';
            document.getElementById('cardViewArea').style.display = 'block';
            document.getElementById('finishCard').style.display = 'none';
            renderCard(false);
        }}

        function showListView() {{
            viewState = 'list';
            document.getElementById('listViewContainer').style.display = 'block';
            document.getElementById('cardViewArea').style.display = 'none';
            document.getElementById('finishCard').style.display = 'none';
            
            const searchInput = document.getElementById('searchInput');
            if (currentMode === 'roots') {{
                searchInput.placeholder = "🔍 搜索词根词缀 (如 're' 或 'tion')...";
            }} else {{
                searchInput.placeholder = "🔍 输入字母搜单词 (如 'ab')...";
            }}

            renderWordList();
        }}

        /* PREFIX-FIRST SEARCH LOGIC & ROOT CATEGORY BOXES */
        function renderWordList() {{
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            const grid = document.getElementById('wordGrid');
            grid.innerHTML = '';

            let filtered = [];

            if (currentMode === 'roots') {{
                if (!query) {{
                    filtered = currentDeck;
                }} else {{
                    let prefixMatches = currentDeck.filter(item => item.affix.toLowerCase().replace('-', '').startsWith(query));
                    if (prefixMatches.length > 0) {{
                        filtered = prefixMatches;
                    }} else {{
                        filtered = currentDeck.filter(item => item.affix.toLowerCase().includes(query) || item.meaning.includes(query));
                    }}
                }}
            }} else {{
                if (!query) {{
                    filtered = currentDeck;
                }} else {{
                    // Rule: Filter words that START WITH the query first!
                    let prefixMatches = currentDeck.filter(item => item.word.toLowerCase().startsWith(query));
                    if (prefixMatches.length > 0) {{
                        filtered = prefixMatches;
                    }} else {{
                        // Fallback: If no prefix matches, filter words that contain the query
                        filtered = currentDeck.filter(item => item.word.toLowerCase().includes(query));
                    }}
                }}
            }}

            if (filtered.length === 0) {{
                grid.style.display = 'grid';
                grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; color:var(--text-muted); padding:20px; font-size:0.85rem;">未搜索到匹配项</div>';
                return;
            }}

            if (currentMode === 'roots') {{
                grid.style.display = 'block';

                const rootCategoryItems = filtered.filter(item => item.type.includes('词根'));
                const prefixCategoryItems = filtered.filter(item => item.type.includes('前缀'));
                const suffixCategoryItems = filtered.filter(item => item.type.includes('后缀'));

                const categories = [
                    {{ title: '🌳 核心词根 (Roots)', items: rootCategoryItems }},
                    {{ title: '🔤 高频前缀 (Prefixes)', items: prefixCategoryItems }},
                    {{ title: '🔠 常用后缀 (Suffixes)', items: suffixCategoryItems }}
                ];

                let html = '';
                categories.forEach(cat => {{
                    if (cat.items.length > 0) {{
                        html += `<div class="root-category-box">
                            <div class="root-category-header">${{cat.title}} <span style="font-size:0.75rem; color:var(--text-muted); font-weight:normal;">(${{cat.items.length}}个)</span></div>
                            <div class="root-chip-grid">`;
                        
                        cat.items.forEach(item => {{
                            const origIndex = currentDeck.indexOf(item);
                            html += `<div class="root-chip-item" onclick="selectWordFromList(${{origIndex}})">
                                <span class="root-chip-affix">${{item.affix}}</span>
                                <span class="root-chip-meaning" title="${{item.meaning}}">${{item.meaning}}</span>
                            </div>`;
                        }});

                        html += `</div></div>`;
                    }}
                }});

                grid.innerHTML = html;
                return;
            }} else {{
                grid.style.display = 'grid';
            }}

            filtered.forEach((item) => {{
                const origIndex = currentDeck.indexOf(item);
                const div = document.createElement('div');
                div.className = 'word-grid-item';
                div.onclick = function() {{
                    selectWordFromList(origIndex);
                }};
                
                div.innerHTML = `
                    <span class="grid-item-num">#${{origIndex + 1}}</span>
                    <span class="grid-item-word">${{item.word}}</span>
                `;
                grid.appendChild(div);
            }});
        }}

        function syncSpeedUI() {{
            const btn08 = document.getElementById('spd08');
            const btn10 = document.getElementById('spd10');
            const btn12 = document.getElementById('spd12');
            
            if (btn08) btn08.classList.remove('active');
            if (btn10) btn10.classList.remove('active');
            if (btn12) btn12.classList.remove('active');

            if (speechSpeed <= 0.85) {{
                if (btn08) btn08.classList.add('active');
            }} else if (speechSpeed >= 1.15) {{
                if (btn12) btn12.classList.add('active');
            }} else {{
                if (btn10) btn10.classList.add('active');
            }}
        }}

        function setSpeed(spd) {{
            speechSpeed = parseFloat(spd);
            localStorage.setItem('zk_speech_speed', speechSpeed);
            syncSpeedUI();
            if (viewState === 'card' && currentMode !== 'roots') {{
                speakSentence();
            }}
        }}

        function loadVoices() {{
            if ('speechSynthesis' in window) {{
                function populateVoices() {{
                    try {{
                        const voices = window.speechSynthesis.getVoices();
                        availableVoices = voices.filter(v => v.lang && (v.lang.startsWith('en') || v.lang.startsWith('EN')));
                        const select = document.getElementById('voiceSelect');
                        select.innerHTML = '<option value="">系统发音人</option>';
                        
                        if (availableVoices.length > 0) {{
                            availableVoices.forEach((v) => {{
                                const option = document.createElement('option');
                                option.value = v.voiceURI;
                                option.textContent = `${{v.name}} (${{v.lang}})`;
                                if (savedVoiceURI && v.voiceURI === savedVoiceURI) {{
                                    option.selected = true;
                                }}
                                select.appendChild(option);
                            }});
                        }}
                    }} catch(e) {{
                        console.log('Voice load non-critical warning');
                    }}
                }}
                populateVoices();
                if (speechSynthesis.onvoiceschanged !== undefined) {{
                    speechSynthesis.onvoiceschanged = populateVoices;
                }}
            }}
        }}

        function changeVoice() {{
            const select = document.getElementById('voiceSelect');
            savedVoiceURI = select.value;
            localStorage.setItem('zk_selected_voice_uri', savedVoiceURI);
            speakWord();
        }}

        function getSelectedVoiceObj() {{
            if (!savedVoiceURI || availableVoices.length === 0) return null;
            return availableVoices.find(v => v.voiceURI === savedVoiceURI) || null;
        }}

        function changeDailyGoal() {{
            dailyGoal = parseInt(document.getElementById('dailyGoalSelect').value);
            localStorage.setItem('zk_daily_goal', dailyGoal);
            buildDeck();
            showListView();
        }}

        function updateCounts() {{
            const mastered = Object.values(memoryState).filter(v => v === true).length;
            const unlearned = Object.values(memoryState).filter(v => v === false).length;
            
            document.getElementById('unlearnedCount').innerText = unlearned;
            
            const today = getTodayStr();
            let dueReviews = 0;
            Object.values(ebbState).forEach(item => {{
                if (item.nextReview <= today && item.stage < EBBINGHAUS_INTERVALS.length) {{
                    dueReviews++;
                }}
            }});
            document.getElementById('reviewCountNum').innerText = dueReviews;
        }}

        function shuffleArray(array) {{
            const arr = [...array];
            for (let i = arr.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }}
            return arr;
        }}

        function categorizeDifficulty(words) {{
            let easy = [], medium = [], hard = [];
            words.forEach(w => {{
                const len = w.word.trim().length;
                if (len <= 4) easy.push(w);
                else if (len <= 7) medium.push(w);
                else hard.push(w);
            }});
            return {{ easy, medium, hard }};
        }}

        function getProportionalDeck(poolWords, goal) {{
            const {{ easy, medium, hard }} = categorizeDifficulty(poolWords);
            
            let nEasy = Math.round(goal * 0.25);
            let nHard = Math.round(goal * 0.25);
            let nMed = goal - nEasy - nHard;

            const selectedEasy = shuffleArray(easy).slice(0, nEasy);
            const selectedMed = shuffleArray(medium).slice(0, nMed);
            const selectedHard = shuffleArray(hard).slice(0, nHard);

            let combined = [...selectedEasy, ...selectedMed, ...selectedHard];

            if (combined.length < goal) {{
                const selectedWords = new Set(combined.map(x => x.word));
                const remaining = poolWords.filter(x => !selectedWords.has(x.word));
                combined.push(...shuffleArray(remaining).slice(0, goal - combined.length));
            }}

            return shuffleArray(combined);
        }}

        function buildDeck(forceReshuffle = false) {{
            const today = getTodayStr();
            
            if (currentMode === 'daily') {{
                const dailyDeckKey = `zk_daily_deck_${{today}}_${{dailyGoal}}`;
                let savedWordNames = null;

                if (!forceReshuffle) {{
                    try {{
                        savedWordNames = JSON.parse(localStorage.getItem(dailyDeckKey));
                    }} catch(e) {{}}
                }}

                if (savedWordNames && Array.isArray(savedWordNames) && savedWordNames.length > 0) {{
                    let mapByName = {{}};
                    rawWordsData.forEach(w => {{ mapByName[w.word] = w; }});
                    
                    let hydrated = [];
                    savedWordNames.forEach(wName => {{
                        if (mapByName[wName]) {{
                            let item = mapByName[wName];
                            const ebb = ebbState[item.word];
                            if (ebb && ebb.nextReview <= today && ebb.stage < EBBINGHAUS_INTERVALS.length) {{
                                item._isReview = true;
                                item._ebbStage = ebb.stage;
                            }} else {{
                                item._isReview = false;
                            }}
                            hydrated.push(item);
                        }}
                    }});
                    
                    if (hydrated.length > 0) {{
                        currentDeck = hydrated;
                        document.getElementById('dailyTotalCount').innerText = currentDeck.length;
                        currentDeckIndex = 0;
                        isFlipped = false;
                        return;
                    }}
                }}

                let reviewItems = [];
                rawWordsData.forEach(item => {{
                    const ebb = ebbState[item.word];
                    if (ebb && ebb.nextReview <= today && ebb.stage < EBBINGHAUS_INTERVALS.length) {{
                        item._isReview = true;
                        item._ebbStage = ebb.stage;
                        reviewItems.push(item);
                    }}
                }});

                let newPool = rawWordsData.filter(item => !ebbState[item.word] && memoryState[item.word] === undefined);
                newPool.forEach(item => {{ item._isReview = false; }});
                
                let sampledNew = getProportionalDeck(newPool, dailyGoal);
                currentDeck = [...shuffleArray(reviewItems), ...sampledNew];

                if (currentDeck.length === 0) {{
                    const unmastered = rawWordsData.filter(item => memoryState[item.word] !== true);
                    currentDeck = getProportionalDeck(unmastered, dailyGoal);
                }}

                const wordNamesToSave = currentDeck.map(item => item.word);
                localStorage.setItem(dailyDeckKey, JSON.stringify(wordNamesToSave));

                document.getElementById('dailyTotalCount').innerText = currentDeck.length;

            }} else if (currentMode === 'unlearned') {{
                const unlearned = rawWordsData.filter(item => memoryState[item.word] === false);
                currentDeck = shuffleArray(unlearned);
            }} else if (currentMode === 'all') {{
                currentDeck = shuffleArray(rawWordsData);
            }} else if (currentMode === 'roots') {{
                currentDeck = rootDataset;
            }}
            
            currentDeckIndex = 0;
            isFlipped = false;
        }}

        function manualRandomShuffleStudy() {{
            if (currentMode === 'roots') {{
                selectWordFromList(0);
                return;
            }}
            buildDeck(true);
            showCardView();
        }}

        function setMode(mode) {{
            currentMode = mode;
            document.querySelectorAll('.btn-mode').forEach(btn => btn.classList.remove('active'));
            if (mode === 'daily') document.getElementById('btnDaily').classList.add('active');
            if (mode === 'unlearned') document.getElementById('btnUnlearned').classList.add('active');
            if (mode === 'all') document.getElementById('btnAll').classList.add('active');
            if (mode === 'roots') document.getElementById('btnRoots').classList.add('active');
            
            buildDeck();
            showListView();
        }}

        function showListView() {{
            viewState = 'list';
            document.getElementById('listViewContainer').style.display = 'block';
            document.getElementById('cardViewArea').style.display = 'none';
            document.getElementById('finishCard').style.display = 'none';
            
            const searchInput = document.getElementById('searchInput');
            if (currentMode === 'roots') {{
                searchInput.placeholder = "🔍 搜索词根词缀 (如 're' 或 'tion')...";
            }} else {{
                searchInput.placeholder = "🔍 输入字母搜单词 (如 'ab')...";
            }}

            renderWordList();
        }}

        /* PREFIX-FIRST SEARCH LOGIC */
        function renderWordList() {{
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            const grid = document.getElementById('wordGrid');
            grid.innerHTML = '';

            let filtered = [];

            if (currentMode === 'roots') {{
                if (!query) {{
                    filtered = currentDeck;
                }} else {{
                    let prefixMatches = currentDeck.filter(item => item.affix.toLowerCase().replace('-', '').startsWith(query));
                    if (prefixMatches.length > 0) {{
                        filtered = prefixMatches;
                    }} else {{
                        filtered = currentDeck.filter(item => item.affix.toLowerCase().includes(query) || item.meaning.includes(query));
                    }}
                }}
            }} else {{
                if (!query) {{
                    filtered = currentDeck;
                }} else {{
                    // Rule: Filter words that START WITH the query first!
                    let prefixMatches = currentDeck.filter(item => item.word.toLowerCase().startsWith(query));
                    if (prefixMatches.length > 0) {{
                        filtered = prefixMatches;
                    }} else {{
                        // Fallback: If no prefix matches, filter words that contain the query
                        filtered = currentDeck.filter(item => item.word.toLowerCase().includes(query));
                    }}
                }}
            }}

            if (filtered.length === 0) {{
                grid.innerHTML = '<div style="grid-column:1/-1; text-align:center; color:var(--text-muted); padding:20px; font-size:0.85rem;">未搜索到匹配项</div>';
                return;
            }}

            filtered.forEach((item) => {{
                const origIndex = currentDeck.indexOf(item);
                const div = document.createElement('div');
                div.className = 'word-grid-item';
                div.onclick = function() {{
                    selectWordFromList(origIndex);
                }};
                
                if (currentMode === 'roots') {{
                    div.innerHTML = `
                        <span class="grid-item-num">#${{origIndex + 1}} [${{item.type.split(' ')[0]}}]</span>
                        <span class="grid-item-word" style="font-size:1.3rem; color:var(--accent-red);">${{item.affix}}</span>
                    `;
                }} else {{
                    div.innerHTML = `
                        <span class="grid-item-num">#${{origIndex + 1}}</span>
                        <span class="grid-item-word">${{item.word}}</span>
                    `;
                }}
                grid.appendChild(div);
            }});
        }}

        function selectWordFromList(deckIdx) {{
            currentDeckIndex = deckIdx;
            viewState = 'card';
            document.getElementById('listViewContainer').style.display = 'none';
            document.getElementById('cardViewArea').style.display = 'block';
            renderCard(true);
        }}

        function startCardStudyFromFirst() {{
            selectWordFromList(0);
        }}

        function renderCard(autoSpeak = false) {{
            const cardEl = document.getElementById('flashcard');
            const cardArea = document.getElementById('cardViewArea');
            const finishCard = document.getElementById('finishCard');

            const today = getTodayStr();
            localStorage.setItem(`zk_daily_index_${{today}}_${{currentMode}}`, currentDeckIndex);

            if (currentDeck.length === 0 || currentDeckIndex >= currentDeck.length) {{
                cardArea.style.display = 'none';
                finishCard.style.display = 'block';

                const reviewsDone = currentDeck.filter(i => i._isReview).length;
                const newDone = currentDeck.length - reviewsDone;
                const unlearnedNum = Object.values(memoryState).filter(v => v === false).length;
                
                document.getElementById('statReviewDone').innerText = reviewsDone;
                document.getElementById('statNewDone').innerText = newDone;
                document.getElementById('statUnlearned').innerText = unlearnedNum;
                return;
            }}

            cardArea.style.display = 'block';
            finishCard.style.display = 'none';

            const item = currentDeck[currentDeckIndex];

            if (currentMode === 'roots') {{
                // Root Mode UI Setup
                document.getElementById('cardModeIndicator').innerText = '🧩 词根词缀专区';
                document.getElementById('cardTag').innerText = `词根 #${{currentDeckIndex + 1}}`;
                document.getElementById('ebbinghausBadge').innerText = item.type;
                
                document.getElementById('cardWord').innerText = item.affix;
                document.getElementById('cardIpa').innerText = item.meaning;
                document.getElementById('frontSentenceLabel').innerText = '💡 词根拆解逻辑';
                document.getElementById('frontSentence').innerText = item.explanation;

                document.getElementById('backWord').innerText = item.affix;
                document.getElementById('backIpa').innerText = `[${{item.type}}]`;
                document.getElementById('backMeaning').innerText = item.meaning;

                document.getElementById('box1Title').innerText = '💡 词根功能解析';
                document.getElementById('backEtymology').innerText = item.explanation;

                document.getElementById('box2Title').innerText = '📚 涵盖核心自考词汇';
                document.getElementById('box2AudioTag').innerText = '';
                document.getElementById('backPhrase').innerText = item.examples;

                document.getElementById('box3Title').innerText = '🌟 词根演变要领';
                document.getElementById('box3AudioTag').innerText = '';
                document.getElementById('backSentence').innerText = `熟记前缀/后缀 ${{item.affix}} 可以批量死磕数十个相关同源派生词汇！`;
                document.getElementById('backTranslation').innerText = '';

                document.getElementById('btnMarkWrong').innerText = '❌ 没记住';
                document.getElementById('btnMarkRight').innerText = '✅ 掌握词根';

            }} else {{
                // Standard Word Mode UI Setup
                const modeText = currentMode === 'daily' ? '今日任务' : (currentMode === 'unlearned' ? '生词本' : '全量词库');
                document.getElementById('cardModeIndicator').innerText = modeText;
                document.getElementById('cardTag').innerText = `#${{currentDeckIndex + 1}} (${{item.word}})`;
                
                const badgeEl = document.getElementById('ebbinghausBadge');
                if (item._isReview) {{
                    badgeEl.innerText = `🔄 艾宾浩斯 (第${{item._ebbStage + 1}}阶段)`;
                }} else {{
                    badgeEl.innerText = `🌟 今日新词`;
                }}

                document.getElementById('cardWord').innerText = item.word;
                document.getElementById('cardIpa').innerText = item.ipa;
                document.getElementById('frontSentenceLabel').innerText = '💬 英文例句语境';
                document.getElementById('frontSentence').innerText = item.sentence;
                
                document.getElementById('backWord').innerText = item.word;
                document.getElementById('backIpa').innerText = item.ipa;
                document.getElementById('backMeaning').innerText = item.meaning;

                document.getElementById('box1Title').innerText = '🧩 词根演变拆解';
                document.getElementById('backEtymology').innerText = item.etymology;

                document.getElementById('box2Title').innerText = '📌 高频短语 (点击读短语)';
                document.getElementById('box2AudioTag').innerText = '🔊 读短语';
                document.getElementById('backPhrase').innerText = `${{item.phrase}} ｜ ${{item.phonics}}`;

                document.getElementById('box3Title').innerText = '💬 例句翻译 (点击听例句)';
                document.getElementById('box3AudioTag').innerText = '🔊 点击听句';
                document.getElementById('backSentence').innerText = item.sentence;
                document.getElementById('backTranslation').innerText = item.translation;

                document.getElementById('btnMarkWrong').innerText = '❌ 没记住';
                document.getElementById('btnMarkRight').innerText = '✅ 记住啦';
            }}

            document.getElementById('currentIndex').innerText = currentDeckIndex + 1;
            document.getElementById('totalIndex').innerText = currentDeck.length;

            const progressPct = ((currentDeckIndex + 1) / currentDeck.length) * 100;
            document.getElementById('progressFill').style.width = progressPct + '%';

            if (isFlipped) {{
                isFlipped = false;
                cardEl.classList.remove('flipped');
            }}

            if (autoSpeak && currentMode !== 'roots') {{
                speakWord();
            }}
        }}

        function toggleFlip() {{
            isFlipped = !isFlipped;
            const cardEl = document.getElementById('flashcard');
            if (isFlipped) cardEl.classList.add('flipped');
            else cardEl.classList.remove('flipped');
        }}

        function speakText(text) {{
            const cleanText = text.replace(/['"']/g, '').trim();
            if (!cleanText) return;

            const isChineseMobileBrowser = /MiuiBrowser|HuaweiBrowser|MicroMessenger|SogouMobileBrowser|UCBrowser/i.test(navigator.userAgent);

            if (!isChineseMobileBrowser && 'speechSynthesis' in window) {{
                try {{
                    window.speechSynthesis.cancel();
                    const u = new SpeechSynthesisUtterance(cleanText);
                    u.lang = 'en-US';
                    u.rate = speechSpeed;
                    const v = getSelectedVoiceObj();
                    if (v) u.voice = v;
                    
                    let spoken = false;
                    u.onstart = function() {{ spoken = true; }};
                    u.onend = function() {{ spoken = true; }};
                    
                    window.speechSynthesis.speak(u);

                    setTimeout(() => {{
                        if (!spoken) {{
                            playUniversalAudio(cleanText);
                        }}
                    }}, 450);
                    return;
                }} catch(e) {{
                    console.log('WebSpeech fallback triggered');
                }}
            }}

            playUniversalAudio(cleanText);
        }}

        function playUniversalAudio(text) {{
            const cleanText = text.replace(/['"']/g, '').trim();
            if (!cleanText) return;

            const audioPlayer = document.getElementById('universalAudioPlayer');
            
            const primaryUrl = `https://fanyi.baidu.com/gettts?lan=en&text=${{encodeURIComponent(cleanText)}}&spd=3&source=web`;
            const secondaryUrl = `https://dict.youdao.com/dictvoice?audio=${{encodeURIComponent(cleanText.slice(0, 30))}}&type=2`;

            audioPlayer.src = primaryUrl;
            audioPlayer.load();
            audioPlayer.playbackRate = speechSpeed;

            const playPromise = audioPlayer.play();
            if (playPromise !== undefined) {{
                playPromise.then(() => {{
                    audioPlayer.playbackRate = speechSpeed;
                }}).catch(err => {{
                    console.log('Primary audio blocked, switching to secondary audio source:', err);
                    audioPlayer.src = secondaryUrl;
                    audioPlayer.load();
                    audioPlayer.playbackRate = speechSpeed;
                    audioPlayer.play().then(() => {{
                        audioPlayer.playbackRate = speechSpeed;
                    }}).catch(e => console.log('Secondary audio error:', e));
                }});
            }}
        }}

        function speakWord() {{
            if (currentMode === 'roots') return;
            if (currentDeck.length === 0 || currentDeckIndex >= currentDeck.length) return;
            speakText(currentDeck[currentDeckIndex].word);
        }}

        function speakPhrase() {{
            if (currentMode === 'roots') return;
            if (currentDeck.length === 0 || currentDeckIndex >= currentDeck.length) return;
            const phrase = currentDeck[currentDeckIndex].phrase;
            const match = phrase.match(/^[a-zA-Z\s'-]+/);
            const engPhrase = match ? match[0].trim() : phrase;
            speakText(engPhrase);
        }}

        function speakSentence() {{
            if (currentMode === 'roots') return;
            if (currentDeck.length === 0 || currentDeckIndex >= currentDeck.length) return;
            speakText(currentDeck[currentDeckIndex].sentence);
        }}

        function markResult(know) {{
            if (currentMode === 'roots') {{
                currentDeckIndex++;
                renderCard(false);
                return;
            }}

            const item = currentDeck[currentDeckIndex];
            const today = getTodayStr();

            memoryState[item.word] = know;
            localStorage.setItem('zk_memory_full_state', JSON.stringify(memoryState));
            
            let currEbb = ebbState[item.word] || {{ stage: 0, lastReview: today, nextReview: today }};
            
            if (know) {{
                const newStage = Math.min(currEbb.stage + 1, EBBINGHAUS_INTERVALS.length);
                const nextDays = EBBINGHAUS_INTERVALS[Math.min(newStage - 1, EBBINGHAUS_INTERVALS.length - 1)];
                const nextDate = addDays(today, nextDays);
                
                ebbState[item.word] = {{
                    stage: newStage,
                    lastReview: today,
                    nextReview: nextDate
                }};
            }} else {{
                ebbState[item.word] = {{
                    stage: 1,
                    lastReview: today,
                    nextReview: addDays(today, 1)
                }};
            }}

            localStorage.setItem('zk_ebbinghaus_state', JSON.stringify(ebbState));
            updateCounts();

            currentDeckIndex++;
            renderCard(true);
        }}

        function continueExtraDeck() {{
            currentDeckIndex = 0;
            buildDeck();
            showListView();
        }}

        document.addEventListener('keydown', (e) => {{
            if (viewState === 'card') {{
                if (e.key === ' ' || e.key === 'Enter') {{
                    toggleFlip();
                }} else if (e.key === 'ArrowLeft') {{
                    markResult(false);
                }} else if (e.key === 'ArrowRight') {{
                    markResult(true);
                }} else if (e.key === 's' || e.key === 'S') {{
                    speakWord();
                }}
            }}
        }});

        window.onload = init;
    </script>
</body>
</html>
"""

html_out_path = r'd:\User\Documents\自考英语\自考英语核心词汇_全功能互动闪卡.html'
with open(html_out_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

# Also update index.html
with open(r'd:\User\Documents\自考英语\index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Successfully compiled version {version_str} with Prefix-First Search, Simplified Tabs, and Dedicated Root/Suffix Card Deck!")
