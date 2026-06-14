
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_planned_cost
from "analytics_db"."curated"."mart_executive_dashboard"
where total_planned_cost is null



  
  
      
    ) dbt_internal_test