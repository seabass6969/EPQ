import database
import eyed3
import os
import tqdm
starting_path = os.path.join("songs/Kevin_MacLeod_Classical_sampler/", "")
print(starting_path)
files = os.listdir(starting_path)
files = [os.path.join(starting_path, file) for file in files if os.path.isfile(os.path.join(starting_path, file))]
files = files[:10]

original_location = "https://freemusicarchive.org/music/Kevin_MacLeod/Classical_Sampler"

eyed3.log.setLevel("ERROR")

for file in tqdm.tqdm(files):
    file_detail = eyed3.load(file)
    licenses = file_detail.tag.copyright
    artist = file_detail.tag.artist
    title = file_detail.tag.title
    genre = file_detail.tag.genre.name
    database.adding_entry(title, artist, file, licenses, original_location, genre)
