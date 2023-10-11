import logging
from tkinter import Tk
from tkinter import filedialog as fd
from moviepy import editor as me
import os
import sys
from logging import StreamHandler


__version__ = '1.0.2'
app_name = f'Py video->audio extractor (mp4->mp3) {__version__}'
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


class Converter:
    def __init__(self):
        self.root = Tk()

    def video_to_mp3(self, bitrate='320k'):
        self.root.withdraw()

        files = fd.askopenfilenames(filetypes=[('mp4 files', '*.mp4')])
        if not files:
            logger.info(f'{app_name}: No files selected')
            sys.exit()

        path = os.path.dirname(files[-1])
        ok, bad = 0, 0
        for file in files:
            name = os.path.basename(file)
            try:
                video = me.VideoFileClip(file)
            except Exception as e:
                logger.warning(f'Issue with opening video "{name}": {e}')
                sys.exit(1)

            audio = video.audio
            if audio:
                codec = audio.reader.acodec
                rate = audio.fps
                channels = audio.nchannels
                logger.info(f'Audio details: codec {codec}, {rate} Hz, '
                            f'{channels} channel(s)')
            else:
                logger.warning(f'Audio not found in "{name}"')

            audioname = os.path.join(path, name.replace('.mp4', '.mp3'))

            try:
                audio.write_audiofile(audioname, bitrate=bitrate)
                ok += 1
            except Exception as e:
                bad += 1
                logger.warning(f'Issue with coonverting file "{name}": {e}')
            finally:
                video.close()

        msg = f'Converted: {ok}, not converted: {bad}. ' \
              f'Total files processed: {ok+bad}'
        logger.info(msg)


if __name__ == "__main__":
    c = Converter()
    c.video_to_mp3()
