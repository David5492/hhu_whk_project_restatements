from tika import parser
import string
import re
import io
import os



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
        # date = parsedPDF["metadata"]["created"][0:5]
        # language = parsedPDF["metadata"]["language"]
        # pages = parsedPDF["metadata"]["xmpTPg:NPages"]
        
        # Text_prep
        text_raw = parsedPDF["content"].replace('\n', "").replace('\t', "").strip().lower() # \n, \t raus und alles lower case
        text_w_num = [word for word in text_raw if word not in string.digits] # digits raus
        text = "".join([word for word in text_w_num if word not in string.punctuation]) # punktierung raus
        
        
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


