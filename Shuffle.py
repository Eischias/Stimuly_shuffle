import random
import os.path
from typing import Iterable

# Function TIME
## interspace fce
def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

## Flatten list
def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

# shufelling option

BlockElement = 6
Stimulus_time = 8
FreeTRtext = "0\tnothing\td0"   #StymSys do noting TR

BIT = 2             # block interstimulus time
BBT = 5             # pause between block
LBBB = 30             # Long breake between block
FMRIS = 160             # number of fMRI sesion

STText = [FreeTRtext] * (Stimulus_time - 1)  # number of free TR
BITText = ["0\tcross.jpg\td0"] + ([FreeTRtext] * (BIT - 1)) # Cross between stimulus
BBTText = [FreeTRtext] * (BBT - 2) # Cross between block
LBBBText = [FreeTRtext] * (LBBB - 2)

# directory of images

ConName = os.listdir("Q:\\System\\Dropbox\\_Petr\\_Aktualni_Vyzkumy\\_Media_GACR\\fMRI_vetev\\Python\\Stimuly_shuffel\\CONCERNING")
DisName = os.listdir("Q:\\System\\Dropbox\\_Petr\\_Aktualni_Vyzkumy\\_Media_GACR\\fMRI_vetev\\Python\\Stimuly_shuffel\\DISTURBING")
NeuName = os.listdir("Q:\\System\\Dropbox\\_Petr\\_Aktualni_Vyzkumy\\_Media_GACR\\fMRI_vetev\\Python\\Stimuly_shuffel\\NEUTRAL")

#   Shufle each type

random.shuffle(ConName)
random.shuffle(DisName)
random.shuffle(NeuName)

#   merge category of con images
Cat1 = list(filter(lambda k: '_GO_' in k, ConName))
Cat2 = list(filter(lambda k: '_ZB_' in k, ConName))
Cat3 = list(filter(lambda k: '_RC_' in k, ConName))
Cat4 = list(filter(lambda k: '_V_' in k, ConName))
Cat5 = list(filter(lambda k: '_PD_' in k, ConName))
Cat6 = list(filter(lambda k: '_KK_' in k, ConName))

ConName = Cat1 + Cat2 + Cat3 + Cat4 + Cat5 + Cat6

### LOOP
for x in range(FMRIS):
#   Loop itineration name
    print(x)
#   add pre end post text for each element
    ConNameTexted = ["0\t" + x + "\td0" for x in ConName]
    DisNameTexted = ["0\t" + x + "\td0" for x in DisName]
    NeuNameTexted = ["0\t" + x + "\td0" for x in NeuName]

# merge stimulus with timing and inter block interval
    ConInterleaved= list(flatten(intersperse(ConNameTexted, (STText+BITText)) + [(STText+BITText)]))
    DisInterleaved= list(flatten(intersperse(DisNameTexted, (STText+BITText)) + [(STText+BITText)]))
    NeuInterleaved= list(flatten(intersperse(NeuNameTexted, (STText+BITText)) + [(STText+BITText)]))

# split lists to blocks
    ConBlocked = [ConInterleaved[x:x+(BlockElement * (len(STText + BITText)+1))] for x in range(0, len(ConInterleaved),BlockElement * (len(STText + BITText)+1))]
    DisBlocked = [DisInterleaved[x:x+(BlockElement * (len(STText + BITText)+1))] for x in range(0, len(DisInterleaved),BlockElement * (len(STText + BITText)+1))]
    NeuBlocked = [NeuInterleaved[x:x+(BlockElement * (len(STText + BITText)+1))] for x in range(0, len(NeuInterleaved),BlockElement * (len(STText + BITText)+1))]

# merge list and shuffle
    StimulyList = ConBlocked + DisBlocked + NeuBlocked
    random.shuffle(StimulyList)

# Add interBlock cross and big brake between
    StimulyListA = StimulyList[:len(StimulyList)//2]    # firts part of stimulus
    StimulyListB = StimulyList[len(StimulyList)//2:]    # second half of stimulus

    StimulyListA_Interleaved = list(flatten(intersperse(StimulyListA, BBTText)))
    StimulyListB_Interleaved = list(flatten(intersperse(StimulyListB, BBTText)))

    FinalStimuliList = StimulyListA_Interleaved + LBBBText + StimulyListB_Interleaved

# save csv
        textfile = open((str(x) + ".stm"), "w")
        for element in FinalStimuliList:
            textfile.write(element + "\n")
        textfile.close()
