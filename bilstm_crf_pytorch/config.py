from pathlib import Path

data_dir = Path("./dataset/cluener")
train_path = data_dir / 'train.json'
dev_path =data_dir / 'dev.json'
test_path = data_dir / 'test.json'
output_dir = Path("./outputs")

label2id = {
    "O": 0,
    "B-goverment":1,
    "B-tool":2,
    "B-goal":3,
    'B-consumer':4,
    'B-cartype':5,
    'B-company':6,
    'B-society':7,
    'B-otherorganization':8,
    'B-technology':9,
    'B-link':10,
    'B-researchinstitutions':11,
    "I-goverment":12,
    "I-tool":13,
    "I-goal":14,
    'I-consumer':15,
    'I-cartype':16,
    'I-company':17,
    'I-society':18,
    'I-otherorganization':19,
    'I-technology':20,
    'I-link':21,
    'I-researchinstitutions':22,
    "S-goverment":23,
    "S-tool":24,
    "S-goal":25,
    'S-consumer':26,
    'S-cartype':27,
    'S-company':28,
    'S-society':29,
    'S-otherorganization':30,
    'S-technology':31,
    'S-link':32,
    'S-researchinstitutions':33,
    "<START>": 34,
    "<STOP>": 35
}

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