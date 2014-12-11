from rflint.common import SuiteRule, ERROR, WARNING
from rflint.parser import SettingTable
import difflib
import itertools
import re

def normalize_name(string):
    '''convert to lowercase, remove spaces and underscores'''
    return string.replace(" ", "").replace("_", "").lower()

class PeriodInSuiteName(SuiteRule):
    '''Warn about periods in the suite name
    
    Since robot uses "." as a path separator, using a "." in a suite
    name can lead to ambiguity. 
    '''
    severity = WARNING
    
    def apply(self,suite):
        if "." in suite.name:
            self.report(suite, "'.' in suite name '%s'" % suite.name, 0)

class InvalidTable(SuiteRule):
    '''Verify that there are no invalid table headers'''
    severity = WARNING

    def apply(self, suite):
        for table in suite.tables:
            if (not re.match(r'settings?|metadata|(test )?cases?|(user )?keywords?|variables?', 
                             table.name, re.IGNORECASE)):
                self.report(suite, "Unknown table name '%s'" % table.name, table.linenumber)


class DuplicateKeywordNames(SuiteRule):
    '''Verify that no keywords have a name of an existing keyword in the same file'''
    severity = ERROR

    def apply(self, suite):
        cache = []
        for keyword in suite.keywords:
            # normalize the name, so we catch things like
            # Smoke Test vs Smoke_Test, vs SmokeTest, which
            # robot thinks are all the same
            name = normalize_name(keyword.name)
            if name in cache:
                self.report(suite, "Duplicate keyword name '%s'" % keyword.name, keyword.linenumber)
            cache.append(name)

class DuplicateTestNames(SuiteRule):
    '''Verify that no tests have a name of an existing test in the same suite'''
    severity = ERROR

    def apply(self, suite):
        cache = []
        for testcase in suite.testcases:
            # normalize the name, so we catch things like
            # Smoke Test vs Smoke_Test, vs SmokeTest, which
            # robot thinks are all the same
            name = normalize_name(testcase.name)
            if name in cache:
                self.report(suite, "Duplicate testcase name '%s'" % testcase.name, testcase.linenumber)
            cache.append(name)

class RequireSuiteDocumentation(SuiteRule):
    '''Verify that a test suite has documentation'''
    severity=WARNING

    def apply(self, suite):
        for table in suite.tables:
            if isinstance(table, SettingTable):
                for row in table.rows:
                    if row[0].lower() == "documentation":
                        return
        # we never found documentation; find the first line of the first
        # settings table, default to the first line of the file
        linenum = 1
        for table in suite.tables:
            if isinstance(table, SettingTable):
                linenum = table.linenumber + 1
                break

        self.report(suite, "No suite documentation", linenum)
            
class TestCasesTooSimilar(SuiteRule):
    """Warn if test cases are too similar to each other"""
    severity = WARNING
    max_similarity = .9

    def normalize(self, string):
        return string.lower().strip().replace(' ', '')

    def apply(self, suite):
        similar_testcases = set()
        testcases = [testcase for testcase in suite.testcases
                     if not testcase.is_templated]
        pairs = itertools.combinations(testcases, 2)
        differ = difflib.SequenceMatcher()
        for pair in pairs:
            # set testcase b to be the first half of the combination because
            # SequenceMatcher caches information about b
            testcase_a = self.normalize(''.join([''.join(step) for step
                                                 in pair[1].steps]))
            testcase_b = self.normalize(''.join([''.join(step) for step
                                                 in pair[0].steps]))
            differ.set_seqs(a=testcase_a, b=testcase_b)
            if (differ.real_quick_ratio() < self.max_similarity
                    or differ.quick_ratio() < self.max_similarity
                    or differ.ratio() < self.max_similarity):
                continue
            similar_testcases.add(pair[0])
            similar_testcases.add(pair[1])
        if similar_testcases:
            similar_testcase_names = {testcase.name for testcase
                                      in similar_testcases}
            self.report(suite, "Similar testcases found: '%s'" % ', '.join(
                similar_testcase_names), list(similar_testcases)[0].linenumber)
