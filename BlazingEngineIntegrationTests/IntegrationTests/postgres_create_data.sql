create table customer ( c_custkey bigint PRIMARY KEY not null, c_name char(32), c_address char(128), c_nationkey bigint, c_phone char(16), c_acctbal double precision, 
                       c_mktsegment char(16), c_comment char(120) );

create table lineitem ( l_orderkey bigint PRIMARY KEY not null, l_partkey bigint, l_suppkey bigint, l_linenumber bigint, l_quantity double precision, 
                       l_extendedprice double precision, 
                       l_discount double precision, l_tax double precision, l_returnflag char(8), l_linestatus char(8), l_shipdate date, l_commitdate  date, 
                       l_receiptdate  date, l_shipinstruct char(32), l_shipmode char(16), l_comment char(48) );

create table nation ( n_nationkey bigint PRIMARY KEY not null, n_name char(32), n_regionkey bigint, n_comment char(152) );

create table orders ( o_orderkey bigint PRIMARY KEY not null, o_custkey bigint, o_orderstatus char(8), o_totalprice double precision, o_orderdate date, 
                     o_orderpriority char(16), 
                     o_clerk char(16), o_shippriority bigint, o_comment char(80) );

create table part ( p_partkey bigint PRIMARY KEY not null, p_name char(56), p_mfgr char(32), p_brand char(16), p_type char(32), 
                   p_size bigint, p_container char(16), p_retailprice double precision, p_comment char(24) );

create table partsupp ( ps_partkey bigint PRIMARY KEY not null, ps_suppkey bigint, ps_availqty bigint, ps_supplycost double precision, ps_comment char(200) );

create table region ( r_regionkey bigint PRIMARY KEY not null, r_name char(32), r_comment char(152) );

create table supplier ( s_suppkey bigint PRIMARY KEY not null, s_name char(32), s_address char(40), s_nationkey bigint, 
                       s_phone char(16), s_acctbal double precision, s_comment char(104) );

ALTER TABLE lineitem DROP CONSTRAINT lineitem_pkey

COPY customer FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\customer.tbl' DELIMITER '|' CSV;
COPY lineitem FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\lineitem.tbl' DELIMITER '|' CSV;
COPY nation FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\nation.tbl' DELIMITER '|' CSV;
COPY orders FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\orders.tbl' DELIMITER '|' CSV;
COPY part FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\part.tbl' DELIMITER '|' CSV;
COPY partsupp FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\partsupp.tbl' DELIMITER '|' CSV;
COPY region FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\region.tbl' DELIMITER '|' CSV;
COPY supplier FROM 'C:\Users\pc\Documents\Blazing\BlazingEngineIntegrationTests\DataSets\TPCH50Mb\supplier.tbl' DELIMITER '|' CSV;