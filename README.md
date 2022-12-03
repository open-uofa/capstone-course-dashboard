# Capstone Course Dashboard

[![Documentation](https://github.com/UAlberta-CMPUT401/capstone-dashboard/actions/workflows/deploy-mkdocs.yaml/badge.svg)](https://ualberta-cmput401.github.io/capstone-dashboard/)
![Backend](https://github.com/UAlberta-CMPUT401/capstone-dashboard/actions/workflows/backend.yaml/badge.svg)
![Frontend](https://github.com/UAlberta-CMPUT401/capstone-dashboard/actions/workflows/frontend.yaml/badge.svg)

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

## Summary

Through using the Capstone Course Dashboard, the teaching staff will be able to
view analytics to monitor for and mitigate risks to enhance students’ learning
experience in capstone courses. The users, professors and teaching assistants,
will be able to view the course performance in three levels: the whole class,
individual teams, and students. Performance is sliced by sprints and based on
peer-review feedback, GitHub analytics and TA notes, which can be imported and
parsed from CSV files and exported to CSV files. Key statistical data will be
displayed in tables and charts for easy analyzing with more details available
within. There are two administration levels, the superuser who is often the
instructor is able to grant permission to TAs and both are able to view,
comment, and flag teams and students.

## Dependencies

- Python (>=3.8)
- Yarn
- Docker (optional)

## Usage

To add a course, login and import course data from CSV files or directly from
Google Sheets (TBA).

Within a course, the dashboard will display its statistics and may be
reconfigured as required.

Further documentation can be found
[here](https://open-uofa.github.io/capstone-course-dashboard/).

## Deployment Instructions

### Prerequisites

- OAuth 2.0 credentials from [Google's API Console](https://console.developers.google.com/)
- A GitHub app

### Docker

Copy your GitHub app's private key to the project's root and rename it to
`id_rsa` (this can be modified in `docker-compose.yml`).

From the project's root, run the following commands:

```
cp docker-compose-example.yml docker-compose.yml
```

Modify `docker-compose.yml` to work with your deployment environment.
See [backend setup](backend/README.md) for help generating your secret key.

Run `docker-compose up -d` (you may need root permissions).

### From Source

#### Backend

See [backend setup](backend/README.md).

#### Frontend

Install `yarn`.

Enter the frontend directory:

```
cd front-end/capstone-dashboard/
```

Create the file `.env` and add the following:

```
VITE_PUBLIC_BASE_PATH=<URL_TO_YOUR_HOSTED_BACKEND>
VITE_PUBLIC_GITHUB_OWNER=<YOUR_GITHUB_ACCOUNT_OR_ORGANIZATION_NAME>
VITE_PRIVATE_GOOGLE_CLIENT_ID=<YOUR_GOOGLE_CLIENT_ID>
```

Set the variables based on your deployment configuration.

<br>

Now, run the following commands:

```
yarn build
yarn preview --host --port 80
```

## Releases

For the duration of the Fall 2022 semester, a release will be made for each sprint.
Sprint dates can be viewed
[here](https://ualberta-cmput401.github.io/capstone-dashboard/projectmanagement/#project-plan).

## License

This project is licensed by the University of Alberta (2022) under the
MIT License (see [LICENSE](LICENSE)).

After the conclusion of the Fall 2022 semester, this project will officially
become an open-source project as part of the University of Alberta's Student
Open-Source Initiative.
