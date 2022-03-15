
import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet
import datetime
from decimal import Decimal

print "&&&&&&&&&&&&&&&&&&&&    one Model script &&&&&&&&&&&&&&&&&&&&&&&"

ph = PostgresHandler("host=127.0.0.1 port=5432 dbname=onemodel user=wmalpica password=blazingIsBetter")
schema="oneModel"
db="oneModel2"
bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)
comp = PostgresComparisonTestSet(bh, ph)


qStr = "select count_distinct(employeeid) from employee"
altqStr = "select count(distinct employeeid) from employee"
#comp.runAndValidateQuery(altqStr, showVerboseQuery=True, orderless=True, fullOrderless = True, altqStr = qStr)


qStr = """select sum(employee.headcount), timeperiods.year, min(timeperiods.date),
dim_gender.level1id, dim_gender.level1name, min(dim_gender.ordering),
dim_country.level1id, dim_country.level1name, min(dim_country.ordering),
dim_performance_rating.level1id, dim_performance_rating.level1name, min(dim_performance_rating.ordering)
from employee

left outer join dim_in_counts
on employee.in_counts = dim_in_counts.id

left outer join performance
on employee.effdt >= performance.effdt
 and employee.person_id = performance.person_id
 and employee.effdt <= performance.enddt

left outer join dim_country on employee.country = dim_country.id

left outer join dim_gender on employee.gender = dim_gender.id

left outer join dim_performance_rating on performance.curr_rating = dim_performance_rating.id


left outer join timeperiods on employee.effdt <= timeperiods.date
 and employee.enddt >= timeperiods.date

where timeperiods.year in ('2008','2009','2010','2011','2012','2013','2014','2015')
and dim_in_counts.level1id in ('1')
and dim_country.level1id in ('AU','CA','DE','JP','GB','US','?')
and dim_performance_rating.level1id in ('#High','#Med','#Low', '?')
and dim_gender.level1id in ('1','2','3','?')


group by timeperiods.year, timeperiods.year, dim_country.level1id, dim_country.level1name, dim_gender.level1id, dim_gender.level1name, dim_performance_rating.level1id, dim_performance_rating.level1name
limit 300"""
comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, fullOrderless = True)

qStr = """select sum(employee.headcount), timeperiods.year, min(timeperiods.date),
dim_performance_rating.level1id, dim_performance_rating.level1name, min(dim_performance_rating.ordering),
dim_gender.level1id, dim_gender.level1name, min(dim_gender.ordering),
dim_country.level1id, dim_country.level1name, min(dim_country.ordering)
from employee

left outer join dim_in_counts
on employee.in_counts = dim_in_counts.id

left outer join performance
on employee.effdt >= performance.effdt
  and employee.person_id = performance.person_id
  and employee.effdt <= performance.enddt
left outer join dim_performance_rating on performance.curr_rating = dim_performance_rating.id

left outer join dim_gender
on employee.gender = dim_gender.id

left outer join dim_country
on employee.country = dim_country.id

left outer join timeperiods on employee.effdt <= timeperiods.date
  and employee.enddt >= timeperiods.date

where timeperiods.year in ('2008','2009','2010','2011','2012','2013','2014','2015')
and dim_in_counts.level1id in ('1')
and dim_performance_rating.level1id in ('#High','#Med','#Low')
and dim_gender.level1id in ('1','2','3')
and dim_country.level1id in ('AU','CA','DE','JP','GB','US')

group by timeperiods.year, timeperiods.year, dim_performance_rating.level1id, dim_performance_rating.level1name, dim_gender.level1id, dim_gender.level1name, dim_country.level1id, dim_country.level1name
limit 300"""

#qStr="""select count(level1id), count(id), count(ordering) from dim_gender
#group by id"""

comp.runAndValidateQuery(qStr, showVerboseQuery=True, orderless=True, fullOrderless = True)
