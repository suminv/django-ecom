## Project Name: Pet Project Online Store

### Project Description:
An online store is a platform designed for buying and selling goods and services over the Internet. 

### Installation and Running the Project:
### 1. Clone the repository:

`git clone https://github.com/suminv/django-ecom.git`


### 2. Install and create a virtual environment:

`pip install virtualenv`

`python3 -m venv env`

### 3. Activate the virtual environment:

On Windows:

`env\Scripts\activate`

On macOS and Linux:

`source env/bin/activate`

### 4. Install the required dependencies:

`pip install -r requirements.txt`

### 5. Apply database migrations:

`python manage.py migrate`

### 6. Create a superuser (admin) account:

`python manage.py createsuperuser`

### 7. Start the development server:

`python manage.py runserver`

### 8. Open your web browser and visit http://localhost:8000 to access the app. 



### Key Features and Capabilities of the Project:
- Registration of new users.
- Login and logout of registered users.
- Adding and reading comments to products.
- Searching for products based on various criteria.
- Managing the shopping cart: adding, removing, and changing the quantity of items.
- Order placement with filling in delivery and payment details.

### License:
We suggest using the [![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/), which allows for free use, modification, and distribution of your project with minimal restrictions.
