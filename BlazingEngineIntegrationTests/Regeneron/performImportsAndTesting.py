import sys
import subprocess
import time
import os

sys.path.append('../Classes')
sys.path.append('./')
from ImportAndTestingTools import setNodesInfo
from LocalBlazingHandler import LocalBlazingHandler
from PostgresComparisonTestSet import PostgresComparisonTestSet


if 'bh' not in locals():
    schema="8"
    db="regeneron"
    # schema="testCompSharedAll"
    # db="tpch1Gb"
    bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)

if 'version' not in locals():
    version = 0

if 'memo' not in locals():
    memo = ""

if 'logFile' not in locals():
    logFile = ""



logFile = "./regeneronTestLog.txt"
version = "master 6/14/2016"
    
comp = PostgresComparisonTestSet(bh, "")

nodesFile = "/disk1/blazing/blazing/nodes.config"
# nodesFile = "/home/wmalpica/repos/nodes.config"

nodeIPs = ["52.40.211.73", "52.40.215.172", "52.27.199.62", "52.38.213.118", "52.27.38.240"]
nodePorts = ["8890", "8890", "8890", "8890", "8890"]

loadDataQuery = """load data infile reg.csv into table regeneronFlatTable fields terminated by ',' enclosed by '\"' lines terminated by '\n'"""
    
queryStr0 = """select gene, chr, start, stop, mask, beta, stderr, odds_ratio, ci_95, log10_pvalue, ensembl75_name, inregnome_gene
       , insecreted_gene, intransmem_gene, num_subjects, num_refref, num_refalt, num_altalt, num_cases, num_controls, case_refref
       , case_refalt, case_altalt, control_refref, control_refalt, control_altalt, file_id, plink_stats_id, phenotype, method_type
       , collaborator, population, test_type, phenotype_category, data_freeze, run_date, phenotype_0, phenotype_1, phenotype_2, functional_prediction
       , hgvs_cdna, hgvs_amino_acid, islof, islast5pct, isancestralallele, isindel, alt_freq
       , pos, ref, alt, rsid, name, hwe_pval, l_ci_95, u_ci_95, hwe_flag, mac_flag, lambda_gc, lambda_flag, istier1_phenotype
from  regeneronFlatTable
where  collaborator in ('34-509-325-8688', '26-282-609-4959', '13-643-597-6305', '25-989-741-2988', '20-781-609-3107') or
(gene_id >= 383081159 and gene_id <= 383097696  and hwe_flag = 'N') limit 1000000"""


queryStr1 = """select gene, chr, start, stop, mask, beta, stderr, odds_ratio, ci_95, log10_pvalue, ensembl75_name, inregnome_gene
       , insecreted_gene, intransmem_gene, num_subjects, num_refref, num_refalt, num_altalt, num_cases, num_controls, case_refref
       , case_refalt, case_altalt, control_refref, control_refalt, control_altalt, file_id, plink_stats_id, phenotype, method_type
       , collaborator, population, test_type, phenotype_category, data_freeze, run_date, phenotype_0, phenotype_1, phenotype_2, functional_prediction
       , hgvs_cdna, hgvs_amino_acid, islof, islast5pct, isancestralallele, isindel, alt_freq
       , pos, ref, alt, rsid, name, hwe_pval, l_ci_95, u_ci_95, hwe_flag, mac_flag, lambda_gc, lambda_flag, istier1_phenotype
from  regeneronFlatTable
where  (run_date < '19920301' and num_altalt =7) or phenotype in (' requests. slyly regular requests cajole furiously final requests. blithely ironic dependencies ought to are furiously. express instructions haggle furiously regular requests. blithely final a',
't the carefully ironic accounts haggle alongside of the final pinto beans. furiously bold courts sleep against the even packages. quickly regular deposits should integrate carefully al',
'ole furiously. slyly express multipliers wake closely? final asymptotes sleep slyly. carefully ironic accounts across the enticingly even packages cajole carefully across the special ',
', even theodolites. regular, final theodolites eat after the carefully pending foxes. furiously regular deposits sleep slyly. carefully bold realms above the ironic dependencies haggle careful',
'ely unusual deposits. deposits poach along the carefully final requests. dependencies boost quickly among the ironic de')
 limit 1000000"""

queryStr2 = """select gene, chr, start, stop, mask, beta, stderr, odds_ratio, ci_95, log10_pvalue, ensembl75_name, inregnome_gene
       , insecreted_gene, intransmem_gene, num_subjects, num_refref, num_refalt, num_altalt, num_cases, num_controls, case_refref
       , case_refalt, case_altalt, control_refref, control_refalt, control_altalt, file_id, plink_stats_id, phenotype, method_type
       , collaborator, population, test_type, phenotype_category, data_freeze, run_date, phenotype_0, phenotype_1, phenotype_2, functional_prediction
       , hgvs_cdna, hgvs_amino_acid, islof, islast5pct, isancestralallele, isindel, alt_freq
       , pos, ref, alt, rsid, name, hwe_pval, l_ci_95, u_ci_95, hwe_flag, mac_flag, lambda_gc, lambda_flag, istier1_phenotype
from  regeneronFlatTable
where  (hwe_pval > 90000 and  num_altalt < 4 and hwe_flag = 'R')
or name in (' blithely ironic ideas. carefully ironic deposits impress furiously. theodolites among the silent deposits sleep against the final, unusual instructions blithely ironic ideas. carefully ironic deposits impress furiously. theodolites among the silent deposits sleep against the final, unusual instructions blithely ironic ideas. carefully ironic deposits impress furiously. theodolites among the silent deposits sleep against the final, unusual instructions blithely ironic ideas. carefully ironic deposits impress furiously. theodolites among the silent deposits sleep against the final, unusual instructions blithely ironic ideas. carefully ironic deposits impress furiously. theodolites among the silent deposits sleep against the final, unusual instructions',
'ously regular deposits wake carefully slyly even courts. theodolites are blithely ruthlessly express foxes. carefully final foxes slously regular deposits wake carefully slyly even courts. theodolites are blithely ruthlessly express foxes. carefully final foxes slously regular deposits wake carefully slyly even courts. theodolites are blithely ruthlessly express foxes. carefully final foxes slously regular deposits wake carefully slyly even courts. theodolites are blithely ruthlessly express foxes. carefully final foxes slously regular deposits wake carefully slyly even courts. theodolites are blithely ruthlessly express foxes. carefully final foxes sl',
'leep quickly ironic deposits. furiously special theodolites use slyly unusual Tiresias. blithely final requests wake carefully. ironically busy frets after the blithely rleep quickly ironic deposits. furiously special theodolites use slyly unusual Tiresias. blithely final requests wake carefully. ironically busy frets after the blithely rleep quickly ironic deposits. furiously special theodolites use slyly unusual Tiresias. blithely final requests wake carefully. ironically busy frets after the blithely rleep quickly ironic deposits. furiously special theodolites use slyly unusual Tiresias. blithely final requests wake carefully. ironically busy frets after the blithely rleep quickly ironic deposits. furiously special theodolites use slyly unusual Tiresias. blithely final requests wake carefully. ironically busy frets after the blithely r',
' carefully unusual ideas. packages use slyly. blithely final pinto beans cajole along the furiously express requests. regular orbits haggle carefully. care carefully unusual ideas. packages use slyly. blithely final pinto beans cajole along the furiously express requests. regular orbits haggle carefully. care carefully unusual ideas. packages use slyly. blithely final pinto beans cajole along the furiously express requests. regular orbits haggle carefully. care carefully unusual ideas. packages use slyly. blithely final pinto beans cajole along the furiously express requests. regular orbits haggle carefully. care carefully unusual ideas. packages use slyly. blithely final pinto beans cajole along the furiously express requests. regular orbits haggle carefully. care',
'sts wake slyly along the deposits. quickly unusual deposits boost silent, ironic packages. unusual excuses wake ironic, unusual deposits. slyly slow instructions boost among the even, even pasts wake slyly along the deposits. quickly unusual deposits boost silent, ironic packages. unusual excuses wake ironic, unusual deposits. slyly slow instructions boost among the even, even pasts wake slyly along the deposits. quickly unusual deposits boost silent, ironic packages. unusual excuses wake ironic, unusual deposits. slyly slow instructions boost among the even, even pasts wake slyly along the deposits. quickly unusual deposits boost silent, ironic packages. unusual excuses wake ironic, unusual deposits. slyly slow instructions boost among the even, even pasts wake slyly along the deposits. quickly unusual deposits boost silent, ironic packages. unusual excuses wake ironic, unusual deposits. slyly slow instructions boost among the even, even pa')
 limit 1000000"""



queryStr3 = """select gene, chr, start, stop, mask, beta, stderr, odds_ratio, ci_95, log10_pvalue, ensembl75_name, inregnome_gene
       , insecreted_gene, intransmem_gene, num_subjects, num_refref, num_refalt, num_altalt, num_cases, num_controls, case_refref
       , case_refalt, case_altalt, control_refref, control_refalt, control_altalt, file_id, plink_stats_id, phenotype, method_type
       , collaborator, population, test_type, phenotype_category, data_freeze, run_date, phenotype_0, phenotype_1, phenotype_2, functional_prediction
       , hgvs_cdna, hgvs_amino_acid, islof, islast5pct, isancestralallele, isindel, alt_freq
       , pos, ref, alt, rsid, name, hwe_pval, l_ci_95, u_ci_95, hwe_flag, mac_flag, lambda_gc, lambda_flag, istier1_phenotype
from  regeneronFlatTable
where  run_date < 19980101 and run_date > 19940101 and
gene in ('Customer#38321', 'Customer#57532', 'Customer#76754', 'Customer#1', 'Customer#19101') limit 1000000"""

queryStr4 = """select gene, chr, start, stop, mask, beta, stderr, odds_ratio, ci_95, log10_pvalue, ensembl75_name, inregnome_gene
       , insecreted_gene, intransmem_gene, num_subjects, num_refref, num_refalt, num_altalt, num_cases, num_controls, case_refref
       , case_refalt, case_altalt, control_refref, control_refalt, control_altalt, file_id, plink_stats_id, phenotype, method_type
       , collaborator, population, test_type, phenotype_category, data_freeze, run_date, phenotype_0, phenotype_1, phenotype_2, functional_prediction
       , hgvs_cdna, hgvs_amino_acid, islof, islast5pct, isancestralallele, isindel, alt_freq
       , pos, ref, alt, rsid, name, hwe_pval, l_ci_95, u_ci_95, hwe_flag, mac_flag, lambda_gc, lambda_flag, istier1_phenotype
from  regeneronFlatTable
where  collaborator in ('34-509-325-8688', '26-282-609-4959', '13-643-597-6305', '25-989-741-2988', '20-781-609-3107')
or name in ('ptotes. quickly pending dependencies integrate furiously. fluffily ironic ideas impress blithely above the express accounts. furiously even epitaphs need to wakptotes. quickly pending dependencies integrate furiously. fluffily ironic ideas impress blithely above the express accounts. furiously even epitaphs need to wakptotes. quickly pending dependencies integrate furiously. fluffily ironic ideas impress blithely above the express accounts. furiously even epitaphs need to wakptotes. quickly pending dependencies integrate furiously. fluffily ironic ideas impress blithely above the express accounts. furiously even epitaphs need to wakptotes. quickly pending dependencies integrate furiously. fluffily ironic ideas impress blithely above the express accounts. furiously even epitaphs need to wak',
'lly against the even deposits. regular, even foxes after the fluffily ironic deposits sleep furiously regular requests. foxes haggle fluffily quickly ironic lly against the even deposits. regular, even foxes after the fluffily ironic deposits sleep furiously regular requests. foxes haggle fluffily quickly ironic lly against the even deposits. regular, even foxes after the fluffily ironic deposits sleep furiously regular requests. foxes haggle fluffily quickly ironic lly against the even deposits. regular, even foxes after the fluffily ironic deposits sleep furiously regular requests. foxes haggle fluffily quickly ironic lly against the even deposits. regular, even foxes after the fluffily ironic deposits sleep furiously regular requests. foxes haggle fluffily quickly ironic ',
'ts nag ironic accounts. furiously even decoys are. express dependencies cajole furiouts nag ironic accounts. furiously even decoys are. express dependencies cajole furiouts nag ironic accounts. furiously even decoys are. express dependencies cajole furiouts nag ironic accounts. furiously even decoys are. express dependencies cajole furiouts nag ironic accounts. furiously even decoys are. express dependencies cajole furiou',
'at blithely ironic deposits. quickly regular packages cajole quickly pending requests. silent packages sleep slyly aloat blithely ironic deposits. quickly regular packages cajole quickly pending requests. silent packages sleep slyly aloat blithely ironic deposits. quickly regular packages cajole quickly pending requests. silent packages sleep slyly aloat blithely ironic deposits. quickly regular packages cajole quickly pending requests. silent packages sleep slyly aloat blithely ironic deposits. quickly regular packages cajole quickly pending requests. silent packages sleep slyly alo',
', even theodolites. regular, final theodolites eat after the carefully pending foxes. furiously regular deposits sleep slyly. carefully bold realms above the ironic dependencies haggle careful, even theodolites. regular, final theodolites eat after the carefully pending foxes. furiously regular deposits sleep slyly. carefully bold realms above the ironic dependencies haggle careful, even theodolites. regular, final theodolites eat after the carefully pending foxes. furiously regular deposits sleep slyly. carefully bold realms above the ironic dependencies haggle careful, even theodolites. regular, final theodolites eat after the carefully pending foxes. furiously regular deposits sleep slyly. carefully bold realms above the ironic dependencies haggle careful, even theodolites. regular, final theodolites eat after the carefully pending foxes. furiously regular deposits sleep slyly. carefully bold realms above the ironic dependencies haggle careful',
'requests sleep quickly regular accounts. theodolites detect. carefully final depths wrequests sleep quickly regular accounts. theodolites detect. carefully final depths wrequests sleep quickly regular accounts. theodolites detect. carefully final depths wrequests sleep quickly regular accounts. theodolites detect. carefully final depths wrequests sleep quickly regular accounts. theodolites detect. carefully final depths w')
limit 1000000"""




FNULL = open(os.devnull, 'w')

startingIteration = 7
endingIteration = 13

for iteration in xrange(startingIteration, endingIteration):

    for numNodes in xrange(0, 5):
        
        nodeIPsIn = [nodeIPs[0]]
        nodePortsIn = [nodePorts[0]]
    #    nodeIPsIn = [nodeIPs[numNodes]]
    #    nodePortsIn = [nodePorts[numNodes]]

        if numNodes + 1 > 1:
            for nodeInd in xrange(1, numNodes + 1):
                nodeIPsIn += [nodeIPs[nodeInd]]
                nodePortsIn += [nodePorts[nodeInd]]
        
        setNodesInfo(nodesFile, nodeIPsIn, nodePortsIn)
        print "$$$$$$$$$$$ testing on node: " + str(numNodes)
        
        p = subprocess.Popen(["Simplicity", "8890", "/disk1/blazing/blazing.conf"], stdout=FNULL, stderr=subprocess.STDOUT)
        print "Starting Blazing Service with subprocess %s" % p.pid
        time.sleep(2)
        
        memo = str(numNodes + 1) + " nodes|" + str(1.2*(iteration+1)) + " rows per node (millions)"
        print memo
        
        bh = LocalBlazingHandler("127.0.0.1", 8890, schema, db)
        bh.limitDataFetch = True
        comp = PostgresComparisonTestSet(bh, "")
    #    comp.runAndValidateQuery(queryStr0, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr1, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr2, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr3, showVerboseQuery=True)
    #    comp.runAndValidateQuery(queryStr4, showVerboseQuery=True)
        comp.runAndValidateQuery(queryStr0)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr1)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr2)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr3)
     #   time.sleep(2)
        comp.runAndValidateQuery(queryStr4)


        comp.logResults(logFile, version, memo)

        p.terminate()
        returncode = p.wait()
        print "Returncode of subprocess: %s" % returncode
        time.sleep(1)


    p = subprocess.Popen(["Simplicity", "8890", "/disk1/blazing/blazing.conf"], stdout=FNULL, stderr=subprocess.STDOUT)
    print "About to loadDataInfile.    Starting Blazing Service with subprocess %s" % p.pid
    time.sleep(2)
    bh.delimiterStr = "','"
    loadStartTime = float(time.time())
    bh.loadDataInfile("reg.csv", "regeneronFlatTable")
    print "load took: " + str(float(time.time()) - loadStartTime)
#    time.sleep(900)
    p.terminate()
    returncode = p.wait()
    print "Finished loadDataInfile.     Returncode of subprocess: %s" % returncode
    time.sleep(1)
