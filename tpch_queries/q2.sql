-- TPC-H/TPC-R Parts/Supplier Relationship Query (Q2)
-- Functional Query Definition
-- Approved February 1998
select
    s.acctbal,
    s.name,
    n.name,
    p.partkey,
    p.mfgr,
    s.address,
    s.phone,
    s.comment
from
    part p,
    supplier s,
    partsupp ps,
    nation n,
    region r
where
    p.partkey = ps.partkey
    and s.suppkey = ps.suppkey
    and p.size = 15
    and p.type like '%BRASS'
    and s.nationkey = n.nationkey
    and n.regionkey = r.regionkey
    and r.name = 'EUROPE'
    and ps.supplycost = (
        select
            min(ps2.supplycost)
        from
            partsupp ps2,
            supplier s2,
            nation n2,
            region r2
        where
            p.partkey = ps2.partkey
            and s2.suppkey = ps2.suppkey
            and s2.nationkey = n2.nationkey
            and n2.regionkey = r2.regionkey
            and r2.name = 'EUROPE'
    )
order by
    s.acctbal desc,
    n.name,
    s.name,
    p.partkey
limit 100 