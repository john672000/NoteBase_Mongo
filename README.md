#NoteHub – Smart Note-Taking App with Image Upload
NoteHub is a full-stack note-taking web application that allows users to create, read, update, and delete notes, with support for uploading and storing images. Designed to demonstrate core concepts in handling relational-like data and BLOB (Binary Large Object) storage using modern web technologies.

🚀 Tech Stack
Frontend: React + Bootstrap (BS)

Backend: FastAPI (Python)

Database: MongoDB (NoSQL with relational data modeling + BLOB support)

Deployment: Render (for API hosting)

🧠 Key Features
🗒️ Create, read, update, and delete rich-text notes

🖼️ Upload and store images alongside notes

🧩 Demonstrates both relational-style data (e.g., note-user relationships) and BLOB storage (for images) in MongoDB

⚡ FastAPI backend for performant and scalable APIs

💡 Simple, responsive UI built with React and Bootstrap

📦 Architecture Highlights
MongoDB is used to handle:

Structured data through embedded documents and references (relational-style modeling)

Binary image uploads stored as BLOBs using GridFS or base64 encoding

FastAPI provides RESTful endpoints for CRUD operations and image handling

React + BS delivers a smooth frontend experience for managing notes and media

Render hosts the backend API, enabling cloud-based deployment
