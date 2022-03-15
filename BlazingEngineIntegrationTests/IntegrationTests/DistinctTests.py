import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet

if 'ph' not in locals():
    ph = PostgresHandler("host=169.53.37.156 port=5432 dbname=tpch50mb user=postgres password=terry")
    
if 'bh' not in locals():
    schema="integrationTests"
    db="tpch50Mb"
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

if 'version' not in locals():
    version = 0
    
if 'memo' not in locals():
    memo = ""
    
if 'logFile' not in locals():
    logFile = ""
    
comp = PostgresComparisonTestSet(bh, ph)


print "**********************************************************************"
print "Starting distinct tests"
print "**********************************************************************"

# distinct string no predicate
qStr = "select distinct o_orderstatus from orders order by o_orderstatus"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# distinct string count no prediate
qStr = "select count(distinct o_orderstatus) from orders"
comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery="select count_distinct(o_orderstatus) from orders")

# distinct long no predicate
qStr = "select distinct n_regionkey from nation order by n_regionkey"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# distinct long count no prediate
qStr = "select count(distinct n_regionkey) from nation"
comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery="select count_distinct(n_regionkey) from nation")

if db=="tpch50Mb":
    # Distinct string with predicate
    qStr = "select distinct ps_comment from partsupp where ps_availqty > 9980"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)

    # Distinct string with predicate with order by, although orderby on strings works differently in postgres than in blazing
    qStr = "select distinct ps_comment from partsupp where ps_availqty > 9980 order by ps_comment"
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
    
# Distinct count string with predicate does not work for strings longer than 8
#qStr = "select count(distinct ps_comment) from partsupp where ps_availqty > 9980"
#comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery= "select count_distinct(ps_comment) from partsupp where ps_availqty > 9980")
# Distinct count string with predicate
qStr = "select count(distinct l_returnflag) from lineitem where l_orderkey < 9980"
comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery= "select count_distinct(l_returnflag) from lineitem where l_orderkey < 9980")

if db=="tpch50Mb":
    # Distinct long with predicate
    qStr = "select distinct ps_partkey from partsupp where ps_availqty > 9980 order by ps_partkey"
    comp.runAndValidateQuery(qStr, showVerboseFails=True)
# Distinct count long with predicate
qStr = "select count(distinct ps_partkey) from partsupp where ps_availqty > 9980"
comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery= "select count_distinct(ps_partkey) from partsupp where ps_availqty > 9980")

if db=="tpch50Mb":
    # Distinct double with predicate
    qStr = "select distinct ps_supplycost from partsupp where ps_supplycost > 998 order by ps_supplycost"
    comp.runAndValidateQuery(qStr, showVerboseFails=True)
# Distinct count double with predicate
qStr = "select count(distinct ps_supplycost) from partsupp where ps_supplycost > 998"
comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery="select count_distinct(ps_supplycost) from partsupp where ps_supplycost > 998")

# Distinct date with predicate
qStr = "select distinct o_orderdate from orders where o_orderdate < '19920103' order by o_orderdate"
comp.runAndValidateQuery(qStr, showVerboseFails=True)
# Distinct count date with predicate
qStr = "select count(distinct o_orderdate) from orders where o_orderdate < '19920103'"
comp.runAndValidateQuery(qStr, showVerboseFails=True, alternateQuery="select count_distinct(o_orderdate) from orders where o_orderdate < '19920103'")

#distinct with multiple columns
# Distinct date with predicate
qStr = "select distinct o_orderdate, o_orderstatus from orders where o_orderdate < '19920103'"
comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
# Distinct date with order by
qStr = "select distinct o_orderdate, o_orderstatus from orders order by o_orderdate, o_orderstatus  limit 1000"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

if db=="tpch50Mb":
    # Distinct double with predicate
    qStr = "select distinct ps_availqty, ps_supplycost from partsupp where ps_supplycost > 998 "
    comp.runAndValidateQuery(qStr, showVerboseFails=True, orderless=True)
    
# Distinct double with order by
qStr = "select distinct ps_availqty, ps_supplycost from partsupp order by ps_availqty, ps_supplycost limit 1000"
comp.runAndValidateQuery(qStr, showVerboseFails=True)

if db=="tpch50Mb":
    # Distinct double with predicate and order by
    qStr = "select distinct ps_availqty, ps_supplycost from partsupp where ps_supplycost > 998 order by ps_availqty, ps_supplycost"
    comp.runAndValidateQuery(qStr, showVerboseFails=True)

    # Distinct double with predicate and order by (reverse order)
    qStr = "select distinct ps_availqty, ps_supplycost from partsupp where ps_supplycost > 998 order by ps_supplycost, ps_availqty"
    comp.runAndValidateQuery(qStr, showVerboseFails=True)



comp.report()
comp.logResults(logFile, version, memo)
