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
- using library celery for send otp code async
- using redis for storage data and message broker
- using database postgresql
- **using boto3 for arvancloud storage** #boto3
- **writing testing project** #testing
- **writing documents project** #documents
- **workflow github action** for tesing project, build docker container added dockerhub ([repository](https://hub.docker.com/r/mortezaei2/parvaz_academy))
- **dockerize project(using docker compose)** 
# Run Project 
```bash
docker compose up -d --build
```
- go to browser localhost

