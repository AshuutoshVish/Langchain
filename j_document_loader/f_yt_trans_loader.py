from langchain_community.document_loaders import YoutubeLoader
loader = YoutubeLoader.from_youtube_url("", add_video_info=False)
loader.load()