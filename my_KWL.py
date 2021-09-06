list_1 = 'daten.scope.wert.method.zahl.standard.bericht.vorjahr.rückwirk'.split('.') #rückwirk nachträglich aufgenommen. 
list_2 = 'korrigier.korrektur.angepasst.anpass.aktualisier.bereinig.vorjahr'.split('.') # vorjahr bei beiden Listen. Grund: "Anpassung ggü Vorjahr" & "Methode aus Vorjahr" sollten beide matchen
middle = '.*'
under_table_pref_1 = '^\d+\W*'  # Weil oft eine Zahl als Aufzählungszeichen/Fußnotenlink unter Tabelle steht
under_table_pref_2 = '^\W'      # Da sist für etwaige andere Aufzählungszeichen unter Tabellen. 


# Die beiden Listen müssen in beide Richtungen zusammengesetzt werden, damit "Werte korrigiert" und "Korrigierte Werte" erkannt werden können -> vice und versa 
for i in list_1:
    for j in list_2:
        vice = i + middle + j
        versa = j + middle + i
        under_table_1 = under_table_pref_1 + j # nur j, weil oft unter Tabellen steht "*angepasst" oder "1angepasst". Würde da mehr stehen, würde das von den anderen Filterngematchet werden. 
        under_table_2 = under_table_pref_2 + j 
        with open("./my_KWL.txt", "a", encoding="utf-8") as File:
            File.write(u"{}\n{}\n{}\n{}\n".format(vice, versa, under_table_1, under_table_2))
