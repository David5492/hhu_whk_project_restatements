list_1 = 'daten.scope.wert.method.zahl.standard.bericht'.split('.') #nachträglich: standrad, bericht
list_2 = 'korrigiert.angepasst.aktualisiert'.split('.') 
middle = '.*'
under_table_pref_1 = '^\d+\W*'
under_table_pref_2 = '^\W'



for i in list_1:
    for j in list_2:
        vice = i + middle + j
        versa = j + middle + i
        under_table_1 = under_table_pref_1 + j
        under_table_2 = under_table_pref_2 + j
        with open("./my_KWL.txt", "a", encoding="utf-8") as File:
            File.write(u"{}\n{}\n{}\n{}\n".format(vice, versa, under_table_1, under_table_2))
