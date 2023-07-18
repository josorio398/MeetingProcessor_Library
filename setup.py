import json
from os import path
from setuptools import setup, find_packages
from sys import version_info

VERSION = "1.0.0"
CURR_PATH = "{}{}".format(path.abspath(path.dirname(__file__)), '/')


def path_format(file_path=None, file_name=None, is_abspath=False,
                ignore_raises=False):
    path_formatted = "{}{}".format(file_path, file_name)
    if ignore_raises:
        return path_formatted
    if file_path is None or not path.exists(file_path):
        raise IOError("Path '{}' doesn't exists".format(file_path))
    if file_name is None or not path.exists(path_formatted):
        raise IOError(
            "File '{}{}' doesn't exists".format(file_path, file_name))
    if is_abspath:
        return path.abspath(path.join(file_path, file_name))
    else:
        return path.join(file_path, file_name)


def read_file(is_json=False, file_path=None, encoding='utf-8',
              is_encoding=True, ignore_raises=False):
    text = None
    try:
        if file_path is None:
            raise Exception("File path received it's None")
        if version_info.major >= 3:
            if not is_encoding:
                encoding = None
            with open(file_path, encoding=encoding) as buff:
                text = buff.read()
        if version_info.major <= 2:
            with open(file_path) as buff:
                if is_encoding:
                    text = buff.read().decode(encoding)
                else:
                    text = buff.read()
        if is_json:
            return json.loads(text)
    except Exception as err:
        if not ignore_raises:
            raise Exception(err)
    return text


def read(file_name=None, is_encoding=True, ignore_raises=False):
    if file_name is None:
        raise Exception("File name not provided")
    if ignore_raises:
        try:
            return read_file(
                is_encoding=is_encoding,
                file_path=path_format(
                    file_path=CURR_PATH,
                    file_name=file_name,
                    ignore_raises=ignore_raises))
        except Exception:
            return 'NOTFOUND'
    return read_file(is_encoding=is_encoding,
                     file_path=path_format(
                         file_path=CURR_PATH,
                         file_name=file_name,
                         ignore_raises=ignore_raises))


setup(
    name='MeetingProcessor',
    version=VERSION,
    license="MIT",
    packages=find_packages(),
    description='A Python Library for Processing Meetings Using GPT-4 and Whisper ASR',
    long_description=read("README.rst"),
    author='Jhonny Osorio Gallego',
    author_email='osoriojohnny1986@gmail.com',
    url='https://github.com/josorio398/MeetingProcessor_Library',
    download_url='https://github.com/josorio398/MeetingProcessor_Library',
    keywords=['meetings', 'processing', 'GPT-4', 'Whisper ASR', 'Python', 'openai'],
    install_requires=[
        'openai-whisper',
        'pytube',
        'pydub',
        'openai',
        'pdf2docx',
    ],
    setup_requires=[
        'openai-whisper',
        'pytube',
        'pydub',
        'openai',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-html',
        'pytest-dependency',
    ],
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

