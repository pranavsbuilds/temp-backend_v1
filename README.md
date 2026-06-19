# Smart Interviewer Backend ⚙️

Hey everyone, this is the FastAPI backend for the Smart Interview platform. It's the engine that powers the whole interview flow.

## What does this do?

Basically, we handle all the heavy lifting here:
- Grabbing technical questions from [QuizAPI](https://quizapi.io). (If we run out or the API tanks, we fall back to our local mock pool).
- Real-time Speech-to-Text (STT) using Vosk over WebSockets.
- Evaluating the candidate's answers using SBERT (Semantic Textual Similarity).
- Running KMeans to cluster their performance results so we can give them decent feedback.

## Setup & Running Locally

Make sure you have Python 3.8+ and that the Vosk model is downloaded and sitting in the right directory.

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Env Vars:**
   Check `Enviornment_Variable.env` and make sure your `QUIZ_API_KEY` is set. The app hits QuizAPI.io directly, so you'll need this.

3. **Spin it up:**
   ```bash
   uvicorn main:app --reload
   ```

## Development Notes
- **Important Workflow Rule:** Please don't edit the base `backend/` directory directly. Any changes you want to make should happen right here in this `backend_v1/` folder.
- If you're testing the WebSocket STT locally without the Vosk model, it'll run in a simulation fallback mode—just check the terminal logs if you aren't sure.

Holler if the clustering gets weird or if you need help tweaking the SBERT scoring thresholds!
