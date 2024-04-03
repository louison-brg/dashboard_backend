import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Initialisation de Flask
app = Flask(__name__)
# CORS pour permettre les requêtes cross-origin
CORS(app)

# Initialisation de l'API YouTube avec votre clé API
api_key = 'AIzaSyCCWBjLdTBnOIF7bXSfhj73BYcY_195iGw'  # pyves
# api_key = 'AIzaSyD3XbQ_CpaN235MAzZOCrhGwErUp0eRQnM' #Louison
# api_key = 'AIzaSyB-QmKyOgODjThs3XJjxW4glgkoYbO9Smc' #virgile
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

def convertISOtoNormal(duration):
    """Convertit la durée ISO 8601 en format 'xx:xx:xx'."""
    pattern = re.compile('PT(\d+H)?(\d+M)?(\d+S)?')
    parts = pattern.match(duration)
    hours = int(parts.group(1)[:-1]) if parts.group(1) else 0
    minutes = int(parts.group(2)[:-1]) if parts.group(2) else 0
    seconds = int(parts.group(3)[:-1]) if parts.group(3) else 0
    duration_formatted = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return duration_formatted


def add_spaces_to_number(number):
    """Ajoute des espaces tous les trois chiffres dans le nombre."""
    return '{:,}'.format(number).replace(',', ' ')


@app.route('/getCreatorInfos', methods=['GET'])
def get_creator_infos():
    """Get information of a creator from the channel name."""
    channel_name = request.args.get('channelName')
    if not channel_name:
        return jsonify({"error": "The channelName parameter is required."}), 400

    request_channel = youtube.search().list(q=channel_name, part="snippet", type='channel', maxResults=1)
    result_channel = request_channel.execute()
    channel_info = {}

    if result_channel['items']:
        channel = result_channel['items'][0]
        channel_id = channel['snippet']['channelId']
        channel_info = {
            "channelDateOfCreation": formatDate(channel['snippet']['publishedAt']),
            "channelName": channel['snippet']['title'],
            "channelDescription": channel['snippet']['description'],
            "channelId": channel_id,
            "channelProfilePicLink": channel['snippet']['thumbnails']['high']['url']
        }

        request_channel_stats = youtube.channels().list(part="statistics", id=channel_id)
        result_stats = request_channel_stats.execute()

        if 'statistics' in result_stats['items'][0]:
            stats = result_stats['items'][0]['statistics']
            channel_info.update({
                "viewCount": add_spaces_to_number(int(stats.get('viewCount', 0))),
                "subscriberCount": add_spaces_to_number(int(stats.get('subscriberCount', 0))),
                "videoCount": add_spaces_to_number(int(stats.get('videoCount', 0)))
            })

        social_links = get_social_links(channel_info["channelName"])
        channel_info.update(social_links)

    return jsonify(channel_info)


@app.route('/getCreatorInfos', methods=['GET'])
def get_social_links(channel_name):
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://socialblade.com/youtube/c/" + channel_name)
    links = {'youtube': 'None', 'instagram': 'None', 'tiktok': 'None', 'twitter': 'None'}
    for i in range(1, 5):
        try:
            button = driver.find_element(By.CSS_SELECTOR, f"#YouTubeUserTopSocial > div:nth-child({i}) > a")
            link = button.get_attribute("href")
            if 'youtube.com' in link:
                links['youtube'] = link
            elif 'instagram.com' in link:
                links['instagram'] = link
            elif 'tiktok.com' in link:
                links['tiktok'] = link
            elif 'twitter.com' in link:
                links['twitter'] = link
        except NoSuchElementException:
            break
    driver.quit()
    return links


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
                    "postPicture": video['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    "postViews": add_spaces_to_number(int(videoStats.get('viewCount', '0'))),
                    "postLikes": add_spaces_to_number(int(videoStats.get('likeCount', '0'))),
                    "postComments": add_spaces_to_number(int(videoStats.get('commentCount', '0'))),
                    "postDuration": convertISOtoNormal(videoDetails['duration'])
                })

    # Si moins de 5 vidéos sont trouvées, toutes seront retournées
    return jsonify(latest_posts)


if __name__ == '__main__':
    app.run(debug=True)
