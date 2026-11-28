<div align="center">

# SmartRoll
### AI-Powered Classroom Attendance Management

**Automate classroom attendance with face recognition and voice-based student identification.**

[![Live App](https://img.shields.io/badge/Live%20App-Open%20SmartRoll-7866D8?style=for-the-badge)](https://smartroll-main.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Backend-Supabase-3FCF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)

<p>
  <img src="assets/student1.png" alt="SmartRoll student illustration" width="180">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/teacher.png" alt="SmartRoll teacher illustration" width="180">
</p>

**Smarter Attendance, Smarter Classrooms.**

</div>

---

## Overview

SmartRoll is an AI-powered attendance management application built for classroom environments. It provides separate **Teacher** and **Student** portals and supports two biometric attendance workflows:

- **Face-based attendance:** Teachers can add classroom photos for facial analysis. Students can also use the camera-based FaceID flow to access their student profile.
- **Voice-based attendance:** Students can register a voice sample, and teachers can record classroom audio for speaker matching during an attendance session.

Alongside attendance, teachers can create subjects, manage class rosters, share enrollment links or QR codes, review attendance results, and view saved records. Students can enroll in subjects and monitor their attendance from their dashboard.

## Features

### Teacher portal

- Teacher account registration and username/password login.
- Dashboard with **Take Attendance**, **Manage Subjects**, and **Attendance Records** views.
- Create subjects with a subject code and section.
- View subject rosters, student counts, and class counts.
- Share a subject code, enrollment link, or QR code with students.
- Add one or more classroom photos and run face analysis.
- Record classroom audio and run voice-based attendance.
- Review present/absent results before confirming and saving attendance.
- View saved attendance records grouped by attendance session.

### Student portal

- Camera-based FaceID login for registered students.
- Register a new student profile using a captured face image.
- Optional voice enrollment during student registration.
- Join a subject using the code shared by the teacher.
- Open a teacher's enrollment link or QR code to start the quick-enrollment flow.
- View enrolled subjects, classes attended, and overall attendance.
- Unenroll from a subject.

### Attendance workflows

| Workflow | What happens |
|---|---|
| Face-based attendance | The teacher selects a subject, adds classroom photos, runs facial analysis, reviews the results, and confirms the attendance records. |
| Voice-based attendance | The teacher records classroom audio. SmartRoll separates usable audio segments, generates voice embeddings, matches them against enrolled voice profiles, and prepares results for review. |
| Student FaceID | A student uses the camera flow. If the face is not recognized, the application offers a new-profile registration flow. |
| Quick enrollment | A student opens a subject invitation link containing a join code and confirms enrollment. |

## How It Works

1. **Teacher creates a subject.** The teacher signs in and creates a subject with its code and section.
2. **Teacher shares an invitation.** SmartRoll provides subject-sharing options, including a QR code and enrollment link.
3. **Student enrolls and registers.** The student joins the subject and completes the required profile registration. Voice enrollment is optional in the student registration flow.
4. **Teacher starts attendance.** The teacher selects a subject and chooses photo-based or voice-based attendance.
5. **Teacher reviews the results.** SmartRoll prepares a present/absent list for the teacher to review.
6. **Attendance is saved.** After confirmation, attendance records are stored and can be viewed later. Students can see attendance information in their dashboard.

## Technology Stack

| Technology | Used for |
|---|---|
| Python | Main application language |
| Streamlit | Application UI, portals, dialogs, and session state |
| OpenCV / dlib | Face-processing workflow and face detection |
| `face_recognition_models` | Pre-trained dlib face landmark and recognition models |
| NumPy | Numerical operations and embedding data |
| scikit-learn | SVC classifier used in the face-identification pipeline |
| Resemblyzer | Voice embedding generation and speaker matching |
| Librosa | Audio loading, resampling, and segmentation |
| Supabase | Database and application data storage |
| bcrypt | Hashing and checking teacher passwords |
| Segno | QR-code generation |
| Pillow | Image loading and processing |
| Pandas | Attendance result preparation and tabular records |

## Project Structure

```text
smartroll-main-shaheed-mohiuddin/
│
├── app.py
├── requirements.txt
├── assets/
│   ├── student1.png
│   └── teacher.png
│
└── src/
    ├── components/
    │   ├── header.py
    │   ├── subject_card.py
    │   ├── dialog_add_photos.py
    │   ├── dialog_attendance_result.py
    │   ├── dialog_auto_enroll.py
    │   ├── dialog_create_subject.py
    │   ├── dialog_enroll.py
    │   ├── dialog_share_subject.py
    │   └── dialog_voice_attendance.py
    │
    ├── database/
    │   ├── config.py
    │   └── db.py
    │
    ├── pipelines/
    │   ├── face_pipeline.py
    │   └── voice_pipeline.py
    │
    ├── screens/
    │   ├── home_screen.py
    │   ├── student_screen.py
    │   └── teacher_screen.py
    │
    └── ui/
        └── base_layouts.py
```

The main entry point is `app.py`. It loads the home screen first and routes to the student or teacher screen based on the selected portal and Streamlit session state.

## Getting Started

### Prerequisites

- Python installed on your machine.
- A Supabase project.
- The Supabase database tables and relationships expected by the application.
- A working camera and microphone for the relevant biometric workflows.

### 1. Clone the repository

```bash
git clone https://github.com/shaheedmohiuddin/smartroll-main-shaheed-mohiuddin.git
cd smartroll-main-shaheed-mohiuddin
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** `dlib-bin` and the voice-processing dependencies may require platform-compatible Python wheels and system libraries. Follow the installation guidance for your operating system if installation fails.

### 4. Configure Supabase credentials

The application reads its Supabase connection values from Streamlit secrets in `src/database/config.py`.

Create this file locally:

```text
.streamlit/secrets.toml
```

Add your own project values:

```toml
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
```

Replace both values with credentials from your Supabase project.

The application accesses these Supabase tables:

- `teachers`
- `students`
- `subjects`
- `subject_students`
- `attendance_logs`

Make sure your Supabase database has the required tables, columns, and relationships before running the application. This repository's `requirements.txt` does not create the database schema automatically.

**Keep secrets private.** Do not commit `.streamlit/secrets.toml`, service-role keys, database credentials, or real student biometric data. The repository's `.gitignore` already includes `.streamlit/` and `secrets.toml` exclusions.

### 5. Run SmartRoll

From the repository root, run:

```bash
streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open that URL in your browser.

## Live Demo

**[Launch SmartRoll](https://smartroll-main.streamlit.app/)**

## Privacy and Responsible Use

SmartRoll processes face images, face embeddings, voice recordings, and voice embeddings. These are sensitive forms of personal and biometric information.

Before using the system in a real classroom:

- Explain what data is collected and how it is used.
- Obtain appropriate consent and follow applicable institutional policies and laws.
- Limit access to biometric profiles and attendance records.
- Define retention and deletion procedures for recordings and biometric data.
- Never upload real student biometric data, private attendance records, or credentials to a public repository.

## Contributing

Suggestions, bug reports, and improvements are welcome. You can open an issue to report a problem or submit a pull request with a proposed change.

## License

No license is currently specified in this repository. Until a `LICENSE` file is added, do not assume that the code is available for reuse, modification, or redistribution.

---

<div align="center">

**SmartRoll — Making classroom attendance faster with AI.**

</div>
