import subprocess
import sys


def cut_intro(f: str) -> str:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", f],
        capture_output=True,
        text=True
    )
    duration = float(res.stdout.strip())
    cut_duration = "00:03:00" if duration >= 360 else "00:02:00"
    output_file = f"{f.rsplit('.', 1)[0]}_no_intro.mp3"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", f,
        "-ss", cut_duration,
        "-c", "copy",
        output_file
    ])
    return output_file


if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        f = input("Enter the path to the audio file: ").strip()
    result = cut_intro(f)
    print(result)
