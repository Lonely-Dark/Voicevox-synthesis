#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.11


import asyncio
import logging

import simpleaudio as sa
import speech_recognition as sr
from helperclass_pack import Helper
from translatepy import Translator
from voicevox import Client


async def main(voice_id: int = 1):
    r = sr.Recognizer()
    tr = Translator()
    log = Helper()
    log.logger.setLevel(logging.DEBUG)

    log.logger.info("Starting...")
    with sr.Microphone() as source:
        while True:
            log.logger.info("Listening...")
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
            except sr.UnknownValueError:
                log.logger.critical('Google Speech Recognition could not understand audio')
                continue
            log.logger.debug("You said: {}".format(text))
            translated = tr.translate(text, 'Japanese')
            log.logger.debug("Translated: {}".format(translated))

            async with Client() as client:
                audio_query = await client.create_audio_query(translated, speaker=voice_id)
                with open('voice.wav', 'wb') as f:
                    f.write(await audio_query.synthesis())

            sa.WaveObject.from_wave_file('voice.wav').play()


if __name__ == '__main__':
    asyncio.run(main())
