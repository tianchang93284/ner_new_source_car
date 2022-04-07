#encoding=utf8
import os,jieba,csv,random,re
import jieba.posseg as psg
from max_seg import PsegMax
import json


""" 新能源汽车 """
dict_path = "dict_label.csv"
psgMax = PsegMax(dict_path)

c_root = os.getcwd() + os.sep + "sourcedata" + os.sep

english2chineselabel = {
    'goverment':'政府',
    'tool':'工具',
    'goal':'目标',
    'consumer':'消费者',
    'cartype':'车型',
    'company':'企业',
    'society':'协会',
    'otherorganization':'其他机构',
    'technology':'技术',
    'link':'环节',
    'researchinstitutions':'科研院所'
}

chinese2englishlabel = {
    '政府':'goverment',
    '工具':'tool',
    '目标':'goal',
    '消费者':'consumer',
    '车型':'cartype',
    '企业':'company',
    '协会':'society',
    '其他机构':'otherorganization',
    '技术':'technology',
    '环节':'link',
    '科研院所':'researchinstitutions'
}

""" 实体类别 """
label = set(chinese2englishlabel.values()) #set(['goverment', 'tool', 'consumer', 'cartype', 'company', 'society', 'otherorganization', 'technology', 'link', 'researchinstitutions'])

""" 句子结尾符号，表示如果是句末，则换行 """
fuhao = set(['。','?','？','!','！',';'])

tihuan = ['\n','\t']

def add_entity(dict_path):
    """
    把实体字典加载到jieba里，
    实体作为分词后的词，
    实体标记作为词性
    """
    
    dics = csv.reader(open(dict_path,'r',encoding='gbk'))
    
    for row in dics:
        
        if len(row)==2:
            jieba.add_word(row[0].strip(),tag=row[1].strip())
            
            """ 保证由多个词组成的实体词，不被切分开 """
            jieba.suggest_freq(row[0].strip())
            

def split_dataset():
    """
    划分数据集，按照7:2:1的比例
    """
    
    file_all = []
    for file in os.listdir(c_root):
        if "txtoriginal.txt" in file:
            file_all.append(file)
            
    random.seed(10)       
    random.shuffle(file_all)
    
    num = len(file_all)
    train_files = file_all[: int(num * 0.7)]
    dev_files = file_all[int(num * 0.7):int(num * 0.9)]
    test_files = file_all[int(num * 0.9):]
    
    return train_files,dev_files,test_files
               

def sentence_seg(sentence,mode="jieba"):
    """
    1: 实体词典+jieba词性标注。mode="jieba"
    2: 实体词典+双向最大匹配。mode="max_seg"
    """
    
    if mode == "jieba": return psg.cut(sentence)
    if mode == "max_seg": return psgMax.max_biward_seg(sentence)


def auto_label(files, data_type, mode="jieba"):
    """
    不是实体，则标记为O，
    如果是句号等划分句子的符号，则再加换行符，
    是实体，则标记为BI。
    """
    
    writer = open("example.%s" % data_type,"w",encoding="utf8")
    
    for file in files:
        fp = open(c_root+file,'r',encoding='utf8')
        
        for line in fp:
            
            """ 按词性分词 """
            words = sentence_seg(line,mode)
            for word,pos in words: 
                word,pos = word.strip(), pos.strip()   
                if not (word and pos):
                    continue
                
                """ 如果词性不是实体的标记，则打上O标记 """
                if pos not in label:
                   
                    for char in word:
                        string = char + ' ' + 'O' + '\n'
                        
                        """ 在句子的结尾换行 """
                        if char in fuhao:
                            string += '\n'
                            
                        writer.write(string)
                        
                else:
                    
                    """ 如果词性是实体的标记，则打上BI标记"""   
                    begin = 0
                    for char in word:
                        
                        if begin == 0:
                            begin += 1
                            string = char + ' ' + 'B-' + pos + '\n'
                            
                        else:
                            string = char + ' ' + 'I-' + pos + '\n'
                            
                        writer.write(string)
                
    writer.close()

def auto_source_label():
    unmatchwords = [chr(ord(u'\u201e')), chr(ord(u'\uf8ff')),
                    chr(ord(u'\uf03d')), chr(ord(u'\uf06e')),
                    chr(ord(u'\u2022')),chr(ord(u'\u2003')),
                    chr(ord(u'\u2002')),chr(ord(u'\ue011')),
                    chr(ord(u'\ue010'))]
    with open('new_energy.json','a') as fjson:
        for file in os.listdir(c_root):
            print(file)
            with open(c_root+file, 'r', encoding='utf-8') as f:
                texts = f.read()
                texts = texts.replace(' ', '')
                texts = texts.replace('\n', '')
                texts = texts.replace('\t', '。')

                texts = re.split('。|？|；', texts)
                # 过滤掉空字符
                texts = list(filter(lambda x: len(x.strip()) != 0, texts))
                for text in texts:
                    words = sentence_seg(text, "max_seg")

                    words = list(filter(lambda x:x[1].strip() in label, words))
                    text_dict = {}
                    text_dict["text"] = text.strip()
                    label_dict = {}
                    unmatch = False
                    for unmatchword in unmatchwords:
                        if unmatchword in text:
                            unmatch = True

                    if unmatch:
                        continue
                    for word, pos in words:
                        word = word.strip()

                        if word:
                            label_dict[pos] = {word:[[text.find(word),text.find(word)+len(word)-1]]}
                    if label_dict:
                        text_dict['label'] = label_dict
                        json.dump(text_dict, fjson, ensure_ascii=False)
                        #json.dump('\r\n', fjson)


def split_josn_file():
    with open('new_energy_split.json', 'w') as f_spilt:
        with open('new_energy.json','r') as f:
            f_txt = f.readline()
            kuohao = []
            startpos = 0
            endpos = 0
            for s in f_txt:
                endpos += 1
                if s == '{':
                    kuohao.append(s)
                elif s == '}':
                    kuohao.pop()
                    if len(kuohao) == 0:
                        f_spilt.write(f_txt[startpos:endpos]+'\n')
                        startpos = endpos


def main():
    
    """ 1: 加载实体词和标记到jieba """
    add_entity(dict_path)
    
    """ 2: 划分数据集 """
    #trains, devs, tests = split_dataset()
    
    """ 3: 自动标注样本 """
    #for files, data_type in zip([trains,devs,tests],["train","dev","test"]):
        #auto_label(files, data_type,mode="max_seg")

    auto_source_label()

    #划分按{}
    split_josn_file()

        
if __name__ == "__main__":
    
    main()