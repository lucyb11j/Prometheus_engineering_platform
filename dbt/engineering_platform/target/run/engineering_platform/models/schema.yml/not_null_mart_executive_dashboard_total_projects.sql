
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_projects
from "analytics_db"."curated"."mart_executive_dashboard"
where total_projects is null



  
  
      
    ) dbt_internal_test