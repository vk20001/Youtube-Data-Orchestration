SELECT 
    video_id,
    channel_id,
    total_views,
    likes,
    dislikes,
    comments,
    category
FROM {{ ref('youtube_transformations') }}