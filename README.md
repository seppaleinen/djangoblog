
<a href='https://coveralls.io/r/seppaleinen/djangoblog?branch=master'><img src='https://coveralls.io/repos/seppaleinen/djangoblog/badge.svg?branch=master' alt='Coverage Status' /></a>
<a href="https://landscape.io/github/seppaleinen/djangoblog/master">
  <img alt="Code Health" src="https://landscape.io/github/seppaleinen/djangoblog/master/landscape.svg?style=flat"/>
</a>
<img src="https://travis-ci.org/seppaleinen/djangoblog.svg" data-bindattr-817="817" title="Build Status Images">
<a href="https://codecov.io/github/seppaleinen/djangoblog?branch=master"><img src="https://codecov.io/github/seppaleinen/djangoblog/coverage.svg?branch=master" alt="Coverage via codecov.io" /></a>
<a href="https://requires.io/github/seppaleinen/djangoblog/requirements/?branch=master"><img src="https://requires.io/github/seppaleinen/djangoblog/requirements.svg?branch=master" alt="Requirements Status" /></a>


#Django

`python manage.py runserver`      To run server and deploy
`python manage.py test`           To test
`python manage.py makemigrations` To make changes scripts to db
`python manage.py migrate`        To run db changes scripts

`gunicorn --config=gunicorn.config.py djangoblog.wsgi` To start gunicorn server running on localhost:8000