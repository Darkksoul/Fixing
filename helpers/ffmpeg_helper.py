import json  # Add this import for JSON operations

async def MergeSubNew(filePath: str, subPath: str, user_id, file_list):
    """
    This method is for Merging Video + Subtitle(s) Together.

    Parameters:
    - `filePath`: Path to Video file.
    - `subPath`: Path to subtitle file.
    - `user_id`: To get the parent directory.
    - `file_list`: List of all input files.

    returns: Merged Video File Path
    """
    LOGGER.info("Generating mux command")
    muxcmd = [
        "ffmpeg",
        "-hide_banner",
    ]
    videoData = ffmpeg.probe(filename=filePath)
    videoStreamsData = videoData.get("streams")
    subTrack = 0
    for i in range(len(videoStreamsData)):
        if videoStreamsData[i]["codec_type"] == "subtitle":
            subTrack += 1
    for i in file_list:
        muxcmd.extend(["-i", i])
    muxcmd.extend([
        "-map", "0:v:0",
        "-map", "0:a:?",
        "-map", "0:s:?",
    ])
    for j in range(1, len(file_list)):
        muxcmd.extend([
            "-map", f"{j}:s",
            f"-metadata:s:s:{subTrack}", f"title=Track {subTrack+1} - tg@Devilservers"
        ])
        subTrack += 1
    muxcmd.extend([
        "-c:v", "copy",
        "-c:a", "copy",
        "-c:s", "srt",
        f"./downloads/{str(user_id)}/[@Devilservers]_softmuxed_video.mkv"
    ])
    LOGGER.info("Sub muxing")
    subprocess.call(muxcmd)
    return f"downloads/{str(user_id)}/[@Devilservers]_softmuxed_video.mkv"


async def MergeAudio(videoPath: str, files_list: list, user_id):
    LOGGER.info("Generating Mux Command")
    muxcmd = [
        "ffmpeg",
        "-hide_banner",
    ]
    videoData = ffmpeg.probe(filename=videoPath)
    videoStreamsData = videoData.get("streams")
    audioTracks = 0
    for i in files_list:
        muxcmd.extend(["-i", i])
    muxcmd.extend([
        "-map", "0:v:0",
        "-map", "0:a:?",
    ])
    for i in range(len(videoStreamsData)):
        if videoStreamsData[i]["codec_type"] == "audio":
            muxcmd.extend([
                f"-disposition:a:{audioTracks}", "0"
            ])
            audioTracks += 1
    fAudio = audioTracks
    for j in range(1, len(files_list)):
        muxcmd.extend([
            "-map", f"{j}:a",
            f"-metadata:s:a:{audioTracks}", f"title=Track {audioTracks+1} - tg@Devilservers"
        ])
        audioTracks += 1
    muxcmd.extend([
        f"-disposition:s:a:{fAudio}", "default",
        "-map", "0:s:?",
        "-c:v", "copy",
        "-c:a", "copy",
        "-c:s", "copy",
        f"downloads/{str(user_id)}/[@Devilservers]_export.mkv"
    ])

    LOGGER.info(muxcmd)
    process = subprocess.call(muxcmd)
    LOGGER.info(process)
    return f"downloads/{str(user_id)}/[@Devilservers]_export.mkv"


async def extractAudios(path_to_file, user_id):
    """
    Extract audio streams and metadata from the input file.

    Parameters:
    - `path_to_file`: Path to the input video file.
    - `user_id`: User ID to get the parent directory.

    Returns: Path to the directory containing extracted audio files.
    """
    dir_name = os.path.dirname(os.path.dirname(path_to_file))
    if not os.path.exists(path_to_file):
        return None
    if not os.path.exists(dir_name + "/extract"):
        os.makedirs(dir_name + "/extract")
    videoStreamsData = ffmpeg.probe(path_to_file)
    extract_dir = dir_name + "/extract"
    audios = []
    for stream in videoStreamsData.get("streams"):
        try:
            if stream["codec_type"] == "audio":
                audios.append(stream)
        except Exception as e:
            LOGGER.warning(e)
    for audio in audios:
        extractcmd = [
            "ffmpeg",
            "-hide_banner",
            "-i",
            path_to_file,
            "-map",
        ]
        try:
            index = audio["index"]
            extractcmd.extend([f"0:{index}"])
            try:
                output_file = f"({audio['tags']['language']}) {audio['tags']['title']}.{audio['codec_type']}.mka"
                output_file = output_file.replace(" ", ".")
            except:
                output_file = f"{audio['index']}.{audio['codec_type']}.mka"
            extractcmd.extend([
                "-c", "copy",
                f"{extract_dir}/{output_file}"
            ])
            LOGGER.info(extractcmd)
            subprocess.call(extractcmd)
        except Exception as e:
            LOGGER.error(f"Something went wrong: {e}")
    if get_path_size(extract_dir) > 0:
        return extract_dir
    else:
        LOGGER.warning(f"{extract_dir} is empty")
        return None


async def extractSubtitles(path_to_file, user_id):
    """
    Extract subtitle streams and metadata from the input file.

    Parameters:
    - `path_to_file`: Path to the input video file.
    - `user_id`: User ID to get the parent directory.

    Returns: Path to the directory containing extracted subtitle files.
    """
    dir_name = os.path.dirname(os.path.dirname(path_to_file))
    if not os.path.exists(path_to_file):
        return None
    if not os.path.exists(dir_name + "/extract"):
        os.makedirs(dir_name + "/extract")
    videoStreamsData = ffmpeg.probe(path_to_file)
    extract_dir = dir_name + "/extract"
    subtitles = []
    for stream in videoStreamsData.get("streams"):
        try:
            if stream["codec_type"] == "subtitle":
                subtitles.append(stream)
        except Exception as e:
            LOGGER.warning(e)
    for subtitle in subtitles:
        extractcmd = [
            "ffmpeg",
            "-hide_banner",
            "-i",
            path_to_file,
            "-map",
        ]
        try:
            index = subtitle["index"]
            extractcmd.extend([f"0:{index}"])
            try:
                output_file = f"({subtitle['tags']['language']}) {subtitle['tags']['title']}.{subtitle['codec_type']}.mka"
                output_file = output_file.replace(" ", ".")
            except:
                try:
                    output_file = f"{subtitle['index']}.{subtitle['tags']['language']}.{subtitle['codec_type']}.mka"
                except:
                    output_file = f"{subtitle['index']}.{subtitle['codec_type']}.mka"
            extractcmd.extend([
                "-c", "copy",
                f"{extract_dir}/{output_file}"
            ])
            LOGGER.info(extractcmd)
            subprocess.call(extractcmd)
        except Exception as e:
            LOGGER.error(f"Something went wrong: {e}")
    if get_path_size(extract_dir) > 0:
        return extract_dir
    else:
        LOGGER.warning(f"{extract_dir} is empty")
        return None
