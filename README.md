# backend

Flask can be run simply with `flask run`

If you want to generate a distribution executable (for perception cluster), this can (after everything is installed) be done with `pyinstaller -F --add-data "templates;templates" --add-data "static;static" app.py` (not elaborately tested yet).