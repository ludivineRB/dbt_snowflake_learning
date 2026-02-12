SELECT
"Hour",
COUNT(*) as nb_trips,
SUM("total_amount") as total_amount_by_hour,
AVG("mean_speed") as mean_speed_by_hour
FROM {{ ref('stg_nyc_taxi') }}
GROUP BY "Hour"