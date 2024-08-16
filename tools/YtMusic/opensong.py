import YouTubeMusicAPI
import webbrowser

def PlaySong(SongName):
    result = YouTubeMusicAPI.search(SongName)
    if result:
        webbrowser.open(result['url'],new=2)
        return result['title']
    else:
        print("No Result Found")
        return f"song with title {SongName} not found!"
    
    