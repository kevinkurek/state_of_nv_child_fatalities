from ..scripts.child_fatality_scrape import *

def test_merge_dicts():
    # Given
    data = {'key1': 'value1', 'key2': ''}
    new_dict = {'key2': 'new_value2', 'key3': 'value3'}

    # When
    result = merge_dicts(data, new_dict)

    # Then
    expected = {'key1': 'value1', 'key2': 'new_value2'}
    assert result == expected