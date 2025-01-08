import settings
import sqlite3
import spectrogram_analysis
import uuid


def connection():
    return sqlite3.connect("database.sqlite")


def write_points(items):
    conn = connection()
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO "points" VALUES (?, ?, ?)', items)
    conn.commit()
    conn.close()

def search_points(searchPairs):
    """
        :params searchPairs pairs from the searchPairs function with all the (deltas, hashes)
    """
    conn = connection()
    time = {}
    for pairs in searchPairs:
        result = conn.execute(
            f'SELECT Song_ID, Time_Offset FROM points WHERE Hash="{pairs[1]}";'
        ).fetchall()
        for r in result:
            if r[0] not in time:
                time[r[0]] = []
            time[r[0]].append(r[1])

    return time


def new_song_entry(song_name, song_author, song_file, License, song_url, genre):
    uuid_song = str(uuid.uuid4())
    sqlstr = f"""
        INSERT INTO "songs" VALUES 
        (
            '{uuid_song}',
            '{song_name}',
            '{song_author}',
            '{song_file}',
            '{License}',
            '{song_url}',
            "{genre}"
        );
    """

    conn = connection()
    cursor = conn.cursor()
    cursor.execute(sqlstr)

    conn.commit()
    conn.close()
    return uuid_song


def adding_entry(song_name, song_author, song_file, License, song_url, genre):
    uuids = new_song_entry(song_name, song_author, song_file, License, song_url, genre)
    pairs = list(spectrogram_analysis.getPairs(song_file, uuids))
    # unique = []
    # for pair in pairs:
    #     if pair not in unique:
    #         unique.append(pair)
    # print(len(unique))
    write_points(pairs)
    if settings.DEBUG:
        print("I wrote {} points".format(len(pairs)))


def get_entry(ID):
    conn = connection()
    item = conn.execute(f'SELECT * FROM songs WHERE Song_ID="{ID}";').fetchone()
    return item


if __name__ == "__main__":
    pass
