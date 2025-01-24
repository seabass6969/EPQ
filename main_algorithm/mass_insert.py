import database
import eyed3
import os
import tqdm
starting_path = os.path.join("songs/Kevin_MacLeod_Classical_sampler/", "")
print(starting_path)
files = os.listdir(starting_path)
files = [file for file in files if os.path.isfile(os.path.join(starting_path, file))]
print(files)
files = files

original_location = "https://freemusicarchive.org/music/Kevin_MacLeod/Classical_Sampler"

eyed3.log.setLevel("ERROR")

for file in tqdm.tqdm(files):
    actual_file_location = os.path.join(starting_path, file)
    file_detail = eyed3.load(actual_file_location)
    licenses = file_detail.tag.copyright
    artist = file_detail.tag.artist
    title = file_detail.tag.title
    genre = file_detail.tag.genre.name
    database.adding_entry(song_name=title, song_author=artist, song_file=file, song_start_directory=starting_path, License=licenses,song_url=original_location,genre=genre)
    # song_name, song_author, song_file, song_start_directory, License, song_url, genre
