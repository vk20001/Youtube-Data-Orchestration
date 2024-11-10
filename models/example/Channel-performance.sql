SELECT 
  dc.channel_title,
  SUM(fv.total_views) AS total_channel_views,
  SUM(fv.likes) AS total_likes
FROM {{ ref('fact_video_stats') }} fv
JOIN {{ ref('dim_channel') }} dc
  ON fv.channel_id = dc.channel_id
GROUP BY dc.channel_title
ORDER BY total_channel_views DESC
