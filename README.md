![made-with-python](https://img.shields.io/badge/Made%20with-Python3-brightgreen)

<!-- LOGO -->
<br />
<p align="center">
  <img src="https://user-images.githubusercontent.com/54740007/212677385-8f453f16-06fd-41e2-83a6-8a25d5435418.png" alt="Logo" width="80" height="80">

  <h3 align="center">TikTokUploder</h3>

  <p align="center">
    Python3 script to upload video to TikTok by sessionId
    <br />
    </p>
</p>


## About The Project

**If you found it helpful, please give me a little star, TKS!**

This project is a Python3 script that allows you to automatically upload and schedule TikTok videos. With this script, you can automate the process of uploading videos to TikTok, allowing you to save time and focus on creating content.

The script is easy to use and requires minimal setup. Simply provide your TikTok *sessionid* cookie, the video file you wish to upload and the video details, and the script will handle the rest.

## Getting Started
To get started you need to have python3. If it is not the case you can download it here : https://www.python.org/downloads <br><br>
You will also need your TikTok ***sessionid* cookie**. To get it log in to your TikTok account and on the page https://www.tiktok.com/ press the F12 key on your keyboard then Application > Storage > Cookies and find the value of the *sessionid* cookie. You should have something like this: `7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d` <br><br>

### Installation
Make sure you've already git installed. Then you can run the following commands to get the scripts on your computer:
   ```sh
   git clone https://github.com/546200350/TikTokUploder.git
   cd TikTokUploder
   ```
The script only requires the `requests` module, you can install it with this command:
```sh
pip install -r requirements.txt
```
   
## Usage
### Import in your script
You can copy the file `uploader.py` and `util.py` in your project folder and use it like this:
```python
from uploader import uploadVideo

session_id = "7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d"
file = "my_video.mp4"
title = "MY SUPER TITLE"
tags = ["Funny", "Joke", "fyp"]
users = ["amazing dear"]
proxy = {'http': 'http://ip:port', 'https': 'https://ip:port'}

# Publish the video
uploadVideo(session_id, file, title, tags, users, proxy=proxy)
```
- `session_id`: Your TikTok *sessionid* cookie.<br>
- `file`: The path to the video you want to upload.<br>
- `title`: The title of your publication (without hashtags).<br>
- `tags`: The list of hashtags you want to add to your post (without `#` symbol). May be empty list `[]`.<br>
- `users`: The list of users you want to mentioned to your post (without `@` symbol). May be empty list `[]`.<br>
- `url_prefix`: default: us, The request domain. Different countries require different domain configurations.<br>
- `schedule_time`: The timestamp (in seconds) at which you want to schedule your video. May be `None` (publish now).<br>
- `proxy`: The proxy you want to use should be in dict format, you can include ```user:pass``` if you require auth. May be ```None```<br>
**Note that you cannot schedule a video more than 10 days in advance.**<br>
**Note that your TikTok *sessionid* cookie needs to be updated every 2 months.**

### With the command line
```
usage: uploader.py [-h] -i SESSION_ID -p PATH -t TITLE [--tags [TAGS ...]]

options:
  -h, --help            show this help message and exit
  -i SESSION_ID, --session_id SESSION_ID
                        Tiktok sessionid cookie
  -p PATH, --path PATH  Path to video file
  -t TITLE, --title TITLE
                        Title of the video
  --tags [TAGS ...]     List of hashtags for the video
  --users [USERS ...]   List of mentioned users for the video
```                        
The `session_id`, `path` and `title` fields are required.
    
#### Example
This command will publish the video `my_video.mp4` as `MY SUPER TITLE #Funny #Joke #fyp`
```sh
python3 ./TikTokUploader/uploader.py -i 7a9f3c5d8f6e4b2a1c9d8e7f6a5b4c3d -p my_video.mp4 -t "MY SUPER TITLE" --tags Funny Joke Fyp --users amazing
```
#### Extendtion
You can achieve various sophisticated automation operations through this plugin.

For example: automatically retrieve and publish user videos from third-party platforms (YouTube, Douyin) or local videos.

For any other ideas, feel free to contact me via [Telegram](https://t.me/bird_biubiubiu).

## <a href="https://bmc.link/gugezhangyK" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee" style="height: 24px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
### Note
 <b>The upload api domain is different from different country. Sometimes, if you upload fail,you may replace all the domain (us.tiktok) to wwww.tikok. you can open the website network pan to find the correct domain.</b>
## Disclaimer
1. This application is an open-source project intended for learning and research purposes.
2. The author assumes no responsibility for any direct or indirect losses incurred through the use of this application.
3. When using this application, it is essential to comply with the laws and regulations of your country or region and refrain from any illegal activities.

By using this application, you agree to and accept all the terms and conditions of this disclaimer. If you do not agree with these terms, please refrain from using this application.

