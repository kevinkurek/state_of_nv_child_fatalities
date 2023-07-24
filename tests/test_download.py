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
