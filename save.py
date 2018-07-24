#!/usr/bin/python

from apiclient.discovery import build
from oauth2client.tools import argparser
from pytube import YouTube

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
cId = "UCA6a0jmtB8RucZFx7l_Ek3A"
videos = []

def youtube_search(pagetoken):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # cId = input("チャンネルIDを指定してください:")
  search_response = youtube.search().list(
    # q=options.q,
    part="snippet",
    channelId=cId,
    maxResults=50,
    order="date",
    pageToken=pagetoken
  ).execute()

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append(search_result["id"]["videoId"])

  try:
      nextPagetoken =  search_response["nextPageToken"]
      youtube_search(nextPagetoken)
  except:
      return

def save_video():
    for ID in videos:
        query = 'https://www.youtube.com/watch?v=' + ID

        print(query+"を保存")
        yt = YouTube(query)
        yt.streams.filter(subtype='mp4').first().download("./videos/shizuoka")

if __name__ == "__main__":
    youtube_search("")
    save_video()
  # argparser.add_argument("--q", help="Search term", default="Google")
  # argparser.add_argument("--max-results", help="Max results", default=25)
  # args = argparser.parse_args()
