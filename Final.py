import csv

import re
import pandas as pd
import time
import tracemalloc

import numpy as np



class Convert_English_to_French:
    dictionary = dict()
    findword = set()
    list3=[[],[],[]]
    __slots__ = ("novel","findWords","translatedFile","df","performance","processTime","memoryUsed")

    def __init__(self):
        self.novel = open("t8.shakespeare.txt", 'r')
        self.findWords = open('find_words.txt', 'r')
        self.translatedFile = open('t8.shakespeare.translated.txt', 'w')
        self.df = pd.DataFrame({'Eng': [], 'French': [], 'Frequency': []})
        self.performance = open("Performance.txt", "w")
        self.processTime = 0
        self.memoryUsed = 0
        self.readDictionaryAndSet()

    def readDictionaryAndSet(self):
        #start_time = time.time()
        reader = csv.reader(open('french_dictionary.csv', 'r'))
        for row in reader:
            k, v = row
            Convert_English_to_French.dictionary[k] = v
        Convert_English_to_French.findword = set(line.strip() for line in self.findWords)

    def checkCases(self, key, value):
        if (key.islower()):
            return value.lower()
        elif (key.isupper()):
            return value.upper()
        elif (key.istitle()):
            return value.title()
        else:
            return value

    def translate(self):
        with self.novel as f:
            start_time = time.time()
            tracemalloc.start()
            count=1

            for line in f:
                list2 = []
                count+=1
                if len(line) > 1:
                    delimiterlist = re.findall(r'[\W]', line)
                else:
                    delimiterlist = []
                for words in line.split():
                    if str("".join(re.findall("[\w]+", words.lower()))) in Convert_English_to_French.findword:
                        frenchword = Convert_English_to_French.checkCases(self,
                                                                          str("".join(re.findall("[a-zA-Z]+", words))),
                                                                          Convert_English_to_French.dictionary[str(
                                                                              "".join(re.findall("[a-zA-Z]+",
                                                                                                 words.lower())))])
                        list2.append(frenchword)
                        Convert_English_to_French.list3[0].append(str("".join(re.findall("[a-zA-Z]+", words.lower()))))
                        Convert_English_to_French.list3[1].append(frenchword.lower())

                        Convert_English_to_French.list3[2].append(0)

                    else:
                        list2.append(words)

                self.translatedFile.write("".join(np.array([[i, j] for i, j in zip(list2, delimiterlist)]).ravel()))
                self.translatedFile.write("\n")

        self.memoryUsed = tracemalloc.get_tracemalloc_memory() / float(1 << 20)
        self.processTime = time.time() - start_time

    def writingIntoFile(self):
        self.df = pd.DataFrame({'Eng': Convert_English_to_French.list3[0], 'French': Convert_English_to_French.list3[1], 'Frequency': Convert_English_to_French.list3[2]})
        self.df = (self.df.groupby(['Eng', 'French'])['Frequency'].count()).drop_duplicates()
        self.df.to_csv('frequency.csv')
        self.performance.write("Time to process:" + str(self.processTime) + " " + "seconds"+"\n")
        self.performance.write("Memory used: " + '{:,.0f}'.format(self.memoryUsed) + " MB" + "\n")
        print("Memory used: " + '{:,.0f}'.format(self.memoryUsed) + " MB")
        print("Time to process:" + str(self.processTime) + " " + "seconds")
        print("Translation done!")


obj = Convert_English_to_French()
obj.translate()
obj.writingIntoFile()