-- models/dim_channel.sql
SELECT DISTINCT
    channel_id,
    channel_title
FROM {{ ref('youtube_transformations') }}
