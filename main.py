import os
import dotenv
import pydub
import dotenv
import time
import base64
import hashlib
import hmac

# going to make this project monolithic, since i want this to be as user friendly as possible so i don't want to have
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

    files_with_metadata = []

    # prepare post request with necessary data

    http_method = "POST"
    http_uri = "/v1/identify"
    data_type = "audio"
    signature_version = "1"

    for file in os.listdir("./tempMusicStorage/"):
        #further preparation for post request, required to be inside the loop so as the timestamp will change with each file processed

        timestamp = time.time()

        string_to_sign = http_method + "\n" + http_uri + "\n" + acrcloud_access_key + "\n" + data_type + "\n" + signature_version + "\n" + str(
            timestamp)

        sign = base64.b64encode(
            hmac.new(acrcloud_access_secret.encode('ascii'),
                     string_to_sign.encode('ascii'),
                     digestmod=hashlib.sha1).digest()).decode('ascii')

    return files_with_metadata


def close_temp_folder():
    """
    closes temporary folder created by the above functions
    doesnt take any inputs
    
    :)
    """

    os.remove("./tempMusicStorage")