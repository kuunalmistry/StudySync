<div align="center">

<h1>🎓 StudySync</h1>

<h3>Cloud-Based Student Assignment & Notes Management System</h3>

<p><strong>Organize. Manage. Store. Study.</strong></p>

<p>
A cloud-based student productivity application for managing assignments,
subjects and academic files from one centralized platform.
</p>

<br>

<a href="https://studysync.kuunalmistry.workers.dev">
<img src="https://img.shields.io/badge/🚀%20LIVE%20DEMO-StudySync-2563EB?style=for-the-badge&logo=cloudflare&logoColor=white" alt="Live Demo">
</a>

&nbsp;

<a href="https://github.com/kuunalmistry/StudySync">
<img src="https://img.shields.io/badge/💻%20SOURCE%20CODE-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>

<br><br>

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
<img src="https://img.shields.io/badge/MySQL-Azure-4479A1?style=flat-square&logo=mysql&logoColor=white" alt="MySQL">
<img src="https://img.shields.io/badge/AWS-S3-FF9900?style=flat-square&logo=amazonaws&logoColor=white" alt="AWS S3">
<img src="https://img.shields.io/badge/Azure-App%20Service-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" alt="Azure">
<img src="https://img.shields.io/badge/Cloudflare-Workers-F38020?style=flat-square&logo=cloudflare&logoColor=white" alt="Cloudflare">

<br><br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,50:2563EB,100:06B6D4&height=150&section=header&text=StudySync&fontSize=44&fontColor=ffffff&animation=fadeIn&fontAlignY=55" width="100%" alt="StudySync">

</div>

---

<h2>✨ About StudySync</h2>

<p>
<strong>StudySync</strong> is a cloud-based student assignment and notes management
application developed using <strong>Python and Flask</strong>. It provides a
centralized workspace for students to organize subjects, manage assignments,
and handle academic files.
</p>

<p>
The application uses a <strong>multi-cloud architecture</strong> combining
<strong>Microsoft Azure</strong>, <strong>Amazon Web Services</strong>, and
<strong>Cloudflare</strong>.
</p>

<br>

<div align="center">

<table>
<tr>

<td align="center" width="25%">
<h3>📚</h3>
<strong>Assignments</strong>
<br>
Create & manage
</td>

<td align="center" width="25%">
<h3>📂</h3>
<strong>Files</strong>
<br>
Upload & manage
</td>

<td align="center" width="25%">
<h3>☁️</h3>
<strong>Cloud</strong>
<br>
Multi-cloud deployment
</td>

<td align="center" width="25%">
<h3>📊</h3>
<strong>Monitoring</strong>
<br>
Application telemetry
</td>

</tr>
</table>

</div>

---

<h2>🚀 Live Application</h2>

<div align="center">

<a href="https://studysync.kuunalmistry.workers.dev">
<img src="https://img.shields.io/badge/OPEN%20STUDYSYNC-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Open StudySync">
</a>

<br><br>

<code>https://studysync.kuunalmistry.workers.dev</code>

</div>

---

<h2>✨ Features</h2>

<table>
<tr>

<td width="50%" valign="top">

<h3>📝 Assignment Management</h3>

<ul>
<li>Create assignments</li>
<li>View assignments</li>
<li>Edit assignments</li>
<li>Delete assignments</li>
<li>Organize assignments by subject</li>
</ul>

</td>

<td width="50%" valign="top">

<h3>📚 Subject Management</h3>

<ul>
<li>Create subjects</li>
<li>View subjects</li>
<li>View subject-wise assignments</li>
<li>Keep academic work organized</li>
</ul>

</td>

</tr>

<tr>

<td width="50%" valign="top">

<h3>📂 File Management</h3>

<ul>
<li>Upload assignment files</li>
<li>Download files</li>
<li>Delete files</li>
<li>Private cloud storage through Amazon S3</li>
</ul>

</td>

<td width="50%" valign="top">

<h3>☁️ Cloud Infrastructure</h3>

<ul>
<li>Azure application hosting</li>
<li>Azure MySQL database</li>
<li>AWS S3 file storage</li>
<li>Cloudflare edge layer</li>
<li>Application Insights monitoring</li>
</ul>

</td>

</tr>
</table>

---

<h2>🏗️ System Architecture</h2>

<div align="center">

<table>
<tr>

<td align="center">
<strong>👤 Student</strong>
<br><br>
Web Browser
</td>

<td align="center">
<strong>→</strong>
</td>

<td align="center">
<strong>☁️ Cloudflare</strong>
<br><br>
Worker / Reverse Proxy
</td>

<td align="center">
<strong>→</strong>
</td>

<td align="center">
<strong>🔷 Azure</strong>
<br><br>
App Service / Flask
</td>

</tr>
</table>

<br>

<table>
<tr>

<td align="center" width="33%">
<strong>🗄️ Azure MySQL</strong>
<br><br>
Structured application data
</td>

<td align="center" width="33%">
<strong>🪣 AWS S3</strong>
<br><br>
Uploaded academic files
</td>

<td align="center" width="33%">
<strong>📊 Application Insights</strong>
<br><br>
Monitoring and telemetry
</td>

</tr>
</table>

</div>

<h3>Architecture Flow</h3>

<div align="center">

<pre>
┌──────────────┐
│    Student   │
│ Web Browser  │
└──────┬───────┘
       │ HTTPS
       ▼
┌──────────────────────┐
│  Cloudflare Worker   │
│ Reverse Proxy / Edge │
└──────────┬───────────┘
           │ HTTPS
           ▼
┌────────────────────────────┐
│     Azure App Service      │
│  Flask / Python Application│
└───────────┬────────────────┘
            │
       ┌────┼─────────────┐
       │    │             │
       ▼    ▼             ▼
┌─────────┐ ┌─────────┐ ┌──────────────────┐
│ Azure   │ │ AWS S3  │ │ Application      │
│ MySQL   │ │ Storage │ │ Insights         │
└─────────┘ └─────────┘ └──────────────────┘
</pre>

</div>

---

<h2>☁️ Cloud Services</h2>

<table>
<thead>
<tr>
<th>Service</th>
<th>Purpose</th>
</tr>
</thead>

<tbody>

<tr>
<td><strong>🔷 Azure App Service</strong></td>
<td>Hosts and runs the Flask StudySync application.</td>
</tr>

<tr>
<td><strong>🗄️ Azure Database for MySQL</strong></td>
<td>Stores structured application data such as assignments and subjects.</td>
</tr>

<tr>
<td><strong>📊 Azure Application Insights</strong></td>
<td>Monitors requests, errors, performance and telemetry.</td>
</tr>

<tr>
<td><strong>🪣 Amazon S3</strong></td>
<td>Provides private object storage for uploaded academic files.</td>
</tr>

<tr>
<td><strong>☁️ Cloudflare Worker</strong></td>
<td>Acts as the public edge and reverse-proxy layer.</td>
</tr>

</tbody>
</table>

---

<h2>🧰 Technology Stack</h2>

<div align="center">

<table>

<tr>
<th>Layer</th>
<th>Technology</th>
</tr>

<tr>
<td>Programming Language</td>
<td>Python</td>
</tr>

<tr>
<td>Web Framework</td>
<td>Flask</td>
</tr>

<tr>
<td>ORM</td>
<td>Flask-SQLAlchemy</td>
</tr>

<tr>
<td>Database Driver</td>
<td>PyMySQL</td>
</tr>

<tr>
<td>Database</td>
<td>Azure Database for MySQL</td>
</tr>

<tr>
<td>File Storage</td>
<td>Amazon S3</td>
</tr>

<tr>
<td>AWS SDK</td>
<td>Boto3</td>
</tr>

<tr>
<td>Frontend</td>
<td>HTML / CSS</td>
</tr>

<tr>
<td>Hosting</td>
<td>Azure App Service</td>
</tr>

<tr>
<td>Monitoring</td>
<td>Azure Application Insights</td>
</tr>

<tr>
<td>Edge Layer</td>
<td>Cloudflare Workers</td>
</tr>

<tr>
<td>Version Control</td>
<td>Git / GitHub</td>
</tr>

</table>

</div>

---

<h2>🔄 Request Flow</h2>

<div align="center">

<table>

<tr>

<td align="center">
<strong>01</strong>
<br><br>
<strong>User</strong>
<br>
Opens StudySync
</td>

<td>→</td>

<td align="center">
<strong>02</strong>
<br><br>
<strong>Cloudflare</strong>
<br>
Receives request
</td>

<td>→</td>

<td align="center">
<strong>03</strong>
<br><br>
<strong>Azure</strong>
<br>
Runs Flask app
</td>

<td>→</td>

<td align="center">
<strong>04</strong>
<br><br>
<strong>MySQL / S3</strong>
<br>
Data operations
</td>

<td>→</td>

<td align="center">
<strong>05</strong>
<br><br>
<strong>Insights</strong>
<br>
Monitors app
</td>

<td>→</td>

<td align="center">
<strong>06</strong>
<br><br>
<strong>Response</strong>
<br>
Returns to user
</td>

</tr>

</table>

</div>

---

<h2>📁 Project Structure</h2>

<pre>
StudySync/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── _sidebar.html
│   ├── assignments.html
│   ├── edit_assignment.html
│   ├── files.html
│   ├── index.html
│   ├── settings.html
│   ├── subject_assignments.html
│   └── subjects.html
│
├── uploads/
├── certs/
├── app.py
├── README.md
├── requirements.txt
├── schema.sql
├── .gitignore
└── .env
</pre>

<blockquote>
<strong>🔒 Security:</strong> Sensitive files such as <code>.env</code>,
database credentials, AWS credentials, certificates and uploaded files
are excluded from the Git repository.
</blockquote>

---

<h2>🗄️ Database</h2>

<p>
StudySync uses <strong>Azure Database for MySQL Flexible Server</strong>
for structured application data.
</p>

<div align="center">

<pre>
Flask Application
       │
       ▼
Flask-SQLAlchemy
       │
       ▼
     PyMySQL
       │
       ▼
Azure Database for MySQL
</pre>

</div>

---

<h2>🪣 AWS S3 File Storage</h2>

<p>
Uploaded files are stored in a private Amazon S3 bucket instead of relying
on local application storage.
</p>

<div align="center">

<pre>
Student
   │
   ▼
StudySync Flask App
   │
   ▼
Boto3 / AWS SDK
   │
   ▼
Amazon S3
   │
   ▼
Private Object Storage
</pre>

</div>

<p>
<strong>Bucket:</strong> <code>studysync-kuunalmistry-files</code>
<br>
<strong>Region:</strong> <code>ap-south-1</code> — Mumbai
</p>

---

<h2>☁️ Cloudflare Worker</h2>

<p>
The Cloudflare Worker acts as the public entry point for StudySync and
forwards incoming requests to the Azure App Service origin.
</p>

<div align="center">

<pre>
Internet
   │
   ▼
Cloudflare Worker
   │
   │ HTTPS
   ▼
Azure App Service
   │
   ▼
Flask Application
</pre>

</div>

---

<h2>📊 Application Monitoring</h2>

<p>
<strong>Azure Application Insights</strong> provides application
observability and diagnostics.
</p>

<div align="center">

<table>
<tr>

<td align="center">
📡
<br>
<strong>Requests</strong>
</td>

<td align="center">
⚡
<br>
<strong>Performance</strong>
</td>

<td align="center">
⚠️
<br>
<strong>Errors</strong>
</td>

<td align="center">
📋
<br>
<strong>Telemetry</strong>
</td>

</tr>
</table>

</div>

---

<h2>🔐 Security</h2>

<p>
Sensitive configuration is stored through environment variables rather than
being hard-coded into the application.
</p>

<pre>
DB_HOST
DB_NAME
DB_PORT
DB_PASSWORD

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
S3_BUCKET_NAME
</pre>

<ul>
<li><code>.env</code> is excluded from Git.</li>
<li>Database certificates are excluded.</li>
<li>Uploaded files are excluded.</li>
<li>Python cache files are excluded.</li>
<li>Cloud credentials are never hard-coded into the application.</li>
</ul>

---

<h2>🧪 Testing</h2>

<table>

<tr>
<th>Component</th>
<th>Tests Performed</th>
</tr>

<tr>
<td><strong>Azure MySQL</strong></td>
<td>Connection, table creation, assignment creation and deletion.</td>
</tr>

<tr>
<td><strong>AWS S3</strong></td>
<td>Upload, download, delete and object verification.</td>
</tr>

<tr>
<td><strong>Azure App Service</strong></td>
<td>Deployment, startup and production access.</td>
</tr>

<tr>
<td><strong>Cloudflare Worker</strong></td>
<td>Request forwarding, static assets and live application access.</td>
</tr>

<tr>
<td><strong>Application Insights</strong></td>
<td>Requests, response times and failed-request monitoring.</td>
</tr>

</table>

---

<h2>🚀 Deployment</h2>

<div align="center">

<table>

<tr>

<td align="center">
<h3>☁️ Cloudflare</h3>
Worker
<br>
Edge / Reverse Proxy
</td>

<td>→</td>

<td align="center">
<h3>🔷 Azure</h3>
App Service
<br>
Flask Application
</td>

<td>→</td>

<td align="center">
<h3>🗄️ Data Layer</h3>
Azure MySQL
<br>
AWS S3
</td>

</tr>

</table>

</div>

---

<h2>💻 Local Development</h2>

<h3>1. Clone the repository</h3>

<pre>
git clone https://github.com/kuunalmistry/StudySync.git
</pre>

<h3>2. Enter the project</h3>

<pre>
cd StudySync
</pre>

<h3>3. Install dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<h3>4. Configure environment variables</h3>

<pre>
DB_HOST=your-database-host
DB_NAME=student_manager
DB_PORT=3306
DB_PASSWORD=your-password

AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=studysync-kuunalmistry-files
</pre>

<h3>5. Run the application</h3>

<pre>
python app.py
</pre>

<h3>6. Open in browser</h3>

<pre>
http://127.0.0.1:5000
</pre>

<blockquote>
<strong>Note:</strong> Production uses Azure MySQL. If the Azure MySQL
server is stopped, the production application cannot connect to its database
until the server is started again.
</blockquote>

---

<h2>📋 Project Information</h2>

<table>

<tr>
<td><strong>Project</strong></td>
<td>StudySync</td>
</tr>

<tr>
<td><strong>Developer</strong></td>
<td>Kuunal Mistry</td>
</tr>

<tr>
<td><strong>App ID</strong></td>
<td>2410130</td>
</tr>

<tr>
<td><strong>Course</strong></td>
<td>Cloud Application Development</td>
</tr>

<tr>
<td><strong>Backend</strong></td>
<td>Python + Flask</td>
</tr>

<tr>
<td><strong>Database</strong></td>
<td>Azure Database for MySQL</td>
</tr>

<tr>
<td><strong>File Storage</strong></td>
<td>Amazon S3</td>
</tr>

<tr>
<td><strong>Hosting</strong></td>
<td>Azure App Service</td>
</tr>

<tr>
<td><strong>Monitoring</strong></td>
<td>Azure Application Insights</td>
</tr>

<tr>
<td><strong>Edge Layer</strong></td>
<td>Cloudflare Worker</td>
</tr>

<tr>
<td><strong>Version Control</strong></td>
<td>Git + GitHub</td>
</tr>

</table>

---

<h2>🎯 Project Objectives</h2>

<div align="center">

<table>

<tr>

<td align="center" width="25%">
<h3>📚</h3>
<strong>Manage</strong>
<br>
Assignments & Subjects
</td>

<td align="center" width="25%">
<h3>☁️</h3>
<strong>Deploy</strong>
<br>
Cloud Application
</td>

<td align="center" width="25%">
<h3>📂</h3>
<strong>Store</strong>
<br>
Academic Files
</td>

<td align="center" width="25%">
<h3>📊</h3>
<strong>Monitor</strong>
<br>
Application Performance
</td>

</tr>

</table>

</div>

---

<h2>📸 Screenshots</h2>

<p>
Add project screenshots here.
</p>

<table>

<tr>

<td align="center" width="50%">

<strong>StudySync Dashboard</strong>

<br><br>

<!-- Add dashboard screenshot here -->

</td>

<td align="center" width="50%">

<strong>Assignment Management</strong>

<br><br>

<!-- Add assignment screenshot here -->

</td>

</tr>

<tr>

<td align="center">

<strong>File Management</strong>

<br><br>

<!-- Add file screenshot here -->

</td>

<td align="center">

<strong>Cloud Infrastructure</strong>

<br><br>

<!-- Add cloud screenshot here -->

</td>

</tr>

</table>

---

<h2>🌟 Highlights</h2>

<div align="center">

<table>

<tr>

<td align="center">
<h3>☁️</h3>
<strong>Multi-Cloud</strong>
<br>
Azure + AWS + Cloudflare
</td>

<td align="center">
<h3>🗄️</h3>
<strong>Managed Database</strong>
<br>
Azure MySQL
</td>

<td align="center">
<h3>🪣</h3>
<strong>Cloud Storage</strong>
<br>
Amazon S3
</td>

<td align="center">
<h3>📊</h3>
<strong>Monitoring</strong>
<br>
Application Insights
</td>

</tr>

</table>

</div>

---

<h2>🔗 Links</h2>

<ul>

<li>
<strong>Live Application:</strong>
<a href="https://studysync.kuunalmistry.workers.dev">
https://studysync.kuunalmistry.workers.dev
</a>
</li>

<li>
<strong>GitHub Repository:</strong>
<a href="https://github.com/kuunalmistry/StudySync">
https://github.com/kuunalmistry/StudySync
</a>
</li>

</ul>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:06B6D4,50:2563EB,100:0F172A&height=120&section=footer" width="100%" alt="Footer">

<h3>🎓 StudySync</h3>

<p>
Cloud-Based Student Assignment & Notes Management System
</p>

<p>
<strong>Built by Kuunal Mistry</strong>
</p>

</div>
