
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_actual_cost
from "analytics_db"."curated"."mart_executive_dashboard"
where total_actual_cost is null



  
  
      
    ) dbt_internal_test