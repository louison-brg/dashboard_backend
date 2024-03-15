api_key = "AIzaSyCCWBjLdTBnOIF7bXSfhj73BYcY_195iGw"
from googleapiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=api_key)
"""
requestVid = youtube.search().list(q="avengers",part="snippet",type="video",maxResults=50)
resultVid = requestVid.execute()
for video in resultVid['items']:
    print(video['snippet']['title'])
"""
rechercheNomChaine = input("Quelle chaine YT cherches-tu ?\n")
requestChannel = youtube.search().list(q=rechercheNomChaine,part="snippet",type='channel',maxResults=1)
resultChannel = requestChannel.execute()

for channel in resultChannel['items']:
    print(channel['snippet'])
    print("Date de création: ",channel['snippet']['publishedAt']) #Date de création
    print("Créateur: ",channel['snippet']['title'])#Nom du créateur
    print("Description: ",channel['snippet']['description'])#Description de la chaine --> PROBLEME : ON A PAS LA DESCRIPTION ENTIERE
    print("ID : ",channel['snippet']['channelId'])#ID de la chaine (je ne sais pas si ça sera utile)
    print("PP: ",channel['snippet']['thumbnails']['default']['url'])#Lien vers la photo de profile


