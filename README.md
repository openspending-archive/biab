# Budget in a Box

Budget in a Box is a Django webapp for generating nice budget and spending visualization
sites automatically from Budget Data Packages. Simply point BiaB at the URL of a valid BDP dataset
and BiaB will create a site with rich visualization views of the data. New BDPs can be added to
the site at any time.

*This is a prototype release with basic functionality, to be presented at OKFest 2014.
As of the writing of this README, literally no functionality has been implemented.*

## contributing

### Setting up a development instance

Create a virtualenv

run 

```
pip install -r requirements.dev.txt
```

Initialize the database
```
DATABASE_URL=sqlite:///biab.sqlite python biab/manage.py syncdb
DATABASE_URL=sqlite:///biab.sqlite python biab/manage.py migrate
```

now start the instance with

```
DATABASE_URL=sqlite:///biab.sqlite honcho start
```
