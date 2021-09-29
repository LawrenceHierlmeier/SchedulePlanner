# SchedulePlanner

## Getting Started

Create a virtual environment:  
`python -m venv venv`

Activate the virtual environment:  
`.\venv\Scripts\Activate.ps1`

Update pip:  
`python -m pip install --upgrade pip`

Install required modules:  
`python -m pip install -r requirements.txt`

Update the requirements.txt after installing any new modules:  
`python -m pip freeze > requirements.txt`

Run the server:  
`python manage.py runserver`

After making any changes to models.py:  
`python manage.py makemigrations`  
`python manage.py migrate`

To import catalog data:  
`python scraper.py`
