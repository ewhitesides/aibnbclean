# aibnbclean

the following is some basic code that helps automate cleaning scheduling and communication for short-term rental properties such as Airbnb listings

- it pulls booking data from airbnb calendars or google calendars
- it uses google spreadsheets to track cleaning schedules and records
- it uses playwright for web scraping and google gemini api to parse user messages for cleaning info
- it sends text message reminders about upcoming cleaning dates via twilio
- it sends cleaner payment tasks to todoist

## Developer setup local machine windows

### initial setup

```pwsh
# install python
winget install python

# install uv package manager
pip install uv

# clone this repo
git clone <repo url>

# cd to the code repo folder
cd <code repo folder>

# create a virtual environment and install dependencies from pyproject.toml
uv sync
```

### .env file

create an .env file at the base of the code repo folder with the following content:

```env
AIBNBCLEAN_CONFIG_DIR="C:/path/to/config/dir"
AIBNBCLEAN_HEADLESS="1"
AIBNBCLEAN_GEMINI_MODEL="gemini-flash-latest"
```

### listings.json

create listings.json in the config directory specified in the .env file

```json
[
    {
        "name": "403M St NW Lower",
        "type": "airbnb",
        "laundry": "yes",
        "url": "https://www.airbnb.com/calendar/ical/xxxxxxxx.ics?s=yyyyyyy",
        "spreadsheet_id": "google_spreadsheet_id",
        "spreadsheet_sheet_name": "Sheet1",
        "spreadsheet_sheet_id": 0,
        "spreadsheet_bitly_url": "bitly_url_to_spreadsheet",
        "default_cleaning_fee": 140,
        "qty_to_process": 10,
        "guests": {
            "min": 1,
            "max": 4
        },
        "beds": {
            "min": 1,
            "max": 2
        },
        "pnp_beds": {
            "min": 0,
            "max": 1
        },
        "days_addrm_notice": 14,
        "todoist_project_name": "airbnb"
    }
]
```

### secrets.json

create listings.json in the config directory specified in the .env file

```json
{
    "gemini_api_key": "api_key",
    "todoist_api_key": "api_key",
    "twilio": {
        "client": "clientid:clientsecret",
        "from_number": "+18005551212",
        "to_number": "+18005562323"
    },
    "google_sa": {
        "type": "service_account",
        "project_id": "google-cloud-project-id",
        "private_key_id": "private_key_id",
        "private_key": "private_key_contents",
        "client_email": "client@project.iam.gserviceaccount.com",
        "client_id": "clientid",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/client%40project.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
}
```

## Production setup on raspberry pi with gui interface

sudo adduser airbnb

sudo usermod -aG adm,dialout,cdrom,sudo,audio,video,render,plugdev,games,users,input,netdev,spi,i2c,gpio,lpadmin airbnb

### config

define config directory, listings.json, secrets.json, .env file similar to developer setup above

### initial install

```bash
# install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# cd to config directory
cd ~/aibnbclean

# create and activate the venv
uv venv
source .venv/bin/activate

# install aibnbclean package into the venv
uv pip install --refresh aibnbclean

# install playwright
playwright install --with-deps

# execute the login function once to create browser_profile with access to airbnb
python -c "import aibnbclean; aibnbclean.login()"

# once logged in you should be able to do a test run
python -c "import aibnbclean; aibnbclean.process()"
```

## run daily using cron

the following example runs at 1:30pm daily

```cron
30 13 * * * date > /tmp/aibnbclean.log
30 13 * * * cd $HOME/aibnbclean; source .venv/bin/activate; python -c "import aibnbclean; aibnbclean.process()" >> /tmp/aibnbclean.log 2>&1
```
