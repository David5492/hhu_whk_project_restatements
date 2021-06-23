import os
import glob

def fetch(folder = "test_data"):
    '''
    Nimmt einen Ordner und listet alle Dateien darin auf.
    Rückgabewert ist eine Pfad-Liste aus vollständigen Pfaden zu diesen Dateien.
    '''
    # initiiere leere Ausgabeliste
    pfad_liste = []

    # Speichere Pfad bis zum Zielordner
    pfad_bis_folder = os.path.dirname(os.path.abspath(folder))

    # Speichere Dateinamen im Zielordner
    folder += "/*"
    pfad_ab_folder = glob.glob(folder)
    
    # Kombiniere beide zu eine rListe vollständiger Pfade
    for pfad in pfad_ab_folder:
        pfad_liste.append(os.path.join(pfad_bis_folder, pfad))

    return(pfad_liste)



