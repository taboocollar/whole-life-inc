# Video Computer Analyzer

A Python module + REST API that extracts frames from short videos (≤60 s) and uses **OpenAI Vision (GPT-4o)** to identify every computer visible in the footage, read or infer hardware specs, and produce a structured evaluation report covering:

* Current specs of each computer found
* Whether each machine meets your stated workload requirements
* Itemised upgrade plan with estimated USD cost ranges
* Future-proofing score and overall buy/upgrade/replace recommendation

---

## How It Works

```
video file
    │
    ▼
FrameExtractor        – samples 1 frame/sec (max 60 frames)
    │
    ▼
ComputerAnalyzer      – sends frames to GPT-4o Vision; returns structured JSON
    │                   with id, type, visible_specs, confidence, notes
    ▼
ReportGenerator       – sends specs to GPT-4o; generates plain-text evaluation
                        report with upgrade plans and cost estimates
```

---

## Quick Start

### 1 – Install dependencies

```bash
pip install -r requirements.txt
```

### 2 – Set your OpenAI API key

```bash
export OPENAI_API_KEY="sk-..."
```

### 3 – Use as a Python library

```python
from video_analyzer import FrameExtractor, ComputerAnalyzer, ReportGenerator

frames   = FrameExtractor().extract_frames("my_computers.mp4")
analysis = ComputerAnalyzer().analyze_frames(
    frames,
    user_needs="4K video editing, running 3 VMs simultaneously"
)
report   = ReportGenerator().generate_report(analysis, user_needs="4K video editing, running 3 VMs simultaneously")
print(report.full_text)
```

### 4 – Run the API server

```bash
uvicorn video_analyzer.server:app --reload --port 8000
```

The server exposes two endpoints:

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/health` | Liveness check |
| `POST` | `/analyze-video` | Upload video + optional `user_needs` string |

Interactive docs: <http://localhost:8000/docs>

---

## ChatGPT Integration (Custom GPT / Project Tool)

You can add this server as a **custom action** in a ChatGPT GPT so that ChatGPT can call the API directly.

### Option A – GPT Builder (recommended)

1. Deploy the server publicly (e.g. Railway, Render, or any VPS).
2. Open **ChatGPT → Explore GPTs → Create → Configure → Add actions**.
3. In the *Schema* field, paste the contents of [`chatgpt_tool_schema.json`](chatgpt_tool_schema.json) – replacing `YOUR_SERVER_HOSTNAME` with your actual domain.
4. Save and test by asking: *"Analyse this video of my computers and tell me if they're good enough for video editing."*

### Option B – ChatGPT Projects file

1. Open your ChatGPT **Project**.
2. Upload `chatgpt_tool_schema.json` as a project file.
3. In the project system prompt, instruct the assistant to use the schema to call the analysis API.

### Option C – Local use with ngrok

```bash
# start the server
uvicorn video_analyzer.server:app --port 8000

# expose it publicly
ngrok http 8000
```

Copy the ngrok URL into `chatgpt_tool_schema.json` → `servers[0].url`.

---

## Configuration

| Environment variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `MAX_VIDEO_DURATION` | `60` | Maximum accepted video length in seconds |

---

## Running Tests

```bash
python -m pytest tests/test_video_analyzer/ -v
```

---

## Module Reference

### `FrameExtractor`

```python
FrameExtractor(max_duration=60, frames_per_second=1)
extractor.extract_frames(video_path: str) -> List[VideoFrame]
```

### `ComputerAnalyzer`

```python
ComputerAnalyzer(api_key=None, model="gpt-4o")
analyzer.analyze_frames(frames, user_needs=None) -> AnalysisResult
```

### `ReportGenerator`

```python
ReportGenerator(api_key=None, model="gpt-4o")
generator.generate_report(analysis, user_needs=None) -> EvaluationReport
```
