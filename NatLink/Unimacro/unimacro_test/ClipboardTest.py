#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 1999 by Joel Gould
#   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#
#   This script performs some basic tests of the NatLink system.  Dragon
#   NaturallySpeaking should be running with nothing in the editor window
#   (that you want to preserve) before these tests are run.
#   performed.
natqh = __import__('natlinkutilsqh')
natut = __import__('natlinkutils')
import actions
reload(actions)

import unittest
import UnimacroTestHelpers



##class UnimacroBasicTest(TestCaseWithHelpers.TestCaseWithHelpers):
class ClipboardTest(UnimacroTestHelpers.UnimacroTestHelpers):
      
    def setUp(self):
        actions.doAction("BRINGUP dragonpad; <<selectall>><<delete>>")

    def tearDown(self):
        actions.doAction("BRINGUP dragonpad; KW")
        
    def test_Something_in_unimacro(self):
        testWindowContents = self.doTestWindowContents
        actions.doKeystroke("testing")
        expected = "testing"
        testWindowContents(expected, "Something testing in ClipboardTest went wrong")
        # tearDown when DragonPad is already closed:
        actions.doAction("KW")
 
    def test_Copy_and_paste_clipboard(self):
        testWindowContents = self.doTestWindowContents
        # This test handles several copy and paste meta actions.
        actions.doKeystroke("testing")
        actions.doAction("<<selectall>><<copy>>{ctrl+end}")
        actions.doAction("<<paste>>")
        # Note in DragonPad it apparently endswith "\r\n"...
        expected = "testingtesting\n"  # natqh getClipboard removes '\r', which was in natlink.getClipboard
        testWindowContents(expected, "Something copying and pasting went wrong")

    def test_Empty_clipboard(self):
        testWindowContents = self.doTestWindowContents
        # This test first empties the clipboard, copies with no selection on
##         and tests if the clipboard is empty.
##         If it is so it restores the previous clipboard and exits
        testActionResult = self.doTestActionResult
        actions.doKeystroke("testing")
        actions.doAction("<<selectall>><<copy>>{ctrl+end}")
        actions.doAction('CLIPSAVE')
        t = natqh.getClipboard()
        self.assert_equal("", t, "Clipboard should be empty now" ) 
        actions.doAction("<<copy>>")
        t = natqh.getClipboard()
        self.assert_equal("", t, "Clipboard should still be empty" ) 
        testActionResult(0, "CLIPISNOTEMPTY")
        ## with empty clipboard restore goes automatically: 
##        actions.doAction("CLIPRESTORE")
        t = natqh.getClipboard()
        self.assert_equal("testing", t, "Clipboard should filled again" ) 

    def test_Non_Empty_clipboard_and_restore(self):
        testWindowContents = self.doTestWindowContents
        testActionResult = self.doTestActionResult
##         This test saves the clipboard, copies two letters
##         so the test CLIPISNOTEMPTY returns true
##         and the clipboard should be restored next
        actions.doKeystroke("testing")
        actions.doAction("<<selectall>><<copy>>{ctrl+end}")
        actions.doAction('CLIPSAVE')
        t = natqh.getClipboard()
        self.assert_equal("", t, "Clipboard should be empty now" ) 
        actions.doAction("{shift+left 2}<<copy>>{ctrl+end}")
        t = natqh.getClipboard()
        self.assert_equal("ng", t, "Clipboard should contain two letters now" ) 
        testActionResult(1, "CLIPISNOTEMPTY")
        actions.doAction("CLIPRESTORE")
        t = natqh.getClipboard()
        self.assert_equal("testing", t, "Clipboard should filled now" ) 

    def test_complete_CLIP_action(self):
        testWindowContents = self.doTestWindowContents
        testActionResult = self.doTestActionResult
##         This test saves the clipboard, copies two letters
##         so the test CLIPISNOTEMPTY returns true
##         and the clipboard should be restored next
##         do not forget CLIPRESTORE!   
        actions.doKeystroke("testing")
        actions.doAction("<<selectall>><<copy>>{ctrl+end}")
        actions.doAction('CLIPSAVE; {shift+left 4}<<copy>>{ctrl+end}; CLIPISNOTEMPTY; {ctrl+end}abcd<<paste>>defg; CLIPRESTORE; <<paste>>')
        testWindowContents("testingabcdtingdefgtesting")

    def test_NON_complete_CLIP_action(self):
        testWindowContents = self.doTestWindowContents
        testActionResult = self.doTestActionResult
##         This test saves the clipboard,breaks off so does not return the ending
        actions.doKeystroke("testing")
        actions.doAction("<<selectall>><<copy>>{ctrl+end}")
        actions.doAction('CLIPSAVE; <<copy>>{ctrl+end}; CLIPISNOTEMPTY; {ctrl+end}abcd<<paste>>defg; CLIPRESTORE; <<paste>>')
        testWindowContents("testing")
        t = natqh.getClipboard()
        # ??? x after testing in test procedure artefact::
        self.assert_equal("testing", t, "Clipboard should filled again now" ) 
        

# no main statement, run from command in _unimacrotest.py.

