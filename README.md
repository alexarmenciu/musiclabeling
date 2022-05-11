# MusicLabling
Python utility to label music files in a directory with their respective metadata.
## Setup
This project uses a python library that depends on ffmpeg to handle mp3 files behind the scenes. As such, you will need to download a copy of ffmpeg (from a site such as this https://www.gyan.dev/ffmpeg/builds/). Once you have downloaded the zip file, extract it. You will then need to add the path to the /bin folder to your windows path environment variable:
![musiclabeling2](https://user-images.githubusercontent.com/65733434/167953475-5d7f09aa-5ee0-46f1-833b-e26261d7a439.png)
Once you have done this, you will also need an acrcloud account to get api keys, as this is the music recogntion service my script uses behind the scenes. To do this, go to https://www.acrcloud.com/ and click sign up. Then, navigate to the acrcloud console, Audio & Video Recognition secion, go to projects, and make a new project with the line in audio setting. 
![musiclabeling1](https://user-images.githubusercontent.com/65733434/167952879-958375fe-5665-4df9-93f9-ec390fafc225.png)
Your project will have 3 fields you need to copy into the .env file. 
![musiclabeling3](https://user-images.githubusercontent.com/65733434/167953735-eea6ebf9-3eb7-48eb-8052-a08f6d55a55d.png)
Set ACR_ACCESS to the value you see in the Access Key field. Set ACR_SECRET to the value you see in your Secret Key field. Set ACR_URL to http://Host/v1/identify, where Host is the value you see in your Host field.
Finally, run the install.cmd file. This should install the requests, eyed3, dotenv, and pydub python libraries. If it doesn't, my bad. Use pip to install them.

## Usage
Run main.py.
