YouTube Data Fetcher
YouTube Data Fetcher is a Flask-based application that interfaces with the YouTube API to fetch and display information about YouTube content creators, including general channel information, social links, and the latest video posts.

Features
Fetch detailed information of a YouTube creator by channel name, including the channel's creation date, description, profile picture, view count, subscriber count, video count, and social media links (YouTube, Instagram, TikTok, Twitter).
Retrieve the 5 latest video posts of a specified channel that are longer than 60 seconds, including the video ID, post date, title, thumbnail, views, likes, comments, and duration in a human-readable format.
Setup and Installation
Install Python and Flask: Make sure you have Python installed on your machine. Flask can be installed using pip:

bash
Copy code
pip install Flask
Install Additional Dependencies: This application also requires google-api-python-client for YouTube API requests and selenium for scraping social links:

bash
Copy code
pip install --upgrade google-api-python-client selenium
Note: For Selenium, you'll also need to download the appropriate WebDriver for your browser and ensure it's accessible from your PATH.

API Key: You need a valid YouTube API key to make requests. Replace the placeholder in the code with your actual API key.

Running the Application: Navigate to the application directory in your terminal and run the following command:

bash
Copy code
flask run
The application will start on localhost with the default port 5000.

Usage
The application exposes three main endpoints:

/getCreatorInfos?channelName=<CHANNEL_NAME>: Fetches and returns information about the specified YouTube channel.
/getLatestPosts?channelId=<CHANNEL_ID>: Retrieves the latest video posts for the specified channel ID.
Contributions
Contributions are welcome! Please fork the repository and submit pull requests with any enhancements. Make sure to follow the existing code style and add comments where necessary.

License
This project is open-sourced under the MIT License. See the LICENSE file for more details.
