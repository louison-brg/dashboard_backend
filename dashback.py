import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from datetime import datetime

# Initialisation de Flask
app = Flask(__name__)

# Initialisation de l'API YouTube avec votre clé API
api_key = "AIzaSyD3XbQ_CpaN235MAzZOCrhGwErUp0eRQnM"#Louison
#api_key = 'AIzaSyCCWBjLdTBnOIF7bXSfhj73BYcY_195iGw'#pyves
youtube = build('youtube', 'v3', developerKey=api_key)

def formatDate(date):
    """Formatte la date en format jour/mois/année."""
    dateObj = datetime.fromisoformat(date)
    dateFormatee = dateObj.strftime("%d/%m/%Y")
    return dateFormatee

def get_video_statistics(video_id):
    """Récupère les statistiques d'une vidéo spécifique."""
    request = youtube.videos().list(part="statistics", id=video_id)
    response = request.execute()
    return response['items'][0]['statistics']

def get_video_duration(video_id):
    """Récupère la durée d'une vidéo spécifique."""
    request = youtube.videos().list(part="contentDetails", id=video_id)
    response = request.execute()
    return response['items'][0]['contentDetails']

def convertDurationToSeconds(duration):
    """Convertit la durée ISO 8601 en secondes."""
    pattern = re.compile('PT(\d+H)?(\d+M)?(\d+S)?')
    parts = pattern.match(duration)
    hours = int(parts.group(1)[:-1]) if parts.group(1) else 0
    minutes = int(parts.group(2)[:-1]) if parts.group(2) else 0
    seconds = int(parts.group(3)[:-1]) if parts.group(3) else 0
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

@app.route('/getCreatorInfos', methods=['GET'])
def get_creator_infos():
    """Récupère les informations d'un créateur à partir du nom de la chaîne."""
    channelName = request.args.get('channelName')
    if not channelName:
        return jsonify({"error": "Le paramètre channelName est requis."}), 400

    requestChannelName = youtube.search().list(q=channelName, part="snippet", type='channel', maxResults=1)
    resultChannel = requestChannelName.execute()
    channel_info = {}

    if resultChannel['items']:
        channel = resultChannel['items'][0]
        channel_info = {
            "channelDateOfCreation": formatDate(channel['snippet']['publishedAt']),
            "channelName": channel['snippet']['title'],
            "channelDescription": channel['snippet']['description'],
            "channelId": channel['snippet']['channelId'],
            "channelProfilePicLink": channel['snippet']['thumbnails']['default']['url']
        }

        requestChannelStats = youtube.channels().list(part="statistics", id=channel_info['channelId'])
        resultStats = requestChannelStats.execute()

        if 'statistics' in resultStats['items'][0]:
            stats = resultStats['items'][0]['statistics']
            channel_info.update({
                "viewCount": stats.get('viewCount', 0),
                "subscriberCount": stats.get('subscriberCount', 0),
                "videoCount": stats.get('videoCount', 0)
            })

    return jsonify(channel_info)

@app.route('/getLatestPosts', methods=['GET'])
def get_latest_posts():
    """Récupère les 5 derniers posts d'une chaîne spécifique d'une durée supérieure à 60 secondes."""
    channelId = request.args.get('channelId')
    if not channelId:
        return jsonify({"error": "Le paramètre channelId est requis."}), 400

    # Augmente le nombre de résultats récupérés pour s'assurer d'obtenir suffisamment de vidéos de plus de 60 secondes
    requestLatestPosts = youtube.activities().list(part="snippet,contentDetails", channelId=channelId, maxResults=50)
    responseLatestPosts = requestLatestPosts.execute()
    latest_posts = []

    for video in responseLatestPosts['items']:
        if len(latest_posts) >= 5:  # Stoppe la boucle une fois que 5 vidéos valides ont été trouvées
            break

        if video['snippet']['type'] == 'upload':
            video_id = video['contentDetails']['upload']['videoId']
            videoDetails = get_video_duration(video_id)
            duration_seconds = convertDurationToSeconds(videoDetails['duration'])

            if duration_seconds > 60:
                videoStats = get_video_statistics(video_id)
                latest_posts.append({
                    "postDate": formatDate(video['snippet']['publishedAt']),
                    "postTitle": video['snippet']['title'],
                    "postPicture": video['snippet']['thumbnails'].get('standard', {}).get('url', ''),
                    "postViews": videoStats.get('viewCount', '0'),
                    "postLikes": videoStats.get('likeCount', '0'),
                    "postComments": videoStats.get('commentCount', '0'),
                    "postDuration": videoDetails['duration']  # Keeping the original format for display
                })

    # Si moins de 5 vidéos sont trouvées, toutes seront retournées
    return jsonify(latest_posts)


# CORS pour permettre les requêtes cross-origin
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)