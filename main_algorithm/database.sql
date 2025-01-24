BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "songs" (
	"Song_ID"	TEXT NOT NULL UNIQUE,
	"Name"	TEXT NOT NULL,
	"Author"	TEXT NOT NULL,
	"Stored_Location"	TEXT,
	"License"	TEXT,
	"Original_location"	TEXT,
    "Genre" TEXT,
	PRIMARY KEY("Song_ID")
);
CREATE TABLE IF NOT EXISTS "points" (
	"Hash"	TEXT NOT NULL,
	"Song_ID"	TEXT NOT NULL,
	"Time_Offset"	NUMERIC NOT NULL,
	FOREIGN KEY("Song_ID") REFERENCES "songs"("Song_ID")
);
INSERT INTO "songs" VALUES ('1d14d8b0-f75b-47dd-b3fe-f18142c94712','Hungarian Dance number 5','Johannes Brahms / US Army Strings','songs/brahm.ogg','Public Domain','https://musopen.org/music/43805-hungarian-dance-no-5-in-f-sharp-minor-woo-1-string-orchestra-arr/');
COMMIT;

DELETE FROM "songs";
DELETE FROM "points";
