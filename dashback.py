api_key = "AIzaSyCCWBjLdTBnOIF7bXSfhj73BYcY_195iGw"
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=api_key)
#channelName = input("Quelle chaine YT cherches-tu ?\n")
def getCreatorInfos(channelName):
    requestChannelName = youtube.search().list(q=channelName, part="snippet", type='channel', maxResults=1)
    resultChannel = requestChannelName.execute()
    channel_info = {}

    for channel in resultChannel['items']:
        channel_info["channelDateOfCreation"] = channel['snippet']['publishedAt']
        channel_info["channelName"] = channel['snippet']['title']
        channel_info["channelDescription"] = channel['snippet']['description']
        channel_info["channelId"] = channel['snippet']['channelId']
        channel_info["channelProfilePicLink"] = channel['snippet']['thumbnails']['default']['url']

    return channel_info

creator_info = getCreatorInfos('squeezie')
print("Date de création de la chaîne:", creator_info["channelDateOfCreation"])
print("Nom de la chaîne:", creator_info["channelName"])
print("Description de la chaîne:", creator_info["channelDescription"])
print("ID de la chaîne:", creator_info["channelId"])
print("Lien vers la photo de profil de la chaîne:", creator_info["channelProfilePicLink"])


def getLatestPosts(channelId, max_posts=3):
    requestLatestPosts = youtube.activities().list(part="snippet,contentDetails", channelId=channelId, maxResults=50)
    responseLatestPosts = requestLatestPosts.execute()
    countUpload = 0
    latest_posts = []

    for video in responseLatestPosts['items']:
        if countUpload == max_posts:
            break
        if video['snippet']['type'] != 'upload':
            pass
        else:
            post_info = {}
            post_info["postDate"] = video['snippet']['publishedAt']
            post_info["postTitle"] = video['snippet']['title']
            post_info["postPicture"] = video['snippet']['thumbnails']['standard']['url']
            post_info["postStats"] = get_video_statistics(video['contentDetails']['upload']['videoId'])
            latest_posts.append(post_info)
            countUpload += 1
    return latest_posts

def get_video_statistics(video_id):
    request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    response = request.execute()
    return response['items'][0]['statistics']

latest_posts = getLatestPosts(channelId=creator_info["channelId"], max_posts=3)
for post in latest_posts:
    print("Moment de parution:", post["postDate"])
    print("Titre:", post["postTitle"])
    print("Miniature:", post["postPicture"])
    print("Statistiques de la vidéo:", post["postStats"])
