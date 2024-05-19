# CITS3403 Project

A book store/review application that will get us an HD.

This project is a bookstore and review application developed as part of our coursework for CITS3401. The application aims to provide users with an application for discovering, purchasing, and reviewing books. It incorporates features such as user authentication, book browsing, reviews, and recommendations to enhance user engagement and satisfaction.

## Purpose

The purpose of this project is to create a bookstore and review application that will earn us an HD grade. The application provides the following features:

**User Authentication:**
- Users can sign up and log in securely to access the application's features.
- Password hashing for enhanced security.

**Book Catalog:**
- Comprehensive catalog of books with detailed information including title, author, genre, synopsis, picture, etc.
- Ability to search for books based on genre.

**Book Reviews:**
- Users can rate and review books they have read once they have signed in.
- Option to sort books by highest rated to lowest rated.
- Users can easily discover and explore new releases.

**About us:**
- Display of the four members who created the page, including their favorite books and a little information about each member.


## Group Members

| UWA ID   | Name                 | Github User |
|----------|---------------------|-------------|
| 23376234 | Myla Do             | Mylaaado    |
| 22915304 | James Rimmer        | Jimmy141619 |
| 23364195 | Camilo Lima Castillo| Onlinepatron|
| 22980141 | William Lodge       | Log1112     |

## Architecture

The application follows a client-server architecture using Flask as the backend framework and SQLAlchemy as the ORM for database management. The frontend is built using HTML, CSS, and JavaScript, with the help of Bootstrap for responsive design.

## Setting up the Python Environment

1. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - For Unix/Linux:
     ```
     source venv/bin/activate
     ```
   - For Windows:
     ```
     venv\Scripts\activate
     ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Launching the Application

1. Initialize the database:
   ```
   flask db init
   ```

2. Apply the database migrations:
   ```
   flask db migrate
   flask db upgrade
   ```

3. Run the application:
   ```
   flask run
   ```

The application will be accessible at `http://localhost:5000`.

## Running the Tests

To run the tests for the application, use the following command:

```
python -m unittest discover tests
```

This command does the following:
- `python -m unittest`: This runs the unittest module as a script, allowing you to execute tests.
- `discover`: This is a command-line option that tells unittest to discover and run tests in a specified directory.
- `-s tests`: This specifies the directory where unittest should start discovering tests. In this case, it assumes that test files are located in a directory named "tests".