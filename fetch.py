import requests
import json
import logging
from google.cloud import pubsub_v1

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# YouTube API and Google Cloud Pub/Sub settings
api_key = "AIzaSyBmqpfdsXA6nJh4cqIfNyBiORZkr-GrG1E"  # Replace with your actual API key
project_id = "composer-youtube"      # Replace with your actual Google Cloud project ID
topic_id = "Trigger-youtube"         # Replace with your actual Pub/Sub topic ID
query = " "               # YouTube query for video search

# YouTube API endpoints
search_endpoint = "https://www.googleapis.com/youtube/v3/search"
video_details_endpoint = "https://www.googleapis.com/youtube/v3/videos"
video_categories_endpoint = "https://www.googleapis.com/youtube/v3/videoCategories"

# Google Cloud Pub/Sub setup
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Fetch video category mapping
def fetch_video_category_mapping(api_key):
    params = {
        'part': 'snippet',
        'regionCode': 'US',  # Use the appropriate region code as needed
        'key': api_key
    }
    response = requests.get(video_categories_endpoint, params=params)
    categories = {}
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            categories[item['id']] = item['snippet']['title']
    return categories

# Fetch the video category mapping
video_category_mapping = fetch_video_category_mapping(api_key)

# Function to fetch data from the YouTube API and publish it to Pub/Sub
def fetch_data():
    try:
        # Step 1: Fetch YouTube videos based on the search query
        search_params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'key': api_key,
            'maxResults': 20
        }

        logger.info("Starting YouTube search...")
        search_response = requests.get(search_endpoint, params=search_params)
        logger.info(f"Received search response with status code: {search_response.status_code}")
        search_response.raise_for_status()

        search_data = search_response.json()
        logger.info(f"Search response data: {json.dumps(search_data, indent=2)}")

        # Extract video IDs from search results
        video_ids = [item['id']['videoId'] for item in search_data.get('items', [])]
        if not video_ids:
            logger.info("No videos found for this query.")
            return

        # Step 2: Fetch detailed video information
        video_params = {
            'part': 'snippet,statistics',
            'id': ','.join(video_ids),
            'key': api_key
        }

        logger.info("Fetching detailed video information...")
        video_response = requests.get(video_details_endpoint, params=video_params)
        logger.info(f"Received video details response with status code: {video_response.status_code}")
        video_response.raise_for_status()

        video_data = video_response.json()
        logger.info(f"Video response data: {json.dumps(video_data, indent=2)}")

        # Step 3: Publish video details to Pub/Sub
        for item in video_data.get('items', []):
            # Get the category ID and map it to the category name
            category_id = item['snippet'].get('categoryId', '')
            category_name = video_category_mapping.get(category_id, 'Unknown')

            # Prepare video details
            video_details = {
                'title': item['snippet']['title'],
                'video_id': item['id'],
                'channel_id': item['snippet']['channelId'],
                'channel_title': item['snippet']['channelTitle'],
                'category': category_name,
                'total_views': int(item['statistics'].get('viewCount', 0)),
                'likes': int(item['statistics'].get('likeCount', 0)),
                'dislikes': int(item['statistics'].get('dislikeCount', 0)),
                'comments': int(item['statistics'].get('commentCount', 0)),
                'publish_time': item['snippet']['publishedAt'],
                'subscription_name': topic_id,
                'message_id': ''  # This will be filled after publishing to Pub/Sub
            }

            message = json.dumps(video_details).encode("utf-8")
            try:
                logger.info("Publishing message to Pub/Sub...")
                future = publisher.publish(topic_path, message)
                video_details['message_id'] = future.result()  # Update with the actual message ID after publishing
                logger.info(f"Published metrics for channel ID: {item['snippet']['channelId']}, Message ID: {video_details['message_id']}")
            except Exception as e:
                logger.error(f"Failed to publish message to Pub/Sub: {e}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed during YouTube API request: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")

# Entry point for running the script
if __name__ == "__main__":
    logger.info("Starting main fetch_data execution...")
    fetch_data()
