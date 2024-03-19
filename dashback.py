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

        # Requête pour obtenir les statistiques de la chaîne
        requestChannelStats = youtube.channels().list(part="statistics", id=channel_info['channelId'])
        resultStats = requestChannelStats.execute()

        # Ajout des statistiques à channel_info
        if 'statistics' in resultStats['items'][0]:
            channel_info["viewCount"] = resultStats['items'][0]['statistics'].get('viewCount', 0)
            channel_info["subscriberCount"] = resultStats['items'][0]['statistics'].get('subscriberCount', 0)
            channel_info["videoCount"] = resultStats['items'][0]['statistics'].get('videoCount', 0)
            channel_info["likes"] = resultStats['items'][0]['statistics'].get('likeCount', 0)
            channel_info["uploads"] = resultStats['items'][0]['statistics'].get('uploadCount', 0)

    return channel_info


creator_info = getCreatorInfos('misterjday')
print("Date de création de la chaîne:", creator_info.get("channelDateOfCreation", "N/A"))
print("Nom de la chaîne:", creator_info.get("channelName", "N/A"))
print("Description de la chaîne:", creator_info.get("channelDescription", "N/A"))
print("Lien vers la photo de profil de la chaîne:", creator_info.get("channelProfilePicLink", "N/A"))
print("Nombre de vues totales de la chaîne:", creator_info.get("viewCount", "N/A"))
print("Nombre total d'abonnés à la chaîne:", creator_info.get("subscriberCount", "N/A"))
print("Nombre total de vidéos mises en ligne:", creator_info.get("videoCount", "N/A"))
print(50*"=","\n")
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
            post_info["postViews"] = get_video_statistics(video['contentDetails']['upload']['videoId'])['viewCount']
            post_info["postLikes"] = get_video_statistics(video['contentDetails']['upload']['videoId'])['likeCount']
            post_info["postComments"] = get_video_statistics(video['contentDetails']['upload']['videoId'])['commentCount']
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
    print("Titre:", post["postTitle"])
    print("Moment de parution:", post["postDate"])
    print("Miniature:", post["postPicture"])
    print("Vues:", post["postViews"])
    print("Likes:", post["postLikes"])
    print("Comments:", post["postComments"],'\n')


