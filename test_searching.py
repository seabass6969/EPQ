import pytest
import settings as settings
import database
import searching
def test_untouched():
    matched = database.search_points(searching.searching("songs/brahm.ogg"))
    print(database.get_entry(list(matched.keys())[0]))
    print(matched)
    assert matched != {}

def test_simple_sine_wave():
    matched = database.search_points(searching.searching("test/simple_sugar.wav"))
    for key in list(matched.keys()):
        database.get_entry(key)
        print(matched[key])
    print(matched)
    assert matched != {}


def test_untouch_shifted():
    matched = database.search_points(searching.searching("test/shifted_sugar.wav"))
    for key in list(matched.keys()):
        database.get_entry(key)
        print(matched[key])
    print(matched)
    assert matched != {}
