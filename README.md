# Jobber

Being able to automatically filter out applications from unqualified applicants can save busy hiring managers a lot of time.
They only need to spend time looking at applicants who meet their minimum qualifications.  Why waste time reading through
delivery driver applications from people who don’t have a vehicle if you require drivers to use their own vehicle?

Jobber determines whether a job application meets a set of minimum qualifications:

* The job application will be a list of questions, each of which has a question id and an answer.
* The qualifications will be a list of question ids, each associated with a list of acceptable answers.
* If an application fails to answer any one of these questions with an acceptable answer, the application should be rejected. Otherwise the application should be accepted.
* The employer should be able to view only the accepted applications.

Jobber achieves the following by:

Accepting a list of questions with an acceptable answer for each question:
```
[
    {
        Id: "id1",
        Question: "string",
        "Answer": "string" }
    ,
    {
        Id: "id2",
        Question: "string",
        "Answer": "string"
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
            Id: "id10", Answer: "string"
        },
        {
            Id: "id20", Answer: "string"
        },
        ...
    ]
}
```

Jobber then decides to either accept or reject each application.

Additionally:

* Accepted applications must answer all questions correctly.
* Accepted applications must be shown to the employer.
* Unaccepted applications must not be shown to the employer.