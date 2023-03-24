#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.11


import asyncio
import logging

import simpleaudio as sa
import speech_recognition as sr
from aiofile import async_open
from helperclass_pack import Helper
from translatepy import Translator
from translatepy.models import TranslationResult
from voicevox import Client


class Recogniser:
    def __init__(self) -> None:
        self.r = sr.Recognizer()
        self.tr = Translator()
        self.log = Helper().logger
        self.log.setLevel(logging.DEBUG)

        self.log.info("Initializing recogniser...")

    async def listenMicro(self) -> sr.AudioData:
        with sr.Microphone() as source:
            self.log.info("Listening...")
            audio = self.r.listen(source)
        return audio

    async def recognise(self, audio: sr.AudioData) -> str:
        try:
            text = self.r.recognize_google(audio, language='ru-RU')
            self.log.debug(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            self.log.error('Google Speech Recognition could not understand audio')

    async def translate(self, text: str) -> TranslationResult:
        translated = self.tr.translate(text, 'Japanese')
        self.log.debug(f"Translated text: {translated}")
        return translated

    async def synthesize(self, text: TranslationResult, voice_id: int = 1, filename: str = 'voice.wav') -> None:
        async with Client() as client:
            audio_query = await client.create_audio_query(text, speaker=voice_id)
            async with async_open(filename, 'wb') as f:
                await f.write(await audio_query.synthesis())
            self.log.info(f"Synthesized {filename}")

    async def play(self, filename: str) -> None:
        self.log.debug(f"Playing {filename}")
        sa.WaveObject.from_wave_file(filename).play()


async def main() -> None:
    recogniser: Recogniser = Recogniser()
    audio: sr.AudioData = await recogniser.listenMicro()
    text: str = await recogniser.recognise(audio)
    translated: TranslationResult = await recogniser.translate(text)
    await recogniser.synthesize(translated, voice_id=1)
    await recogniser.play('voice.wav')


if __name__ == '__main__':
    asyncio.run(main())
