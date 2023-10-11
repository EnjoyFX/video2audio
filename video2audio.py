"""Module for converting video to audio"""
import logging
import os
import sys
from tkinter import Tk
from tkinter import filedialog as fd
from logging import StreamHandler
from moviepy import editor as me


__version__ = '1.0.2'
app_name = f'Py video->audio extractor (mp4->mp3) {__version__}'
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


class Converter:
    """Class for converting video to audio with different bitrate"""
    def __init__(self):
        self.root = Tk()

    def video_to_mp3(self, bitrate='320k'):
        """
        Method for converting video to audio
        :param bitrate: Audio bitrate, given as a string like '50k', '320k'...
        :return: None
        """
        self.root.withdraw()

        files = fd.askopenfilenames(filetypes=[('mp4 files', '*.mp4')])
        if not files:
            msg = f'{app_name}: No files selected'
            logger.info(msg)
            sys.exit()

        path = os.path.dirname(files[-1])
        ok, bad = 0, 0
        for file in files:
            name = os.path.basename(file)
            try:
                video = me.VideoFileClip(file)
            except KeyError as e:
                msg = f'Issue with opening video "{name}": {e}'
                logger.warning(msg)
                sys.exit(1)

            audio = video.audio
            if audio:
                codec = audio.reader.acodec
                rate = audio.fps
                channels = audio.nchannels
                msg = f'Details: {codec=}, {rate=} Hz, {channels=}'
                logger.info(msg)
            else:
                msg = f'Audio not found in "{name}"'
                logger.warning(msg)

            audio_name = os.path.join(path, name.replace('.mp4', '.mp3'))

            try:
                audio.write_audiofile(audio_name, bitrate=bitrate)
                ok += 1
            except AttributeError as e:
                bad += 1
                msg = f'Issue with converting file "{name}": {e}'
                logger.warning(msg)
            finally:
                video.close()

        total = ok + bad
        msg = f'Converted: {ok}({ok/total:.1%}), ' \
              f'not converted: {bad}({bad/total:.1%}). ' \
              f'Total files processed: {total}'
        logger.info(msg)


if __name__ == "__main__":
    c = Converter()
    c.video_to_mp3()
