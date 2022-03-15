# coding=utf-8
import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler


path = "../DataSets/OneModel/"
tableFileList = ["employee.dat", "performance.dat", "timeperiods.dat", "dim_in_counts.dat", "dim_country.dat", "dim_performance_rating.dat", "dim_gender.dat"]
tableNameList = ["employee", "performance", "timeperiods", "dim_in_counts", "dim_country", "dim_performance_rating", "dim_gender"]


# Create database on Postgres
ph = PostgresHandler("host=127.0.0.1 port=5432 dbname=onemodel user=wmalpica password=blazingIsBetter")
# ph.createDatabase("host=127.0.0.1 port=5432 user=wmalpica password=blazingIsBetter", "onemodel")

employeeDesc = """record_id INT,  person_id VARCHAR(20), effdt DATE,  enddt DATE, seqnr INT, revseqnr INT, status VARCHAR(256), fullname VARCHAR(256), firstname VARCHAR(256),
  lastname VARCHAR(256), dob DATE, gender VARCHAR(256), nationality VARCHAR(256), ethnicgroup VARCHAR(256), eeojob VARCHAR(20), exempt VARCHAR(20), hire_DATE DATE, tenure_DATE DATE,
  term_DATE DATE, email VARCHAR(256), phone VARCHAR(256), country VARCHAR(256), state VARCHAR(256), city VARCHAR(256), zip VARCHAR(256), department VARCHAR(20),
  costcenter VARCHAR(20), positionid VARCHAR(20), jobid VARCHAR(20), jobfamily VARCHAR(256), jobfunction VARCHAR(256), critical VARCHAR(256), manager VARCHAR(256),
  matrixmanager VARCHAR(256), annual_salary FLOAT, annual_salary_range VARCHAR(256), bonus FLOAT, hourly_rate FLOAT, emp_type VARCHAR(256), reg_temp VARCHAR(256),
  full_part VARCHAR(256), contractor VARCHAR(256), risk_of_loss VARCHAR(256), impact_of_loss VARCHAR(256), is_manager VARCHAR(10), headcount INT, fte FLOAT, in_counts VARCHAR(8)"""

performanceDesc = """record_id INT, employee_record_id INT, person_id VARCHAR(20), effdt DATE, enddt DATE, seqnr INT, revseqnr INT, review_DATE DATE,
  review_type VARCHAR(20), review_status VARCHAR(20), reviewed_by DATE, curr_rating VARCHAR(20), prev_rating VARCHAR(20), prev_rating_same_type VARCHAR(20),
  review_difference VARCHAR(20), review_occurrence INT"""

timeperiodsDesc = """date DATE, year VARCHAR(20), quarter VARCHAR(100), quartername VARCHAR(100), month VARCHAR(50), monthname VARCHAR(50), week VARCHAR(20),
  day VARCHAR(20), dayname VARCHAR(20), daynameabbrev VARCHAR(10), daynumberofyear VARCHAR(20), daysinmonth VARCHAR(20), ordering VARCHAR(50)"""

dim_in_countsDesc = "id VARCHAR(8), level1id VARCHAR(8), level1name VARCHAR(16), ordering FLOAT"

dim_countryDesc = "id VARCHAR(8), level1id VARCHAR(8), level1name VARCHAR(24), ordering FLOAT"

dim_performance_ratingDesc = "id VARCHAR(8), level1id VARCHAR(8), level1name VARCHAR(8), level2id VARCHAR(24), level2name VARCHAR(24), ordering FLOAT"

dim_genderDesc = "id VARCHAR(8), level1id VARCHAR(8), level1name VARCHAR(24), ordering FLOAT"
tableDescriptionList = [employeeDesc, performanceDesc, timeperiodsDesc, dim_in_countsDesc, dim_countryDesc, dim_performance_ratingDesc, dim_genderDesc]


#ph.dropTables(tableNameList)
# ph.importDatabaseTables(tableNameList, path, tableFileList, tableDescriptionList)
print "Done Importing"
# ph.describeDatabaseVerbose()

# Create Blazing database on local
schema="oneModel"
db="oneModel2"

bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

# bh.dropDatabase()

employeeDesc = """record_id long,  person_id string(20), effdt date,  enddt date, seqnr long, revseqnr long, status string(256), fullname string(256), firstname string(256),
  lastname string(256), dob date, gender string(8), nationality string(256), ethnicgroup string(256), eeojob string(20), exempt string(20), hire_date date, tenure_date date,
  term_date date, email string(256), phone string(256), country string(8), state string(256), city string(256), zip string(256), department string(20),
  costcenter string(20), positionid string(20), jobid string(20), jobfamily string(256), jobfunction string(256), critical string(256), manager string(256),
  matrixmanager string(256), annual_salary double, annual_salary_range string(256), bonus double, hourly_rate double, emp_type string(256), reg_temp string(256),
  full_part string(256), contractor string(256), risk_of_loss string(256), impact_of_loss string(256), is_manager string(10), headcount long, fte double, in_counts string(8)"""


performanceDesc = """record_id long, employee_record_id long, person_id string(20), effdt date, enddt date, seqnr long, revseqnr long, review_date date,
  review_type string(20), review_status string(20), reviewed_by date, curr_rating string(8), prev_rating string(20), prev_rating_same_type string(20),
  review_difference string(20), review_occurrence long"""
  

timeperiodsDesc = """date date, year string(20), quarter string(100), quartername string(100), month string(50), monthname string(50), week string(20),
  day string(20), dayname string(20), daynameabbrev string(10), daynumberofyear string(20), daysinmonth string(20), ordering string(50)"""


dim_in_countsDesc = "id string(8), level1id string(8), level1name string(16), ordering double"

dim_countryDesc = "id string(8), level1id string(8), level1name string(24), ordering double"

dim_performance_ratingDesc = "id string(8), level1id string(8), level1name string(8), level2id string(24), level2name string(24), ordering double"

dim_genderDesc = "id string(8), level1id string(8), level1name string(24), ordering double"
tableDescriptionList = [employeeDesc, performanceDesc, timeperiodsDesc, dim_in_countsDesc, dim_countryDesc, dim_performance_ratingDesc, dim_genderDesc]

try:
    bh.initializeDatabase(tableNameList, path, tableFileList, tableDescriptionList, compressed=False, createSchema=False, createDatabase=True)
    bh.runQuery("list tables",verbose=True)
except RuntimeError as detail:
    print "Error: ",  detail
    #bh.dropDatabase()
