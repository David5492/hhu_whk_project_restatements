import subprocess

def match_in_perl(satz: str, key: str):
    '''
    Nimmt einen Satz und einen key als String entgegen und übergibt das an ein Perl-Script "perl.pl".
    perl.pl prüft, wie oft der Key in dem Satz vorkommt.
    Gibt anzal der Matches als integer aus
    '''
    output = subprocess.run(['perl', 'C:/Users/test/Documents/GitHub/hhu_whk_project_restatements/modules/perl.pl', satz, key], shell=True, capture_output=True)
    return(int(output.stdout))


# test = match_in_perl("Das ist ein wertvoller Beispielsatz mit wert darin. Wert", "wert")
# print(test)