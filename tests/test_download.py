import os
import pytest
from unittest.mock import MagicMock, patch
import requests

from ..scripts.child_fatality_scrape import (
    download_all_pdfs,
    list_files,
    restructure_alphabetical_dict,
    merge_dicts,
)


@pytest.fixture
def mock_html_page():
    # Mock HTML page containing a few anchor tags.
    return """
    <html>
    <body>
        <a href="/uploadedFiles/dcfsnvgov/content/Programs/CWS/CPS/ChildFatalities/Clark/document1.pdf">Document 1</a>
        <a href="/uploadedFiles/dcfsnvgov/content/Programs/CWS/CPS/ChildFatalities/Clark/document2.pdf">Document 2</a>
    </body>
    </html>
    """


@pytest.fixture
def mock_pdf_content():
    # Mock binary PDF content
    return b"%PDF-1.7 mock pdf content"


def test_download_all_pdfs(mock_html_page, mock_pdf_content):
    url = "https://dcfs.nv.gov/Programs/CWS/CPS/ChildFatalities/Clark/"

    # Mock the network requests
    with patch.object(requests, "get") as mock_get:
        mock_get.return_value.text = mock_html_page
        mock_get.return_value.content = mock_pdf_content

        # Mock the filesystem operations
        with patch.object(os.path, "exists") as mock_exists, patch(
            "builtins.open", new_callable=MagicMock
        ):
            mock_exists.return_value = True  # simulate directory already exists
            output_directory = download_all_pdfs(url)
            print(output_directory)

            # Check the filesystem was used correctly
            assert mock_exists.call_count == 2  # Check exists was called for each file
            assert os.path.basename(output_directory) == "Clark_pdfs"

            # Check the network requests were called correctly
            assert mock_get.call_count == 3  # One for the HTML page, two for the PDFs
            print(mock_get.call_args_list)
            assert (
                mock_get.call_args_list[0][0][0] == url
            )  # First request is for the HTML page
            assert (
                mock_get.call_args_list[1][0][0]
                == "https://dcfs.nv.gov//uploadedFiles/dcfsnvgov/content/Programs/CWS/CPS/ChildFatalities/Clark/document1.pdf"
            )  # Second request is for the first PDF
            assert (
                mock_get.call_args_list[2][0][0]
                == "https://dcfs.nv.gov//uploadedFiles/dcfsnvgov/content/Programs/CWS/CPS/ChildFatalities/Clark/document2.pdf"
            )  # Third request is for the second PDF


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
