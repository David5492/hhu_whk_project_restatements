import re
import os
import unicodedata
from glob import glob
from tika import parser
import datetime
import pandas as pd 

start = datetime.datetime.now()

# Liste der Output-Variablen:

# Company
# Year
# ISIN
# SR
# NFE
# GRI (hatte Kajan nicht gelistet, mache ich aber noch dazu)
# Date_SR/NFE
# Date_AR
# ReportSize_SR/NFE
# ReportSentence_SR/NFE
# ReportWords_SR/NFE
# Keywords
# KeywordsClean
# SentenceRestatement
# ReportSize_AR
# ReportSentence_AR
# ReportWords_AR

# 0. KWL laden, alles klein schreiben:
KWL = []
with open("my_KWL.txt", "r", encoding="utf-8") as KWL_file:
    for line in KWL_file:
        KWL.append(line.strip())

# 0. ISIN-dict laden:
df = pd.read_excel('C:/Users/test/Documents/GitHub/hhu_whk_project_restatements/kajan_isin_korrekt.xlsx')
isin_dict = {}
for index, row in df.iterrows():
    isin_dict[row['Company'].lower().strip()] = row['ISIN'].strip()

list_of_isin_comp_tuples = []

for i in isin_dict.keys():
    list_of_isin_comp_tuples.append((i, isin_dict[i]))

# list_of_isin_comp_tuples.remove(('all for one steep', 'DE0006851603')) # einzelner Fehler wird korrigiert. Isin war falsch. 
# list_of_isin_comp_tuples.append(('verallia', 'DE0006851603'))

# 1. Pfad-Liste zur Bearbeitung erstellen
# Alle deutschen Dateipfade sammeln.

# PATH = 'C:\\Users\\test\\Documents\\GitHub\\hhu_whk_project_restatements\\test_data'
# PATH = 'C:\\Users\\test\\sciebo\\FACC SHK-WHB Berichte' 
# PATH = 'C:\\Users\\test\\Documents\\GitHub\\hhu_whk_project_restatements\\data\\raw_nachgeliefert_ganz' 
PATH = "D:\Berichte"
paths = [y for x in os.walk(PATH) for y in glob(os.path.join(x[0], '*.pdf'))]
paths_de = [pfad for pfad in paths if 'eng.' not in pfad.lower()]
paths_de_SR = [pfad for pfad in paths_de if not ('ar.' in pfad.lower()) | ('gb' in pfad.lower()) | ('ea.' in pfad.lower()) | ('_ar' in pfad.lower()) | ('abschlu' in pfad.lower()) | ('jb' in pfad.lower()) | ('annual' in pfad.lower())]

for pfad in paths:
    with open("alle_pfade.txt", mode="a", encoding="utf-8") as file:
        file.write(pfad + '\n')

for pfad in paths_de:
    with open("alle_pfade_de.txt", mode="a", encoding="utf-8") as file:
        file.write(pfad + '\n')

for pfad in paths_de_SR:
    with open("alle_pfade_angeschaute_berichte_de.txt", mode="a", encoding="utf-8") as file:
        file.write(pfad + '\n')


# Davon die in eine Liste ablegen, die noch nicht bearbeitet wurden. 
ist_eingelesen = []

with open("eingelesen.txt", mode="r", encoding="utf-8") as eingelesen:
    for line in eingelesen:
        ist_eingelesen.append(line.strip())

nicht_eingelesen = [pfad for pfad in paths_de_SR if pfad not in ist_eingelesen]

# 2. Schleife initiieren

eingelesene_pfade  = 0
pfad_counter = 1

with open("eingelesen.txt", mode="r", encoding="utf-8") as file:
    for line in file:
        eingelesene_pfade += 1
if eingelesene_pfade > 0:
    pfad_counter = eingelesene_pfade


for pfad in nicht_eingelesen:

    # file laden
    parsedPDF = parser.from_file(pfad, requestOptions={'timeout': 300}) 

    # Ausgabe-Variablen initiieren und ggf direkt f??llen. 
    Company = os.path.basename(pfad).split('20')[0].lower().strip()

    if (Company == '') | (Company == ' '):

        for element in pfad.split('\\'):
            if ('AG' in element) | ('SE' in element) | ('vzo' in element.lower())| ('kgaa' in element.lower()):
                Company = element.lower().strip()
    
    if (Company == '') | (Company == ' '):

        for element in pfad.split('\\'):
            Company = element.lower().strip()


    # Company f??r sp??tere analyse ablegen
    companies = []
    with open('companies.txt', 'r+', encoding="utf-8") as file:

        for line in file:
            companies.append(line.strip())

        if Company not in companies:
            file.write(Company + '\n')


    Year = re.findall(r'\d{4}', pfad)[-1]
    SR = 0
    NFE = 0

    # SR wird ggf in der Meta-Daten-Loop weiter unten nochmal behandelt. 
    if ('SR' in pfad) | ('crb' in pfad.lower()) | ('nhb' in pfad.lower()) | ('nb' in pfad.lower()) | ('nachhaltigkeit' in pfad.lower()):
        SR = 1

    if ('nfb' in pfad.lower()) | ('nfe' in pfad.lower()) | ('nichtfinanziell' in pfad.lower()):
        NFE = 1
    
    ISIN = 'fehlt'
    for k,v in list_of_isin_comp_tuples:
        if Company in k:
            ISIN = v
    if ISIN == 'fehlt':
        for k,v in list_of_isin_comp_tuples:
            firm = Company.split(' ')[0]
            if firm in k:
                ISIN = v

    # Datum SRNFE:
    try:
        Date_SRNFE = '.'.join(parsedPDF['metadata']['Creation-Date'][:10].split('-')[::-1])
        if Date_SRNFE == '':
            Date_SRNFE = '.'.join(parsedPDF['metadata']['created'][:10].split('-')[::-1])
        if Date_SRNFE == '':
            Date_SRNFE = 'fehlt'
    except:
        Date_SRNFE = 'fehlt'

    report_size_SRNFE = 0 
    report_sentence_SRNFE = 0
    report_words_SRNFE = 0 
    Date_AR = 0
    report_size_AR = 0 
    report_sentence_AR = 0
    report_words_AR = 0 


    is_gri = 0                              # 1, wenn match mit " gri " oder "(gri)" irgendwo im Text ist. 
    page_number = 0                         # wo ist aktuell angezeigter Satz
    satz = 'a'                              # Platzhalter f??r einen Satz

    # Bericht als Liste von Seiten speichern.
    try:
        pages_raw = unicodedata.normalize("NFKD", parsedPDF['content']).strip().split('\n\n\n') # l??st ein uni-encode-problem. Da stand vor jedem Wort "\xa0". L??st evtl. auch andere Problem mit komischen Fragmenten im Output.
        pages = [page for page in pages_raw if len(page)] # l??scht alle leeren pages. 

        # report_size zuweisen
        report_size_SRNFE = len(pages)
        
        # SCHLEIFE F??R META-DATEN SR:
        for page in pages: 

            # Spaltennamen von Tabellen standen immer hinter \n\n. Das durch Punkt ersetzt um Satzl??nge k??nstlich zu k??rzen. Tabellen werden jetzt nicht mehr als (wirre) S??tze gelesen. 
            text_SR = page.replace('\n\n', ".").replace('\n', "").replace('*','.').replace('..','.').replace('\t', "").replace(";", '').strip().lower()
            satz_liste_SR = text_SR.split('.')
            report_sentence_SRNFE += len(satz_liste_SR)

            # report_words aufaddieren
            report_words_SRNFE += len(text_SR.split(' '))

            # gri
            regex_gri = r'\W+gri\W|^gri\W*|global reporting initiative'
            for satz in satz_liste_SR:
                if re.search(regex_gri, satz):
                    is_gri = 1
                
            # SR
        for page in pages[:3]:
            # Spaltennamen von Tabellen standen immer hinter \n\n. Das durch Punkt ersetzt um Satzl??nge k??nstlich zu k??rzen. Tabellen werden jetzt nicht mehr als (wirre) S??tze gelesen. 
            text_SR = page.replace('\n\n', ".").replace('\n', "").replace('*','.').replace('..','.').replace('\t', "").replace(";", '').strip().lower()
            satz_liste_SR = text_SR.split('.')
            report_sentence_SRNFE += len(satz_liste_SR)

            if ('nachhaltigkeitsbericht' in satz_liste_SR) | ('sustainability report' in satz_liste_SR) | ('corporate responsibility' in satz_liste_SR):
                SR = 1


        if SR|NFE:  
            # AR zu SRNFE finden
            pfad_AR = 'a'
            for kandidat in paths_de:
                if ' ' in Company:
                    firm = Company.split(' ')[0]
                else: 
                    firm = Company

                if ((firm in kandidat.lower()) & (Year in kandidat) & ('ar' in kandidat.lower())) | ((firm in kandidat.lower()) & (Year in kandidat) & ('gb' in kandidat.lower())):
                    pfad_AR = kandidat

            # AR einlesen und Metadaten sammeln
            try:
                AR = parser.from_file(pfad_AR) 
                Date_AR = '.'.join(AR['metadata']['Creation-Date'][:10].split('-')[::-1])
                if Date_AR == '':
                    Date_AR = '.'.join(AR['metadata']['created'][:10].split('-')[::-1])
                if Date_AR == '':
                    Date_AR = 'fehlt'
                pages_raw_AR = unicodedata.normalize("NFKD", AR['content']).strip().split('\n\n\n') # l??st ein uni-encode-problem. Da stand vor jedem Wort "\xa0". L??st evtl. auch andere Problem mit komischen Fragmenten im Output.
                pages_AR = [page for page in pages_raw_AR if len(page)] # l??scht alle leeren pages. 
                report_size_AR = len(pages)



                # SCHLEIFE F??R META-DATEN AR:
                for page in pages_AR: 

                    # Spaltennamen von Tabellen standen immer hinter \n\n. Das durch Punkt ersetzt um Satzl??nge k??nstlich zu k??rzen. Tabellen werden jetzt nicht mehr als (wirre) S??tze gelesen. 
                    text_AR = page.replace('\n\n', ".").replace('\n', "").replace('*','.').replace('..','.').replace('\t', "").replace(";", '').strip().lower()
                    satz_liste_AR = text_AR.split('.')
                    report_sentence_AR += len(satz_liste_AR)

                    # report_words aufaddieren
                    report_words_AR += len(text_AR.split(' '))

            except:
                Date_AR = 'fehlt'
                pages_raw_AR = 'fehlt'
                pages_AR = 'fehlt'
                report_size_AR = 'fehlt'
                report_sentence_AR = 'fehlt'
                report_words_AR = 'fehlt'

            # initiieren von restatement-var, damit Berichte ohne res auch gespeichert werden. 
            restatement = 0

            # Seite f??r Seite durchgehen
            for page in pages: 
                page_number += 1
                print(u'Datei {} / {}. Seite {} / {}'.format(pfad_counter, len(paths_de_SR), page_number, report_size_SRNFE))

                # Spaltennamen von Tabellen standen immer hinter \n\n. Das durch Punkt ersetzt um Satzl??nge k??nstlich zu k??rzen. Tabellen werden jetzt nicht mehr als (wirre) S??tze gelesen. 
                text_SR = page.replace('\n\n', ".").replace('\n', "").replace('*','.').replace('..','.').replace('\t', "").replace(";", '').strip().lower()

                satz_liste_raw = text_SR.split('.')
                satz_liste = [satz.strip() for satz in satz_liste_raw if len(satz.strip()) > 4] # mindestens 4 weil k??rzestes Wort in KWL ("wert")

                # Satzweise die gesamte KWL checken lassen. Wenn Match, dann Satz mit Nummer in Match_Liste ablegen
                for satz in satz_liste:
                    satz_drin = 0
                    for key_word in KWL:
                        if satz_drin:
                            break
                        if re.search(key_word, satz):
                            satz_drin = 1
                            restatement = 1
                            key_word_clean = ''.join([char for char in key_word.replace('.',' ').replace('\d', '') if char not in '*+\W^'])
                            with open("./output_nachgeliefert2.csv", "a", encoding="utf-8") as File:
                                File.write(u"{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(Company, Year, ISIN, restatement, SR, NFE, Date_SRNFE, Date_AR, report_size_SRNFE, report_sentence_SRNFE, report_words_SRNFE, is_gri, key_word, key_word_clean, satz.replace(u'\ufffd', ' '), report_size_AR, report_sentence_AR, report_words_AR, pfad))
                            satz_drin = True
            if not restatement:
                with open("./output_nachgeliefert2.csv", "a", encoding="utf-8") as File:
                    key_word = 'fehlt'
                    key_word_clean = 'fehlt'
                    satz = 'fehlt'
                    File.write(u"{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(Company, Year, ISIN, restatement, SR, NFE, Date_SRNFE, Date_AR, report_size_SRNFE, report_sentence_SRNFE, report_words_SRNFE, is_gri, key_word, key_word_clean, satz, report_size_AR, report_sentence_AR, report_words_AR, pfad))

            with open("eingelesen.txt", mode="a", encoding="utf-8") as file:
                file.write(pfad + '\n')
    except:
        with open("fehlerhafte_dateien.txt", mode="a", encoding="utf-8") as file:
            file.write(pfad + '\n')
    pfad_counter +=1


stop = datetime.datetime.now()
print(u'\nBen??tigte Zeit: {}\n'.format(stop - start))





# F??r Output-Datei: 
# Company;Year;ISIN;restatement;SR;NFE;Date SRNFE;Date AR;ReportSize SRNFE;ReportSentence SRNFE;ReportWords SRNFE;GRI;Keywords;KeywordsClean;SentenceRestatement;ReportSize AR;ReportSentence AR;ReportWords AR
