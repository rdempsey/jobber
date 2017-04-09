# Jobber

![Image of Jobber 1.0](https://github.com/rdempsey/jobber/docs/Jobber_1.0.png)

## Overview

Being able to automatically filter out applications from unqualified applicants can save busy hiring managers a lot of time.
They only need to spend time looking at applicants who meet their minimum qualifications.  Why waste time reading through
delivery driver applications from people who don’t have a vehicle if you require drivers to use their own vehicle?

## Requirements

Jobber determines whether a job application meets a set of minimum qualifications:

* The job application will be a list of questions, each of which has a question id and an answer.
* The qualifications will be a list of question ids, each associated with a list of acceptable answers.
* If an applicant fails to answer any one of these questions with an acceptable answer, their application should be rejected. Otherwise the application should be accepted.
* The employer should be able to view only the accepted applications.

Additionally:

* Accepted applications must have all questions answered correctly.
* Accepted applications must be shown to the employer.
* Unaccepted applications must not be shown to the employer.

## Meeting the Requirements

Jobber achieves the above by providing an API that:

Accepting a list of questions with an acceptable answer for each question:
```
[
    {
        id: "id1",
        question: "string",
        answer: "string"
    },
    {
        id: "id2",
        question: "string",
        answer: "string"
    },
    ...
]
```

Receives job applications where each application is a JSON document conforming to this design:
```
{
    Name: "string",
    Questions: [
        {
            id: "id10",
            answer: "string"
        },
        {
            id: "id20",
            answer: "string"
        },
        ...
    ]
}
```

Upon receiving the job application Jobber decides to either accept or reject each application.

## Quickstart

### Requirements

Jobber has been tested with the following:

* Docker >= 1.13
* Docker Compose >= 1.8.0

### Running Jobber

Jobber is fully dockerized and consists of two containers: 1) an API-only backend, and 2) a Flask web application front-end.
To build and run the containers do the following:

```
git clone git@github.com:rdempsey/jobber.git
cd jobber
docker-compose up --build -d
```

If need be you can edit the provided docker-compose file to change the ports.

Open a web browser to `http://localhost:5000` to reach the Jobber dashboard. In addition, the API documentation is available at `http://localhost:8080/1.0/ui/`