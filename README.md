# JobTrack

#### Video Demo: https://youtu.be/WfCr5PV7C_M

#### Description

JobTrack is a web application designed to help users organise and manage their job applications in one place. Applying for jobs can involve keeping track of different companies, job titles, application dates, application statuses, and useful notes. JobTrack provides a central dashboard where users can record this information and update it as they progress through the application process.

The application was developed using Python, Flask, SQLite, HTML, Jinja templates, CSS, and JavaScript. Flask handles the server-side application logic and routes, while SQLite stores application records. HTML and Jinja are used to generate the pages, CSS provides the styling, and JavaScript supports the dashboard search functionality.

#### Features

Users can add job applications with details such as the company name, job title, application date, optional job posting URL, notes, and status. The dashboard displays saved applications and summary cards that help users understand their current application progress. Users can search for applications by company or job title, update an application's status, and open a details page to view an individual record.

JobTrack also allows users to edit and delete existing applications. Form validation helps prevent incomplete or invalid information from being saved. For example, required fields are checked, dates are validated, and job URLs must use HTTP or HTTPS when provided. Flash messages provide feedback after actions, helping users understand whether an operation succeeded or encountered an error.

The available application statuses are Applied, Interview, Offer, and Rejected. These options provide a simple way to track the outcome of each application without requiring a separate spreadsheet.

#### Files

- `app.py` contains the main Flask application. It defines the routes for displaying the dashboard, adding applications, viewing details, editing records, updating statuses, and deleting applications. It also contains input-validation logic and handles form submissions and feedback messages.
- `db.py` provides the database connection used by the application. Separating database access from the routes helps keep the application code organised.
- `init_db.py` creates and initialises the database structure needed to store job applications.
- `jobtrack.db` is the SQLite database file that stores application data created during use.
- `templates/index.html` displays the dashboard, summary cards, application records, search functionality, and available actions.
- `templates/add.html` contains the form for creating a new job application.
- `templates/edit.html` contains the form for modifying an existing application.
- `templates/details.html` displays the information associated with an individual application.
- `static/style.css` contains the CSS used to style the application's pages and interface.

#### Design Decisions

I chose Flask because it provides a straightforward way to build a Python web application with separate routes and templates. SQLite was selected because it is lightweight and does not require a separate database server, making it suitable for a small, single-user project. The database connection is handled in a separate file to avoid duplicating that responsibility throughout the application.

I used separate templates for the dashboard, adding an application, editing an application, and viewing details. This makes each page easier to maintain and gives each task a clear interface. The edit feature allows information to be corrected without creating a duplicate record, while the details page provides a dedicated view of an application. Input validation and parameterised SQL queries help make form handling and database operations more reliable.

#### Development and Testing

During development, I tested the main application workflows, including adding records, viewing them, editing their details, changing statuses, and deleting records. I also checked input validation and confirmed that the Python files compile successfully. Testing each workflow helped identify issues and verify that the main features worked together.

AI tools were used for initial inspiration and guidance during development. I reviewed and tested the application as I built it in the CS50 Codespace.

JobTrack was developed as my CS50x final project to practise Python, web development, database operations, form handling, validation, and building a practical application around a real-world task.

## AI Acknowledgement
ChatGPT was used at the beginning of the project for initial inspiration.The project was developed and tested in the CS50 Codespace.
