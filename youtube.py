import yt_dlp

class YouTubeModule:
    def download_info(self, url):
        """Obtiene info de video YouTube."""
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'No title')