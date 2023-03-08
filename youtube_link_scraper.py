import googleapiclient.discovery

# Replace YOUR_API_KEY with your actual API key
api_key = 'YOUR_API_KEY'

# Create a YouTube API client
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

# Call the API to get the playlist ID of the channel's uploads playlist
channel_response = youtube.channels().list(
    part='contentDetails',
    id='THE_ID_OF_THE_CHANNELL_YOU_ARE_SCRAPING'
).execute()

# print(channel_response)
# print(channel_response.keys())
uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Call the API to get all videos in the uploads playlist
videos = []
next_page_token = None
while True:
    playlist_items_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    ).execute()
    videos.extend(playlist_items_response['items'])
    next_page_token = playlist_items_response.get('nextPageToken')
    if not next_page_token:
        break

# Save the video links and titles to a text file
with open('video_links.txt', 'w') as f:
    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_title = video['snippet']['title']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        f.write(f'{video_title}: {video_link}\n')
