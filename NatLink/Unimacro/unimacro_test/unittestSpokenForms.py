#
# Python Macro Language for Dragon NaturallySpeaking
#   (c) Copyright 1999 by Joel Gould
#   Portions (c) Copyright 1999 by Dragon Systems, Inc.
#
# unittestNumbersSpokenForms.py
# testing the Unimacro mechanism to switch back and forth
# with numbers to spoken forms
# see spokenforms.py in the Unimacro directory
import sys, os, os.path

#need this here (hard coded, sorry) for it can be run without NatSpeak being on
extraPaths = r"C:\natlink\unimacro", r"D:\natlink\unimacro"
for extraPath in extraPaths:
    if os.path.isdir(extraPath):
        if extraPath not in sys.path:
            sys.path.append(extraPath)
import spokenforms, inivars
import sys, unittest
import os
import os.path
import time, pprint
import TestCaseWithHelpers
class TestError(Exception):pass

DNSVersion = 12  # can test in other versions too

expected_n2s =    {0: ['oh', 'zero'],
 1: ['one'],
 2: ['two', 'too'],
 3: ['three'],
 4: ['four', 'for'],
 5: ['five'],
 6: ['six'],
 7: ['seven'],
 8: ['eight'],
 9: ['nine'],
 10: ['ten'],
 11: ['eleven'],
 12: ['twelve'],
 13: ['thirteen'],
 14: ['fourteen'],
 15: ['fifteen'],
 16: ['sixteen'],
 17: ['seventeen'],
 18: ['eighteen'],
 19: ['nineteen'],
 20: ['twenty'],
 21: ['twenty-one'],
 22: ['twenty-two'],
 23: ['twenty-three'],
 24: ['twenty-four'],
 25: ['twenty-five'],
 26: ['twenty-six'],
 27: ['twenty-seven'],
 28: ['twenty-eight'],
 29: ['twenty-nine'],
 30: ['thirty'],
 31: ['thirty-one'],
 32: ['thirty-two'],
 33: ['thirty-three'],
 34: ['thirty-four'],
 35: ['thirty-five'],
 36: ['thirty-six'],
 37: ['thirty-seven'],
 38: ['thirty-eight'],
 39: ['thirty-nine'],
 40: ['forty'],
 41: ['forty-one'],
 42: ['forty-two'],
 43: ['forty-three'],
 44: ['forty-four'],
 45: ['forty-five'],
 46: ['forty-six'],
 47: ['forty-seven'],
 48: ['forty-eight'],
 49: ['forty-nine'],
 50: ['fifty'],
 51: ['fifty-one'],
 52: ['fifty-two'],
 53: ['fifty-three'],
 54: ['fifty-four'],
 55: ['fifty-five'],
 56: ['fifty-six'],
 57: ['fifty-seven'],
 58: ['fifty-eight'],
 59: ['fifty-nine'],
 60: ['sixty'],
 61: ['sixty-one'],
 62: ['sixty-two'],
 63: ['sixty-three'],
 64: ['sixty-four'],
 65: ['sixty-five'],
 66: ['sixty-six'],
 67: ['sixty-seven'],
 68: ['sixty-eight'],
 69: ['sixty-nine'],
 70: ['seventy'],
 71: ['seventy-one'],
 72: ['seventy-two'],
 73: ['seventy-three'],
 74: ['seventy-four'],
 75: ['seventy-five'],
 76: ['seventy-six'],
 77: ['seventy-seven'],
 78: ['seventy-eight'],
 79: ['seventy-nine'],
 80: ['eighty'],
 81: ['eighty-one'],
 82: ['eighty-two'],
 83: ['eighty-three'],
 84: ['eighty-four'],
 85: ['eighty-five'],
 86: ['eighty-six'],
 87: ['eighty-seven'],
 88: ['eighty-eight'],
 89: ['eighty-nine'],
 90: ['ninety'],
 91: ['ninety-one'],
 92: ['ninety-two'],
 93: ['ninety-three'],
 94: ['ninety-four'],
 95: ['ninety-five'],
 96: ['ninety-six'],
 97: ['ninety-seven'],
 98: ['ninety-eight'],
 99: ['ninety-nine'],
 100: ['hundred', 'one hundred'],
 1000: ['thousand', 'one thousand'],
 10000: ['ten thousand'],
 100000: ['hundredthousand'],
 1000000: ['million', 'one million']}

expected_s2n =  {'eight': 8,
 'eighteen': 18,
 'eighty': 80,
 'eighty-eight': 88,
 'eighty-five': 85,
 'eighty-four': 84,
 'eighty-nine': 89,
 'eighty-one': 81,
 'eighty-seven': 87,
 'eighty-six': 86,
 'eighty-three': 83,
 'eighty-two': 82,
 'eleven': 11,
 'fifteen': 15,
 'fifty': 50,
 'fifty-eight': 58,
 'fifty-five': 55,
 'fifty-four': 54,
 'fifty-nine': 59,
 'fifty-one': 51,
 'fifty-seven': 57,
 'fifty-six': 56,
 'fifty-three': 53,
 'fifty-two': 52,
 'five': 5,
 'for': 4,
 'forty': 40,
 'forty-eight': 48,
 'forty-five': 45,
 'forty-four': 44,
 'forty-nine': 49,
 'forty-one': 41,
 'forty-seven': 47,
 'forty-six': 46,
 'forty-three': 43,
 'forty-two': 42,
 'four': 4,
 'fourteen': 14,
 'hundred': 100,
 'hundredthousand': 100000,
 'million': 1000000,
 'nine': 9,
 'nineteen': 19,
 'ninety': 90,
 'ninety-eight': 98,
 'ninety-five': 95,
 'ninety-four': 94,
 'ninety-nine': 99,
 'ninety-one': 91,
 'ninety-seven': 97,
 'ninety-six': 96,
 'ninety-three': 93,
 'ninety-two': 92,
 'oh': 0,
 'one': 1,
 'one hundred': 100,
 'one million': 1000000,
 'one thousand': 1000,
 'seven': 7,
 'seventeen': 17,
 'seventy': 70,
 'seventy-eight': 78,
 'seventy-five': 75,
 'seventy-four': 74,
 'seventy-nine': 79,
 'seventy-one': 71,
 'seventy-seven': 77,
 'seventy-six': 76,
 'seventy-three': 73,
 'seventy-two': 72,
 'six': 6,
 'sixteen': 16,
 'sixty': 60,
 'sixty-eight': 68,
 'sixty-five': 65,
 'sixty-four': 64,
 'sixty-nine': 69,
 'sixty-one': 61,
 'sixty-seven': 67,
 'sixty-six': 66,
 'sixty-three': 63,
 'sixty-two': 62,
 'ten': 10,
 'ten thousand': 10000,
 'thirteen': 13,
 'thirty': 30,
 'thirty-eight': 38,
 'thirty-five': 35,
 'thirty-four': 34,
 'thirty-nine': 39,
 'thirty-one': 31,
 'thirty-seven': 37,
 'thirty-six': 36,
 'thirty-three': 33,
 'thirty-two': 32,
 'thousand': 1000,
 'three': 3,
 'too': 2,
 'twelve': 12,
 'twenty': 20,
 'twenty-eight': 28,
 'twenty-five': 25,
 'twenty-four': 24,
 'twenty-nine': 29,
 'twenty-one': 21,
 'twenty-seven': 27,
 'twenty-six': 26,
 'twenty-three': 23,
 'twenty-two': 22,
 'two': 2,
 'zero': 0}

expected_spoken2char = {'Alpha': 'a', 'Bravo': 'b', 'Charlie': 'c', 'Delta': 'd', 'Echo': 'e'}
expected_char2spoken =   {'a': ['Alpha'],
                            'b': ['Bravo'],
                            'c': ['Charlie'],
                            'd': ['Delta'],
                            'e': ['Echo']}
expected_abbrev2spoken11 =  {'enx': ['E N X', 'enx'], 'fra': ['F R A'], 'nld': ['N L D'], 'qh': ['Kuwait']}

expected_spoken2abbrev11 =    {'E N X': 'enx', 'F R A': 'fra', 'Kuwait': 'qh', 'N L D': 'nld', 'enx': 'enx'}

expected_abbrev2spoken10 =   {'enx': ['E. N. X.', 'enx'],
                                'fra': ['F. R. A.'],
                                'nld': ['N. L. D.'],
                                'qh': ['Kuwait']}

expected_spoken2abbrev10 =   {'E. N. X.': 'enx',
                                'F. R. A.': 'fra',
                                'Kuwait': 'qh',
                                'N. L. D.': 'nld',
                                'enx': 'enx'}

expected_spoken2ext10 =      {'I. N. I.': ['ini'],
                                'P. why': ['py'],
                                'P. why W.': ['pyw'],
                                'X. L. S.': ['xls'],
                                'X. L. S. X.': ['xlsx'],
                                'doc': ['doc'],
                                'doc X.': ['docx'],
                                'excel': ['xlsx', 'xls'],
                                'python': ['py', 'pyw'],
                                'word': ['docx', 'doc']}
expected_spoken2ext11 =     {'I N I': ['ini'],
                                'P why': ['py'],
                                'P why W': ['pyw'],
                                'X L S': ['xls'],
                                'X L S X': ['xlsx'],
                                'doc': ['doc'],
                                'doc X': ['docx'],
                                'excel': ['xlsx', 'xls'],
                                'python': ['py', 'pyw'],
                                'word': ['docx', 'doc']}

expected_ext2spoken10 =     {'doc': ['word', 'doc'],
                                'docx': ['word', 'doc X.'],
                                'ini': ['I. N. I.'],
                                'py': ['python', 'P. why'],
                                'pyw': ['python', 'P. why W.'],
                                'xls': ['excel', 'X. L. S.'],
                                'xlsx': ['excel', 'X. L. S. X.']}

expected_ext2spoken11 =     {'doc': ['word', 'doc'],
                                'docx': ['word', 'doc X'],
                                'ini': ['I N I'],
                                'py': ['python', 'P why'],
                                'pyw': ['python', 'P why W'],
                                'xls': ['excel', 'X L S'],
                                'xlsx': ['excel', 'X L S X']}

expected_spoken2punct =     {'colon': ':', 'exclamation mark': '!', 'point': '.', 'semi colon': ';'}

expected_punct2spoken =     {'!': ['exclamation mark'],
                            '.': ['point'],
                            ':': ['colon'],
                            ';': ['semi colon']}


#---------------------------------------------------------------------------
class UnittestNumbersSpokenForms(TestCaseWithHelpers.TestCaseWithHelpers):
    def setUp(self):
        spokenforms.resetSpokenformsGlobals()
        self.numbers = spokenforms.SpokenForms('test', DNSVersion=DNSVersion)
    
    def tearDown(self):
        pass

    def test_basic_dicts(self):
        n = self.numbers

        self.assert_equal(expected_s2n, n.s2n, "numbers, spoken2numbers is not as expected")
        
        self.assert_equal(expected_n2s, n.n2s, "numbers, numbers2spoken is not as expected")

        # alphabet:
        self.assert_equal(expected_char2spoken, n.char2spoken, "alphabet, first instance char2spoken is not as expected")
        self.assert_equal(expected_spoken2char, n.spoken2char, "alphabet, first instance spoken2char is not as expected")

        # abbrevs:
        if DNSVersion <= 10:
            self.assert_equal(expected_abbrev2spoken10, n.abbrev2spoken, "abbrevs, first instance abbrev2spoken is not as expected")
            self.assert_equal(expected_spoken2abbrev10, n.spoken2abbrev, "abbrevs, first instance spoken2abbrev is not as expected")
        else:
            self.assert_equal(expected_abbrev2spoken11, n.abbrev2spoken, "abbrevs, first instance abbrev2spoken is not as expected")
            self.assert_equal(expected_spoken2abbrev11, n.spoken2abbrev, "abbrevs, first instance spoken2abbrev is not as expected")

        # extensions:
        if DNSVersion <= 10:
            self.assert_equal(expected_ext2spoken10, n.ext2spoken, "abbrevs, first instance ext2spoken is not as expected")
            self.assert_equal(expected_spoken2ext10, n.spoken2ext, "abbrevs, first instance spoken2ext is not as expected")
        # else:
            self.assert_equal(expected_ext2spoken11, n.ext2spoken, "abbrevs, first instance ext2spoken is not as expected")
            self.assert_equal(expected_spoken2ext11, n.spoken2ext, "abbrevs, first instance spoken2ext is not as expected")
        
        # punctuation:
        self.assert_equal(expected_punct2spoken, n.punct2spoken, "abbrevs, first instance punct2spoken is not as expected")
        self.assert_equal(expected_spoken2punct, n.spoken2punct, "abbrevs, first instance spoken2punct is not as expected")
        
        # next instance:
        m = spokenforms.SpokenForms('test', DNSVersion=DNSVersion)
        self.assert_equal(expected_s2n, m.s2n, "numbers, second instance spoken2numbers is not as expected")
        
        
        self.assert_equal(expected_n2s, m.n2s, "numbers, second instance numbers2spoken is not as expected")

        self.assert_equal(expected_char2spoken, m.char2spoken, "alphabet, second instance char2spoken is not as expected")
        self.assert_equal(expected_spoken2char, m.spoken2char, "alphabet, second instance spoken2char is not as expected")

        # abbrevs second:
        if DNSVersion <= 10:
            self.assert_equal(expected_abbrev2spoken10, m.abbrev2spoken, "abbrevs, second instance abbrev2spoken is not as expected")
            self.assert_equal(expected_spoken2abbrev10, m.spoken2abbrev, "abbrevs, second instance spoken2abbrev is not as expected")
        else:
            self.assert_equal(expected_abbrev2spoken11, m.abbrev2spoken, "abbrevs, second instance abbrev2spoken is not as expected")
            self.assert_equal(expected_spoken2abbrev11, m.spoken2abbrev, "abbrevs, second instance spoken2abbrev is not as expected")
        # we believe the mechanism is OK for the second time test of the other dicts...

        
    def test_switching_language(self):
        n = self.numbers
        self.assert_equal(expected_s2n, n.s2n, "numbers, spoken2numbers is not as expected")

        self.assert_equal(expected_n2s, n.n2s, "numbers, numbers2spoken is not as expected")
        
        # next instance non existing language:
        print '\nexpect messages from spokenforms, as it is switched to a non existing language'
        m = spokenforms.SpokenForms('othertest', DNSVersion=DNSVersion)
        expected_othertest =   {}
        self.assert_equal(expected_othertest, m.s2n, "numbers, other language (no entries) spoken2numbers is not as expected")
        
        self.assert_equal(expected_othertest, m.n2s, "numbers, other language (no entries) numbers2spoken is not as expected")
        
        # back to language 'test'
        n = spokenforms.SpokenForms('test', DNSVersion=DNSVersion)
        self.assert_equal(expected_s2n, n.s2n, "numbers again, spoken2numbers is not as expected")
        
        self.assert_equal(expected_n2s, n.n2s, "numbers again, numbers2spoken is not as expected")
        print '-----end of these expected messages\n'


        
    def test_make_mixed_list(self):
        """make a list of spoken forms if the numbers are there
        """
        n = self.numbers
        L = [1, 2, 4, 5, 6]
        got = n.getMixedList(L)
        expected =     ['one', 'two', 'too', 'four', 'for', 'five', 'six']
        self.assert_equal(expected, n.getMixedList(L), "numbers: spoken forms list not as expected")

        # non existing language:        
        print '\nexpect messages from spokenforms.ini, as language is unknown'
        m = spokenforms.SpokenForms('othertest', DNSVersion=DNSVersion)

        got = n.getMixedList(L)
        expected =    ['1', '2', '4', '5', '6']
        self.assert_equal(expected, n.getMixedList(L), "numbers: spoken forms list not as expected")

        # back to previous:
        n = spokenforms.SpokenForms('test', DNSVersion=DNSVersion)
        got = n.getMixedList(L)
        expected = ['one', 'two', 'too', 'four', 'for', 'five', 'six']

        self.assert_equal(expected, n.getMixedList(L), "numbers: spoken forms list not as expected")
        print '----end of these expected messages'

    def test_get_number_back_from_spoken_form(self):
        """the reverse process, occurring after a recognition
        """
        n = self.numbers
        expected = 1
        self.assert_equal(expected, n.getNumberFromSpoken('one'), "numbers: get number back from spoken form not as expected")
        
        expected = 5
        self.assert_equal(expected, n.getNumberFromSpoken(5), "numbers: get number back from spoken form not as expected")

        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('foo'), "numbers: get number back from spoken form not as expected")
        
        # with original list:
        originalList = [1, 2, 5, 6, 7]
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('foo', originalList), "numbers: get number back from spoken form not as expected (with originalList)")

        expected = 7
        self.assert_equal(expected, n.getNumberFromSpoken('7', originalList), "numbers: get number back from spoken form not as expected (with originalList)")

        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('8', originalList), "numbers: get number back from spoken form not as expected (with originalList)")

        expected = 2
        self.assert_equal(expected, n.getNumberFromSpoken('2', originalList), "numbers: get number back from spoken form not as expected (with originalList)")

        expected = 2
        self.assert_equal(expected, n.getNumberFromSpoken('too', originalList), "numbers: get number back from spoken form not as expected (with originalList)")
        
        # real check! in instance, but not in originalList:
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('four', originalList), "numbers: get number back from spoken form not as expected (with originalList)")
        
        # originalList ints:
        originalList = [0,1,2]
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('four', originalList), "numbers: get number back from spoken form not as expected (with originalList)")
        expected = 1
        self.assert_equal(expected, n.getNumberFromSpoken('one', originalList), "numbers: get number back from spoken form not as expected (with originalList)")
        expected = 1
        self.assert_equal(expected, n.getNumberFromSpoken(1, originalList), "numbers: get number back from spoken form not as expected (with originalList)")
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken(10, originalList), "numbers: get number back from spoken form not as expected (with originalList)")

    def test_get_number_back_from_spoken_form_asStr(self):
        """the reverse process, occurring after a recognition, return as string
        """
        n = self.numbers
        expected = '1'
        self.assert_equal(expected, n.getNumberFromSpoken('one', asStr=True), "numbers: get number back as str from spoken form not as expected")
        
        expected = '5'
        self.assert_equal(expected, n.getNumberFromSpoken(5, asStr=True), "numbers: get number back as str from spoken form not as expected")

        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('foo', asStr=True), "numbers: get number back as str from spoken form not as expected")
        
        # with original list:
        originalList = [1, 2, 5, 6, 7]
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('foo', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")

        expected = '7'
        self.assert_equal(expected, n.getNumberFromSpoken('7', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")

        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('8', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")

        expected = '2'
        self.assert_equal(expected, n.getNumberFromSpoken('2', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")

        expected = '2'
        self.assert_equal(expected, n.getNumberFromSpoken('too', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")
        
        # real check! in instance, but not in originalList:
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('four', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")
        
        # originalList ints:
        originalList = [0,1,2]
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken('four', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")
        expected = '1'
        self.assert_equal(expected, n.getNumberFromSpoken('one', originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")
        expected = '1'
        self.assert_equal(expected, n.getNumberFromSpoken(1, originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")
        expected = None
        self.assert_equal(expected, n.getNumberFromSpoken(10, originalList, asStr=True), "numbers: get number back as str from spoken form not as expected (with originalList)")
        
    def doTestGetListOfSpokenForms(self, number, list):
        """test the automatic generation of a list of spoken forms for larger numbers
        """
        func = self.numbers.generateSpokenFormsFromNumber
        result = func(number)
        self.assert_equal(list, result, "test generateSpokenFormsFromNumber test failed for number: %s"% number)
        
    def test_get_list_of_spoken_forms_larger_number(self):
        """construct a list of spoken forms for numbers up to 10000
        """
        n = self.numbers
        testfunc = self.doTestGetListOfSpokenForms
        testfunc(123, ['hundred twenty-three', 'one twenty-three'])
        testfunc(203, ['two oh three', 'too oh three', 'two hundred three', 'too hundred three'])
        testfunc(300, ['three hundred'])
        testfunc(301, ['three oh one', 'three hundred one'])
        testfunc(323, ['three hundred twenty-three', 'three twenty-three'])
        #testfunc(1000, ['one thousand'])  # should not go through this function
        testfunc(1003, ['one oh oh three', 'thousand three', 'one thousand three'])
        testfunc(1011, ['thousand eleven', 'one thousand eleven', 'ten eleven'])
        testfunc(2303, ['twenty-three oh three'])
        testfunc(2003,    ['two oh oh three',
                            'too oh oh three',
                            'two thousand three',
                            'too thousand three'])
        testfunc(2010,  ['two thousand ten', 'too thousand ten', 'twenty ten'])
        testfunc(2310, ['twenty-three ten'])

    def doTestGenerateMixedListOfSpokenForms(self, number, list):
        """test the automatic generation of a list of spoken forms for larger numbers
        """
        func = self.numbers.generateMixedListOfSpokenForms
        result = func(number)
        self.assert_equal(list, result, "test generateMixedListOfSpokenForms test failed for number: %s"% number)
        
    def doTestDictOfSpokenForms(self, List, ExpDict):
        """test the automatic generation of a dict of spoken forms for given values list
        """
        func = self.numbers.getDictOfMixedSpokenForms
        result = func(List)
        self.assert_equal(ExpDict, result, "test getDictOfMixedSpokenForms test failed for List: %s"% List)
        

    def test_get_mixed_list_of_spoken_forms(self):
        """construct a list of spoken forms from filenames etc
        """
        n = self.numbers
        testfunc = self.doTestGenerateMixedListOfSpokenForms
        testfunc('file 100', ['file hundred', 'file one hundred'])
        testfunc('test file', ['test file'])
        testfunc('10test 203file',
                          ['ten test two oh three file',
                            'ten test too oh three file',
                            'ten test two hundred three file',
                            'ten test too hundred three file'])
        testfunc('test 10 20 2011 file',
                   ['test ten twenty two thousand eleven file',
                    'test ten twenty too thousand eleven file',
                    'test ten twenty twenty eleven file'])
        testfunc('test-1-4-2010-file',
                    ['test one four two thousand ten file',
                        'test one four too thousand ten file',
                        'test one four twenty ten file',
                        'test one for two thousand ten file',
                        'test one for too thousand ten file',
                        'test one for twenty ten file'])

    def test_get_mixed_list_of_spoken_forms_skip_numbers(self):
        """construct a list of spoken forms from filenames etc with skipping numbers
        
        
        1_hello should skip the 1 and also include
        testing (2) should skip the (2) (AND also include)
        """
        n = self.numbers
        testfunc = self.doTestGenerateMixedListOfSpokenForms
        testfunc('1_file.txt', ['file txt', 'one file txt'])
        testfunc('2_dir', ['dir', 'two dir', 'too dir'])
        
        testfunc('directory avp (3)', ['directory avp', 'directory avp three'])
        testfunc('file (4).doc', ['file four doc', 'file for doc'])

    def test_get_mixed_list_of_spoken_forms_skip_start_letters(self):
        """construct a list of spoken forms from filenames etc with skipping start letters
        
        a_test should be a test and test
        b_file.txt should be b file txt and file txt
        """
        n = self.numbers
        testfunc = self.doTestGenerateMixedListOfSpokenForms
        testfunc('a_test directory', ['test directory', 'a test directory'])
        testfunc('b_file.txt', ['file txt', 'b file txt'])

        testfunc('az_test directory', ['test directory', 'az test directory'])
        testfunc('bb_file.txt', ['file txt', 'bb file txt'])
        
        # but:
        
        testfunc('this_file.txt', ['this file txt'])
        

    def test_get_dict_of_spoken_forms(self):
        """construct a dict of spoken forms from a list of values (sheets in excel)
        """
        testfunc = self.doTestDictOfSpokenForms
        testfunc(['Sheet1', 'Sheet2'],
                {'Sheet one': 'Sheet1', 'Sheet too': 'Sheet2', 'Sheet two': 'Sheet2'})

    def doTestSortedByNumbersValues(self, expected, list_spoken, valueSpokenDict=None):
        """test the checking of a numbers list and sort by the number
        """
        func = self.numbers.sortedByNumbersValues
        result = func(list_spoken, valueSpokenDict=valueSpokenDict)
        self.assert_equal(expected, result, "test SortedByNumbersValues test failed for spoken forms list: %s"% list_spoken)
        
    def test_get_list_of_spoken_forms_sorted_by_number_values(self):
        """list of spoken forms, check numbers behind the items and sort by numbers
        """
        testfunc = self.doTestSortedByNumbersValues
        testfunc(None, ['one', 'two', 'unknown word'])
        testfunc(['one', 'two', 'three'], ['three', 'two', 'one'])
        testfunc({1: ['one'], 2: ['two'], 3: ['three']}, ['three', 'two', 'one'], valueSpokenDict=1)

    def doTestFormatSpokenFormsFromNumbersDict(self, expected, D):
        """formatted list of numbers spoken forms, for show ini files
        """
        func = inivars.formatReverseNumbersDict
        result = func(D)
        self.assert_equal(expected, result, "test formatReverseNumbersDict test failed for dict: %s"% D)
        
    def test_format_spoken_forms_from_numbers_dict(self):
        testfunc = self.doTestFormatSpokenFormsFromNumbersDict     
        expected = 'one ... three'
        testfunc(expected, {1: ['one'], 2: ['two'], 3: ['three']})

    def doTestGetPunctuationList(self, expected, spoken, originalList=None):
        """test the get punctuation function
        """
        func = self.numbers.getPunctuationFromSpoken
        result = func(spoken, originalList)
        self.assert_equal(expected, result, "test getPunctuationFromSpoken failed for spoken: %s and originalList %s"% (spoken, originalList))
 

    def test_get_punctuation_list(self):
        """test the punctuation from the punctuationreverse section
        """
        testfunc = self.doTestGetPunctuationList
        
        # ok, 'colon' returns ':'
        testfunc(":", 'colon')

        # not in the list:
        testfunc(None, 'comma')  # 'comma' is not in the list in hte test_spokenforms.ini


        # with the originalList given:
        testfunc(":", 'colon', originalList=[':', '.'])
        testfunc(":", 'colon', originalList=':.')
        testfunc(None, 'colon', originalList='.')
        testfunc(":", 'colon', originalList='')
        testfunc(":", 'colon', originalList=None)

        

def run():
    print 'starting UnittestNumbersSpokenForms'
    unittest.main()
    

if __name__ == "__main__":
    run()
