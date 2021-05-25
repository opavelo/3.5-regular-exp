from pprint import pprint
import re
import csv
import pandas as pd

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ

phonebook = []

phonebook.append(contacts_list[0])

for i in contacts_list[1:]:
    fio = re.findall('\w+', str(i[:3]))
    lastname = fio[0]
    firstname = fio[1]
    if len(fio) > 2:
        surname = fio[2]
    else:
        surname = ''
    tel = re.sub('[^0-9]', '', i[5])
    tel = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\d{4})', r'+7(\2)-\3-\4-\5 доб.\6', tel)
    tel = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)-\3-\4-\5', tel)
    new_line = []
    new_line.extend([lastname, firstname, surname, i[3], i[4], tel, i[6]])
    phonebook.append(new_line)

phonebook = pd.DataFrame(phonebook)
phonebook = phonebook.rename(columns=phonebook.iloc[0])
phonebook = phonebook[1:]
phonebook = phonebook.groupby(['lastname', 'firstname']).agg({'surname':'max', 'organization':'max', 'position':'max', 'phone':'max', 'email':'max'}).reset_index()
print(phonebook)
phonebook.to_csv('phonebook.csv',index = False)


# # TODO 2: сохраните получившиеся данные в другой файл
# # код для записи файла в формате CSV
#
# with open("phonebook.csv", 'w', newline='') as f:
#     datawriter = csv.writer(f)
# #    Вместо contacts_list подставьте свой список
#     datawriter.writerows(phonebook)