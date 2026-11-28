# SmartRoll – AI-Powered Attendance Management System

SmartRoll is an AI-powered classroom attendance platform designed to make attendance tracking faster and easier for teachers and students. It combines facial recognition and voice-based verification with classroom and subject management features.

Teachers can create and manage subjects, share enrollment codes or QR codes, take attendance, review results, and access attendance records. Students can join subjects and monitor their attendance through a dedicated student workspace.

> **SmartRoll — Smarter Attendance, Smarter Classrooms.**

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Technology Stack](#technology-stack)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Run the Flask Landing Page](#run-the-flask-landing-page)
- [Live Demo](#live-demo)
- [Notes](#notes)

## Features

### AI-powered attendance
- **Face-based attendance:** Identify students from classroom photos and prepare attendance results for teacher review.
- **Voice-based attendance:** Support attendance through voice verification.
- **Attendance review:** Review detected students and their attendance status before saving a session.
- **Attendance records:** View previously saved attendance sessions.

### Teacher workspace
- Create and manage subjects.
- View subject rosters and class information.
- Share subject enrollment codes and QR codes with students.
- Start photo-based or voice-based attendance sessions.
- Review and confirm attendance results.

### Student workspace
- Join a subject using a shared subject code or QR code.
- Register a student profile.
- View enrolled subjects.
- Track classes attended and subject-wise attendance.

## How It Works

1. **Create or join a subject:** Teachers create a subject and share its enrollment code or QR code. Students use the shared details to join.
2. **Register students:** Students complete the profile and biometric registration flow provided by the application.
3. **Take attendance:** A teacher selects a subject and uses photo-based or voice-based attendance.
4. **Review and save:** The teacher checks the attendance results and confirms the session.
5. **Track attendance:** Students and teachers can access the attendance information available in their respective workspaces.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Streamlit | Attendance application interface |
| Flask | Landing page |
| HTML, CSS and JavaScript | Landing page structure, styling and interactions |
| OpenCV | Computer vision |
| Face Recognition / Dlib | Facial recognition |
| Resemblyzer | Voice embeddings |
| Librosa | Audio processing |
| Supabase | Database and cloud services |

## Screenshots

The screenshots below use the image paths in this repository. Keep the `static/img/demo/` folder when uploading the project to GitHub.

### Landing page

![SmartRoll landing page](static/img/demo/smartroll-landing.png)

### Student workspace

![Student dashboard](static/img/demo/smartroll-student-flow-3-dashboard.png)

### Teacher workspace

![Teacher dashboard](static/img/demo/smartroll-teacher-flow-2-dashboard.png)

### Photo-based attendance

![Photo attendance workflow](static/img/demo/smartroll-teacher-flow-5.2-photo-attendance.png)

### Voice-based attendance

![Voice attendance workflow](static/img/demo/smartroll-teacher-flow-5.1-voice-attendance.png)

### Subject sharing

![Share subject using QR code or link](static/img/demo/smartroll-teacher-flow-4-share-qr-or-link.png)

## Project Structure

The Flask landing-page files are organised as follows:

```text
SmartRoll/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── styles.css
    └── img/
        ├── logo.png
        └── demo/
            ├── smartroll-landing.png
            ├── smartroll-student-flow-1-login.png
            ├── smartroll-student-flow-2-enroll.png
            ├── smartroll-student-flow-3-dashboard.png
            ├── smartroll-teacher-flow-1-login.png
            ├── smartroll-teacher-flow-2-dashboard.png
            ├── smartroll-teacher-flow-3-create-course.png
            ├── smartroll-teacher-flow-4-share-qr-or-link.png
            ├── smartroll-teacher-flow-5.1-voice-attendance.png
            ├── smartroll-teacher-flow-5.2-photo-attendance.png
            └── smartroll-teacher-flow-5-see-stored-records.png
```

The AI attendance workspace is accessed through the deployed application linked below. The structure above describes the Flask landing-page portion of the project.

## Run the Flask Landing Page

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub details.

### 2. Create and activate a virtual environment (recommended)

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the landing-page requirements

```bash
pip install -r requirements.txt
```

### 4. Start Flask

```bash
python app.py
```

Open the local landing page at:

```text
http://127.0.0.1:5002
```

> These instructions run the Flask landing page. The deployed AI attendance workspace is linked separately below.

## Live Demo

- **AI Attendance Application:** [SmartRoll](https://smartroll-main.streamlit.app/)

## Notes

- Keep the image files in `static/img/` and `static/img/demo/` at the paths referenced by the HTML template. Otherwise, the landing page screenshots and logo will not load.
- The Flask landing page and the deployed Streamlit attendance application are separate parts of the SmartRoll experience.
- Before deploying biometric attendance in a real classroom, provide appropriate notice, obtain required consent, and protect biometric data through suitable access controls and retention practices.

## Contributing

Suggestions and improvements are welcome. Feel free to open an issue or submit a pull request.

## License

Add a license file to this repository before describing the project as open source. Until then, no reuse or redistribution license is specified.
