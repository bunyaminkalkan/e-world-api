# E-World-Api

Welcome to Your Django E-World-api! This project aims to [Creating an Interactive Card Trading Platform].

## Getting Started

To get this project up and running on your local machine, follow these steps:

### Prerequisites

- Python 3.x
- pip package manager

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/bunyaminkalkan/e-world-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd e-world-api/
    ```

3. Create a virtual environment:

    ```bash
    python -m venv env
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        .\env\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source env/bin/activate
        ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Perform database migrations:

    ```bash
    python manage.py migrate
    ```

7. Create a superuser (admin):

    ```bash
    python manage.py createsuperuser
    ```

8. Start the development server:

    ```bash
    python manage.py runserver
    ```

9. Access the Django admin:

    Open a web browser and go to `http://127.0.0.1:8000/admin/` to access the admin panel. Log in using the superuser credentials created earlier.

## Usage

The project features several endpoints with specific functionalities:

1) At `http://127.0.0.1:8000/`, two request methods are permitted:
   - **GET method**: Lists all available cards.
   - **POST method**: Executes the purchase of a card for logged-in users.

2) At `http://127.0.0.1:8000/factions/`, only the **GET method** is allowed.
   - **GET method**: Lists information related to factions.

3) At `http://127.0.0.1:8000/inventory/<str:username>/`, only the **GET method** is allowed.
   - **GET method**: Lists the cards owned by the logged-in user.

4) At `http://127.0.0.1:8000/user/login/`, only the **POST method** is allowed.
   - **POST method**: Enables user login functionality.

5) At `http://127.0.0.1:8000/user/logout/`, only the **POST method** is allowed.
   - **POST method**: Allows logged-in users to log out.

6) At `http://127.0.0.1:8000/user/register/`, only the **POST method** is allowed.
   - **POST method**: Facilitates user account creation.

7) At `http://127.0.0.1:8000/user/update/<str:username>`, three request methods are permitted:
   - **GET method**: Lists information about the logged-in user.
   - **PUT method**: Allows users to update their information.
   - **DELETE method**: Allows users to delete their account.

These endpoints define the allowed HTTP methods and their functionalities, handling various aspects such as user authentication, card purchase, user registration, information retrieval, and user account management.


## Contributing

If you'd like to contribute to this project, you can follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/fooBar`)
3. Make necessary changes, commit, and push to the new branch (`git push origin feature/fooBar`)
4. Create a Pull Request
