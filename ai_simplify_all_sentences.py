# -*- coding: utf-8 -*-
"""
AI 极简助记例句全量重构脚本
规则：
1. 废除所有带 ... 的截断碎片句。
2. 废除所有包含生僻词 (如 immaculate, obscene, pike, stalking) 的复杂例句。
3. 替换为 4 - 8 个简单单词构成的极简高频助记例句 + 准确中文翻译。
"""

import json
import re

AI_SIMPLE_SENTENCES = {
    "instead": ("Let's walk instead of driving.", "我们走路去，而不是开车。"),
    "institute": ("He works at a research institute.", "他在一家研究所工作。"),
    "interest": ("Music is my main interest.", "音乐是我的主要兴趣。"),
    "invite": ("She invited me to her party.", "她邀请我参加她的聚会。"),
    "island": ("They live on a small island.", "他们生活在一个小岛上。"),
    "item": ("This is a very important item.", "这是一件非常重要的物品。"),
    "joke": ("He told a funny joke.", "他讲了一个幽默的笑话。"),
    "journal": ("She writes in her journal every day.", "她每天在日志里写东西。"),
    "kick": ("He kicked the ball into the net.", "他把球踢进了网里。"),
    "kitchen": ("Mom is cooking in the kitchen.", "妈妈正在厨房做饭。"),
    "lake": ("They go fishing in the lake.", "他们去湖里钓鱼。"),
    "large": ("They live in a large house.", "他们住在一间大房子里。"),
    "law": ("Everyone must follow the law.", "每个人都必须遵守法律。"),
    "learned": ("She learned a lot from her teacher.", "她从老师那里学到了很多。"),
    "leave": ("Please do not leave me alone.", "请不要留下我一个人。"),
    "life": ("Enjoy your happy life every day.", "享受你每一天的快乐生活。"),
    "light": ("Turn on the light, please.", "请把灯打开。"),
    "lion": ("The lion is the king of animals.", "狮子是百兽之王。"),
    "list": ("Make a list of words to remember.", "列一张要记住的单词清单。"),
    "local": ("We love buying local food.", "我们喜欢买当地的食物。"),
    "look": ("Look at the blue sky.", "看那蔚蓝的天空。"),
    "lose": ("Do not lose your confidence.", "不要失去你的信心。"),
    "loudly": ("Do not speak loudly in public.", "不要在公共场所大声说话。"),
    "lovely": ("What a lovely day today!", "今天真是美好的一天！"),
    "low": ("The sun is low in the sky.", "太阳在天空低处。"),
    "abandon": ("Never abandon your dream.", "永远不要放弃你的梦想。"),
    "ability": ("She has the ability to succeed.", "她有成功的能力。"),
    "absent": ("He was absent from school today.", "他今天上学缺席了。"),
    "absorb": ("Dry paper can absorb water quickly.", "干纸能快速吸水。"),
    "abstract": ("Art can be simple or abstract.", "艺术可以是简单的或抽象的。"),
    "abundant": ("The land has abundant water.", "这片土地有丰富的淡水。"),
    "academic": ("He has a strong academic background.", "他有很强的学术背景。"),
    "accelerate": ("Drive carefully and do not accelerate.", "小心驾驶，不要加速。"),
    "accent": ("She speaks with a strong accent.", "她说话带有一股很重的口音。"),
    "accept": ("I accept your kind offer.", "我接受你的好意。"),
    "access": ("Students have free access to the library.", "学生可以免费进入图书馆。"),
    "accident": ("Drive slow to avoid an accident.", "开慢点以避免发生事故。"),
    "accommodate": ("The hotel can accommodate 200 guests.", "这家酒店能容纳200位客人。"),
    "accompany": ("May I accompany you home?", "我可以陪你回家吗？"),
    "accomplish": ("We can accomplish our task on time.", "我们可以按时完成任务。"),
    "accord": ("They reached a peace accord.", "他们达成了和平协议。"),
    "account": ("I need to open a bank account.", "我需要开一个银行账户。"),
    "accumulate": ("We accumulate experience by working hard.", "我们通过努力工作积累经验。"),
    "accurate": ("His answer was accurate and clear.", "他的回答准确而清晰。"),
    "accuse": ("Do not accuse others without proof.", "没有证据不要指责他人。"),
    "achieve": ("Work hard to achieve your goal.", "努力工作来实现你的目标。"),
    "acknowledge": ("He acknowledged his mistake.", "他承认了自己的错误。"),
    "acquire": ("Read books to acquire knowledge.", "读书以获取知识。"),
    "across": ("Walk across the street carefully.", "小心穿过这条街道。"),
    "adapt": ("You will adapt to the new environment soon.", "你很快会适应新环境。"),
    "add": ("Add some sugar to the coffee.", "给咖啡加点糖。"),
    "addict": ("Do not become a phone addict.", "不要成为手机沉迷者。"),
    "addition": ("In addition, we need more time.", "此外，我们需要更多时间。"),
    "address": ("Write your name and address here.", "在这里写下你的姓名和地址。"),
    "adequate": ("Make sure you get adequate sleep.", "确保你有足够的睡眠。"),
    "adjust": ("Adjust the chair to fit your height.", "调节椅子以适应你的身高。"),
    "administration": ("She works in school administration.", "她在学校行政部门工作。"),
    "admire": ("I really admire your courage.", "我真的很钦佩你的勇气。"),
    "admit": ("He admitted that he was wrong.", "他承认了他错了。"),
    "adopt": ("They decided to adopt a puppy.", "他们决定收养一只小狗。"),
    "adult": ("An adult should act responsibly.", "成年人应该负责任地行事。"),
    "advance": ("Technology will advance rapidly.", "技术将会快速进步。"),
    "advantage": ("Good health is a big advantage.", "健康是极大的优势。"),
    "advertise": ("They advertise products on TV.", "他们在电视上登广告宣传产品。"),
    "advice": ("Thank you for your valuable advice.", "谢谢你宝贵的建议。"),
    "advocate": ("We advocate a healthy lifestyle.", "我们提倡健康的生活方式。"),
    "affair": ("Mind your own business and affairs.", "管好你自己的事情。"),
    "affect": ("Bad weather will affect our trip.", "坏天气会影响我们的旅行。"),
    "afford": ("I cannot afford such a expensive car.", "我买不起这么贵的车。"),
    "afraid": ("Do not be afraid of making mistakes.", "不要害怕犯错误。"),
    "afternoon": ("See you tomorrow afternoon.", "明天下午见。"),
    "agency": ("She works for a travel agency.", "她在一家旅行社工作。"),
    "agenda": ("What is on the meeting agenda today?", "今天会议的议程是什么？"),
    "agent": ("He is a real estate agent.", "他是一名房地产中介代理人。"),
    "aggressive": ("Keep away from aggressive dogs.", "远离有攻击性的狗。"),
    "agree": ("I completely agree with you.", "我完全同意你的看法。"),
    "agriculture": ("Agriculture is vital for feeding people.", "农业对养活人口至关重要。"),
    "aid": ("They sent medical aid to the area.", "他们向该地区提供了医疗援助。"),
    "aim": ("Aim high and work hard.", "目标远大，努力奋斗。"),
    "alarm": ("Set an alarm for 6 o'clock.", "设定一个6点的闹钟。"),
    "alcohol": ("Do not drive after drinking alcohol.", "饮酒后切勿驾车。"),
    "alert": ("Stay alert while walking at night.", "夜间行走请保持警惕。"),
    "alien": ("It feels like an alien world.", "这感觉像是一个异域世界。"),
    "alike": ("The two sisters look very alike.", "这两姐妹看起来非常相似。"),
    "alive": ("Keep your hope and dream alive.", "让你的希望与梦想保持生机。"),
    "allow": ("Smoking is not allowed here.", "这里禁止吸烟。"),
    "ally": ("They are strong allies in trade.", "他们是贸易上的强力盟友。"),
    "almost": ("It is almost time to start.", "几乎到了开始的时间。"),
    "alone": ("He likes to travel alone.", "他喜欢独自一个人旅行。"),
    "already": ("I have already finished my work.", "我已经完成了我的工作。"),
    "alter": ("You cannot alter the past.", "你无法改变过去。"),
    "alternative": ("We have no other alternative.", "我们没有别的选择。"),
    "always": ("Always keep a warm smile.", "始终保持温暖的微笑。"),
    "amaze": ("Her beautiful singing will amaze you.", "她美妙的歌声会让你惊叹。"),
    "ambition": ("His ambition is to be a doctor.", "他的雄心是成为一名医生。"),
    "ambulance": ("Call an ambulance immediately!", "立刻叫救护车！"),
    "amend": ("We must amend this old rule.", "我们必须修改这条旧规则。"),
    "amount": ("A large amount of work remains.", "仍有大量工作要做。"),
    "analyze": ("We need to analyze the data carefully.", "我们需要仔细分析数据。"),
    "ancestor": ("Our ancestors lived in harmony with nature.", "我们的祖先与自然和谐共处。"),
    "anchor": ("Drop the anchor in the bay.", "在海湾里抛锚。"),
    "ancient": ("Rome is an ancient city with long history.", "罗马是一座历史悠久的古城。"),
    "anger": ("Control your anger and stay calm.", "控制你的愤怒，保持冷静。"),
    "angle": ("Look at the problem from a new angle.", "从全新的角度看问题。"),
    "angry": ("Do not get angry over small things.", "不要为小事发怒。"),
    "animal": ("Dogs are very loyal animals.", "狗是非常忠诚的动物。"),
    "anniversary": ("Happy wedding anniversary!", "结婚纪念日快乐！"),
    "announce": ("They will announce the winner soon.", "他们很快会宣布获胜者。"),
    "annoy": ("Loud noise will annoy the neighbors.", "噪音会打扰邻居。"),
    "annual": ("We hold an annual company party.", "我们举办一年一度的公司晚会。"),
    "anxious": ("She felt anxious about the exam.", "她对考试感到焦虑。"),
    "apologize": ("You should apologize for being late.", "你应当为迟到道歉。"),
    "apparent": ("The cause of problem is apparent.", "问题的成因是很显而易见的。"),
    "appeal": ("Bright colors appeal to children.", "鲜艳的颜色对儿童很有吸引力。"),
    "appear": ("Stars appear in the sky at night.", "夜幕降临时星星出现在天空。"),
    "appetite": ("Exercise gives you a good appetite.", "运动会给你带来好食欲。"),
    "applaud": ("The audience began to applaud loudly.", "观众开始热烈鼓掌。"),
    "application": ("Fill out the job application form.", "填写求职申请表。"),
    "apply": ("Apply the medicine to the skin.", "把药物涂抹在皮肤上。"),
    "appoint": ("They appoint him as team leader.", "他们任命他为团队负责人。"),
    "appreciate": ("I really appreciate your kind help.", "非常感谢你的热心帮助。"),
    "approach": ("A train is approaching the station.", "一列火车正驶近车站。"),
    "appropriate": ("Wear appropriate clothes for the interview.", "面试时穿合适的衣服。"),
    "approval": ("The plan won official approval.", "该计划赢得了官方批准。"),
    "approve": ("My parents approve of my choice.", "我父母赞成我的选择。"),
    "approximate": ("The approximate distance is five miles.", "大约的距离是5英里。"),
    "architecture": ("I love modern city architecture.", "我喜欢现代城市建筑。"),
    "area": ("This area is very quiet and safe.", "这个区域非常安静安全。"),
    "argue": ("Do not argue over silly things.", "不要为无聊的小事争吵。"),
    "arise": ("Problems will arise if we rush.", "如果我们仓促行事就会产生问题。"),
    "army": ("He joined the army last year.", "他去年参军了。"),
    "around": ("We walked around the lake.", "我们绕着湖散步。"),
    "arrange": ("Please arrange a meeting for tomorrow.", "请安排明天的会议。"),
    "arrest": ("Police arrest the dangerous thief.", "警察逮捕了危险的贼。"),
    "arrive": ("What time will the flight arrive?", "航班几点到达？"),
    "arrow": ("The arrow hit the bullseye.", "箭射中了正中靶心。"),
    "article": ("Read this interesting news article.", "读读这篇有趣的新闻文章。"),
    "artificial": ("This flower is made of artificial silk.", "这朵花是用人造丝做的。"),
    "artist": ("She is a famous piano artist.", "她是一位著名的钢琴艺术家。"),
    "ashamed": ("Do not feel ashamed to ask help.", "不要觉得寻求帮助是可耻的。"),
    "aside": ("Put your worries aside and sleep.", "把你的烦恼抛在一边去睡觉吧。"),
    "ask": ("Feel free to ask any question.", "随时提出任何问题。"),
    "asleep": ("The baby is fast asleep in bed.", "宝宝在床上熟睡着。"),
    "aspect": ("Consider every aspect of the plan.", "考虑计划的方方面面。"),
    "assemble": ("We assemble the wooden desk together.", "我们一起组装这张木桌。"),
    "assess": ("We need to assess the total cost.", "我们需要评估总成本。"),
    "asset": ("Health is your most valuable asset.", "健康是你最宝贵的资产。"),
    "assign": ("The teacher will assign homework.", "老师会布置作业。"),
    "assist": ("I am happy to assist you.", "我很乐意协助你。"),
    "associate": ("People associate summer with ice cream.", "人们把夏天与冰淇淋联系在一起。"),
    "assume": ("Do not assume everything is easy.", "不要假定一切都很简单。"),
    "assure": ("I assure you that everything is fine.", "我向你保证一切都很好。"),
    "astonish": ("His amazing magic will astonish you.", "他神奇的魔术会让惊讶。"),
    "athlete": ("He is a fast running athlete.", "他是一位快速奔跑的运动员。"),
    "atmosphere": ("The cafe has a cozy atmosphere.", "这家咖啡馆有温馨的氛围。"),
    "attach": ("Attach a photo to your resume.", "在简历上附上一张照片。"),
    "attack": ("Lions attack their prey in team.", "狮子团队合作攻击猎物。"),
    "attain": ("She worked hard to attain success.", "她努力工作以取得成功。"),
    "attempt": ("Make an attempt to try new things.", "尝试去尝试新鲜事物。"),
    "attend": ("I will attend the meeting on time.", "我会按时参加会议。"),
    "attention": ("Pay attention to your health.", "注意你的健康。"),
    "attitude": ("A positive attitude brings good luck.", "积极的态度会带来好运。"),
    "attract": ("Flowers attract bees and butterflies.", "鲜花吸引蜜蜂和蝴蝶。"),
    "attribute": ("Patience is an important attribute.", "耐心是一项重要的品质。"),
    "auction": ("They sold the art at an auction.", "他们在拍卖会上卖出了艺术品。"),
    "audience": ("The audience loved the musical show.", "观众喜欢这场音乐表演。"),
    "author": ("Who is the author of this book?", "这本书的作者是谁？"),
    "authority": ("He is an authority on science.", "他是科学领域的权威。"),
    "auto": ("Drive an auto along the highway.", "沿着高速公路开汽车。"),
    "automatic": ("The automatic door opens quickly.", "这扇自动门开得很快。"),
    "available": ("Fresh fruit is available all year.", "新鲜水果全年都有供应。"),
    "avenue": ("Trees line both sides of the avenue.", "大道两侧绿树成荫。"),
    "average": ("His test score is above average.", "他的考试成绩高于平均水平。"),
    "avoid": ("Wear a mask to avoid catching cold.", "戴口罩以避免感冒。"),
    "await": ("Good news awaits you soon.", "好消息很快在等待着你。"),
    "awake": ("I stay awake until midnight.", "我保持清醒直到深夜。"),
    "award": ("She won the first place award.", "她赢得了第一名奖项。"),
    "aware": ("Be aware of traffic rules.", "意识到并遵守交通规则。"),
    "away": ("Stay away from dangerous places.", "远离危险的地方。"),
    "awful": ("The taste of bitter medicine is awful.", "苦药的味道太糟糕了。"),
    "awkward": ("There was an awkward silence in room.", "房间里出现了尴尬的沉默。"),
}

def clean_sentence_and_translation(word, sentence, translation, meaning):
    if word.lower() in AI_SIMPLE_SENTENCES:
        return AI_SIMPLE_SENTENCES[word.lower()]

    s = sentence.replace('...', '').strip()
    t = translation.replace('...', '').replace('…', '').strip()

    words = s.split()

    if len(words) > 9 or not s.endswith(('.', '!', '?')) or not s[0].isupper() or '...' in sentence:
        clean_m = re.sub(r'^[a-z]+\.\s*', '', meaning).split(';')[0].split(',')[0].split('；')[0].strip()
        w = word.strip()
        
        # Build clean 4-6 word natural sentence
        if w.endswith('ly'):
            s = f"She spoke very {w}."
            t = f"她说话非常{clean_m}。"
        elif w.endswith('ed'):
            s = f"They {w} together yesterday."
            t = f"他们昨天一起{clean_m}。"
        elif w.endswith('ing'):
            s = f"He is {w} now."
            t = f"他现在正在{clean_m}。"
        elif w.endswith('tion') or w.endswith('ment') or w.endswith('ness'):
            s = f"Health is a great {w}."
            t = f"健康是一种伟大的{clean_m}。"
        else:
            s = f"This is a useful {w}."
            t = f"这是一个实用的{clean_m}。"

    return s, t

def main():
    with open('target_words_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for item in data:
        w = item['word']
        orig_s = item.get('sentence', '')
        orig_t = item.get('translation', '')
        meaning = item.get('meaning', '')

        new_s, new_t = clean_sentence_and_translation(w, orig_s, orig_t, meaning)

        if new_s != orig_s or new_t != orig_t:
            item['sentence'] = new_s
            item['translation'] = new_t
            updated_count += 1

    with open('target_words_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated_count} sentences in target_words_data.json!")

if __name__ == '__main__':
    main()
