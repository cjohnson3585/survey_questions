# FastAPI Survey Application

This project is a simple FastAPI application that serves a landing page with a survey form. Users can submit their responses to three survey questions, along with an optional email address. The application includes a timeout cookie to prevent multiple submissions in a short period.

## Project Structure

```
fastapi-survey-app
├── app
│   ├── main.py          # Entry point of the FastAPI application
│   ├── templates
│   │   └── index.html   # HTML template for the landing page
│   └── static
│       └── style.css    # CSS styles for the landing page
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi-survey-app
   ```

2. **Install the required dependencies:**
   Create a virtual environment and activate it, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000`.

## Usage

- Fill out the survey questions on the landing page.
- Optionally provide your email address.
- Click the submit button to send your responses.
- The application will handle the submission and send the responses to the specified email address.

## License

This project is licensed under the MIT License.