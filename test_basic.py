# import sys, os
# sys.path.insert(0, os.path.dirname(__file__))

from  basic_info import *
file_location = 'samples/gatheringstorm_ch1.txt'
(text, sentences) = massage_raw(get_raw(file_location))
res = flesch_kincaid(text,sentences)

def test_massage_raw_text_exists():
    assert text != None

def test_massage_raw_sent_exists():
    assert sentences != None

def test_massage_raw_text_length():
    assert len(text) == 3740

def test_massage_raw_sent_length():
    assert len(sentences) == 618

def test_words():
    assert res['words'] == 3712

def test_grade_level():
    assert round(res['grade_level'], 2) == 5.37

def test_reading_ease():
    assert round(res['reading_ease'], 2) == 67.25

