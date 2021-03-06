"""Unimacro grammar that controls/shows/traces state of other grammars

"""
__version__ = "$Rev: 569 $ on $Date: 2016-06-06 10:41:38 +0200 (ma, 06 jun 2016) $ by $Author: quintijn $"
# This file is part of a SourceForge project called "unimacro" see
# http://unimacro.SourceForge.net and http://qh.antenna.nl/unimacro
# (c) copyright 2003 see http://qh.antenna.nl/unimacro/aboutunimacro.html
#    or the file COPYRIGHT.txt in the natlink\natlink directory 
#
# _control.py, adapted version of_gramutils.py
# Author: Bart Jan van Os, Version: 1.0, nov 1999
# starting new version Quintijn Hoogenboom, August 2003

import string,os,sys,re # cPickle
import natlink
from natlinkutils import *
from natlinkmain import loadedFiles, unloadModule, loadModule
natbj = __import__('natlinkutilsbj')
natut = __import__('natlinkutils')
natqh = __import__('natlinkutilsqh')
import D_

# extra commands for controlling actions module:
try:
    actions = __import__('actions')
except ImportError:
    actions = None
    print 'warning: actions module not imported'
try:
    spokenforms = __import__('spokenforms')
except ImportError:
    spokenforms = None
    print 'warning: spokenforms module not imported'

tracecount = map(str, range(1, 10))

#Words that are 'filtered out' (actually: removed) in Filter Mode
#See below for the different modes
def ReadFilteredWords(Filename):
    #reads all words from the Filtered words file    
    #does not really belong here
    try:
        File=open(Filename,'r')
    except:
        return []
    Words = File.readlines()
    File.close
    for w in Words:
        Words[Words.index(w)]=w[:-1]
    freq={}        
    for w in Words:
        if freq.has_key(w):
            freq[w]=freq[w]+1
        else:
            freq[w]=1
    Words=freq.keys()
    return Words

FilteredWords = ['in','the','minimum','to','and','end','a','of','that','it',
                 'if', 'its', 'is', 'this', 'booth', 'on', 'with',"'s"]
#(taken from natlinkmain, to prevent import:)
baseDirectory = natqh.getUnimacroUserDirectory()
FilterFileName=baseDirectory+'\\filtered.txt'
FilteredWords=natbj.Union(FilteredWords, ReadFilteredWords(FilterFileName))


#Constants for the UtilGrammar
Normal=0
Training=1 #obsolete
Command=2 #obsolete
Filter=4
FilterTraining=5
Display=6


showAll = 1  # reset if no echo of exclusive commands is wished
#voicecodeHome = None
#if 'VCODE_HOME' in os.environ:
#    voicecodeHome = os.environ['VCODE_HOME']
#    if os.path.isdir(voicecodeHome):
#        for subFolder in ('Admin', 'Config', 'Mediator'):
#            newFolder = os.path.join(voicecodeHome, subFolder)
#            if os.path.isdir(newFolder) and newFolder not in sys.path:
#                sys.path.append(newFolder)
#                print 'appending to sys.path: %s'% newFolder
#    else:
#        print '_control: VCODE_HOME points NOT to a directory: %s'% voicecodeHome
#        voicecodeHome = None
        

ancestor = natbj.IniGrammar
class UtilGrammar(ancestor):
    language = natqh.getLanguage()
    iniIgnoreGrammarLists = ['gramnames', 'tracecount', 'message'] # are set in this module

    name = 'control'
##    normalSet = ['show', 'edit', 'trace', 'switch', 'message']
##    exclusiveSet = ['showexclusive', 'message']
    # commands for controlling module actions
    specialList = []
    if actions:
        specialList.append("actions")
    if spokenforms:
        specialList.append("'spoken forms'")
    if specialList:
        specials = "|" + '|'.join(specialList)
    else:
        specials = ""
    
    gramRules = ['show', 'edit', 'switch', 'showexclusive', 'resetexclusive', 'checkalphabet', 'message']
    gramDict = {}
    gramDict['show'] = """<show> exported = show ((all|active) grammars |
                        {gramnames} | (grammar|inifile) {gramnames}
                         """ + specials + """);"""
    gramDict['edit'] = """<edit> exported = edit ({gramnames}| (grammar|inifile) {gramnames}"""+ specials +""");"""
    gramDict['switch'] = """<switch> exported = switch ((on|off) ((all grammars)|{gramnames}|grammar {gramnames})|
                            ((all grammars)|{gramnames}|grammar {gramnames})(on|off));"""
    gramDict['showexclusive'] = """<showexclusive> exported = show (exclusive |exclusive grammars);"""
    gramDict['resetexclusive'] = """<resetexclusive> exported = reset (exclusive | exclusive grammars);"""
    gramDict['checkalphabet'] = """<checkalphabet> exported = check alphabet;"""
    gramDict['message'] = """<message> exported = {message};"""

    gramSpec = []
    assert set(gramRules) == set(gramDict.keys())

    if language == 'nld':
        gramDict['checkalphabet'] = """<checkalphabet> exported = controleer alfabet;"""

    for rulename in gramRules:
        gramSpec.append(gramDict[rulename])
    
    
    ## extra: the trace rule:    
    if specials:
        specials2 = specials[1:]  # remove initial "|" (at show it is  "| actions | 'spoken forms'", here it is
                                  #     "actions | 'spoken forms'" only, because gramnames etc are not implemented
                                  #     for tracing)
        traceSpecial = """<trace> exported = trace (("""+ specials2 +""") |
                              ((on|off| {tracecount})("""+ specials2 +""")) |
                              (("""+ specials2 +""") (on|off|{tracecount}))) ;"""
        gramSpec.append(traceSpecial) # add trace for actions of spoken forms (latter not implemented)


    Mode = Normal
    LastMode = Normal
    CurrentWord = 0
    Repeat = 0

    def initialize(self):
        global loadedNames
        # temp set allResults to 0, disabling the messages trick:
        if not self.load(self.gramSpec, allResults=showAll):
            return None
        natbj.RegisterControlObject(self)
        self.emptyList('message')
        self.setList('gramnames', natbj.loadedGrammars.keys())
        self.setNumbersList('tracecount', tracecount)
        
        self.activateAll()
        self.setMode(Normal)
        self.startExclusive = self.exclusive # exclusive state at start of recognition!
##        if natqh.getUser() == 'martijn':
##            print 'martijn, set exclusive %s'% self.name
##            self.setExclusive(1)

    def unload(self):
        natbj.UnRegisterControlObject(self)
        ancestor.unload(self)

    def gotBegin(self, moduleInfo):
        #Now is the time to get the names of the grammar objects and
        # activate the list for the <ShowTrainGrammar> rule
        if natbj.grammarsChanged:
            prevSet = set(self.Lists['gramnames'])
            newSet = set(natbj.loadedGrammars.keys())
            if prevSet != newSet:
                if newSet - prevSet:
                    print '_control, added Unimacro grammar(s): %s'% list(newSet - prevSet)
                if prevSet - newSet:
                    print '_control, removed Unimacro grammar(s): %s'% list(prevSet - newSet)
                self.setList('gramnames', list(newSet))
            natbj.ClearGrammarsChangedFlag()
        if self.checkForChanges:
            self.checkInifile()
            
        self.startExclusive = self.exclusive # exclusive state at start of recognition!

    def gotResultsInit(self,words,fullResults):
        if self.mayBeSwitchedOn == 'exclusive':
            print 'recog controle, switch off mic: %s'% words
            natbj.SetMic('off')
        if self.exclusive:
            try:
                self.DisplayMessage('<%s>'% ' '.join(words))
            except natlink.NatError:
                print 'DisplayMessage failed: "%s"'% ' '.join(words)

    def resetExclusiveMode(self):
        """no activateAll, do nothing, this grammar follows the last unexclusive grammar
        """
        pass
    
    def setExclusiveMode(self):
        """no nothing, control follows other exclusive grammars
        """
        pass
    
    def gotResultsObject(self,recogType,resObj):
        if natbj.IsDisplayingMessage:
            return
        mes = natbj.GetPendingMessage()
        if mes:
            mes = '\n\n'.join(mes)
            natbj.ClearPendingMessage()
            self.DisplayMessage(mes)
            return
        natqh.doPendingBringUps()  # if there were
        natqh.doPendingExecScripts()  # if there were

        if self.startExclusive and self.exclusive and showAll:
            # display recognition results for exclusive grammars
            # with showAll = None (in top of this file), you can disable this feature
            if recogType == 'reject':
                URName = ''
                exclGram = natbj.exclusiveGrammars
                exclGramKeys = exclGram.keys()
                if len(exclGramKeys) > 1 and self.name in exclGramKeys:
                    exclGramKeys.remove(self.name)
                if len(exclGramKeys) > 1:
                    URName = ', '.join(exclGramKeys)
                k = exclGramKeys[0]
                v = exclGram[k]
                # UE stands for unrecognised exclusive:
                # if more exclusive grammars,
                # the last one is taken
                URName = URName or v[2]   # combined name or last rule of excl grammar
                msg = '<'+URName+': ???>'
                self.DisplayMessage(msg, alsoPrint=0)

    #Utilities for Filter Modes and other special modes
    def setMode(self,NewMode):
        self.LastMode = self.Mode
        self.Mode = NewMode

    def restoreMode(self):
        self.Mode = self.LastMode
        
    def gotResults_checkalphabet(self,words,fullResults):
        """check the exact spoken versions of the alphabet in spokenforms
        """
        import spokenforms
        version = natqh.getDNSVersion()
        spok = spokenforms.SpokenForms(self.language, version)
        alph = 'alphabet'
        ini = spokenforms.ini
        for letter in string.ascii_lowercase:
            spoken = ini.get(alph, letter, '')
            if not spoken:
                print 'fill in in "%s_spokenform.ini", [alphabet] spoken for: "%s"'% (self.language, letter)
                continue
            if version < 11:
                normalform = '%s\\%s'% (letter.upper(), spoken)
            else:
                normalform = '%s\\letter\\%s'% (letter.upper(), spoken)
            try:
                natlink.recognitionMimic([normalform])
            except natlink.MimicFailed:
                print 'invalid spoken form "%s" for "%s"'% (spoken, letter)
                if spoken == spoken.lower():
                    spoken = spoken.capitalize()
                    trying = 'try capitalized variant'
                elif spoken == spoken.capitalize():
                    spoken = spoken.lower()
                    trying = 'try lowercase variant'
                else:
                    continue
                if version < 11:
                    normalform = '%s\\%s'% (letter.upper(), spoken)
                else:
                    normalform = '%s\\letter\\%s'% (letter.upper(), spoken)
                try:
                    natlink.recognitionMimic([normalform])
                except natlink.MimicFailed:
                    print '%s fails also: "%s" for "%s"'% (trying, spoken, letter)
                else:
                    print 'alphabet section is corrected with: "%s = %s"'% (letter, spoken)
                    ini.set(alph, letter, spoken)
        ini.writeIfChanged()
           

    def gotResults_trace(self,words,fullResults):
        print 'control, trace: %s'% words
        traceNumList = self.getNumbersFromSpoken(words) # returns a string or None
        if traceNumList:
            traceNum = int(traceNumList[0])
        else:
            traceNum = None

        if self.hasCommon(words, 'actions'):
            if self.hasCommon(words, 'show'):
                actions.debugActionsShow()
            elif self.hasCommon(words, 'off'):
                actions.debugActions(0)
            elif self.hasCommon(words, 'on'):
                actions.debugActions(1)
            elif traceNum:
                actions.debugActions(traceNum)
            else:
                actions.debugActions(1)
        elif self.hasCommon(words, 'spoken forms'):
            print "no tracing possible for spoken forms"

    #def gotResults_voicecode(self,words,fullResults):
    #    """switch on if requirements are fulfilled
    #
    #    voicecodeHome must exist
    #    emacs must be in foreground
    #    """
    #    wxmed = os.path.join(voicecodeHome, 'mediator', 'wxmediator.py')
    #    if os.path.isfile(wxmed):
    #        commandLine = r"%spython.exe %s > D:\foo1.txt >> D:\foo2.txt"% (sys.prefix, wxmed)
    #        os.system(commandLine)
    #    else:
    #        print 'not a file: %s'% wxmed
            
    def gotResults_switch(self,words,fullResults):
        #print 'control, switch: %s'% words
        if self.hasCommon(words, 'on'):
            funcName = 'switchOn'
        elif self.hasCommon(words, 'off'):
            funcName = 'switchOff'
        else:
            try:
                t = {'nld': '<%s: ongeldig schakel-commando>'% self.GetName()}[self.language]
            except:            
                t = '<%s: invalid switch command>'% self.GetName()
            self.DisplayMessage(t)
            return
        if self.hasCommon(words, 'all grammars'):
            #print '%s all grammars:'% funcName
            for g in natbj.loadedGrammars:
                gram = natbj.loadedGrammars[g]
                if gram == self:
                    print 'no need to switch on _control (should always be on...)'
                else:
                    self.switch(gram, g, funcName)
        else:
            gramname = self.hasCommon(words, natbj.loadedGrammars.keys())
            if gramname:
                gram = natbj.loadedGrammars[gramname]
                if gram == self:
                    print 'No %s of grammar _control needed or allowed!'% funcName
                else:
                    self.switch(gram, gramname, funcName)
            else:
                print 'no grammar name found: %s'% gramname

    def switch(self, gram, gramName, funcName):
        """switch on or off grammar, and set in inifile,
        
        force the setting!
        """
        func = getattr(gram, funcName)
        # in case manual changes were done:
        #gram.checkInifile()
        if funcName == 'switchOn':
            self.checkInifile()
            if not gram.mayBeSwitchedOn:
                gram.ini.set('general', 'initial on', 1)
                #gram.mayBeSwitchedOn = 1
                gram.ini.write()
                print 'reload grammar "%s" after 1 seconds (switching on)'% gram.getName()
                natqh.Wait(1)
            else:
                print 'reload grammar "%s"'% gram.getName()
                
            modName = gram.__module__
            unloadModule(modName)
            loadModule(modName)
            #print 'reloaded "%s"'% modName
            return 1
        elif funcName == 'switchOff':
            if gram.mayBeSwitchedOn:
                gram.ini.set('general', 'initial on', 0)
                gram.ini.writeIfChanged()
                gram.mayBeSwitchedOn = 0
                result =  func()
                print 'grammar "%s" switched off'% gram.getName()
            else:
                result = func()
                print 'grammar "%s" switched off (again)'% gram.getName()
        else:
            raise ValueError('switching on/off should have as function "switchOn" or "switchOff", not: %s'% func)

            
    def gotResults_showexclusive(self,words,fullResults):

        All = 0
        name = 'exclusive grammars'
        if len(name)>0:                
            Start=(string.join(name),[])
        else:
            Start=()
        # fix state at this moment (in case of Active grammars popup)
        if natbj.exclusiveGrammars:
            Exclusive = 1
            self.BrowsePrepare(Start, All, Exclusive)
            T = ['exclusive grammars:']
            for e in natbj.exclusiveGrammars:
                T.append('\t'+e)
            T.append('\t'+self.name)
            T.append('')
            T.append('')
            T.append("Note: exclusive mode is still on, so the buttons of this dialog cannot be clicked by voice.")
            T.append('')
            T.append("Reset the exclusive mode by toggling the microphone")
            T.append('or by calling the command "reset exclusive mode"')
            T.append('')
            T.append("Show details of exclusive Unimacro grammars?")
            msg = '\n'.join(T)
            if actions.YesNo(msg, "Exclusive grammars", icon="information", defaultToSecondButton=1):
                self.BrowseShow()
        else:
            self.DisplayMessage('no exclusive grammars')
            

    def gotResults_resetexclusive(self,words,fullResults):
        print 'reset exclusive'
        if natbj.exclusiveGrammars:
            T = ['exclusive grammars:']
            for e in natbj.exclusiveGrammars:
                T.append(e)
            T.append(self.name)
            T.append('... reset exclusive mode')
            self.DisplayMessage(' '.join(T))
            natbj.GlobalResetExclusiveMode()
            natqh.Wait(1)
            self.DisplayMessage('reset exclusive mode OK')
        else:
            self.DisplayMessage('no exclusive grammars')
        
##    def setExclusive(self, state):
##        """control grammar, do NOT register, set and maintain state
##
##        special position because of ControlGrammar
##        """
##        print 'control set exclusive: %s'% state
##        if state == None:
##            return
##        if state == self.exclusive:
##            return
##        print 'control, (re)set exclusive: %s'% state
##        self.gramObj.setExclusive(state)
##        self.exclusive = state

    def gotResults_show(self,words,fullResults):
        # special case for actions:
        if self.hasCommon(words, 'actions'):
            actions.showActions(comingFrom=self, name="show actions")
            return
        if self.hasCommon(words, 'spoken forms'):
            spokenforms.showSpokenForms(comingFrom=self, name="show spoken forms", language=self.language)
            return
        Exclusive = 0
        if natbj.exclusiveGrammars:
            print 'exclusive grammars (+ control) are: %s'% ' '.join(natbj.exclusiveGrammars.keys())
            self.gotResults_showexclusive(words, fullResults)
            return

        grammars = natbj.loadedGrammars
        gramNames = grammars.keys()
        gramName = self.hasCommon(words, gramNames)
        if gramName:
            grammar = grammars[gramName]
            if not grammar.isActive:
                # off, show message:
                self.offInfo(grammar)
                return
            if not self.hasCommon(words, 'grammar'):
                grammar.showInifile()
                return
                try:
                    grammar.showInifile()
                    return
                except AttributeError:
                    try:
                        grammar.showGrammar()
                        return
                    except AttributeError:
                        pass
        
        # now show the grammar in the browser application:      
        if gramName:
            name = [gramName]
        else:
            name = words[1:-1]
        
        All=1
        if len(name)>0:
            All=self.hasCommon(words, 'all')
        Active = self.hasCommon(words, 'active')
        if Active:
            All = 0
        elif All:
            All = 1
        
        if len(name)>0:                
            Start=(string.join(name),[])
        else:
            Start=()
        # fix state at this moment (in case of Active grammars popup)
        self.BrowsePrepare(Start, All, Exclusive)
        if Active:
            #print 'collect and show active, non-active and non-Unimacro grammars'
            activeGrammars, inactiveGrammars, switchedOffGrammars = [], [], []
            otherGrammars = loadedFiles.keys()  # start with all keys from natlinkmain
            for g in natbj.loadedGrammars:
                gram = natbj.loadedGrammars[g]
                result = getattr(gram, 'isActive')
                modName = gram.__module__
                #print 'gram: %s, modName: %s, result: %s'% (gram, modName, result)
                if result:
                    activeGrammars.append(g)
                    if modName in otherGrammars:
                        otherGrammars.remove(modName)
                    else:
                        print 'cannot remove from otherGrammars: %s'% modName
                elif result == 0:
                    maySwitchOn = gram.mayBeSwitchedOn
                    if maySwitchOn:
                        inactiveGrammars.append(g)
                    else:
                        switchedOffGrammars.append(g)
                    #print 'gram: %s, name: %s'% (gram, modName)
                    if modName in otherGrammars:
                        otherGrammars.remove(modName)
                    else:
                        print 'cannot remove from otherGrammars: %s'% modName
            if not activeGrammars:
                msg = 'No Unimacro grammars are active'
            elif activeGrammars == [self.name]:
                msg = 'No grammars are active (apart from "%s")'% self.name
            elif inactiveGrammars or switchedOffGrammars:
                msg = 'Active Unimacro grammars:\n' + ', '.join(activeGrammars)
            else:
                msg = 'All Unimacro grammars are active:\n' + ', '.join(activeGrammars)

            if inactiveGrammars:
                inactive = 'Inactive (but "Switched on") grammars:\n' + ', '.join(inactiveGrammars)
                msg += '\n\n' + inactive
                
            if switchedOffGrammars:
                switchedoff = '"Switched off" grammars:\n' + ', '.join(switchedOffGrammars)
                msg += '\n\n' + switchedoff

            if otherGrammars:
                other = 'Other grammars (outside Unimacro):\n' + ', '.join(otherGrammars)
                msg = msg + '\n\n' + other
            if activeGrammars and activeGrammars != [self.name]:
                msg = msg + '\n\n' + "Show details of active Unimacro grammars?"
                if not actions.YesNo(msg, "Active grammars", icon="information", defaultToSecondButton=1):
                    return
            else:
                msg = msg + '\n\n' + 'Activate with\n\t"switch on <grammar name>" or \n\t"switch on all grammars".'
                actions.Message(msg, "No active Unimacro grammars", icon="information")
                return


        self.BrowseShow()
        

    def gotResults_edit(self,words,fullResults):
        # special case for actions:
        if self.hasCommon(words, 'actions'):
            actions.editActions(comingFrom=self, name="edit actions")
            return
        elif self.hasCommon(words, 'spoken forms'):
            actions.Message('Warning: spoken forms lists do NOT refresh automatically.\n\nA restart of NatSpeak is required after you edited the "spokenforms.ini" file')
            spokenforms.editSpokenForms(comingFrom=self, name="edit spoken forms", language=self.language)
            return

        grammars = natbj.loadedGrammars
        gramNames = grammars.keys()
        gramName = self.hasCommon(words[-1:], gramNames)
        if gramName:
            grammar = grammars[gramName]
            if self.hasCommon(words, 'grammar'):
                module = grammar.__module__
                filename = natqh.getModuleFilename(module)
                #print 'open for edit file: %s'% filename
                self.openFileDefault(filename, mode="edit", name='edit grammar %s'% gramName)
                natqh.setCheckForGrammarChanges(1)
            else:
                # edit the inifile
                try:
                    grammar.switchOn()
                    grammar.editInifile()
                except AttributeError:
                    self.DisplayMessage('grammar "%s" has no method "editInifile"'% gramName)
                    return
        else:
            print 'no grammar name found'

    def switchOff(self, **kw):
        """overload, this grammar never switches off

        """        
        print 'remains switched on: %s' % self

    def switchOn(self, **kw):
        """overload, just switch on

        """
        self.activateAll()
        return 1


    def offInfo(self, grammar):
        """gives a nice message that the grammar is switched off

        Gives also information on how to switch on.

        """        
        name = grammar.getName()
        try:
            t = {'nld': ['Grammatica "%s" is uitgeschakeld'% name,
                         '', 
                         '"Schakel in %s" om te activeren'% name]}[self.language]
            title = {'nld': 'Grammatica %s'% name}[self.language]
        except KeyError:
            t = ['Grammar "%s" is switched off'% name,
                 '"Switch On Grammar %s" to activate'% name]
            title = 'Grammar %s'% name
        if natbj.loadedMessageGrammar:
            t = ';  '.join(t)
            self.DisplayMessage(t)
        else:
            t = t.replace('; ', '\n')
            actions.Message(t)

class MessageDictGrammar(natut.DictGramBase):
    def __init__(self):
        natut.DictGramBase.__init__(self)

    def initialize(self):
        print 'initializing/loading DictGrammar!!'
        self.load()
        natbj.RegisterMessageObject(self)

    def unload(self):
        natbj.UnRegisterMessageObject(self)
        natut.DictGramBase.unload(self)
        
    def gotResults(self, words):
        pass
        #print 'messageDictGrammar: heard dictation:  %s '% words


# standard stuff Joel (adapted for possible empty gramSpec, QH, unimacro)
messageDictGrammar = MessageDictGrammar()
messageDictGrammar.initialize()
print 'messageDictGrammar initialized'


# standard stuff Joel (adapted for possible empty gramSpec, QH, unimacro)
utilGrammar = UtilGrammar()
if utilGrammar.gramSpec:
    utilGrammar.initialize()
    
else:
    print 'grammar _control has no specification for this language---------'
    utilGrammar = None

def unload():
    global utilGrammar, messageDictGrammar
    if utilGrammar: utilGrammar.unload()
    utilGrammar = None
    if messageDictGrammar:
        messageDictGrammar.unload()
    messageDictGrammar = None
    
def changeCallback(type,args):
    global utilGrammar
    # Whenever the mic is turned off, the intercept mode is turned off.
    # and any special modes, except training
    if ((type == 'mic') and (args=='on')):
        return   # check WAS in natlinkmain...
    natbj.GlobalResetExclusiveMode()
    if utilGrammar:    
        utilGrammar.setMode(Normal)
        #This could be done anywhere, but not within natlinkutilsbj
        #Because that module is 'imported from'.
        if utilGrammar.interceptMode:
            CallAllGrammarObjects('setInterceptMode',[0])
        
        
    
