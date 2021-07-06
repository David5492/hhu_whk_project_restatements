# PERL wird in main.py aufgerufen 
# Dabei erhält PERL (also dieses Skript hier) einen einzelnen Satz und praed_list, sowie sub_list, was Listen mit Prädikaten und Substantiven aus den der aktuellsten KWL ist.
# Hier werden praed, sub, year, opt jeweils mit 0 initiiert. 
# PERL öffnet eine for-Schleife und sucht so nach allen Substantiv-Matches innerhalb des Satzes. Dabei gehen die Zählervariable sub hoch, falls ein Match vorliegt. 
# WENN sub nicht 0 ist, dann komm eine 2. for-Schleife und sucht so nach allen Prädiakt-Matches innerhalb des Satzes. Dabei gehen die Zählervariable präd hoch, falls ein Match vorliegt. 
# WENN sub nicht 0 ist, sucht PERL auch nach dem regex "vorjahr*" und nach Jahreszahlen "[0-9]{4}"



