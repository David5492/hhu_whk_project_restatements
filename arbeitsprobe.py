from modules import Path 

from tika import parser
import string
import re
import io
import os


# In dieser Datei soll eine Neue Datei geschrieben.
# Für jeden Jahresabschluss, den diese Datei einließt, soll eine Excel-Arbeitsmappe erstellt 
# werden, die anhand einer KeyWordListe matches abgleicht und den Satz des Matches extrahiert. 

# Easy Approach: Das Matching ist simpel, jedes Dokument wird in Sätze zerlegt.

# Hard Approach: Das Matching wird komplex, man extrahiert keine Sätze sondern die Postion des 
# matches +- eine Zeichenanzahl. Text kann dabei in Form von Rohdaten bleiben. Vorteil: 
# Man übersieht nicht aus versehen Matches (z.B.) unter Grafiken (sind keine Sätze).

#=============================================================================================
# 1. EASY APPROACH
#=============================================================================================

# Pfadliste
pfade = Path.fetch("test_data")
print(pfade)

parser.from_file(pfade[0])





# for file in pfade:
#     print(file)
    
#     # Jahresabschluss einlesen
#     parsedPDF = parser.from_file(file)
#     break










#     # Metadaten sammeln
#     name = os.path.basename(file)
#     keywords = []
    
#     # Text_prep
#     text = parsedPDF["content"].replace('\n', "").replace('\t', "").strip().lower() # \n, \t raus und alles lower case
    
#     # Regex-Matcher
#     # matches = 0
#     # KWL = []
    
#     # with open("KWL.txt", "r", encoding="utf-8") as KWL_file:
#     #     for line in KWL_file:
#     #         KWL.append(line.strip())
    
#     # for key in KWL:
        
#     #     if re.search(key, text):
#     #         matches += 1
#     #         keywords.append(key)
#     # matches = str(matches)
#     print(text)
#     break








def Extractor(path_list):
    
    """
    Bekommt Liste mit Dateipfaden.
    Öffnet jeden Pfad.
    Extrahiert Roh-text und Metadaten: Datum, Sprache, Seitenanzahl
    Führt komplettes NLP am Text durch. Achtet dabei auf die Sprache der Datein.
        1. Lowercase
        2. Nummern raus
        3. Satzzeichen raus
        4. Leerzeichen raus
    
    """
    
    global matches, keywords
    
    for file in path_list:
        
        # Lesen
        parsedPDF = parser.from_file(file)
        
        # Metadaten
        name = os.path.basename(file)
        keywords = []
        
        # Text_prep
        text = parsedPDF["content"].replace('\n', "").replace('\t', "").strip().lower() # \n, \t raus und alles lower case

        
        
        # Regex-Matcher
        
        matches = 0
        KWL = []
        
        with open("KWL.txt", "r", encoding="utf-8") as KWL_file:
            for line in KWL_file:
                KWL.append(line.strip())
        
        for key in KWL:
            
            if re.search(key, text):
                matches += 1
                keywords.append(key)
        matches = str(matches)
        
        # Create new row
        
        keywords = ';'.join(keywords)
        
        input_list = ",".join([name,  matches, keywords]) # language, date, pages,
        
        with open("./final.csv", "a", encoding="utf-8") as File:
            File.write(f"{input_list}\n")       
        
        with open("./eingelesen.txt", "a", encoding="utf-8") as File:
            File.write(f"{file}\n")
        
        print(f"done: {name}. Matches: {matches} {keywords}")



#=============================================================================================
# 1. HRAD APPROACH
#=============================================================================================