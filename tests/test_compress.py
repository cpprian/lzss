from lzss.compress import extract_repeat, find_duplicate

def test_extract_repeat():
    assert extract_repeat(b'abc', 6) == b'abcabc'
    assert extract_repeat(b'12345', 10) == b'1234512345'
    assert extract_repeat(b'xyz', 4) == b'xyzx'

def test_find_duplicate_simple():
    data = b'abcabcabc'
    assert find_duplicate(data, 3) == (3, 6)

def test_find_duplicate_complex():
    data = b'abcdefabcdefghijk'
    assert find_duplicate(data, 6) == (6, 6)
    assert find_duplicate(data, 12) is None

def test_find_duplicate_longer_match():
    data = b'abcabcabcdef'
    assert find_duplicate(data, 3) == (3, 6)

def test_find_duplicate_no_match():
    data = b'abcdefghijk'
    assert find_duplicate(data, 3) is None