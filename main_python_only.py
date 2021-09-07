from modules import Path 
from tika import parser
import re
import os
import unicodedata

import datetime

start = datetime.datetime.now()

# Pfadliste
pfade = Path.fetch("test_data")

# Outputdatei initiieren:
with open("./output.csv", "w", encoding="utf-8") as File:
    File.write(u"firm;year;report_size;report_words;is_gri;page_number;key_word_clean;key_word;satz\n")

# KWL laden, alles klein schreiben:
KWL = []
with open("my_KWL.txt", "r", encoding="utf-8") as KWL_file:
    for line in KWL_file:
        KWL.append(line.strip())


pfad_counter = 0

for pfad in pfade:

    pfad_counter +=1

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

    # year bestimmen:
    regex_year = r'\d{4}'
    year = re.findall(regex_year, firm)[0]

    # Bericht als Liste von Seiten speichern.
    pages_raw = unicodedata.normalize("NFKD", parsedPDF['content']).strip().split('\n\n\n') # löst eine uni-encode-problem. Da stand vor jedem Wort "\xa0". Löst evtl. auch andere Problem mit komischen Fragmenten im Output.
    pages = [page for page in pages_raw if len(page)] # löscht alle leeren pages. 

    # report_size zuweisen
    report_size = len(pages)

    # SCHLEIFE FÜR META-DATEN:
    for page in pages: 

        # Spaltennamen von Tabellen standen immer hinter \n\n. Das durch Punkt ersetzt um Satzlänge künstlich zu kürzen. Tabellen werden jetzt nicht mehr als (wirre) Sätze gelesen. 
        text = page.replace('\n\n', ".").replace('\n', "").replace('*','.').replace('..','.').replace('\t', "").replace(";", '').strip().lower()
        satz_liste = text.split('.')

        # report_words aufaddieren
        report_words += len(text.split(' '))

        # gri
        for satz in satz_liste:

            regex_gri = r'\W+gri\W|^gri\W*|global reporting initiative'
            if re.search(regex_gri, satz):
                is_gri = 1
        
    # Seite für Seite durchgehen
    for page in pages: 
        page_number += 1
        print(u'Datei {} / {}. Seite {} / {}'.format(pfad_counter, len(pfade), page_number, report_size))

        # Spaltennamen von Tabellen standen immer hinter \n\n. Das durch Punkt ersetzt um Satzlänge künstlich zu kürzen. Tabellen werden jetzt nicht mehr als (wirre) Sätze gelesen. 
        text = page.replace('\n\n', ".").replace('\n', "").replace('*','.').replace('..','.').replace('\t', "").replace(";", '').strip().lower()

        satz_liste_raw = text.split('.')
        satz_liste = [satz for satz in satz_liste_raw if len(satz.strip()) > 4] # mindestens 4 weil kürzestes Wort in KWL ("wert")

        # Satzweise die gesamte KWL checken lassen. Wenn Match, dann Satz mit Nummer in Match_Liste ablegen
        for satz in satz_liste:
            satz_drin = False
            for key_word in KWL:
                if satz_drin:
                    break
                if re.search(key_word, satz):
                    key_word_clean = ''.join([char for char in key_word.replace('.',' ').replace('\d', '') if char not in '*+\W^'])
                    with open("./output.csv", "a", encoding="utf-8") as File:
                        File.write(u"{};{};{};{};{};{};{};{};{}\n".format(firm, year, report_size, report_words, is_gri, page_number, key_word_clean, key_word, satz)) #, restatement
                    satz_drin = True
                

stop = datetime.datetime.now()
print(u'\nBenötigte Zeit: {}\n'.format(stop - start))