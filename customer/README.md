# tabernacle_customer_success

1) Create a virtual enviroment using "python -m venv <environment_name>"
2) Specify the name of the environment file to the gitignore.
3) Activate virtual environment
4) In terminal, run "pip install -r requirements.txt" to install all packages mentioned in requirements.txt.
5) Install postgres and use that instead of sqlite. run "pip freeze > requirements.txt" to update your requirements.txt file with the newly installed packages.
6) Using terminal or using PGAdmin interface create a postgres database there named "tabernacle_internship" with user "tbcs_admin" and password as "pa$$word". Specify the same configuration in the django "settings.py" file.
7) Create two django-apps. One named "customer" and one named "user".
8) Do the neccessary configurations to set up the template source and asset files like css, js, images in your settings.py file.
8) In terminal, run "python manage.py migrate"
9) Then run, "python manage.py runserver"
