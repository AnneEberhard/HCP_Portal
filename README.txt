THis is only a backend, no frontend implemented. Testing needs to be done via postman or comaparable.

To prepare the application:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
(follow the prompts in the terminal)

To start the application:
python manage.py runserver

To access django admin panel in the browser:
http://127.0.0.1:8000/admin/

IN POSTMAN
To test get patient:
http://127.0.0.1:8000/api/patients/

To test del patient:
http://127.0.0.1:8000/api/patients/1/
(1: add id in database)

To post patient
http://127.0.0.1:8000/api/patients/
    {
        "username": "Mamsell",
        "first_name": "Mamsell",
        "last_name": "Gehrau",
        "email": "Mamsell@manor.de",
        "is_doctor": false,
        "is_patient": true
    }
CAVE: if logged in, add x-CRSF Token to the request

To test get doctor:
http://127.0.0.1:8000/api/doctors/

To test del doctor:
http://127.0.0.1:8000/api/doctors/1/
(1: add id in database)

To test post doctor:
http://127.0.0.1:8000/api/doctors/
{
    "username": "DrSmith",
    "first_name": "John",
    "last_name": "Smith",
    "email": "drsmith@example.com",
    "is_doctor": true,
    "is_patient": false,
    "specialization": "Chirurgie",
    "title": "Dr.med."
}
CAVE: if logged in, add x-CRSF Token to the request

To test appointment, you'll need to login first:
http://127.0.0.1:8000/login/
{
    "username": "your_username",
    "password": "your_password"
}

You'll receive sessionid and x-crsf Token - add these to the respective headers in the appointment testing

To test get appointment:
http://127.0.0.1:8000/api/appointments/

To test del appointment:
http://127.0.0.1:8000/api/appointments/1/
(1: add id in database)

To test post appointment:
http://127.0.0.1:8000/api/appointments/
{
    "title": "Routine Checkup",
    "description": "Routine annual checkup",
    "date": "2024-06-12T10:00:00Z",
    "doctor": 1,
    "patient": 2
}
(1: add doctor id from database, 2: add patient id from database)

If you want to test different user_ids, user logout first:
http://127.0.0.1:8000/logout/
(add X-CRSF-Token from login)

To run in-built tests:
python manage.py test
