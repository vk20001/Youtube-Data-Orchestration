SELECT 
    category,
    AVG(total_views) AS avg_views,
    AVG(likes) AS avg_likes,
    AVG(comments) AS avg_comments
FROM {{ ref('fact_video_stats') }}
GROUP BY category
ORDER BY avg_views DESC
