import xlrd
list = []
data = xlrd.open_workbook('C:/Users/zhang/Desktop/给D100的表格.xlsx')
table = data.sheet_by_name(data.sheet_names()[0])
for i in range(1,table.nrows):
    list.append(str(table.row_values(i)[6])[:-2])
print(list)
print(len(list))
