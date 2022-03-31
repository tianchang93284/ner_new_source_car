
import csv
import codecs
import xlrd

excel = xlrd.open_workbook("ner_dict_policy.xls")
sheet = excel.sheet_by_index(0)
#rows: list = sheet.row_values(0)
#index = rows.index('username')
#listindes = sheet.col_values(index)

nrows = sheet.nrows
ncols = sheet.ncols

name = 'ner_dict_policy_process.csv'
f_writeopen = open(name,'w+')
f_wtritecsv = csv.writer(f_writeopen)
f_writeopen.close()
j = 0
row = 1
#with open
for i in range(2,nrows):
    # if j == 0:
    #     j=j+1
    #     continue
    # if i == 10564:
    #     continue
    print(i)
    datastr = sheet.cell(i,row).value
    if datastr.find(',') is not -1:
        datas = sheet.cell(i,row).value.split(',')
    else:
        datas = sheet.cell(i, row).value.split(';')
    for data in datas:
        data = data.strip()
        is_write = True
        f_writeprocee_open = open(name, 'r')
        f_readprocee = csv.reader(f_writeprocee_open)
        for f_read in f_readprocee:
            if len(f_read) is not 0 and data == f_read[0]:
                is_write = False
                break
        f_writeprocee_open.close()
        if is_write:
            fcodecopen = codecs.open(name, 'a', 'gbk')
            f_writeprocee = csv.writer(fcodecopen)
            f_writeprocee.writerow([data])
            fcodecopen.close()













