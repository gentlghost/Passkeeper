PASSKEEPER
#### Video Demo:  <URL HERE>
## Description:
PassKeeper is a free local desktop password manager. This password manager can be used on any system with little to no issues.

#### Why a remote password manager?
While using a built-in browser password manager is sufficient and secure for everyday use, it still relies on the internet to ensure that the user can still access their accounts. Since typically it uses whatever account is associated with developer of the browser (Google, Microsoft, Mozilla, etc.), malicious actors have one entry point to get the user's passwords. Therefore, if an actor cracks the account for the browser, they can access all of the user's account.

With a remote password manager, users do not need to worry about dependence on a browser manufacturer account and makes it harder for actors to access information. In order for an actor to gain access to the passwords, they need to access the device itself. However, if the device goes missing, then you lose the passwords. Also, unlike browser managers, there is no way to back up passwords via a server or the cloud, and it has to be backed up via storage. While a user gains the control over their passwords, they do lose the benefits of browser-based managers.

#### Features
PassKeeper allows you to store any password for any service. PassKeeper allows multiple users to use the game instance of the application; however, they will not have access to the other users. Users then can add any password associated with their accounts.

#### Technologies
For this project, I used PyQt5 -- a Python version of the Qt framework -- and SQLite. PyQt5 is a desktop framework that allows for cross platform desktop development. I also used the QtCreator to design the UI for the project. SQLite is used to store users and their accounts.

For encryption and hashing, I used Fernet and Argon. Argon is used to hash the users' passwords to log into PassKeeper and store them to the database. So, even if the malicious actor has access to the database, they need to use Argon. The problem with just hashing passwords is hashing is a one-way process, so hashing a password is easier than unhashing a password. Fernet is used for the passwords on each individual account. When stored on the 

For source control, I used Git with GitHub being the hosting grounds.