import os
import pydub

# going to make this file a little monolithic, since i want this to be as user friendly as possible so i don't want to have
# the user cart around two scripts wherever they need the functionality


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
    
    Args:
        files (file list): list of music files to be reduced in size
    """
    os.makedirs("tempMusicStorage")

    for file in files:
        if f.endswith(".mp3"):
            audio = pydub.AudioSegment.from_mp3()


def query_acrcloud(reduced_music_files):
    """
    returns a list of tuples, of music files and their metadata as recognized by acrcloud

    Args:
        reduced_music_files (file list): list of music files below 1mb to be identified by acrcloud
    """

    return []