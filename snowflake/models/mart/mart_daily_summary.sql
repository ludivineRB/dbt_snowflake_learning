SELECT
"date",
COUNT("DOLocationID") as nb_trips,
AVG("trip_distance") as mean_distance,
SUM("total_amount") as total_amount_by_day
FROM {{ ref('stg_nyc_taxi') }}
GROUP BY "date"