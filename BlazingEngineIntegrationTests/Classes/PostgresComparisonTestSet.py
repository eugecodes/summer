# coding=utf-8
import datetime
import time
from decimal import Decimal

class PostgresComparisonTestSet:
    'Manages a collection of integration tests that compare the Blazing engine to Postgres. It assumes that there are already two identical databases already setup in blazing and postgres respectively.'

    def __init__(self, blazingQueryHandler, postgresQueryHandler):
        self.passList = []
        self.queryList = []
        self.blazTimes1 = []
        self.blazTimes2 = []
        self.rowsReturned = []
        self.postgresTimes = []
        self.testStartTime = float(time.time())
        self.bq = blazingQueryHandler
        self.pq = postgresQueryHandler

    def runAndValidateQuery(self, qStr, **kwargs):
        #optional parameters
        showPass = kwargs.get("showPass", False)
        showQuery = kwargs.get("showQuery", False)
        showVerboseQuery = kwargs.get("showVerboseQuery", False)
        showVerboseFails = kwargs.get("showVerboseFails", False)
        queryForBlazing = kwargs.get("alternateQuery", "")
        orderless = kwargs.get("orderless", False)
        fullOrderless = kwargs.get("fullOrderless", False)
        precision = kwargs.get("precision", 0)
        fetchResults = kwargs.get("fetch", True)

        if len(queryForBlazing) == 0:
            queryForBlazing = qStr

        self.queryList += [qStr]

        if showVerboseQuery:
            if self.bq != "":
                print "Running Blazing query"
                self.bq.runQuery(queryForBlazing, verbose=True)
            if self.pq != "":
                print "Running Postgres query"
                if not fetchResults:
                    self.pq.runQuery(qStr, verbose=True, fetch=False)
                else:
                    self.pq.runQuery(qStr, verbose=True)

        else:
            if self.bq != "":
                self.bq.runQuery(queryForBlazing)
            if self.pq != "":
                self.pq.runQuery(qStr)

        if self.bq != "" and self.pq != "":
            passStr = self.validate(self.bq.getResultsArray(), self.pq.getResultsArray(), orderless, fullOrderless, precision)
            if passStr == "Pass":
                passed = True
            else:
                passed = False

            if showQuery and not showVerboseQuery:
                print qStr
                print "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-"
                print "  "
            if showPass or showQuery or showVerboseQuery:
                print passStr
                print "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-"
                print "  "
            if showVerboseFails and not passed and not showQuery:
                print qStr + " FAILED "
                print passStr
                print "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-"
                print "  "

            self.passList += [passed]
            self.postgresTimes += [self.pq.timeElapsed]
            self.blazTimes1 += [self.bq.blazingTimeElapsed]
            self.blazTimes2 += [self.bq.timeElapsed]
            self.rowsReturned += [self.bq.rowsReturned]
        else:
            self.passList += [True]
            if self.bq != "":
                self.bq.getResultsArray()
                self.blazTimes1 += [self.bq.blazingTimeElapsed]
                self.blazTimes2 += [self.bq.timeElapsed]
                self.rowsReturned += [self.bq.rowsReturned]
            if self.pq != "":
                self.postgresTimes +=[self.pq.timeElapsed]

    def validate(self, barr, parr, orderless = False, fullOrderless = False, precision = 0):
        
        # Giving error on some operations that were good http://stackoverflow.com/questions/15182804/python-3-30-typeerror-object-of-type-int-has-no-len
        #print type(barr)
        #print type(parr)
        #print range(parr)
        try:
            if type(barr) is list:
                length_barr = len(barr)
            elif type(barr) is int:
                length_barr = range(barr)
        except:
            print "Object barr is string or dict or nonetype maybe"
            
        try:
            if type(parr) is list:
                length_parr = len(parr)
            elif type(parr) is int:
                length_parr = range(parr)
        except:
            print "Object parr is string or dict or nonetype maybe"
            
        try:
            if length_barr != length_parr:
                if (length_barr == 1 and len(barr[0]) == 1 and barr[0][0] == "empty result" and length_parr == 0):
                    return "Pass"
                else:
                    return "Array sizes don't match: len(barr)= " + str(length_barr) + " len(parr)= " + str(length_parr)
            if length_barr > 0 and length_parr > 0:
                if len(barr[0]) != len(parr[0]):
                    return "Array sizes don't match: len(barr[0])= " + str(len(barr[0])) + " len(parr[0])= " + str(len(parr[0]))
            else:
                return "FAIL one or more of the results is empty"
        except:
            if range(len(barr)) != range(parr):
                if (range(barr) == 1 and range(barr[0]) == 1 and barr[0][0] == "empty result" and range(parr) == 0):
                    return "Pass"
                else:
                    return "Array sizes don't match: len(barr)= " + str(range(barr)) + " len(parr)= " + str(range(parr))
            if len(barr) > 0 and len(parr) > 0:
                if len(barr[0]) != len(parr[0]):
                    return "Array sizes don't match: range(barr[0])= " + str(range(barr[0])) + " range(parr[0])= " + str(range(parr[0]))
            else:
                return "FAIL one or more of the results is empty"

        if orderless or fullOrderless:
            return self.orderlessCompare(barr, parr, precision, fullOrderless)
        else:
            return self.standardArrayCompare(barr, parr, precision)

        return "Pass"

    def standardArrayCompare(self, barr, parr, precision = 0):
        try:
            for i in xrange(0, len(barr)):
                for j in xrange(0, len(barr[i])):
                    result = self.compare(barr[i][j], parr[i][j], precision)
                    if result != "Pass":
                        return "Mismatch at row " + str(i) + " column " + str(j) + " --> " + result

            return "Pass"

        except ValueError:
            return str(("#standardArrayCompare ValueError# at row " + str(i) + " column " + str(j) + " --> ", barr[i][j], parr[i][j]))
        except TypeError:
            return str(("#standardArrayCompare TypeError# at row " + str(i) + " column " + str(j) + " --> ", barr[i][j], parr[i][j]))

    def orderlessCompare(self, barr, parr, precision = 0, fullOrderless=False):
        try:
            fullOutFailCount = 0
            numRows = len(barr)
            numCols = len(barr[0])
            notYetMatched = range(0, numRows)
            ptype = type(parr[0][0])
            for bInd in xrange(0, numRows):
                matchInd = None
                notYetInd = 0
                for pInd in notYetMatched:
                    result = self.compare(barr[bInd][0], parr[pInd][0], precision)
                    if result == "Pass":
                        if numCols > 1:
                            if self.restOfRowMatches(barr[bInd], parr[pInd], precision):
                                matchInd = notYetInd
                                break
                            else:
                                notYetInd += 1
                        else:
                            matchInd = notYetInd
                            break
                    else:
                        notYetInd += 1

                if matchInd == None:
                    if fullOrderless:
                        fullOutFailCount += 1
                        print "No match found for blazing row " + str(bInd + 1) + ": " + str(barr[bInd][0])
                    else:
                        return "No match found for blazing row " + str(bInd + 1) + ": " + str(barr[bInd][0])
                else:
                    del notYetMatched[matchInd]

            if fullOrderless:
                if fullOutFailCount == 0:
                    return "Pass"
                else:
                    return "Failed " + str(fullOutFailCount) + " rows out of " + str(numRows)
            else:
                return "Pass"

        except ValueError:
            return str(("#orderlessCompare ValueError# at row " + str(bInd) + " column " + str(0) + " --> ", barr[bInd][0], ptype))

    def restOfRowMatches(self, brow, prow, precision):
        try:
            for i in xrange(1, len(brow)):
                result = self.compare(brow[i], prow[i], precision)
                if result != "Pass":
                    return False

            return True
        except ValueError:
            return False

    def compare(self, origBval, origPval, precision):
        bval = origBval
        pval = origPval
        ptype = type(pval)

        try:
            # first check for nulls
            if str(bval) == "null" or str(pval) == "None":
                #print "Blazing=" + str(origBval) + " Postgres=" + str(origPval)
                if (str(bval) == "null" and str(pval) == "None") or (str(bval) == "0" and str(pval) == "None"):
                    return "Pass"
                else:
                    return "Mismatch=> Blazing=" + str(origBval) + " Postgres=" + str(origPval)

            # convert postgres and blazing values to same type for comparison
            if ptype is int or ptype is float or ptype is long or ptype is Decimal:
                # if postgres value is numeric convert both values to float
                pval = float(pval)
                if type(bval) is unicode:
                    if bval.find('L') != -1:
                        bval = float(long(bval))
                    elif bval.find('.') != -1:
                        bval = float(bval)
                    else:
                        bval = float(int(bval))
                else:
                    bval = float(bval)
            elif ptype is datetime.date:
                bval = str(bval)
                pval = str(pval)
            elif ptype is str:
                bval = str(bval)
            else:
                return "Postgres value was of an unknown type: " + str(origPval) + " type=" + str(type(origPval))

            # perform comparison
            if type(pval) is float and precision != 0:
                if abs(bval - pval) < precision:
                    return "Pass"
                else:
                    return "Mismatch=> Blazing=" + str(origBval) + " Postgres=" + str(origPval)
            else:
                if bval == pval:
                    return "Pass"
                else:
                    return "Mismatch=> Blazing=" + str(origBval) + " Postgres=" + str(origPval)
        except ValueError:
            return "#compare ValueError# => Blazing=" + str(origBval) + " type=" + str(type(origBval)) + " Postgres=" + str(origPval) + " type=" + str(type(origPval))
        except TypeError:
            return "#compare TypeError# => Blazing=" + str(origBval) + " type=" + str(type(origBval)) + " Postgres=" + str(origPval) + " type=" + str(type(origPval))

    def report(self):

        if self.pq != "":
            passCount = 0
            totalCount = len(self.passList)
            for p in xrange(0,totalCount):
                if self.passList[p]:
                    passCount += 1
                else:
                    print "FAILED: " + self.queryList[p]
            failCount = totalCount - passCount
            print "**********************************************************************"
            print "SUMMARY: " +  str(passCount) + "/" + str(totalCount) + " PASSED, " + str(failCount) + "/" + str(totalCount) + " FAILED"
            timeElapsed = float(time.time()) - self.testStartTime
            print "Total time elapsed: " + str(timeElapsed) + " => Blazing queries: " + str(sum(self.blazTimes2)) + " Postgres queries: " + str(sum(self.postgresTimes)) + " Validation: " + str(timeElapsed - sum(self.blazTimes2) - sum(self.postgresTimes))
            print "**********************************************************************"
        else:
            print "**********************************************************************"
            if 'version' not in locals():
                print "SUMMARY: Timing Only Run"
            else:
                print "SUMMARY: Timing Only Run for version: " + str(version)
            print "Total Blazing queries time elapsed: " + str(sum(self.blazTimes2))
            print "**********************************************************************"

    def logResults(self, logFile, version, memo):

        if logFile == "":
            return  # do nothing
        else:
            with open(logFile,"a+") as f:
                totalCount = len(self.passList)
                curDateTime = str(datetime.datetime.now().isoformat())
                for q in xrange(0,totalCount):
                    qStr = self.queryList[q]
                    qStr = qStr.replace("\n"," ")
                    qStr = qStr.replace("     "," ")
                    #Need to log three diff. potential options
                    if self.bq != "" and self.pq != "":
                        outputLine = version + "|" + str(curDateTime) + "|" + memo + "|" + qStr + "|" + str(self.passList[q]) + "|" + str(self.blazTimes1[q]) + "|" + str(self.blazTimes2[q]) + "|" + str(self.rowsReturned[q]) + "|" + str(self.postgresTimes[q]) +  "\n"
                    else:
                        if self.bq != "":
                            outputLine = version + "|" + str(curDateTime) + "|" + memo + "|" + qStr + "|" + str(self.passList[q]) + "|" + str(self.blazTimes1[q]) + "|" + str(self.blazTimes2[q]) + "|" + str(self.rowsReturned[q]) + "\n"
                        if self.pq != "":
                            outputLine = version + "|" + str(curDateTime) + "|" + memo + "|" + qStr + "|" + str(self.passList[q]) + "|"  + str(self.postgresTimes[q]) +  "\n"
                    f.write(outputLine)
