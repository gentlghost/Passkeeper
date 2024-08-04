PASSKEEPER
#### Video Demo:  https://youtu.be/XTdhiSlVAzU
## Description:
PassKeeper is a free local desktop password manager. This password manager can be used on any system with little to no issues.

#### Features
PassKeeper allows you to store any password for any service. PassKeeper allows multiple users to use the game instance of the application; however, they will not have access to the other users. Users then can add any password associated with their accounts.

PassKeeper also works on Windows and Linux.

#### Technologies
For this project, I used PyQt5 -- a Python version of the Qt framework -- and SQLite. PyQt5 is a desktop framework that allows for cross platform desktop development. I also used the QtCreator to design the UI for the project. SQLite is used to store users and their accounts.

For encryption and hashing, I used Fernet and Argon. Argon is used to hash the users' passwords to log into PassKeeper and store them to the database. So, even if the malicious actor has access to the database, they need to use Argon. The problem with just hashing passwords is hashing is a one-way process, so hashing a password is easier than unhashing a password. Fernet is used for the passwords on each individual account. When stored on the 

For source control, I used Git with GitHub being the hosting grounds.

#### File Walkthrough
`app.py` is the main file that runs the application. It contains all classes for each page, the main window, and the account widget for each account displayed on the home page.

`utilities.py` has all the functions that interact between SQLite and Python via the official SQLite Python Library.

The `pages` directory has all the classes for the UI of each page (minus the home page).

The `ui` directory contains all the `.ui` files for each page (minus the home page). The UI was made with Qt Creator.

`passkeeper.db` contains each user and account stored in the app.