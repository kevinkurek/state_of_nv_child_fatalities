import os
import pytest
from unittest.mock import MagicMock, patch
import requests
from ..scripts.child_fatality_scrape import (
    list_files,
    restructure_alphabetical_dict,
    merge_dicts,
)


def test_list_files(tmp_path):
    # tmp_path is a pytest fixture that provides a temporary directory unique to this test invocation
    dummy_files = ["file1.txt", "file2.txt"]
    for file_name in dummy_files:
        # Create dummy files in the temporary directory
        (tmp_path / file_name).touch()

    assert set(list_files(tmp_path)) == set(
        dummy_files
    )  # Test that the list_files function correctly lists out the files


def test_restructure_alphabetical_dict():
    input_dict = {
        "A": "Date of the notification to the child welfare agency of the fatality/near fatality of a child:\n4/13/2023\n",
        "B": "Location of child at the time of death or near fatality (city/county):\nLas Vegas, Clark\n",
    }
    expected_output_dict = {
        "Date of the notification to the child welfare agency of the fatality/near fatality of a child": "4/13/2023",
        "Location of child at the time of death or near fatality (city/county)": "Las Vegas, Clark",
    }

    assert restructure_alphabetical_dict(input_dict) == expected_output_dict


def test_merge_dicts():
    # Given
    data = {"key1": "value1", "key2": ""}
    new_dict = {"key2": "new_value2", "key3": "value3"}

    # When
    result = merge_dicts(data, new_dict)

    # Then
    expected = {"key1": "value1", "key2": "new_value2"}
    assert result == expected
