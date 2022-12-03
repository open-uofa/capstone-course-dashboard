# Project Requirements

## Executive Summary

Through using the Capstone Course Dashboard, the teaching staff will be able to view analytics to monitor for and mitigate risks to enhance students’ learning experience in capstone courses. The users, professors and teaching assistants, will be able to view the course performance in three levels: the whole class, individual teams, and students. Performance is sliced by sprints and based on peer-review feedback, GitHub analytics and TA notes, which can be imported and parsed from CSV files and exported to CSV files. Key statistical data will be displayed in tables and charts for easy analyzing with more details available within. There are two administration levels, the superuser who is often the instructor is able to grant permission to TAs and both are able to view, comment, and flag teams and students. Data will be imported from csv files with import from the course portal and direct from google sheets under consideration. Ideally users can also reconfigure the dashboard for adding and removing a report or chart.

## Project Glossary

**Class**
A class represents the set of data recorded for a course.

**Instructor**
An instructor represents the owner of a class. They have full adminstrative privileges.

**TA**
A TA is a user whose account has a limited subset of an instructor's prvileges.

**Student**
A student represents a person attending a capstone course. They have class-related data and personal data associated with them but do not have an account.

**Team**
A team is a group of students working on the same project and contains aggregated data of all students within it.

**Peer-Review Feedback**
Peer-review feedback is assigned to a student within a team and contains the opinions of other team members for that student.

**Red Flag**
A red flag is an attribute assigned when some threshold is not met (such as number of commits). It is used by users to quickly identify possible issues.

**Note**
A note, also referred to as a comment, is a text field that users can attach to teams.

**Dashboard**
The dashboard is where users will see analytics of a class at multiple levels in various graphical formats.

**Sprint**
More generically a "milestone", these represent a time span during which teams dedicate themselves towards completing a specific set of features and tasks.
Users can view what teams have completed each sprint.

## User Stories
### 1.XX Viewing Data

=== "US 1.01 - View Class GitHub Analytics"
    **As** a User, **I want** to be able to view GitHub Analytics data for all the students of the class for each sprint, **so that** I can analyze students' performance in comparison to the rest of the class.
    
    **Acceptance Tests**
    
    1. User can view a list of students with their GitHub Analytics data for each sprint.
    2. Data is expressed in tables or charts containing various GitHub Analytics data.
    3. With the selected sprint, user cannot see data from other sprints.
    4. User can see aggregate data when no sprint is selected.

    **Story Points: ** 5

=== "US 1.02 - View Class Peer Review Ratings"
    **As** a User, **I want** to be able to view peer review ratings for all the students of the class for each sprint, **so that** I can analyze how well students are getting along with their teams in comparison to the rest of the class.

    **Acceptance Tests**

    1. User can view a list of students with their peer review ratings for each sprint.
    2. With the selected sprint, user cannot see ratings from other sprints.
    3. User can see aggregate data when no sprint is selected.

    **Story Points: ** 3

=== "US 1.03 - View Class Form Submissions"
    **As** a User, **I want** to be able to view form submissions for all the students of the class, **so that** I can tell at a glance how many students still have to submit their forms.
 
    **Acceptance Tests**
 
    1. User can view a list of students with their form submission status.
    2. User can select which form to check submission status for.

    **Story Points: ** 2

=== "US 1.04 - View Team Performance"
    **As** a User, **I want** to be able to view the performance of a team for each sprint, **so that** I can mitigate risks and improve team quality.
    
    **Acceptance Tests**
    
    1. User can view team performance for each sprint 
    2. Performance is expressed in GitHub analytics. 
    3. With the selected sprint, user can not see performance of other sprints.
    4. User can see aggregate data when no sprint is selected.

    **Story Points: ** 3

=== "US 1.05 - Display Meeting Minutes"
    **As** a User, **I want** to be able to see each team's meeting minutes, **so that** I can get an idea of what is being discussed during meetings.
 
    **Acceptance Tests**
 
    1. User can view meeting minutes for all of a team’s meetings in the selected sprint.
    2. User can view the date of a meeting.
    3. User can view the agenda, attendees, minutes, and action items.

    **Story Points: ** 2

=== "US 1.06 - Display Comments"
    **As** a User, **I want** to be able to view comments on teams for each sprint, **so that** I can get an idea of any previous issues the team had that were noted down.

    **Acceptance Tests**

    1. User can view all comments for a team for the selected sprint.
    2. The timestamp of when the comment was made is displayed.
    3. User cannot view comments for sprints that were not selected.
    4. If no sprint is selected, all comments for the team are displayed.

    **Story Points: ** 1

=== "US 1.07 - View Student’s GitHub Analytics"
     **As** a User, **I want** to be able view a student’s GitHub Analytics data for each sprint, **so that** I can ensure students are active and contributing to their project.

    **Acceptance Tests**

    1. User can view GitHub Analytics data on a student’s information page.
    2. With the selected sprint, user cannot see the data from other sprints.
    3. User can see aggregate data when no sprint is selected.

    **Story Points: ** 3

=== "US 1.08 - View Student’s Peer Review Ratings"
     **As** a User, **I want** to be able to view a student’s peer review ratings for each sprint, **so that** I can ensure students are getting along well with their team members.

    **Acceptance Tests**

    1. User can view peer review ratings on a student’s information page.
    2. With the selected sprint, user cannot see the ratings from other sprints.
    3. User can see aggregate ratings when no sprint is selected.   

    **Story Points: ** 2

=== "US 1.09 - View Student Profile"
     **As** a User, **I want** to be able to view a student's profile, **so that** I can know about a student's personal experience and programming background.

    **Acceptance Tests**

    1. User can access student's profile.
    2. User can see their personal experience and courses taken on their profile.
    3. Test with an existent student in the course.

    **Story Points: ** 2
------------------------------------------------
### 2.XX Login and Authorization
=== "US 2.01 - Authentication"
     **As** a User, **I want** to authenticate with my University of Alberta account, **so that** I can get access to the app's functionalities.

    **Acceptance Tests**

    1. User can sign in with correct U of A credentials (ualberta.ca email and password)
    2. User can not sign in with correct email and incorrect password
    3. User can not sign in with incorrect email
    4. User can not sign in with a non U of A email
    5. User can not access app's functionalities without signing in 

    **Story Points: ** 2

=== "US 2.02 - Grant Permission"
     **As** an Instructor, **I want** to grant permission to TAs for a course, **so that** they can get access to the app's functions.
    
     **Acceptance Tests**
    
     1. Instructor can provide a TA’s email address to be allowed as a user through a MongoDB shell command.
     2. Test TA login once permission has been granted (Pass).
     3. Test TA login without permission (Fail).
     4. Test granting permission to TA who already has permission (Fail).
     5. Test invalid email address (Fail).

     **Story Points: ** 3

=== "US 2.03 - Revoke Access"
     **As** an Instructor, **I want** to be able to revoke the access of a TA **so that** once a TA has left the teaching team, they will no longer have access to the app.
    
     **Acceptance Tests**
    
     1. Instructor can input an email address to revoke access for through a MongoDB shell command.
     2. Test TA login after revoking access (Fail).
     3. Test with incorrect TA email (Fail).
     4. Test with TA email that does not have access (Fail).

     **Story Points: ** 3

=== "US 2.04 - Logout"
     **As** a User, **I want** to be able to logout, **so that** I can prevent unauthorized access or let someone else login.
    
     **Acceptance Tests**
    
     1. User cannot use the app after logging out without signing back in.  

     **Story Points: ** 2

=== "US 2.05 - Security"
     **As** a User, **I want** to be sure that my app is secure, **so that** I do not have to worry about data leaks.
    
     **Acceptance Tests**
    
     1. A non-user cannot access application data through common security vulnerabilities.
         - Users are authenticated through eClass OAuth.
         - CSRF tokens should be used for all POST requests.
     2. A User cannot inject javascript into the application (e.g. XSS).

     **Story Points: ** 5

=== "US 2.06 - Admin Portal"
     **As** an Admin, **I want** to be able to have a separate login **so that** I can view and change permissions of other users.

    **Acceptance Tests**

    1. Admins can login to the portal.
    2. Admins can view user permissions.
    3. Admins can change user permissions.  

    **Story Points: ** 3
------------------------------------------------
### 3.XX Data Intake
=== "US 3.01 - Import CSV Files"
     **As** a User, **I want** to be able to import a CSV file into the app, **so that** I can view the data in a centralized manner.

    **Acceptance Tests**

    1. User can upload a CSV file with peer-review feedback.
    2. User can upload a CSV file with student experience.

    **Story Points: ** 2

=== "US 3.02 - Import Google Sheets Data"
     **As** a User, **I want** to be able to provide a link to a Google Sheets page and have the app import the data from there **so that** I can view the data in a centralized manner.
    
     **Acceptance Tests**
    
     1. User can provide a valid link and data will be imported successfully.
     2. Test with a non-Google Sheets link (Fail).
     3. Test with a link to a Google Sheets page that has an unexpected table format (Fail).

     **Story Points: ** 2

=== "US 3.03 - Import CSVs with different formats (i.e. different columns)"
     **As** a User, **I want** to be able to import my own CSV files that may have a different format, **so that** I can use the dashboard for many courses.

    **Acceptance Tests**

    1. User can import any kind of CSV file successfully.

    **Story Points: ** 5

=== "US 3.04 - Export CSV"
     **As** a User, **I want** to be able to export all the app’s data as a CSV file, **so that** I can use the data elsewhere.

    **Acceptance Tests**

    1. User can download a CSV file to their device.
    2. CSV file contains all of the app's data.

    **Story Points: ** 2

=== "US 3.05 - Import GitHub Analytics Data"
     **As** a User, **I want** to be able to import data for each team from GitHub Analytics, **so that** I can view GitHub-related data for teams and students.
    
     **Acceptance Tests**
    
     1. User can provide a URL to a GitHub repository and have all the data automatically  imported.
     2. GitHub analytics are associated with the correct team.

     **Story Points: ** 3
     
=== "US 3.06 - Import Meeting Minutes"
     **As** a User, **I want** to be able to import each team’s meeting minutes, **so that** I can view them in an aggregated fashion within the app.

    **Acceptance Tests**

    1. User can provide a link to the GitHub page containing the team’s meeting minutes.
    2. Test with incorrect link (fail).

    **Story Points: ** 3

=== "US 3.07 - Enter Comments"
     **As** a User, **I want** to be able to comment on teams for each sprint **so that** I can make note of any issues and refer back to them later.
    
     **Acceptance Tests**
    
     1. User can leave a comment on a team.
     2. User can chain more comments to an existing comment.

     **Story Points: ** 3

=== "US 3.08 - Delete Comments"
     **As** a User, **I want** to be able to delete comments on teams, **so that** I can remove any comments for issues that have been resolved, or remove a comment that was made by mistake.
    
     **Acceptance Tests**
    
     1. Each comment can be deleted.
     2. User can delete any comment made for a team.
     3. Other comments will not be deleted.

     **Story Points: ** 2
------------------------------------------------
### 4.XX Data Tables
=== "US 4.01 - Sort Data"
     **As** a User, **I want** to be able to sort data in ascending or descending order of a selected variable, **so that** I can get an idea of the top students/teams and bottom students/teams.

    **Acceptance Tests**

    1. User can sort data to rank students based on their GitHub commits.
    2. User can sort data to rank students based on their peer evaluation ratings.
    3. Test sorting can be done in ascending and descending order.  

    **Story Points: ** 2

=== "US 4.02 - Filter Data"
     **As** a User, **I want** to be able to filter data by certain conditions, **so that** I can focus on students matching specific criteria and ignore the rest.
    
     **Acceptance Tests**
    
     1. User can filter data to see which students have not submitted a certain form.
     2. User can filter data to see which students have less than x amount of commits.  

     **Story Points: ** 2

=== "US 4.03 - Highlight Red Flags"
     **As** a User, **I want** to be able to see students that meet certain conditions highlighted in the table, **so that** I can easily see students that may require attention.
    
     **Acceptance Tests**
    
     1. User can set up a threshold to highlight students.
     2. Only students that match the specified conditions are highlighted.  

     **Story Points: ** 5
     
------------------------------------------------
### 5.XX Create and Customize
=== "US 5.01 - Reconfigure Dashboard"
     **As** a User, **I want** to be able to reconfigure the charts and diagrams displayed on the dashboard, **so that** I can view whichever information I think is most important.
    
     **Acceptance Tests**
    
     1. There is adequate documentation on how to reconfigure the dashboard.
     2. Charts and diagrams can easily be added to the dashboard in the backend.
     3. Charts and diagrams can easily be removed from the dashboard in the backend.

     **Story Points: ** 8

=== "US 5.02 - Add Other Capstone Courses"
     **As** an Instructor, **I want** to be able to add other capstone courses to the dashboard, **so that** I can use the same app to view the performance of multiple courses.
    
     **Acceptance Tests**
    
     1. Instructor can add other capstone courses.
     2. Instructor can view performance of the added course.    

     **Story Points: ** 5

## MoSCoW
### Must Have

* US 1.01 - View Class GitHub Analytics
* US 1.02 - View Class Peer Review Ratings
* US 1.03 - View Class Form Submissions
* US 1.04 - View Team Performance
* US 1.07 - View Student’s GitHub Analytics
* US 1.08 - View Student’s Peer Review Ratings
* US 1.09 - View Student Profile
* US 2.01 - Authentication
* US 2.04 - Logout
* US 2.05 - Security
* US 3.01 - Import CSV files
* US 3.04 - Export CSV file
* US 3.05 - Import GitHub Analytics Data
* US 4.01 - Sort Data

### Should Have

* US 1.06 - Display Comments
* US 2.02 - Grant Permission
* US 2.03 - Revoke Access
* US 3.07 - Enter Comments
* US 3.08 - Delete Comments
* US 4.02 - Filter Data

### Could Have

* US 3.03 - Import Different Kinds of CSV Files
* US 3.06 - Import Meeting Minutes
* US 4.03 - Highlight Red Flag
* US 5.01 - Reconfigure Dashboard

### Would Like But Won't Get

* US 1.05 - Display Meeting Minutes
* US 2.06 - Admin Portal
* US 3.02 - Import Google Sheets Data
* US 5.02 - Add Other Capstone Course


## Similar Products

* [Google Analytics](https://marketingplatform.google.com/about/analytics/)
    * Analytics Dashboard
    * Help users identify trends and patterns in how visitors engage with their websites.
    * Features enable data collection, analysis, monitoring, visualization and reporting.
    * Integration with other applications.
    * We can use it as inspiration for how to display a dashboard of graphs and statistics professionally.
* [Google Looker Studio](https://cloud.google.com/looker-studio)
    * Google Analytics but web based for general data
    * Visual inspiration for a modern web data dashboard
* [Power Bi](https://powerbi.microsoft.com/)
    * Lets users view dashboards, reports, and Power BI apps — a type of content that combines related dashboards and reports
    * Used to create the data models before disseminating reports throughout the organization
    * We can use it as inspiration for how to display a dashboard of graphs and statistics professionally.
* [Tableau](https://www.tableau.com/)
    * Tableau is basically a data visualization tool which provides pictorial and graphical representations of data.
    * Real-time analytics.
    * Intuitive Dashboard Creation and UX.
    * Connect to a variety of data sources (and easily integrate with existing technology)
    * Role-based permissions.
    * Simple sharing and collaboration.
    * Mobile accessibility.
    * Querying in natural language with ask data.
    * We can use it as inspiration for how to display a dashboard of graphs and statistics professionally.
* [Kallidus](https://www.kallidus.com/)
    * Supports the entire employee lifecycle.
    * From onboarding and upskilling, to performance reviews and employee farewells
    * We can use it as a reference for displaying team / student progress in a comprehensible and effective way.

## Open Source Projects

* [freeboard](https://freeboard.io/)
* [grafana](https://grafana.com/)
* [redash](https://redash.io/)
* [metabase](https://www.metabase.com/)

## Technical Resources
### Backend: FastAPI + MongoDB

* [FastAPI Documentation](https://fastapi.tiangolo.com/)
* [MongoDB Documentation](https://www.mongodb.com/docs/)
* [PyTest](https://docs.pytest.org/)

### Deployment: Cybera + Docker (TBD)

* [Cybera RAC Guide](https://wiki.cybera.ca/display/RAC/Rapid+Access+Cloud+Guide%3A+Part+1)
* [Docker Documentation](https://docs.docker.com/)

### Frontend: Svelte

* [Svelte Documentation](https://svelte.dev/docs)
* [Svelte Tutorial](https://svelte.dev/tutorial/basics)
* [Plotly Dash](https://dash.plotly.com/)
    * Open-source dashboard frontend.
* [Selenium](https://www.selenium.dev/)
* [Katalon](https://katalon.com/web-testing)
