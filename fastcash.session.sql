-- drop table producttaglink cascade;
-- drop table product cascade;
-- drop table tag cascade;
-- drop table producttype cascade;
select *
from product;
-- select *
-- from producttaglink
--     inner join product on product.id = producttaglink.product_id
--     inner join tag on tag.id = producttaglink.tag_id;