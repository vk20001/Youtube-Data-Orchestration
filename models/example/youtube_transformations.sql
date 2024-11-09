WITH initial_ranking AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY channel_id ORDER BY total_views DESC) AS row_num
    FROM {{ source('youtube_data', 'raw_data') }}
),
filtered_data AS (
    SELECT 
        title,
        video_id,
        channel_id,
        channel_title,
        total_views,
        COALESCE(likes, 0) AS likes,
        COALESCE(dislikes, 0) AS dislikes,
        COALESCE(comments, 0) AS comments,
        COALESCE(category, 'unknown') AS category
    FROM initial_ranking
    WHERE row_num = 1
),
final_ranking AS (
    SELECT 
        * ,
        ROW_NUMBER() OVER (PARTITION BY channel_id ORDER BY total_views DESC) AS row_num
    FROM filtered_data
)
SELECT *
FROM final_ranking
WHERE row_num = 1
AND (
    title IS NOT NULL
    OR video_id IS NOT NULL
    OR channel_id IS NOT NULL
    OR channel_title IS NOT NULL
    OR total_views IS NOT NULL
    OR likes IS NOT NULL
    OR dislikes IS NOT NULL
    OR comments IS NOT NULL
    OR category IS NOT NULL
)
