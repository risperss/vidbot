import requests


# video_url = "https://video.twimg.com/ext_tw_video/1619774854533619714/pu/vid/0/0/480x676/RagzGzOz3uN0MdWl.mp4"

# response = requests.get(video_url)

# with open("temp.mp4", "wb") as file:
#     file.write(response.content)

urls = [
    "https://video.twimg.com/ext_tw_video/1619774854533619714/pu/vid/0/0/480x676/RagzGzOz3uN0MdWl.mp4",
    "https://video.twimg.com/ext_tw_video/1619774854533619714/pu/vid/0/2600/480x676/7zvqfszYfSypEpAV.m4s",
]

content = b""

for url in urls:
    r = requests.get(url)
    content += r.content

with open("temp.mp4", "wb") as file:
    file.write(content)
