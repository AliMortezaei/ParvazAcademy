# ParvazAcademy
## :iphone: a platform for learning
#### with three different roles: student, teacher, admin
# :monocle_face: Specification: 
- Teacher and admin can define and manage a course (teacher can only manage the course he createdr)
- A student can join a course
- Each course can have several sections
- Anyone can see the courses
- Teacher and student can manage their own profile
- Authentication with phone number and email .......
  # Tools and Features
- **using library celery for asynchronous tasks**
- **using redis for storage data and message broker**
- **using database postgresql**
- **using boto3 for arvancloud storage**
- **using JWT(JSON Web Token) for authentication** 
- **writing testing project**
- **writing documents project** 
- **workflow github action** for tesing project, build docker container added dockerhub ([repository](https://hub.docker.com/r/mortezaei2/parvaz_academy))
- **dockerize project(using docker compose)** 
# Run Project 
```bash
docker compose up -d --build
```
- go to browser localhost 0.0.0.0:8000

