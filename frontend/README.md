# Todo Frontend

A React frontend for the Todo application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000` and will proxy API requests to the FastAPI backend at `http://localhost:8000`.

## Features

- User authentication (Login/Register)
- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- Modern, responsive UI
- Protected routes

## API Integration

The frontend expects the FastAPI backend to be running on `http://localhost:8000` with the following endpoints:

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/todos` - Get all todos (requires auth)
- `POST /api/v1/todos` - Create a todo (requires auth)
- `PATCH /api/v1/todos/{id}` - Update a todo (requires auth)
- `DELETE /api/v1/todos/{id}` - Delete a todo (requires auth)





