import sys, getopt
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet


def main(argv):

    version=""
    memo=""
    runPostgresCompare=True

    try:
        opts, arge = getopt.getopt(argv,"htv:m:",["help","timingonly","version=","memo="])
    except getopt.GetoptError:
        print 'ExecuteAllIntegrationTests.py -t -v <versionName> -m <descriptionMemo>'
        print 'ExecuteAllIntegrationTests.py --timingonly --version <versionName> --memo <descriptionMemo>'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'ExecuteAllIntegrationTests.py -t -v <versionName> -m <descriptionMemo>'
            print 'ExecuteAllIntegrationTests.py --timingonly --version <versionName> --memo <descriptionMemo>'
            sys.exit()
        elif opt in ("-t", "--timingonly"):
            runPostgresCompare = False
        elif opt in ("-v", "--version"):
            version = arg
        elif opt in ("-m", "--memo"):
            memo = arg
         
    

    if runPostgresCompare:
        #ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch50mb user=postgres password=terry")
        # ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch1gb user=postgres password=terry")
        ph = PostgresHandler("host=127.0.0.1 port=5432 dbname=tpch1gb user=wmalpica password=blazingIsBetter")
    else:
        ph = ""

    
    # schema="integrationTests"
    # db="tpch10gb"
    
    # schema="testCompSharedAll2"
    # db="tpch50Mb"
    
    schema="testCompSharedAll"
    db="tpch1Gb"
    
    # schema="testCompNothingMasterAll33"
    # db="tpch1Gb"
    
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

    logFile = '../TestLogs/' + db + 'Log.txt'
    

    print "########***********#############************############***********"
    print "########***********#############************############***********"
    print "Starting all integration tests"
    print "########***********#############************############***********"
    print "########***********#############************############***********"

    #
    execfile("SimpleAggregatesTests.py")
    execfile("SimplePredicatesTests.py")
    execfile("PredicatesWithAggregatesTests.py")
    execfile("CompoundPredicates.py")
    execfile("WhereNot.py")
    # # # # # execfile("DistinctTests.py")
    # # # # # currently nor working with horiz scale
    execfile("GroupByTests.py")
    execfile("WhereInTests.py")
    execfile("WhereBetweenTests.py")
    execfile("JoinsTests.py")
    execfile("OuterJoinsTests.py")
    execfile("NestedQueriesTest.py")
    execfile("UnionQueries.py")
    execfile("GroupByWithTransformations.py")
    execfile("AggregationsWithoutGoupByWithTransformations.py")
    execfile("TransformationProcessorCombinationsTests.py")
    execfile("NullIfAndNvlTransformTests.py")
    execfile("CaseTransformTests.py")
    

if __name__ == "__main__":
    main(sys.argv[1:])
