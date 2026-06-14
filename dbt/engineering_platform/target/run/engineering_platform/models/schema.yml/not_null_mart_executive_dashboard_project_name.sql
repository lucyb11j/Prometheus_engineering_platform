
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select project_name
from "analytics_db"."curated"."mart_executive_dashboard"
where project_name is null



  
  
      
    ) dbt_internal_test