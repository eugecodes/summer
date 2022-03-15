# coding=utf-8
import sys
sys.path.append('../Classes')
from PostgresHandler import PostgresHandler
from LocalBlazingHandler import LocalBlazingHandler



# Create Blazing database on local
schema="8"
db="regeneron7"

bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)
bh.delimiterStr = "','"

#bh.dropDatabase()

tableDesc = """gene string(24), num_altalt long, case_refalt long, control_altalt long, chr string(8),
start long, gene_id long, phenotype_id long, stop double, beta double, stderr double, log10_pvalue double, l_ci_95 double,
u_ci_95 double, mask string(8), islof string(8), islast5pct string(8), isancestralallele string(8), isindel string(8),
hwe_flag string(8), mac_flag string(8), lambda_flag string(8), intransmem_gene string(16), run_date date, alt_freq double,
hwe_pval double, odds_ratio string(16), inregnome_gene string(16), insecreted_gene string(16),
method_type string(16), collaborator string(16), population string(16), test_type string(16), phenotype_category string(16),
data_freeze string(16), lambda_gc string(16), istier1_phenotype string(16), ci_95 string(120), ensembl75_name string(120),
file_id string(120), plink_stats_id string(120), functional_prediction string(120), rsid string(120), num_cases long,
num_controls long, case_altalt long, num_subjects long, num_refref long, num_refalt long, case_refref long, control_refref long,
control_refalt long, pos long, phenotype string(200), phenotype_0 string(200), phenotype_1 string(200), phenotype_2 string(200),
ref string(400), alt string(400), hgvs_cdna string(1000), hgvs_amino_acid string(1000), name string(1000)"""

path = "./"

try:
    bh.initializeDatabase(["regeneronFlatTable"], path, ["smallReg.csv"], [tableDesc], compressed=False, createSchema=False, createDatabase=True, copyUploadFiles=True)
    bh.runQuery("list tables",verbose=True)
except RuntimeError as detail:
    print "Error: ",  detail
    #bh.dropDatabase()
