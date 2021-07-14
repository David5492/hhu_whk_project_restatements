from modules import Path 
from tika import parser
import re
import os

import datetime

start = datetime.datetime.now()


# In dieser Datei soll eine Neue Datei geschrieben.
# Für jeden Jahresabschluss, den diese Datei einließt, soll eine Excel-Arbeitsmappe erstellt 
# werden, die anhand einer KeyWordListe matches abgleicht und den Satz des Matches extrahiert. 

#=============================================================================================
# 0. VORBEREITUNG: Pfade sammlen, KWL laden.
#=============================================================================================

# Pfadliste
pfade = Path.fetch("test_data")

# KWL laden, alles klein schreiben:
KWL = []
with open("my_KWL.txt", "r", encoding="utf-8") as KWL_file:
    for line in KWL_file:
        KWL.append(line.strip())

#=============================================================================================
# 0. Ich teste ab hier mit dem ertsen file und dem ersten keyword. 
#=============================================================================================
for pfad in pfade:

    # file laden
    parsedPDF = parser.from_file(pfad) 

    # Ausgabe-Variablen initiieren
    firm = os.path.basename(pfad)[0:-4] # alles außer '.pdf'

    year = 0 # hier regex-matcher für 4 Zahlen im file_name

    report_size = 0 # Seitenzahl des gesamten reports

    report_words = 0 # Anzahl der Wörter im gesamten Report

    is_gri = 0 # 1, wenn match mit " gri " oder "(gri)" irgendwo im Text ist. 

    page_number = 0 # wo ist aktuell angezeigtes Restatement

    key_word = 0 # anhand welchen keys wurde das Restatement erkannt

    # Lasse ich erstmal weg: 
    # restatement = 0 # Bool für den ganzen File, falls ein Restatement drin ist. 

    # year bestimmen:
    regex_year = r'\d{4}'
    year = re.findall(regex_year, firm)[0]

    # Bericht als Liste von Seiten speichern.
    pages_raw = parsedPDF['content'].split('\n\n\n\n')
    pages = [page for page in pages_raw if len(page)]

    # report_size zuweisen
    report_size = len(pages)


    # SCHLEIFE FÜR META-DATEN:
    for page in pages: 

        # Text_prep: Absätze (\n), Tabs (\t) und Semikoli raus; Liste aus Sätzen erstellen // Normalerweise schriebt man noch alles klein, aber wegen KWL nicht möglich. 
        text = page.replace('\n', "").replace('\t', "").replace(";", '').strip().lower()
        satz_liste = text.split('.')

        # report_words aufaddieren
        report_words += len(text.split(' '))

        # gri
        for satz in satz_liste:

            regex_gri = r'\W+gri\W|^gri\W*|global reporting initiative'
            if re.search(regex_gri, satz):
                is_gri = 1



    for page in pages: 
        page_number += 1

        # Text_prep: Absätze (\n), Tabs (\t) und Semikoli raus; Liste aus Sätzen erstellen // Normalerweise schriebt man noch alles klein, aber wegen KWL nicht möglich. 
        text = page.replace('\n', "").replace('\t', "").replace(";", '').strip().lower()
        satz_liste = text.split('.')

        # Satzweise die gesamte KWL checken lassen. Wenn Match, dann Satz m it Nummer in Match_Liste ablegen
        for satz in satz_liste:
            for key_word in KWL:
                if re.search(key_word, satz):
                    key_word_clean = ''.join([char for char in key_word.replace('.',' ').replace('\d', '') if char not in '*+\W^'])
                    with open("./output.csv", "a", encoding="utf-8") as File:
                        File.write(u"{};{};{};{};{};{};{};{};{}\n".format(firm, year, report_size, report_words, is_gri, page_number, key_word_clean, key_word, satz)) #, restatement
                

stop = datetime.datetime.now()
print(stop - start)
