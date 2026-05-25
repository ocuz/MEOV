How to use the script:

- Extract the .zip file into a folder
- Install python added to path.EXE
- Run "pip install requests colorama"


For custom pattern, this is how it works:
C=consonant
V=vowel
D=digit
L=letter
Q=letter/digit
_=underscore (once, not start/end)
[X]=exact char example, if you put [P] it will put P
[XY]=select from the table example, if you put [MS] it will choose between M or S

Example: C[K]CV[h]
= consonant,"K",consonant,vowel,"h"
= bKteh,rKloh,mKpah,tKfuh,sKnih
