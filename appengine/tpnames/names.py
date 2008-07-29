#!/usr/bin/python
import random
import re
import sys
import time
    
def main():
   names = generate(sys.stdin, None)
   for name in names:
     print name

def genFromFile(filename, seed):
   file = open(filename, 'r')
   return generate(file, seed)

def generate(input, seed):
    if (seed == None):
      seed = time.time() 

    if not isinstance(seed, (int, long, float, complex)):
      seed = hash(seed)

    syllabary = makeSyllabary(input)
    names = list()
    for i in range(15):
      generatedWord = generateWord(seed + i, syllabary)
      names.append(generatedWord)
    return names

def makeSyllabary(input):
    """Breaks each line down into syllables, returning a list of lists of syllables.
       Upper case syllables after the first are prepended with a space.
       Underscore is replaced with a space (e.g. Ursae_Majoris)"""
    syllabary = list()
    startsWithUpper = re.compile('^[A-Z]')
    for line in input:
        line = line.strip()
        if not line.startswith('#'):
            raw_syllables = line.strip().split(' ')
            syllables = list()
            for i in range(len(raw_syllables)):
                syllable = raw_syllables[i]
                syllable = syllable.replace('_', ' ')
                if i > 0 and startsWithUpper.search(syllable):
                    syllables.append(' ' + syllable)
                else:
                    syllables.append(syllable)
            if len(syllables) >= 2:
                syllabary.append(syllables)
    return syllabary
    
def generateWord(seed, syllabary):
    r = random.Random(seed)
    choice = r.randrange(0, len(syllabary))
    sourceword = syllabary[choice]
    generatedWord = sourceword[0]
    syllableIndex = 0
    while True:
        syllableIndex += 1
        choice = r.randrange(0, len(syllabary))      
        randomSourceWord = syllabary[choice]
        lastSyllableIndex = len(randomSourceWord) - 1
        if lastSyllableIndex <= syllableIndex:
            syllable = randomSourceWord[-1]
            generatedWord += syllable
            break
        else:
            syllable = randomSourceWord[syllableIndex]
            generatedWord += syllable
    return generatedWord
    
if __name__ == "__main__":
    main()
