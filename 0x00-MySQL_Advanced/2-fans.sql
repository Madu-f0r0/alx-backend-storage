-- Computes the total number of fans for all the bands originating from each country
-- origin: the country of origin of the bands
-- nb_fans: total number of (non-unique) fans for 
SELECT origin, SUM(fans) as nb_fans
    FROM metal_bands
    GROUP BY origin
    ORDER BY nb_fans DESC;
