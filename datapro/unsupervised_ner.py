# coding:utf-8

import jieba
import jieba.analyse
import jieba.posseg
import paddlehub as hub
from keybert import KeyBERT
import pke
import os
import csv

c_root = os.getcwd() + os.sep + "sourcedata" + os.sep
#csv_name = 'data.csv'

methods = ['TFIDF', 'textrank', 'LDA'
    #, 'keybert'
    , "TextRank", "PositionRank", "SingleRank", "TopicRank", 'MultipartiteRank'
    ]


def read_data(name):
    global lda_news,model,extractor
    wordcount = 40
    csv_name = 'data_'+name+'.csv'
    if name == 'LDA':
        lda_news = hub.Module(name="lda_news")
    elif name == 'keybert':
        model = KeyBERT('bert-base-chinese')
    elif name == 'TextRank':
        extractor = pke.unsupervised.TextRank()
    elif name == 'PositionRank':
        extractor = pke.unsupervised.PositionRank()
    elif name == 'SingleRank':
        extractor = pke.unsupervised.SingleRank()
    elif name == 'TopicRank':
        extractor = pke.unsupervised.TopicRank()
    elif name == 'MultipartiteRank':
        extractor = pke.unsupervised.MultipartiteRank()
    with open(csv_name, 'a', encoding='utf-8') as csv_open:
        csv_w = csv.writer(csv_open)

        for file in os.listdir(c_root):
            with open(c_root+file, 'r', encoding='utf-8') as f:
                texts = f.read()
                texts = texts.replace(' ', '')
                texts = texts.replace('\n', '')
                texts = texts.replace('\t', '。')
                texts = texts.replace('{', '')
                texts = texts.replace('}', '')
                texts = texts.strip()
                if name == 'TFIDF':
                    ans = jieba.analyse.extract_tags(texts, topK=wordcount, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nt'))
                elif name == 'textrank':
                    ans = jieba.analyse.textrank(texts, topK=wordcount, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nt'))
                elif name == 'LDA':
                    ans = lda_news.cal_doc_keywords_similarity(texts)
                elif name == 'keybert':
                    doc = " ".join(jieba.cut(texts))
                    ans = model.extract_keywords(doc, keyphrase_ngram_range=(1,1),  top_n=wordcount)
                elif name == 'TextRank':
                    extractor.load_document(input=texts, language='zh', normalization ='none')
                    extractor.candidate_selection()
                    extractor.candidate_weighting()
                    ans = extractor.get_n_best(n=wordcount)
                csv_w.writerow((texts, ans))


def add_entity(dict_path):
    """
    把实体字典加载到jieba里，
    实体作为分词后的词，
    实体标记作为词性
    """

    dics = csv.reader(open(dict_path, 'r', encoding='gbk'))

    for row in dics:

        if len(row) == 2:
            jieba.add_word(row[0].strip(), tag=row[1].strip())

            """ 保证由多个词组成的实体词，不被切分开 """
            jieba.suggest_freq(row[0].strip())

dict_path = "dict_label.csv"
add_entity(dict_path)
for meth in methods:
    read_data(meth)


# @process_txt
# def TFIDF():
#     words = jieba.analyse.extract_tags(text, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nt'))
#     return words


#def textrank():
    #jieba.analyse.textrank(text, topK=20, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nt'))



# def LDA():
#     text = "美国总统拜登当地时间26日又语出惊人。据路透社报道，拜登当天在波兰的演 讲中，称俄罗斯总统普京“不能继续掌权了”。白宫官员随后出来解释，克里姆林宫同日 也作出回应，称“这不是由拜登决定的”。报道称，在华沙皇家城堡发表的讲话中，拜登在谴责普京后表示“看在上帝的份上，这个人不能继续掌权了”。对此，路透社表示，该言论引发了华盛顿方面对局势升级的担忧，美国一直避免直接对乌克兰进行军事干预，并明确表示不支持政权更迭。随后，一名白宫官员对拜登这番话进行解释，称拜登的言论并不代表华盛顿政策的转变，其目的是让世界为乌克兰问题上的长期冲突做好准备。该官员称，拜登意为“不能 允许普京对其邻国或该地区行使权力”，而不是在讨论普京在俄罗斯的权力或俄 罗斯的政权 更迭问题。同日，路透社称，被问及拜登这一言论时，俄罗斯总统新闻秘书佩斯科夫作出回应，称“这不是由拜登决定的。俄罗斯总统是由俄罗斯人选举产生的”。此前 ，俄罗斯安全会议副主席梅德韦杰夫接受俄媒采访时曾表示，俄特别军事行动既定目标包括实现乌克兰去军事化、去纳粹化、成为中立国家、不奉行反俄政策。俄开展特别军事行动首先是因为其设定的目标未能通过外交方式实现。他表示，社会调查显示，四分之三的俄罗斯民众支持在乌开展特别军事行动。西方国家企图通过制裁影响俄民众，煽动他们反对政府，结果适得其反。"
#     extractor = pke.unsupervised.TextRank()
#     extractor.load_document(input=text, language='zh', normalization ='none')
#     extractor.candidate_selection()
#     extractor.candidate_weighting()
#     ans = extractor.get_n_best(n=20)
#     print(ans)
#
# LDA()




