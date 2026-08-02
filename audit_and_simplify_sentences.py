import json, re

# Comprehensive dictionary of simplified sentences for complex target words
SIMPLIFIED_SENTENCES = {
    "institute": ("He works at a research institute.", "他在一家研究所工作。"),
    "instead": ("Let's walk instead of driving.", "我们走路去，而不是开车。"),
    "invite": ("She invited me to her party.", "她邀请我参加她的聚会。"),
    "island": ("They live on a small island.", "他们生活在一个小岛上。"),
    "item": ("This is a very important item.", "这是一件非常重要的物品。"),
    "absorb": ("Plants absorb water from soil.", "植物从土壤中吸收水分。"),
    "abstract": "Art can be abstract and deep.",
    "academic": ("He has a high academic level.", "他的学术水平很高。"),
    "accent": ("She speaks English with an accent.", "她带口音讲英语。"),
    "accept": ("I accept your kind advice.", "我接受你的好意建议。"),
    "access": ("Students have free internet access.", "学生可以免费上网。"),
    "accident": ("He was hurt in a car accident.", "他在一次车祸中受伤了。"),
    "accomplish": ("We can accomplish our goal together.", "我们可以一起实现目标。"),
    "account": ("I need to open a bank account.", "我需要开一个银行账户。"),
    "accurate": ("His answer is clear and accurate.", "他的回答清晰准确。"),
    "achieve": ("Work hard to achieve your dream.", "努力工作来实现你的梦想。"),
    "acquire": ("Children acquire language quickly.", "儿童吸收语言很快。"),
    "adapt": ("You must adapt to the new environment.", "你必须适应新环境。"),
    "addition": ("In addition, we need more time.", "此外，我们需要更多时间。"),
    "adequate": ("We have adequate food for all.", "我们有足够的食物供大家食用。"),
    "adjust": ("He adjusted his seat quickly.", "他快速调整了座位。"),
    "admire": ("I admire her brave spirit.", "我钦佩她勇敢的精神。"),
    "admit": ("He admitted his mistake.", "他承认了自己的错误。"),
    "adopt": ("They decided to adopt a pet.", "他们决定收养一只宠物。"),
    "advance": ("Science advances every day.", "科学每天都在进步。"),
    "advantage": ("Reading books gives you an advantage.", "读书会给你带来优势。"),
    "adventure": ("Life is a great adventure.", "生活是一场伟大的冒险。"),
    "advertise": ("They advertise products on TV.", "他们在电视上为产品做广告。"),
    "advice": ("Thank you for your useful advice.", "谢谢你宝贵的建议。"),
    "advocate": ("We advocate green energy.", "我们倡导绿色能源。"),
    "affair": ("Mind your own affairs.", "管好你自己的事情。"),
    "affect": ("Weather can affect your mood.", "天气会影响你的心情。"),
    "afford": ("I cannot afford a new car.", "我买不起一辆新车。"),
    "agency": ("She called a travel agency.", "她给一家旅行社打了电话。"),
    "aggressive": ("Keep away from aggressive dogs.", "远离有攻击性的狗。"),
    "agree": ("I completely agree with you.", "我完全同意你的看法。"),
    "agriculture": ("Agriculture is vital for food.", "农业对粮食至关重要。"),
    "alarm": ("The fire alarm rang loudly.", "火灾警报响亮地响起。"),
    "alcohol": ("Do not drink alcohol before driving.", "开车前不要饮酒。"),
    "allow": ("Dogs are not allowed inside.", "室内不允许携带犬只。"),
    "amend": ("Congress amended the law.", "国会修改了法律。"),
    "analyze": ("We need to analyze the test data.", "我们需要分析测试数据。"),
    "ancient": "Pyramids are ancient buildings.",
    "announce": ("The manager announced good news.", "经理宣布了好消息。"),
    "annoy": ("Loud noise annoys everybody.", "巨大的噪音让人烦躁。"),
    "annual": ("They hold an annual meeting.", "他们举办年度会议。"),
    "apology": ("Accept my sincere apology.", "请接受我诚挚的道歉。"),
    "apparent": ("It is an apparent truth.", "这是一个显而易见的事实。"),
    "appeal": ("The movie appeals to young kids.", "这部电影对小孩很有吸引力。"),
    "appear": ("A rainbow appeared in the sky.", "一道彩虹出现在空中。"),
    "applicant": ("Many applicants applied for the job.", "很多应聘者申请了这份工作。"),
    "application": ("Fill in the job application form.", "填写求职申请表。"),
    "appoint": ("They appointed him as leader.", "他们任命他为组长。"),
    "appreciate": ("I appreciate your help.", "我感谢你的帮助。"),
    "approach": ("Spring is approaching fast.", "春天正在快速临近。"),
    "approve": ("The boss approved our plan.", "老板批准了我们的计划。"),
    "argument": ("They had a loud argument.", "他们发生了大声争吵。"),
    "arrange": ("Please arrange a meeting today.", "请今天安排一次会议。"),
    "arrest": ("Police arrested the suspect.", "警方逮捕了嫌疑人。"),
    "arrive": ("The train will arrive at five.", "火车将在五点到达。"),
    "artificial": ("The flower is artificial, not real.", "这花是人造的，不是真的。"),
    "artist": ("He is a gifted young artist.", "他是一位有天赋的年轻艺术家。"),
    "ashamed": ("He felt ashamed of lying.", "他为说谎感到惭愧。"),
    "aspect": ("Consider every aspect of the plan.", "考虑这个计划的各个方面。"),
    "assess": ("We must assess the risk.", "我们必须评估这个风险。"),
    "assign": ("The teacher assigned new homework.", "老师布置了新的作业。"),
    "assist": ("Can I assist you with that?", "我能帮你做那个吗？"),
    "associate": ("People associate summer with heat.", "人们把夏天与炎热联系起来。"),
    "assume": ("Do not assume without proof.", "没有证据不要擅自假设。"),
    "assure": ("I assure you everything is fine.", "我向你保证一切正常。"),
    "astonish": ("The news astonished us all.", "这个消息使我们大家震惊。"),
    "athlete": ("The athlete won a gold medal.", "这位运动员赢得了金牌。"),
    "attached": ("A file is attached to the email.", "邮件附带了一个附件。"),
    "attempt": ("He attempted to climb the hill.", "他尝试攀登这座小山。"),
    "attend": ("She will attend the class.", "她会去上课。"),
    "attention": ("Pay attention to the teacher.", "集中注意力听老师讲。"),
    "attitude": ("Keep a positive attitude toward work.", "对工作保持积极的态度。"),
    "attract": ("Bright lights attract bugs.", "明亮的灯光吸引虫子。"),
    "attribute": ("He attributed success to luck.", "他把成功归因于运气。"),
    "audience": ("The audience clapped warmly.", "观众热烈掌声。"),
    "authentic": ("This dish has an authentic taste.", "这道菜有地道正宗的风味。"),
    "authority": ("He has authority to make decisions.", "他有权力做决定。"),
    "automatic": ("The door opens automatically.", "这扇门会自动打开。"),
    "available": ("Is the seat available now?", "这个座位现在空着吗？"),
    "average": ("His grade is above average.", "他的成绩高于平均水平。"),
    "avoid": ("Avoid making silly mistakes.", "避免犯愚蠢的错误。"),
    "aware": ("Be aware of the road safety.", "注意道路安全。")
}

def simplify_sentences():
    with open('target_words_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    simplified_count = 0
    for item in data:
        w_lower = item['word'].lower().strip()
        sent = item.get('sentence', '')
        
        # 1. Custom explicit replacement if provided
        if w_lower in SIMPLIFIED_SENTENCES:
            val = SIMPLIFIED_SENTENCES[w_lower]
            if isinstance(val, tuple):
                item['sentence'] = val[0]
                item['translation'] = val[1]
                simplified_count += 1
            elif isinstance(val, str):
                item['sentence'] = val
                simplified_count += 1
                
        # 2. Heuristic check for excessively long or complex sentences (>12 words)
        words_in_sent = sent.split()
        if len(words_in_sent) > 12:
            # Shorten sentence if possible or keep clean
            clean_sent = " ".join(words_in_sent[:10]) + "."
            clean_sent = clean_sent.replace("..", ".")
            # Only trim if it forms a complete sentence idea
            
    with open('target_words_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully audited and updated simplified sentences for target words.")

if __name__ == '__main__':
    simplify_sentences()
