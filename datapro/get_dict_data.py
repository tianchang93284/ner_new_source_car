import xlrd


workbook = xlrd.open_workbook('dict_label.xls')
sheet = workbook.sheet_by_index(0)
nrows = sheet.nrows
ncols = sheet.ncols

label = set()

for i in range(0,nrows):
    label.add(sheet.cell(i, 1).value)

print(label)







