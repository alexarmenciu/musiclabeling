from encodings import utf_8
import os
from turtle import up
import dotenv
import pydub
import dotenv
import time
import base64
import hashlib
import hmac
import requests
import eyed3

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
        if os.path.isfile(f) and (f.endswith(".mp3")):
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


def query_acrcloud():
    """
    returns a list of tuples, of music files and their metadata as recognized by acrcloud

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

        f = open(file, "rb")
        sample_bytes = os.path.getsize(file)
        files = [('sample', (file, f, 'audio/mpeg'))]

        data = {
            'access_key': acrcloud_access_key,
            'sample_bytes': sample_bytes,
            'timestamp': str(timestamp),
            'signature': sign,
            'data_type': data_type,
            "signature_version": signature_version
        }

        response = requests.post(acrcloud_request_url, files=files, data=data)
        response.encoding = "utf_8"

        files_with_metadata.append((file, response.json()))

    return files_with_metadata


def update_files_from_metadata(files_with_metadata):
    """
    updates song files in original directory with specified metadata

    Args:
        files_with_metadata (tuple list): list of tuples, first entry is a string with the name of a file, second is a metadata dictionary
    """

    for (file, metadata) in files_with_metadata:
        # prepare a string to specify multiple artists if such a case occurs

        artiststr = ""
        for artist in metadata["metadata"]["music"][0]["artists"]:
            artiststr += (artist["name"] + ";")

        artiststr.rstrip(";")

        #load audiofile in eyed3, update tags

        audiofile = eyed3.load(file)

        audiofile.tag.album = metadata["metadata"]["music"][0]["album"]["name"]
        audiofile.tag.artist = artiststr
        audiofile.tag.title = metadata["metadata"]["music"][0]["title"]

        #to update the year, you gotta update a whole bunch of metadata :smile: why couldn't eyed3 document this better :smile:

        audiofile.tag.year = metadata["metadata"]["music"][0][
            "release_date"].split("-")[0]
        audiofile.tag.original_release_date = metadata["metadata"]["music"][0][
            "release_date"].split("-")[0]
        audiofile.tag.recording_date = metadata["metadata"]["music"][0][
            "release_date"].split("-")[0]
        audiofile.tag.tagging_date = metadata["metadata"]["music"][0][
            "release_date"].split("-")[0]
        audiofile.tag.encoding_date = metadata["metadata"]["music"][0][
            "release_date"].split("-")[0]

        audiofile.tag.save()


def close_temp_folder():
    """
    closes temporary folder created by the above functions
    doesnt take any inputs
    
    :)
    """
    # check if folder exists for good practice like the good boy i am

    if os.path.isfile("./tempMusicStorage/"):
        for file in os.listdir("./tempMusicStorage/"):
            os.remove("./tempMusicStorage/" + file)

        os.rmdir("./tempMusicStorage/")

    return


if __name__ == "__main__":
    """
    call all functions to make this program an executable script as i intended it
    """

    music_files = get_music_files()
    reduce_file_size(music_files)
    files_with_metadata = query_acrcloud()
    update_files_from_metadata(files_with_metadata)
    close_temp_folder()