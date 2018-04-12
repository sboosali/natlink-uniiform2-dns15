"""actions from application frescobaldi, the editor for lilypond music note printing

"""
from actionbases import AllActions
import pprint
from natlinkutils import playString
import natlinkutilsqh as natqh
import time

class FrescobaldiActions(AllActions):
    def __init__(self, progInfo):
        AllActions.__init__(self, progInfo)
        
    def hasSelection(self):
        """returns the text if text is selected, otherwise None
        """
        natqh.saveClipboard()
        playString("{ctrl+c}")
        t = natqh.getClipboard() or None
        natqh.restoreClipboard()
        return t

    def getPrevNext(self, n=1):
        """return character to the left and to the right of the cursor
        assume no selection active.
        normally return cursor in same position
        """
        natqh.saveClipboard()
        playString("{left %s}"% n)
        playString("{shift+right %s}"% (n*2,))
        playString("{ctrl+c}")
        playString("{left}{right %s}"% n)
        result = natqh.getClipboard()
        natqh.restoreClipboard()
        if len(result) == 2:
            return result[0], result[1]
        elif result == '\n':
            print 'getPrevNext, assume at end of file...'
            # assume at end of file, could also be begin of file, but too rare too handle
            playString("{right}")
            return result, result
        else:
            # print 'getPrevNext, len not 2: %s, (%s)'% (len(result), repr(result))
            return "", result
        
    def getNextLine(self, n=1):
        """get line following the cursor

        n > 1, take more lines down for a larger range
        """
        playString("{shift+down %s}{ctrl+c}"% n)
        natqh.Wait()        
        result = natqh.getClipboard()
        nup = result.count('\n')
        if nup:
            playString("{shift+up %s}"% nup)
        return result
        
    def getPrevLine(self, n=1):
        """get line preceding the cursor
        
        more lines possible, if n > 1
        """
        playString("{shift+up %s}{ctrl+c}"% n)
        natqh.Wait()        
        result = natqh.getClipboard()
        ndown = result.count('\n')
        if ndown:
            playString("{shift+down %s}"% ndown)
        return result
        
        
                   
    
if __name__ == '__main__':
    # search all frescobaldi instances and dump the controls:
    # does not give a useful result
    import messagefunctions as mf
    # trying to hack into frescobaldi, no luck (yet)
    tw = mf.findTopWindows(wantedText="frescobaldi")
    for t in tw:
        dw = mf.dumpWindow(t)
        if dw:
            print 'top: %s, length dump: %s'% (t, len(dw))
            for subwindow in dw:
                print 'sub: %s'% subwindow
                hndle = subwindow[0]
                subhndle = subwindow[-1][0]
                try:
                    numl = mf.getNumberOfLines(hndle, classname='Scintilla')
                    print 'hndle: %s, subhndle: %s, numlines: %s'% (hndle, subhndle, numl)
                except TypeError:
                    print 'wrong hndle: %s'% subhndle
        else:
            print 'try topwindow'
            hndle = t
            try:
                numl = mf.getNumberOfLines(hndle, classname='Scintilla')
                print 'top hndle: %s, numlines: %s'% (hndle, numl)
            except TypeError:
                print 'wrong hndle: %s'% subhndle
            
            print 'top: %s, mp dumpwindow'% t
        # pprint.pprint( mf.dumpWindow(t) )
    progInfo = ('frescobaldi', 'naamloos', 'top', 787682)
    fa = FrescobaldiActions( progInfo )
        