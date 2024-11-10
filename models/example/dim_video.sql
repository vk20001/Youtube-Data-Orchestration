-- models/dim_video.sql
SELECT DISTINCT
    video_id,
    title,
    category
FROM {{ ref('youtube_transformations') }}
