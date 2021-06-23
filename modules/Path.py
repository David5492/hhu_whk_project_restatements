import os
import glob




def Fetcher(folder):
    '''
    VORSICHT: Pfade werden nur direkt aus einem einzigen Ordner geholt! Muss irgendwann gefixt werden. 
    
    '''
#     # öffne leere Liste für die Ausgabe
#     path_list = []
    
#     # definiere "folder", welcher bis ans Ende durchsucht werden soll aus path
#     folder = os.path.abspath('C:/Users/test/Desktop/Data Science/WHK/projekt_restatements/data/raw/2008_2018/*.pdf')

#     # geht die Ordnerstruktur entlang und fügt die Dateipfade zu path_list hinzu.
#     for root, dirs, files in os.walk(".",topdown = False):
#         for name in files:
#             path_list.append(os.path.join(folder,root[2:], name))

#     # Rückstände von Python-Checkpoints herausfiltern: KLAPPT AUS GRÜNDEN NICHT
#     path_list_clean = [i for i in path_list if "checkpoint" not in i]
            
#     return path_list_clean


    # definiere "folder", welcher bis ans Ende durchsucht werden soll aus path
    folder = os.path.abspath('C:/Users/test/Desktop/Data Science/WHK/projekt_restatements/data/raw/2008_2018/*.pdf')
    
    # rstelle Liste
    return glob.glob(folder)
