# state_of_nv_child_fatalities
`TLDR; All NV Child Fatality PDFs -> 1 CSV per county`.

This serves as a first-step of Nevada Child Fatality pdfs and moves into a consistent csv schema across counties in Nevada.

### Directory Structure
```
├── state_of_nv_child_fatalities
      ├───config                              # hardcoded urls, paths and values
      ├───output_files                        # output csv and pdfs
      ├───research                            # original exploration and debugging
      ├───scripts                             # actual python code
          ├─── child_fatality_scraper.py      # core file
      ├───tests                               # unit tests of python functions
      ├── main.py                             # file that runs python code in scripts folder
      ├── requirements.txt                    # package requirements
      └── tox.ini                             # Test runner for multi-environment Python testing
```

Example:  
Clark County (Las Vegas) original URL which housed all pdfs: https://dcfs.nv.gov/Programs/CWS/CPS/ChildFatalities/Clark/  
Example PDF:  https://dcfs.nv.gov/uploadedFiles/dcfsnvgov/content/Programs/CWS/CPS/ChildFatalities/Clark/2023/2023-01-17_ID_1469166.pdf  
![image](https://github.com/kevinkurek/state_of_nv_child_fatalities/assets/28911996/219f4f12-a82b-4f9f-9c4a-a79a4c83682e)

