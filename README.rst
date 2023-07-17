MeetingProcessor
================

**MeetingProcessor** is a powerful Python library designed to convert meeting audio (video from a YouTube URL or a local file) into a summarized PDF document in LaTeX format. This library leverages OpenAI's Whisper and GPT-4 models for audio transcription and text summarization, respectively.

This library is designed to be simple and efficient, enabling anyone to convert their meeting recordings into structured summaries. It's perfect for students, researchers, businesses, and anyone else who needs to extract the most valuable information from their meetings.

Key features of MeetingProcessor include:

1. Downloading videos from YouTube.
2. Converting video files into audio.
3. Transcribing audio using OpenAI's Whisper model.
4. Processing transcriptions and generating summaries with OpenAI's GPT-4 model.
5. Creating LaTeX documents from the summaries and converting them into PDF files.

Prerequisites
-------------

* A GPU is required to use the Whisper model for audio transcription.
* An OpenAI API key is necessary to use the GPT-4 model for text summarization.

|whisper| |openai| |python| |gpt4| |LaTeX|

.. |whisper| image:: https://img.shields.io/badge/Whisper%20-FF7A00.svg?&style=flat&logo=openai&logoColor=white
  :target: https://openai.com/research/whisper/
  :alt: Whisper

.. |openai| image:: https://img.shields.io/badge/OpenAI%20-3b6e99.svg?&style=flat&logo=openai&logoColor=white
  :target: https://openai.com/
  :alt: OpenAI

.. |python| image:: https://img.shields.io/badge/Python%20-%2314354C.svg?&style=flat&logo=python&logoColor=white
  :target: https://www.python.org/
  :alt: Python

.. |gpt4| image:: https://img.shields.io/badge/GPT--4%20-0f3366.svg?&style=flat&logo=openai&logoColor=white
  :target: https://openai.com/
  :alt: GPT-4

.. |LaTeX| image:: https://img.shields.io/badge/LaTeX%20-%23008080.svg?&style=flat&logo=latex&logoColor=white
  :target: https://www.latex-project.org/
  :alt: LaTeX

Installation
============

The MeetingProcessor library may be installed using pip...

.. code:: python

    !pip install MeetingProcessor

To use MeetingProcessor you can use:

.. code:: python

    from MeetingProcessor import Meet

    meeting = Meet('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    meeting.process()

Google Colaboratory Support
---------------------------

MeetingProcessor can also be used in Google Colab by following the steps below:

**Clone repository**

.. code:: python

    !git clone https://github.com/josorio398/MeetingProcessor_Library

**Installation of requirements**

.. code:: python

    %%capture
    %cd /content/MeetingProcessor_Library
    !pip install -r requirements.txt

**LaTeX Installation**

.. code:: python

    %%capture
    %cd /content/
    !apt install texlive-fonts-recommended texlive-fonts-extra cm-super dvipng

**Library Import**

.. code:: python

    import sys
    sys.path.append('/content/MeetingProcessor_Library')

    from MeetingProcessor import Meet

    meeting = Meet('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    meeting.process()

This process installs all the necessary dependencies, clones the repository into the Google Colab environment, installs LaTeX packages, and imports the MeetingProcessor library. It finally processes a meeting from a YouTube URL.


Usage
=====

The primary class in this library is `Meet`. To use it, initialize an instance of `Meet` with the URL of a YouTube video or the path to a local video file. Then, call the `process` method on the instance to start the transcription and summary process.