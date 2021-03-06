__version__ = "$Revision: 323 $, $Date: 2010-09-27 14:46:38 +0200 (ma, 27 sep 2010) $, $Author: quintijn $"
# (unimacro - natlink macro wrapper/extensions)
# (c) copyright 2003 Quintijn Hoogenboom (quintijn@users.sourceforge.net)
#                    Ben Staniford (ben_staniford@users.sourceforge.net)
#                    Bart Jan van Os (bjvo@users.sourceforge.net)
#
# This file is part of a SourceForge project called "unimacro" see
# http://unimacro.SourceForge.net).
#
# "unimacro" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, see:
# http://www.gnu.org/licenses/gpl.txt
#
# "unimacro" is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; See the GNU General Public License details.
#
# "unimacro" makes use of another SourceForge project "natlink",
# which has the following copyright notice:
#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 1999 by Joel Gould
#   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#
# _spokenforms.py 
#  written by: Quintijn Hoogenboom (QH softwaretraining & advies)
#  June 2011
#

"""This module contains a class spokenforms that maintains spoken forms
for numbers, thus making it possible to use spoken forms for all numbers lists
in Unimacro grammars which need numbers 

tested with unittestSpokenForms.py (in unimacro_test directory of Unimacro)
"""
import re, string, os, sys, types, shutil, os.path, copy
import operator
import win32api
import inivars
import natlinkstatus
class NumbersError(Exception): pass

# for generateMixedListOfSpokenForms:
reNonAlphaNumeric = re.compile(r'[^a-zA-Z0-9]')
reNumeric = re.compile(r'([0-9]+)')
reNumericUnderscore = re.compile(r'^([0-9]+[_])')
reNumericBracketsEnd = re.compile(r'\s*[(][0-9]+[)]\s*$')
reLetterUnderscore = re.compile(r'^([a-zA-z]{1,2}[_])')

# for A or A. in spoken forms
reMatchUpperCaseLetter = re.compile(r'\b[A-Z]\b(?![.])')
reMatchUpperCaseLetterDot= re.compile(r'\b[A-Z]\.')
def addDot( match ):
    """for use in reMatchUpperCaseLetter"""
    return match.group() + '.'
def looseDot( match ):
    """for use in reMatchUpperCaseLetterDot"""
    return match.group()[0]

def fixSingleLetters(spoken, DNSVersion):
    """replace A by A. in Dragon <= 10 and A. in A in Dragon >= 11
    
    >>> fixSingleLetters("A. BC D", 10)
    'A. BC D.'
    >>> fixSingleLetters("C. DE. F", 11)
    'C DE. F'
    
    """
    if DNSVersion <= 10:
        m = reMatchUpperCaseLetter.search(spoken)
        if m:
            spoken= reMatchUpperCaseLetter.sub(addDot, spoken)
    else:
        # Dragon 11
        m = reMatchUpperCaseLetterDot.search(spoken)
        if m:
            spoken= reMatchUpperCaseLetterDot.sub(looseDot, spoken)
    return spoken


thisBaseDirectory = os.path.split(sys.modules[__name__].__dict__['__file__'])[0]

# special list names to be defined here:
number1to99stripped = range(1, 20) +  range(20, 91, 10)


#####
##### get spokenforms.ini from baseDirectory or SampleDirectory into userDirectory:
status = natlinkstatus.NatlinkStatus()
# baseDirectory = status.getUnimacroDirectoryFromIni()
# if not baseDirectory:
#     baseDirectory = ""
#     #raise ImportError( 'no baseDirectory found while loading spokenforms.py, stop loading this module')
# sampleBases = [thisBaseDirectory.lower()]
# if thisBaseDirectory.lower() != baseDirectory.lower():
#     print 'actions module has ambiguous baseDirectory: |%s|, this: |%s|: take the latter one!'% (baseDirectory, thisBaseDirectory)
#     sampleBases.insert(0, baseDirectory.lower())
    
unimacroDirectory = status.getUnimacroDirectory().lower()
sampleBases = [unimacroDirectory]                   
sampleDirectories = [os.path.join(base, 'sample_ini') for base in sampleBases]
sampleDirectories = [p for p in sampleDirectories if os.path.isdir(p)]
      
if not sampleDirectories:
    print '\nNo Unimacro sample directory not found: %s\nCHECK YOUR CONFIGURATION!!!!!!!!!!!!!!!!\n'
#else:
#    print 'sample_directories: %s'% sampleDirectories
    
userDirectory = status.getUnimacroUserDirectory()

if not os.path.isdir(userDirectory):
    try:
        os.mkdir(userDirectory)
    except OSError:
        print 'cannot make inifiles directory: %s'% userDirectory
####

currentlanguage = None
inifile = None
ini = None

def resetSpokenformsGlobals():
    """utility function for unittest, to ensure there is a fresh start
    """
    global currentlanguage, ini, inifile
    currentlanguage = ini = inifile = None
    
def checkSpokenformsInifile(language):
    """copy if needed the correct inifile into the userDirectory
    
    print message if no valid file found and return False 
    """
    global currentlanguage, ini, inifile
    if language and language == currentlanguage and ini:
        return inifile # all OK
    ini = None
    currentlanguage = language
    filename = '%s_spokenforms.ini'% language
    inifile = os.path.join(userDirectory, '%s_spokenforms.ini'% language)
    if not os.path.isfile(inifile):
        # now try to copy from the samples:
        print '---try to find spokenforms.ini file in old version (UserDirectory) or sample_ini directory'
        for sample in sampleDirectories:
            sampleinifile = os.path.join(sample, filename)
            if os.path.isfile(sampleinifile):
                print '---copy spokenforms.ini from\nsamples directory: %s\nto %s\n----'% (sampleinifile, inifile)
                shutil.copyfile(sampleinifile, inifile)
                if os.path.isfile(inifile):
                    break
                else:
                    print 'cannot copy sample spokenforms inifile to: "%s"'% inifile
                    inifile = None
                    return
        else:
            print 'no valid sample "%s" file found in one of %s sample directories:\n|%s|'% \
                      (filename, len(sampleDirectories), sampleDirectories)
            return
    # now assume valid inifile:
    try:
        ini = inivars.IniVars(inifile, returnStrings=True)
    except inivars.IniError:
        print 'Error in spokenforms inifile: "%s"'% inifile
        m = str(sys.exc_info()[1])
        print 'message: %s'% m
        print '\n\n===please edit %s (open by hand)'% inifile
        #win32api.ShellExecute(0, "open", inifile, None , "", 1)    
    else:
        return inifile 

oldversioninifile = 'spokenforms.ini' # new with language prefix...
for dir in (userDirectory,): ### baseDirectory):
    old = os.path.join(dir, oldversioninifile)
    if os.path.isfile(old):
        print 'remove "%s" from directory (obsolete): %s'% (old, dir)
        os.remove(old)

def openInifile(inifilepath):
    global inifile, ini
    if os.path.isfile(inifilepath):
        inifile = inifilepath
        try:
            ini = inivars.IniVars(inifile)
        except inivars.IniError:
            
            print 'Error in numbers inifile: %s'% inifile
            m = str(sys.exc_info()[1])
            print 'message: %s'% m
            pendingMessage = 'Please repair spokenforms.ini file\n\n' + m
            ini = None
            print 'please edit %s (open by hand)'% inifile
            #win32api.ShellExecute(0, "open", inifile, None , "", 1)
        else:
            return ini
    else:
        ini = inifile = None
        print 'no inifile spokenforms.ini found. Please repair'

def editSpokenForms(comingFrom=None, name=None, language=None):
    """show the spokenforms.ini file in a editor
    """
    if not language:
        print 'editSpokenForms: call with language is required!'
        return
    
    inifile = checkSpokenformsInifile(language)
    if not inifile:
        print 'editSpokenForms: no valid spokenforms inifile for language "%s" available'% language
        return        
    if comingFrom:
        name=name or ""
        comingFrom.openFileDefault(inifile, name=name)
    else:
        print 'inifile: ', inifile
        print 'please edit (open by hand): %s'% inifile
    #win32api.ShellExecute(0, "open", inifile, None , "", 1)
    print 'note: you need to restart Dragon after editing the spoken forms inifile.'
    

showSpokenForms = editSpokenForms

class SpokenForms(object):
    """maintain a (class wide) dict of numbers -> spoken forms and vice versa
    a language is required at __init__ time.
    
    Also characters (a, b, etc) to spoken and vice versa
    
    It is assumed only one language can be active at the same time, so the dicts
    are kept global in the class
    """
    n2s = {}
    s2n = {}
    char2spoken = {} # characters of radio alphabet possibly extended
    spoken2char = {}
    abbrev2spoken = {} # lists of spoken forms
    spoken2abbrev = {}
    ext2spoken = {}    # file extensions (without the dot) (section "extensions")
    spoken2ext = {}    
    punct2spoken = {}  # punctuation, from section punctuationreverse (other way round!)
    spoken2punct = {}
    
  
    language = None
    
    def __init__(self, language, DNSVersion):
        # global in this module, does not extra work if language did not change:
        checkSpokenformsInifile(language)
        self.DNSVersion = DNSVersion
        
        if self.language is None or self.language != language:
            self.__class__.language = None
            if self.filldicts(language):
                self.__class__.language = language
                
                
    def filldicts(self, language):
        """fill the base dictionaries for the class
        """
        self.n2s.clear()
        self.s2n.clear()
        if ini is None:
            print 'no inifile for numbers spoken forms'
            return
        # section in spokenforms.ini file:
        section = "numbers"
        if not section in ini.get():
            print 'no section in spokenforms.ini for language: %s'% section
            return
        for k in ini.get(section):
            v = ini.get(section, k)
            try:
                n = int(k)
            except ValueError:
                print 'invalid entry in spokenforms.ini for language: %s\n' \
                      '%s = %s  (key must be a integer)'% (language, k, v)
                continue
            for splitChar in ",;|":
                if v.find(splitChar) > 0:
                    V = [s.strip() for s in v.split(splitChar)]
                    break
            else:
                V = [v]
            for w in V:
                self.s2n[w] = n
            self.n2s[n] = V
        
        section = 'alphabet'
        for k in ini.get(section):
            v  = ini.get(section, k)
            if not v:
                continue
            for splitChar in ",;|":
                if v.find(splitChar) > 0:
                    V = [s.strip() for s in v.split(splitChar)]
                    break
            else:
                V = [v]
            for w in V:
                self.spoken2char[w] = k
            self.char2spoken[k] = V
            
        section = 'abbrevs'
        for k in ini.get(section):
            v  = ini.get(section, k)
            if not v:
                v = ' '.join(l.upper() for l in k)
            for splitChar in ",;|":
                if v.find(splitChar) > 0:
                    V = [s.strip() for s in v.split(splitChar)]
                    break
            else:
                V = [v]
            V = [fixSingleLetters(s, self.DNSVersion) for s in V]
            for w in V:
                self.spoken2abbrev[w] = k
            self.abbrev2spoken[k] = V

        section = 'extensions'
        for k in ini.get(section):
            v  = ini.get(section, k)
            if not v:
                v = ' '.join(l.upper() for l in k)
            for splitChar in ",;|":
                if v.find(splitChar) > 0:
                    V = [s.strip() for s in v.split(splitChar)]
                    break
            else:
                V = [v]
            V = [fixSingleLetters(s, self.DNSVersion) for s in V]
            for w in V:
                # extensions can point back to more extensions, eg excel to .xls and to .xlsx
                self.spoken2ext.setdefault(w, []).append(k)
            self.ext2spoken[k] = V

        section = 'punctuationreverse'
        for k in ini.get(section):
            try:
                v  = ini.get(section, k)
            except inivars.IniError:
                print 'Error in ["%s"] section of spokenforms.ini files'% section
                m = str(sys.exc_info()[1])
                print 'message: %s'% m
                v = None
                
            if not v:
                continue
                # extensions can point back to more extensions, eg excel to .xls and to .xlsx
            self.spoken2punct[k] = v
            self.punct2spoken.setdefault(v, []).append(k)
        
        return 1
    
    def correctLettersForDragonVersion(self, spoken):
        """convert A to A. in NatSpeak <= 10 and B. int B for Dragon 11
        """
        return fixSingleLetters(spoken, self.DNSVersion)
    
    def getSpokenFormsList(self, n):
        """return a list of spoken forms, also for numbers larger than filldicts gave
        
        this one goes one way, only fills n2s if not available yet. Larger numbers may be included
        for future references.
        """
        if n in self.n2s:
            return self.n2s[n]
        else:
            spokenforms = self.generateSpokenFormsFromNumber(n)
            if spokenforms:
                self.n2s[n] = spokenforms
                return spokenforms
            else:
                return 
    
    def getMixedCharactersList(self, ListOfChars=None):
        """return a list of strings with either the number or the spoken forms
        """
        if ListOfChars is None:
            ListOfChars = string.ascii_lowercase
        L = []
        for s in ListOfChars:
            if s in self.char2spoken:
                L.extend(self.char2spoken[s])
            else:
                L.append(s)
        return L
    
    def getMixedList(self, ListOfNumbers):
        """return a list of strings with either the number or the spoken forms
        """ 
        L = []
        for s in ListOfNumbers:
            i = int(s) # in case we started with a string
            spokenforms = self.getSpokenFormsList(i)
            if spokenforms:
                L.extend(spokenforms)
                for name in spokenforms:
                    # needed for retrieving the numbers
                    # spokenforms back to the numbers:
                    if not name in self.s2n:
                        self.s2n[name] = i
            else:
                print 'no spoken forms found for %s'% i
                L.append(str(i))
        return L

    def generateSpokenFormsFromNumber(self, n):
        """return a list of possible spoken forms strings
        """
        for i in 100, 1000, 0, 1:
            if not i in self.n2s:
                print 'spokenforms.ini should have entry or entries for %s'%i
                return [str(n)]
        hundred = self.n2s[100][0]
        thousand = self.n2s[1000][0]
        oh = self.n2s[0][0]
        one = self.n2s[1][0]
        s = str(n)
        if n < 100:
            print 'should not come here for %s, all numbers below 100 should be in ini file'%n
            return
        if n < 1000:
            if n == 100:
                print 'should %s take from n2s'% n
                return s
            elif s.endswith('00'):
                digitstrings = self.n2s[int(s[0])]
                return [d+' '+hundred for d in digitstrings]
            elif s[1] == '0':
                # one oh three 103 etc
                sp1 = self.n2s[int(s[0])]
                sp2 = self.n2s[int(s[2])]
                spList =['%s %s %s'% (s1, oh, s2) for s1 in sp1 for s2 in sp2]
                if s[0] == '1':
                    sp1 = self.n2s[100]
                else:
                    sp1 = ['%s %s'% (d, hundred) for d in self.n2s[int(s[0])]]
                spList.extend(['%s %s'% (s1, s2) for s1 in sp1 for s2 in sp2])
                return spList
            elif s[0] == '1':
                # hundred ... or  one ...
                sp = self.n2s[int(s[1:])]
                spList = ['%s %s'% (hundred, s) for s in sp]
                spList.extend(['%s %s'% (one, s) for s in sp])
                return spList
            else:
                sp1 = self.n2s[int(s[0])]
                sp2 = self.n2s[int(s[1:])]
                spList = ['%s %s %s'% (s1, hundred, s2) for s1 in sp1 for s2 in sp2]
                spList.extend(['%s %s'% (s1, s2) for s1 in sp1 for s2 in sp2])
                return spList
        elif n < 10000:
            if n == '1000':
                print 'should %s take from n2s'% n
                return s
            elif s.endswith('000'):
                digitstrings = self.n2s[int(s[0])]
                return [d+' '+thousand for d in digitstrings]
            elif s[1:3] == '00':
                # one oh three 103 etc
                sp1 = self.n2s[int(s[0])]
                sp2 = self.n2s[int(s[3])]
                spList =['%s %s %s %s'% (s1, oh, oh, s2) for s1 in sp1 for s2 in sp2]
                if s[0] == '1':
                    sp1 = self.n2s[1000]
                else:
                    sp1 = ['%s %s'% (d, thousand) for d in self.n2s[int(s[0])]]
                spList.extend(['%s %s'% (s1, s2) for s1 in sp1 for s2 in sp2])
                return spList
                    
            elif s[1] == '0':
                # thousand ... or  ten ...
                if s[0] == '1':
                    sp1 = self.n2s[1000]
                else:
                    sp1 = ['%s %s'% (d, thousand) for d in self.n2s[int(s[0])]]
                sp2 = self.n2s[int(s[2:])]
                spList = ['%s %s'% (s1, s2) for s1 in sp1 for s2 in sp2]
                
                # twenty eleven:
                sp1 = self.n2s[int(s[0:2])]
                spList.extend(['%s %s'% (s1, s2) for s1 in sp1 for s2 in sp2])
                return spList
            else:
                sp1 = self.n2s[int(s[0:2])]
                if s[2] == '0':
                    sp2 = ['%s %s'% (oh, d) for d in self.n2s[int(s[3])]]
                else:
                    sp2 = self.n2s[int(s[2:4])]
                spList = ['%s %s'% (s1, s2) for s1 in sp1 for s2 in sp2]
                return spList
       
    def generateMixedListOfSpokenForms(self, s):
        """return spoken forms with at number places spoken forms replaced
            use for filenames with numbers in it
            
        if name startswith number_ skip it optionally
        if name endswith (number) skip it optionally
            
        if name startswith letter_ skip it optionally    
            
        """
        # make number _ at start and numbers in brackets at end of name optional
        # by recursing this function
        # eg 1_testing and website test (2)
        #
        t = reNumericUnderscore.sub('', s)
        t = reNumericBracketsEnd.sub('', t)
        t = reLetterUnderscore.sub('', t)

        if t == s:
            prevResult = None
        else:
            prevResult = self.generateMixedListOfSpokenForms(t)
            #print 'intermediate: %s'% prevResult   
            
        Result = None # end result
        result = []   # intermediate result
        
        s = reNonAlphaNumeric.sub(' ', s)
        s = reNumeric.split(s)
        s = filter(None, s)

        for item in s:
            item = item.strip()
            if not item:
                continue
            try:
                n = int(item)
            except ValueError:
                result.append(item)
            else:
                spok = self.getSpokenFormsList(n)
                if spok:
                    result.append(spok)
        for item in result:
            if type(item) == types.ListType:
                if Result:
                    Result = ['%s %s'% (i,j) for i in Result for j in item]
                else:
                    Result = [j for j in item]
            else:
                if Result:
                    Result = ['%s %s'% (r, item) for r in Result]
                else:
                    Result = [item]
        if prevResult:
            Result = prevResult + Result
        return Result
    
    def getDictOfMixedSpokenForms(self, Values):
        """return a dict with spoken forms (multiple) as keys, and the Values as values
        (in grammar excel)
        """
        if not Values:
            return {}
        D = {}
        for v in Values:
            L = self.generateMixedListOfSpokenForms(v)
            if not L:
                continue
            for key in L:
                D[key] = v
        return D
    
    def getCharFromSpoken(self, spoken, originalList=None):
        """try to retrieve the called character from the dict spoken2char in this class

        check result with originalList, 
        """
        first = self.spoken2char.get(spoken, None)
        if originalList is None:
            return first
        if first in originalList:
            return first
    
    def getPunctuationFromSpoken(self, spoken, originalList=None):
        """try to retrieve the called character from the dict spoken2char in this class

        check result with originalList, which may be any sequence
        """
        first = self.spoken2punct.get(spoken, None)
        if originalList:
            if first in originalList:
                return first
        else:
            return first

    def getNumberFromSpoken(self, spoken, originalList=None, asStr=None):
        """try to retrieve the called number from the dict s2n in this class

        check result with originalList, or try to make a number from spoken
        if asInt == True, return as str, otherwise return a int

        passing a list of words is handled in natlinkutilsbj.        
        """
        first = self.s2n.get(spoken, None)
        if originalList:
            orig = map(int, originalList)
            if first is None:
                try:
                    first = int(spoken)
                except ValueError:
                    pass
            if first != None and first in orig:
                if asStr:
                    first = str(first)
                return first
        else:
            # take result anyway:
            if first != None:
                if asStr:
                    first = str(first)
                return first
            # try is spoken represents a int:
            try:
                n = int(spoken)
                if asStr:
                    return str(n)
                else:
                    return n
            except ValueError:
                pass
    
    def filldictsAboveHundred(self, num):
        """make spoken forms for numbers above 100
        eg 360 returns ['three sixty', 'three hundred sixty']
        """
        if num <= 100:
            raise ValueError('numbers, fillDictsAboveHundred call with number > 100, not: %s'% num)
        if num > 1000:
            raise ValueError('numbers, fillDictsAboveHundred call with number <= 1000, not: %s'% num)
        prefixSection = 'prefixes'
        numbersSection = 'numbers'
        if num == 1000:
            thousand = ini.getList(prefixSection, 'thousand') or ['thousand']
            self.n2s[1000] = thousand
            for t in thousand:
                self.s2n[t] = 1000
            return
        self.n2s[num] = [str(num)]
        self.s2n[str(num)] = num
        return
        h, rest = num / 100, num%100
        hundred = ini.getList(prefixSection, 'hundred', None) or ['hundred']
        if rest:
            restspoken = ini.getList(numbersSection, str(rest), None)
            if not restspoken:
                return [str(num)]
        else:
            restspoken = ['']
        if num == 100:
            hspoken = ini.getList(numbersSection, str(100), None) or hundred
        elif h == 1:
            hspoken = ini.getList(numbersSection, str(100), None) or hundred
        else:
            hundredspoken = hundred[0]
            numspoken = ini.getList(numbersSection, str(h), None)
            if numspoken:
                # numbers + hundred or numbers:
                hspoken = [n + ' ' + hundredspoken for n in numspoken] + numspoken
            else:
                return [str(num)]
        spokenlist = [(a+ ' ' + b).strip() for a in hspoken for b in restspoken]
        self.n2s[num] = spokenlist
        for sp in spokenlist:
            self.s2n[sp] = num
            
    def sortedByNumbersValues(self, grammarsList, valueSpokenDict=None):
        """return sorted list if this is a numbers list (sorted by the number value)
        
        if valueSpokenDict == True: return the dict, like {1: ['one'], }
        otherwise return only the spoken forms like [ 'one', ...]
        
        If list contains items that do not go back to a number, return None
        
        """
        dec = {}
        for g in grammarsList:
            value = self.getNumberFromSpoken(g)
            if value is None:
                return
            dec.setdefault(value, []).append(g)
        if valueSpokenDict:
            return dec
        else:
            return reduce(operator.add, dec.values())
        return []
        

    ## function to give numerical list:
    def getNumberList(self, listName):
        """returns the list of numbers for inserting in a grammar
    
        The list can be predefined here, and even be specific for different
        language versions.
    
        If the list is not predefined, it is extracted here.
    examples:
        number1to3 gives: [1, 2, 3]
        0-20 gives: [0, 1, ..., 20]
        
        but number10to99 gives [10, 11, ..., 99]
        
    Note:
        0-360 or number1to360 gives [0, 10, ..., 360]
        """
        #print 'try to fill numbers list: "%s"'% listName
        try:
            return globals()[listName]
        except KeyError:
            pass
        
        # not found in predefined names, extract automatically:
        if listName[:6] == 'number':
            numbersSpec = listName[6:]
        elif listName[0] == 'n':
            numbersSpec = listName[1:]
        if numbersSpec.find('to') > 0:
            L = numbersSpec.split('to')
        elif '-' in numbersSpec:
            L = numbersSpec.split('-')
        if len(L) != 2:
            print 'getNumbersList, (1) seems not to be a valid definition of a numbers list: %s'% listName
            return []
        try:  
            n1 = int(L[0])
            n2 = int(L[1])
        except ValueError:
            print 'getNumbersList, (1) seems not to be a valid definition of a numbers list: %s'% listName
            return []
        
        if n1 == 0 and n2 == 0:
            print 'getNumbersList, (2) seems not to be a valid definition of a numbers list: %s'% listName
            return []
            
        if n1%10 == 0 and n2%10==0 and (n2 > 100 or n1 >= 10):
            L = range(n1, n2+1, 10)
        else:
            L = range(n1, n2+1)
        #return [str(i) for i in L]
        return L

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()