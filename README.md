# 🌿 PlantCare AI — Smart Plant Identification & Care Assistant

PlantCare AI is an AI-powered web application built using **Python, Streamlit, and Groq API**. It helps users identify plants from images, understand plant diseases, learn balcony gardening techniques, ask plant-related questions, and explore estimated plant prices.

The application supports different types of plants, including vegetables, flowers, herbs, grasses, indoor plants, and trees.

## ✨ Features

### 1. 🔎 Plant Identification
- Upload an image of a plant.
- Identify its possible common and scientific names.
- Learn about plant characteristics and properties.
- Explore its origin, natural distribution, and growing regions.
- Understand its life cycle and approximate mature height.
- Learn about common pests and diseases.
- Get information about potential uses and edibility, with appropriate safety warnings.
- Download the generated plant report.

### 2. 🌍 Multilingual Support
- Select your preferred output language.
- Receive plant information in languages such as English, Kannada, Hindi, Marathi, Tamil, Telugu, and others.
- View plant names and care instructions in the selected language.

*Note: AI-generated translations may not always use the correct local botanical name.*

### 3. 🩺 Plant Disease Doctor
- Upload an image of an affected leaf, stem, root, flower, fruit, or whole plant.
- Analyze visible symptoms.
- Explore possible diseases and alternative causes.
- Learn about possible environmental, pest-related, nutritional, and watering problems.
- Receive preliminary treatment, prevention, and plant-care recommendations.
- Download the generated plant health report.

### 4. 🪴 Balcony Gardening Assistant
- Create a gardening plan based on available space and sunlight.
- Explore suitable plants for balconies, terraces, and windowsills.
- Get advice about soil, pots, drainage, watering, and fertilizers.
- Receive a simple plant-care routine.
- Learn how to grow vegetables, herbs, flowers, fruits, and indoor plants at home.

### 5. 💬 Plant Chatbot
- Ask questions about plants and gardening.
- Get assistance with watering, sunlight, soil, plant diseases, and plant maintenance.
- Ask how to use the PlantCare AI website.
- Continue conversations with contextual follow-up questions.

### 6. 🛒 Plant Price Guide
- Explore indicative price ranges for different plant categories.
- Compare example prices for seedlings, herbs, flowers, indoor plants, fruit saplings, and more.
- Learn what to inspect before purchasing a plant.
- Get practical buying and maintenance advice.

**Note:** The current price guide uses sample estimates, not verified live market prices or actual seller listings.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and backend processing |
| Streamlit | Interactive web interface |
| Groq API | AI-powered text generation and image analysis |
| Qwen vision model | Plant image identification and preliminary disease analysis |
| GPT-OSS text model | Chatbot and gardening recommendations |
| Pillow (PIL) | Image processing and resizing |
| TOML | Secure local API key configuration |

## 📁 Project Structure

```text
PlantCareAI/
│
├── app.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

- `app.py` — Main Streamlit application.
- `requirements.txt` — Python dependencies.
- `README.md` — Project documentation.
- `.streamlit/secrets.toml` — Local Groq API key configuration.

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible newer version.
- Visual Studio Code or another Python editor.
- Internet connection.
- Groq API key.

### Step 1: Clone or download the project

If your project is hosted on GitHub:

```bash
git clone YOUR_REPOSITORY_URL
cd PlantCareAI
```

Alternatively, open your existing project folder in VS Code.

### Step 2: Install dependencies

Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

If the requirements file has not been created, add:

```text
streamlit
groq
Pillow
```

### Step 3: Configure the Groq API key

Create the following file:

`.streamlit/secrets.toml`

Add your API key:

```toml
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

Replace the placeholder with your actual key.

Get your API key from the [Groq Console](https://console.groq.com/keys).

**Security:** Never commit your real API key to a public repository.

### Step 4: Configure the AI models

The application currently uses these model identifiers in `app.py`:

```python
VISION_MODEL = "qwen/qwen3.8-27b"
TEXT_MODEL = "openai/gpt-oss-120b"
```

Check the [Groq Models documentation](https://console.groq.com/docs/models) if a model becomes unavailable or your account does not have access to it.

### Step 5: Run the application

Execute:

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser to use PlantCare AI.

## 🚀 How to Use PlantCare AI

1. Open the website in your browser.
2. Choose a feature from the sidebar.
3. Select your preferred output language.
4. Upload a plant image or enter the requested information.
5. Click the appropriate analysis or generation button.
6. Read the results and download reports when available.
7. Use the chatbot for additional questions.

## 🔐 Security

- Keep your Groq API key in `.streamlit/secrets.toml`.
- Do not share API keys in screenshots, public repositories, or source code.
- Add the following entries to your `.gitignore` file:

```gitignore
.streamlit/secrets.toml
__pycache__/
.venv/
venv/
.env
```

If you deploy the application, configure the API key using the deployment platform's secrets-management feature.

## ⚠️ Limitations and Safety

- Plant identification can be incorrect, particularly when species have similar appearances.
- Disease analysis is a preliminary AI assessment, not a confirmed diagnosis.
- Plant images alone cannot establish whether a plant is safe to eat.
- Consult a qualified horticulture expert for serious or spreading plant problems.
- Follow pesticide and fertilizer labels; never mix chemicals without verified instructions.
- Price estimates are illustrative and are not connected to live nursery inventories.
- AI responses and translations may contain inaccuracies.
- Groq rate limits may restrict the number or size of requests.

## 🔮 Future Enhancements

Potential improvements include:

- Live plant prices and nursery listings.
- Plant purchase links and seller information.
- A database for saving plant reports and user preferences.
- Plant growth tracking and care reminders.
- Location-based plant recommendations.
- Weather-aware watering suggestions.
- More reliable disease classification using validated plant-disease datasets.
- User accounts and personalized gardens.
- A dedicated plant encyclopedia with verified botanical sources.

## 🎯 Project Objective

The main objective of PlantCare AI is to make plant knowledge accessible to everyone by combining artificial intelligence with practical gardening guidance. The application aims to help users identify plants, understand possible plant-health problems, and grow plants successfully at home, especially in balconies and small spaces.

## 👩‍💻 Project Information

**Project Name:** PlantCare AI  
**Category:** Artificial Intelligence / Web Application  
**Domain:** Plant Identification, Plant Health, and Smart Gardening  
**Frontend:** Streamlit  
**Programming Language:** Python  
**AI Integration:** Groq API

---

*PlantCare AI — Learn. Grow. Protect. 🌿*
