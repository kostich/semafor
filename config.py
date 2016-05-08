import os

programdir = os.path.dirname(os.path.realpath(__file__))
# If we are frozen via cx_Freeze on Windows, we need to readjust the programdir var
if programdir[-11:] == 'library.zip':
    programdir = programdir[:-12]