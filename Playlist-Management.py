# Node class for each song in a playlist
class SongNode: 
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None

# Doubly linked list for a playlist's songs
class Playlist:
    def __init__(self, name):
        self.name = name  
        self.head = None
        self.tail = None

    def add_song(self, song):
        new_node = SongNode(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node 
        else: 
            self.tail.next = new_node
            new_node.prev = self.tail 
            self.tail = new_node 

    def traverse_songs(self):
        current = self.head
        print(f"Playlist '{self.name}':")
        while current:
            print(current.song, end=" <-> ")
            current = current.next
        print("None")

    def delete_song(self, song):
        current = self.head
        while current is not None:
            if current.song == song:
                if current == self.head:
                    self.head = current.next
                    if self.head is not None:
                        self.head.prev = None
                    else:
                        self.tail = None
                elif current == self.tail:
                    self.tail = current.prev
                    if self.tail is not None:
                        self.tail.next = None
                    else:
                        self.head = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev

                del current
                print(f"Song '{song}' deleted from playlist '{self.name}'")
                return
            current = current.next
        print(f"Song '{song}' not found in playlist '{self.name}'")
    
    def search_song(self, song_name):
        current = self.head
        while current:
            if current.song == song_name:
                print(f"Song '{song_name}' found in playlist '{self.name}'.")
                return current
            current = current.next
        print(f"Song '{song_name}' not found in playlist '{self.name}'.")
        return None

# Node class for each playlist in the collection
class PlaylistNode:
    def __init__(self, playlist):
        self.playlist = playlist 
        self.next = None  

# Linked list for the collection of playlists
class PlaylistCollection:
    def __init__(self):
        self.head = None

    def add_playlist(self, playlist_name):
        new_playlist = Playlist(playlist_name)
        new_node = PlaylistNode(new_playlist)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        print(f"Playlist '{playlist_name}' added to the collection.")

    def display_playlists(self):
        if not self.head:
            print("No playlists available.")
            return
        current = self.head
        print("Available Playlists:")
        while current:
            print(f"- {current.playlist.name}")
            current = current.next

    def find_playlist(self, playlist_name):
        current = self.head
        while current:
            if current.playlist.name == playlist_name:
                return current.playlist
            current = current.next
        print(f"Playlist '{playlist_name}' not found.")
        return None

class SongCollection:
    def __init__(self):
        self.head = None

    def add_song(self, song_name):
        new_song = SongNode(song_name)  
        if not self.head:
            self.head = new_song
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_song
        print(f"Song '{song_name}' added to the collection.")

    def display_songs(self):
        if not self.head:
            print("No songs available.")
            return
        current = self.head
        print("Available Songs:")
        while current:
            print(f"- {current.song}")
            current = current.next

    def search_song(self, song_name):
        current = self.head
        while current:
            if current.song == song_name:
                print(f"Song '{song_name}' found.")
                return current
            current = current.next
        print(f"Song '{song_name}' not found.")
        return None

# Song Menu--------------------->    
def song_menu(playlist):
    while True:
        print("------------------\nSong Menu")
        print("1. Create Song")
        print("2. Update Song")
        print("3. Delete Song")
        print("4. Search Song")
        print("5. Exit")
        print("------------------")

        choice = int(input("\nSelect Option: "))

        if choice == 1:
            song_create = input("Enter new song name: ")
            playlist.add_song(song_create)
        elif choice == 2:
            song_update = input("Enter song to update (delete and re-add): ")
            playlist.delete_song(song_update)
            new_song = input("Enter updated song name: ")
            playlist.add_song(new_song)
        elif choice == 3:
            song_delete = input("Enter song to delete: ")
            playlist.delete_song(song_delete)
        elif choice == 4:
            song_search = input("Enter song to search: ")
            playlist.search_song(song_search)  # Call the search_song method
        elif choice == 5:
            break
        else:
            print("Invalid option. Please try again.")

# Playlist Menu--------------------->    
def playlist_menu(collection):
    while True:
        print("------------------\nPlaylist Menu")
        print("1. Create Playlist")
        print("2. Search Playlist")
        print("3. Edit Playlist")
        print("4. Delete Playlist")
        print("5. Exit")
        print("------------------")

        choice = int(input("\nSelect Option: "))

        if choice == 1:
            playlist_name = input("Enter new playlist name: ")
            collection.add_playlist(playlist_name)
        elif choice == 2:
            playlist_name = input("Enter playlist name to search: ")
            playlist = collection.find_playlist(playlist_name)
            if playlist:
                playlist.traverse_songs()
        elif choice == 3:
            playlist_name = input("Enter playlist name to edit: ")
            playlist = collection.find_playlist(playlist_name)
            if playlist:
                edit_playlist_menu(playlist)
        elif choice == 4:
            playlist_delete = input("Enter playlist name to delete: ")
            
        elif choice == 5:
            break
        else:
            print("Invalid option. Please try again.")

# Edit Playlist Menu--------------------->      
def edit_playlist_menu(playlist):
    while True:
        print("------------------\nDisplay Playlist by:")
        print("1. Add Song")
        print("2. Delete Song")
        print("3. Exit")
        print("------------------")

        choice = int(input("\nSelect Option: "))

        if choice == 1:
            song_name = input("Song Name: ")
            playlist.add_song(song_name)
        elif choice == 2:
            song_name = input("Song Name to delete: ")
            playlist.delete_song(song_name)
        elif choice == 3:
            break
        else:
            print("Invalid option. Please try again.")
from flask import Flask, request, jsonify

app = Flask(__name__)

# Placeholder collections for songs and playlists
playlists = {}
songs = {}


# Song Endpoints:
@app.route('/song', methods=['POST'])
def create_song():
    song = request.json
    songs[song['name']] = song  # Add song
    return jsonify({"message": "Song created successfully", "song": song}), 201


@app.route('/song/<string:song_name>', methods=['PUT'])
def update_song(song_name):
    if song_name in songs:
        updated_song = request.json
        songs[song_name] = updated_song
        return jsonify({"message": "Song updated successfully", "song": updated_song}), 200
    return jsonify({"message": "Song not found"}), 404


@app.route('/song/<string:song_name>', methods=['DELETE'])
def delete_song(song_name):
    if song_name in songs:
        del songs[song_name]
        return jsonify({"message": "Song deleted successfully"}), 200
    return jsonify({"message": "Song not found"}), 404


@app.route('/song/<string:song_name>', methods=['GET'])
def get_song(song_name):
    song = songs.get(song_name)
    if song:
        return jsonify(song), 200
    return jsonify({"message": "Song not found"}), 404


# Playlist Endpoints:
@app.route('/playlist', methods=['POST'])
def create_playlist():
    playlist = request.json
    playlist['songs'] = []
    playlists[playlist['name']] = playlist
    return jsonify({"message": "Playlist created successfully", "playlist": playlist}), 201


@app.route('/playlist/<string:playlist_name>', methods=['GET'])
def get_playlist(playlist_name):
    playlist = playlists.get(playlist_name)
    if playlist:
        return jsonify(playlist), 200
    return jsonify({"message": "Playlist not found"}), 404


@app.route('/playlist/<string:playlist_name>', methods=['PUT'])
def update_playlist(playlist_name):
    playlist = playlists.get(playlist_name)
    if playlist:
        updated_playlist = request.json
        playlists[playlist_name] = updated_playlist
        return jsonify({"message": "Playlist updated successfully", "playlist": updated_playlist}), 200
    return jsonify({"message": "Playlist not found"}), 404


@app.route('/playlist/<string:playlist_name>', methods=['DELETE'])
def delete_playlist(playlist_name):
    if playlist_name in playlists:
        del playlists[playlist_name]
        return jsonify({"message": "Playlist deleted successfully"}), 200
    return jsonify({"message": "Playlist not found"}), 404


# Additional Endpoints:
@app.route('/playlist/<string:playlist_name>/add_song', methods=['POST'])
def add_song_to_playlist(playlist_name):
    song_name = request.json.get('song_name')
    playlist = playlists.get(playlist_name)
    if playlist:
        song = songs.get(song_name)
        if song:
            playlist['songs'].append(song_name)
            return jsonify({"message": f"Song '{song_name}' added to playlist '{playlist_name}'"}), 200
        return jsonify({"message": "Song not found"}), 404
    return jsonify({"message": "Playlist not found"}), 404


@app.route('/playlist/<string:playlist_name>/remove_song', methods=['POST'])
def remove_song_from_playlist(playlist_name):
    song_name = request.json.get('song_name')
    playlist = playlists.get(playlist_name)
    if playlist:
        if song_name in playlist['songs']:
            playlist['songs'].remove(song_name)
            return jsonify({"message": f"Song '{song_name}' removed from playlist '{playlist_name}'"}), 200
        return jsonify({"message": "Song not found in playlist"}), 404
    return jsonify({"message": "Playlist not found"}), 404


@app.route('/playlist/<string:playlist_name>/sort_songs', methods=['POST'])
def sort_songs_in_playlist(playlist_name):
    playlist = playlists.get(playlist_name)
    if playlist:
        sort_by = request.json.get('sort_by', 'name')
        playlist['songs'].sort(key=lambda song_name: songs[song_name][sort_by])
        return jsonify({"message": f"Songs in playlist '{playlist_name}' sorted by {sort_by}"}), 200
    return jsonify({"message": "Playlist not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
