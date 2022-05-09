import os
import dotenv
import pydub
import dotenv

# going to make this file a little monolithic, since i want this to be as user friendly as possible so i don't want to have
# the user cart around two scripts wherever they need the functionality

dotenv.load_dotenv()

acrcloud_access_key = os.environ.get("ACR_ACCESS")
acrcloud_access_secret = os.environ.get("ACR_SECRET")
acrcloud_request_url = os.environ.get("ACR_URL")


def get_music_files():
    """
    Get a list of supported files in the current directory
    """
    files = []

    for f in os.listdir("."):
        if os.path.isfile(f) and (f.endswith(".mp3") or f.endswith(".wav")):
            files.append(f)

    return files


def reduce_file_size(files):
    """
    Creates a temporary folder with the music files at a reduced size since the acrcloud service accepts <1mb files
    returns no output
    
    Args:
        files (file list): list of music files to be reduced in size
    """
    os.makedirs("tempMusicStorage")

    # iterate through each file, cut to 15 sec, save in temp folder
    for file in files:
        if file.endswith(".mp3"):

            audio = pydub.AudioSegment.from_mp3(file=file)
            first_fifteen = audio[:15000]

            first_fifteen.export("./tempMusicStorage/" + file, format=".mp3")


def query_acrcloud(reduced_music_files):
    """
    returns a list of tuples, of music files and their metadata as recognized by acrcloud

    Args:
        reduced_music_files (file list): list of music files below 1mb to be identified by acrcloud
    """

    for file in os.listdir("./tempMusicStorage/"):
        print(1)

    return []


def close_temp_folder():
    """
    closes temporary folder created by the above functions
    doesnt take any inputs
    
    :)
    """

    os.remove("./tempMusicStorage")