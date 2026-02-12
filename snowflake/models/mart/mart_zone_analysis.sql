SELECT
"PULocationID",
COUNT(*) as nb_trips,
AVG("total_amount") as mean_amount,
DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS "Popularity_rank" -- même chose que rank mais avec les ex aequo
FROM {{ ref('stg_nyc_taxi') }}
GROUP BY "PULocationID"