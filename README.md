# state_of_nv_child_fatalities
`TLDR; All NV Child Fatality PDFs -> 1 CSV per county`.

This serves as a first-step of Nevada Child Fatality pdfs and moves into a consistent csv schema across counties in Nevada.

### Env setup (recommended but not required)
```
$ conda create --name child_nv python=3.10      # create python3.10 virtual env
$ conda activate child_nv                       # turn on virtual env
$ pip install tox                               # install tox
$ tox                                           # run tox: installs requirements.txt & runs pytests
```
### Local Run
1. `CONFIG.py - can change values like SCRAPE_YEARS to additional years`
2. `$ python main.py  # run primary pdf scraper per county (don't need virtual env to run this)`
### Directory Structure
```
├── state_of_nv_child_fatalities
      ├───config                              # hardcoded urls, paths and values
          ├─── CONFIG.py                      # Change values in here
      ├───output_files                        # output csv and pdfs
      ├───research                            # original exploration and debugging
      ├───scripts                             # actual python code
          ├─── child_fatality_scraper.py      # core file
          ├─── prior_history.py               # gets number of past calls on child
      ├───tests                               # unit tests of python functions
      ├── requirements.txt                    # package requirements
      ├── tox.ini                             # Multi-environment Python testing
      └── Dockerfile                          # Docker build image, run tox, execute main.py
```

**Example:**  
[Clark County (Las Vegas) original URL for all pdfs](https://dcfs.nv.gov/Programs/CWS/CPS/ChildFatalities/Clark/)  

**Example Single PDF:**  [Near fatality marijuana access](https://dcfs.nv.gov/uploadedFiles/dcfsnvgov/content/Programs/CWS/CPS/ChildFatalities/Clark/2023/2023-01-17_ID_1469166.pdf)  
![image](https://github.com/kevinkurek/state_of_nv_child_fatalities/assets/28911996/219f4f12-a82b-4f9f-9c4a-a79a4c83682e)  

**Output Table for Clark.**     
`output_files/child_fatality_Clark.csv`

![image](https://github.com/kevinkurek/state_of_nv_child_fatalities/assets/28911996/9360689d-e655-43f3-98ce-4a8891274e6c)


### Still in DEV below this line for GCP/AWS workflow.

### Docker Instructions

```
Docker Run:
$ docker build -t child_fatalities .                                      # build docker image
$ docker run -d --name child_fatalities_container child_fatalities        # run container & actual python
$ docker ps                                                               # confirm you see container running
$ docker exec -it child_fatalities_container /bin/bash                    # look inside container
    $ cd output_files && ls                                               # view output csv files after container finishes
$ docker logs child_fatalities_container                                  # look at internal print statements/logs
```

### Docker Reset
WARNING: Only do this to start from scratch, it will delete **ALL** images & containers.
```
Stop & delete containers:
$ docker stop $(docker ps -aq)
$ docker rm $(docker ps -aq)

Remove all images:
$ docker rmi $(docker images -aq)

Remove any dangling/unused images:
$ docker system prune -a -f
```

### Upload to Google Cloud Platform (GCP)
Note: Google's Container Registry is being deprecated so now images will now live in Artifact Registry.
```
1. Create a .env file at the project root
2. Create & set 3 env variables inside .env: GCP_PROJECT_ID, GCP_SERVICE_ACCOUNT_KEY_PATH, TAG (example: TAG="v1.0")
      2a. You will need privileges from admin to access these.
3. Run bash script
$ ./build_and_push.sh

    Note: If you get a permission error run: 
    $ chmod +x build_and_push.sh
    $ ./build_and_push.sh

4. Answer "yes" to any potential prompts
5. Check the image uploaded successfully: GCP -> Artifact Registry -> Repositories -> gcr.io.
```

### Run inside GCP (roughly)

1. Containerize the application as in the "Upload to Google Cloud Platform" section above.
2. Configure a Cloud Run Service inside GCP
3. Deploy Cloud Run Service.
4. Create Cloud Function and select "Cloud Run" trigger; select your Cloud Run Service.
5. Set a scheduler job.
