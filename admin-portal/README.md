# Admin portal documentation

This is a standalone cmd line admin portal application. This application uses the same .env file as backend

## Dependencies

Please install the required dependency using `pip install tabulate`

## How to use the admin portal

- Run the admin.py file using `python admin.py`
- Enter the login credentials.
- After successful login, the user is presented with the following choices:  
   1 : Get user list  
   2 : Add user  
   3 : Delete user  
   4 : Revoke user  
   5 : Assign course  
   6 : Unassign course  
   7 : Authorize user  
   8 : Exit

### 1 : Get user list

Enter 1 to see a list of users with their Email, Assigned courses and Authorization information

### 2 : Add user

Enter 2 to add a user and Enter the user information when prompted.  
The following information is required when adding a user  
 1 - Email  
 2 - Assigned courses (separated by ',')  
 3 - Authorization (Y/N)

### 3 : Delete user

Enter 3 to delete a user  
The following information is required when deleting a user  
 1 - Email

### 4 : Revoke user

Enter 4 to revoke a user's authorization  
The following information is required when revoking a user  
 1 - Email

### 5 : Assign course

Enter 5 to assign a course to a user  
The following information is required to assign a course  
 1 - Email  
 2 - Course Name (separated by ',')

### 6 : Unassign course

Enter 6 to unassign a course  
The following information is required to unassign a course  
 1 - Email  
 2 - Course Name (separated by ',')

### 7 : Authorize user

Enter 7 to authorize a user  
The following information is required to authorize a user  
 1 - Email

### 8 : Exit

Enter 8 to exit the application
