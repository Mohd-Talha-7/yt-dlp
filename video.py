import yt_dlp

url=input("Enter the URL:")

ydl_opts={'output':'sampletestvideo.%(ext)s'}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download Completed")