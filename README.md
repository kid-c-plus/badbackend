# BAD BACKEND
### <span style="color: blue">(it's good, actually)</span>

Modular, extensible API framework & deployment-ready implementation for Icecast radio station content additions, such as comments, show themes, and more. 

## Installation

- Download into an appropriate directory such as `/var/www/` if you're using Apache:

    cd /var/www
    git clone https://github.com/kid-c-plus/badbackend.git 

- Install dependencies:

    pip3 install -r requirements.txt

## Usage

The recommended usage is to serve this as a WSGI script using the provided run.wsgi script with the webserver of your choice. I recommend Apache, as detailed [here](https://www.howtoforge.com/tutorial/python-apache-mod_wsgi_ubuntu/), but you can also run it with a pure Python server such as gunicorn using this command to run on port 5000:

    gunicorn --bind 0.0.0.0:5000 run:flaskapp


