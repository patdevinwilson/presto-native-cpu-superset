-- TPC-H/TPC-R Top Supplier Query (Q15)
-- Functional Query Definition
-- Approved February 1998
with revenue0 as (
        select
                l.suppkey as supplier_no,
                sum(l.extendedprice * (1 - l.discount)) as total_revenue
        from
                lineitem l
        where
                l.shipdate >= date '1996-01-01'
                and l.shipdate < date '1996-01-01' + interval '3' month
        group by
                l.suppkey
)
select
        s.suppkey,
        s.name,
        s.address,
        s.phone,
        total_revenue
from
        supplier s,
        revenue0
where
        s.suppkey = revenue0.supplier_no
        and revenue0.total_revenue = (
                select
                        max(total_revenue)
                from
                        revenue0
        )
order by
        s.suppkey 