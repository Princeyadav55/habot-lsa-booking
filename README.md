\# HabotConnect LSA Service Booking Backend



\*\*Candidate:\*\* Prince Yadav  

\*\*Position:\*\* Python Backend Developer  

\*\*Project:\*\* HabotConnect Hiring Project



\## Overview



This project is a backend prototype for HabotConnect, a platform connecting parents with Learning Support Assistants (LSAs).



The backend is built using Python, Django, Django REST Framework, and SQLite.



\## Features



\- Parent, LSA Profile, Booking Request, and Payment entities

\- LSA search by skill

\- Available LSA filtering

\- Booking creation API

\- Overlapping booking prevention

\- Payment webhook integration

\- Mock external payment service using Python `requests`

\- Automated unit tests

\- GitHub Actions CI workflow



\## Technology Stack



\- Python 3.13

\- Django 6.1

\- Django REST Framework

\- SQLite

\- Requests

\- GitHub Actions



\## Project Structure



```text

habot-lsa-booking/

│

├── booking/

│   ├── migrations/

│   ├── models.py

│   ├── serializers.py

│   ├── views.py

│   ├── urls.py

│   ├── payment\_service.py

│   └── tests.py

│

├── config/

│   ├── settings.py

│   ├── urls.py

│   ├── asgi.py

│   └── wsgi.py

│

├── .github/

│   └── workflows/

│       └── tests.yml

│

├── manage.py

├── requirements.txt

└── README.md

