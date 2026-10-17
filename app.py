import base64
import io
import streamlit as st
from groq import Groq
from PIL import Image

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f4fbf3, #edf7ee);
}

[data-testid="stSidebar"] {
    background: #123d2b;
}

/* Sidebar text */
[data-testid="stSidebar"] {
    background: #123d2b;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Language dropdown text */
[data-testid="stSidebar"] [data-testid="stSelectbox"] div,
[data-testid="stSidebar"] [data-testid="stSelectbox"] input {
    color: #123d2b !important;
}

/* Dropdown options */
[data-testid="stPopover"] {
    color: #123d2b !important;
}

.hero {
    padding: 32px 24px;
    background: linear-gradient(120deg, #124b32, #398653);
    border-radius: 22px;
    color: white;
    text-align: center;
    margin-bottom: 24px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 17px;
}

div.stButton > button {
    background: #237447;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 18px;
}

div.stButton > button:hover {
    background: #155631;
    color: white;
    border: none;
}

[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dcebdc;
}

h1, h2, h3 {
    color: #174b30;
}

.plant-note {
    background: #e1f1e2;
    padding: 15px;
    border-radius: 12px;
    color: #19482b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- API SETTINGS ----------------
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = ""

# Change these IDs in one place if Groq changes availability.
VISION_MODEL = "qwen/qwen3.8-27b"
TEXT_MODEL =  "openai/gpt-oss-120b"

if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    client = None

# ---------------- HELPER FUNCTIONS ----------------
def ask_text_ai(prompt, history=None):
    """Ask Groq a text-based question."""
    if not client:
        return "Please configure GROQ_API_KEY in .streamlit/secrets.toml."

    messages = [
        {
            "role": "system",
            "content": (
                "You are PlantCare AI, a helpful botanical and gardening "
                "assistant. Give clear, structured, practical answers. "
                "Distinguish established facts from uncertain estimates. "
                "Never claim certainty when evidence is insufficient. "
                "For plant edibility, warn users not to eat plants based "
                "only on AI identification. For plant diseases, mention "
                "when expert inspection may be needed. Answer in the "
                "language requested by the user."
            )
        }
    ]

    if history:
        messages.extend(history[-12:])

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=TEXT_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=1800
    )
    return response.choices[0].message.content


def analyze_plant_image(image, task, language):
    """Send an uploaded image to Groq's vision model."""
    if not client:
        return "Please configure GROQ_API_KEY in .streamlit/secrets.toml."

    # Resize large photos and convert them into a supported format.
    picture = image.convert("RGB")
    picture.thumbnail((1200, 1200))

    buffer = io.BytesIO()
    picture.save(buffer, format="JPEG", quality=85)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

    if task == "identify":
        instructions = f"""
Examine this image to identify the plant.

Write your answer in {language}.

Use these headings:
1. Common name
2. Scientific name
3. Other names, if known
4. Plant category: vegetable, fruit, flower, herb, grass, tree,
   indoor plant, or other
5. Identification confidence and visual evidence
6. Physical properties and characteristics
7. Is it edible? State uncertainty and possible toxicity clearly.
8. Approximate height at maturity
9. Life cycle: annual, biennial, perennial, or unknown
10. Native origin and natural distribution
11. Climate and regions where it commonly grows
12. Traditional or practical uses, with cautions
13. Common diseases and pests
14. Balcony growing guide: sunlight, pot size, soil, drainage,
    watering, fertilizer, spacing and maintenance
15. Propagation methods
16. Special precautions

Do not invent precise facts if the plant cannot be identified.
Give the likely identification and alternatives if necessary.
Do not claim that a plant is safe to eat from the image alone.
"""
    else:
        instructions = f"""
Examine this image of a possibly diseased plant or plant part.

Write your answer in {language}.

Use these headings:
1. Visible symptoms
2. Most likely disease or problem
3. Other possible causes
4. Confidence level and limitations
5. Why it may have happened
6. Immediate steps to help the plant
7. Treatment options and precautions
8. Watering, sunlight, soil and drainage adjustments
9. Prevention and future monitoring
10. When to consult a local horticulture expert

Consider fungal, bacterial, viral, pest-related, nutritional,
watering, heat and other environmental causes where relevant.
Do not claim a definite diagnosis from a photo alone.
Do not recommend unsafe chemical mixtures or unlabelled pesticides.
If symptoms are unclear, explain what additional photos or
information would help.

Do not assume every spot or yellow leaf is an infectious disease.
"""
    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instructions},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded}"
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        max_completion_tokens=2500
    )
    return response.choices[0].message.content


def show_answer(answer):
    st.markdown(answer)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("# 🌿 PlantCare AI")
    st.caption("Your personal plant companion")

    page = st.radio(
        "Explore",
        [
            "🏡 Home",
            "🔎 Identify a Plant",
            "🩺 Plant Disease Doctor",
            "🌱 Balcony Gardening",
            "💬 Plant Chatbot",
            "🛒 Plant Price Guide",
            "ℹ️ About"
        ],
        label_visibility="visible"
    )

    st.markdown("---")
    st.markdown("### 🌍 Output language")

    language = st.selectbox(
        "Choose your preferred language",
        [
            "English",
            "Kannada",
            "Hindi",
            "Marathi",
            "Tamil",
            "Telugu",
            "Malayalam",
            "Bengali",
            "Gujarati",
            "Punjabi",
            "Urdu",
            "French",
            "Spanish"
        ],
        index=0
    )

    st.markdown("---")
    st.caption("Grow green. Live green. 🌿")


# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🌿 PlantCare AI</h1>
    <p>Identify plants • Detect plant problems • Grow your own garden</p>
    <p>Discover the world of plants, from tiny herbs to giant trees.</p>
</div>
""", unsafe_allow_html=True)

if not client:
    st.warning(
        "API key not configured. Add GROQ_API_KEY to "
        ".streamlit/secrets.toml before using AI features."
    )

# ---------------- HOME PAGE ----------------
if page == "🏡 Home":

    st.subheader("Welcome to your green world 🌱")
    st.write(
        "Discover a plant, learn how to care for it, and create "
        "your own garden at home."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔍")
        st.markdown("**Identify any plant**")
        st.write("Learn plant names, properties, uses and growing needs.")

    with col2:
        st.markdown("### 🩺")
        st.markdown("**Plant health assistant**")
        st.write("Explore possible diseases and practical care options.")

    with col3:
        st.markdown("### 🪴")
        st.markdown("**Balcony gardening**")
        st.write("Find suitable pots, soil, sunlight and watering tips.")

    st.markdown("---")
    st.subheader("What would you like to do?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔎 Identify a plant", use_container_width=True):
            st.session_state["navigate_to"] = "🔎 Identify a Plant"
            st.rerun()

        if st.button("🩺 Check plant disease", use_container_width=True):
            st.session_state["navigate_to"] = "🩺 Plant Disease Doctor"
            st.rerun()

    with col2:
        if st.button("🌱 Learn balcony gardening", use_container_width=True):
            st.session_state["navigate_to"] = "🌱 Balcony Gardening"
            st.rerun()

        if st.button("💬 Ask the chatbot", use_container_width=True):
            st.session_state["navigate_to"] = "💬 Plant Chatbot"
            st.rerun()

    st.markdown("---")
    st.info(
        "Tip: Upload a clear photo of the leaves, flowers, fruit or "
        "whole plant. Include more than one view when possible."
    )

# Handle navigation buttons on the home page.
if "navigate_to" in st.session_state:
    target = st.session_state.pop("navigate_to")
    # Streamlit's radio is controlled through its session-state key.
    st.session_state["Explore"] = target
    st.rerun()

# ---------------- IDENTIFY A PLANT ----------------
elif page == "🔎 Identify a Plant":

    st.subheader("🔎 Discover your plant")
    st.write(
        "Upload a photo of a vegetable, flower, tree, herb, grass, "
        "fruit or indoor plant."
    )

    uploaded = st.file_uploader(
        "Upload plant photo",
        type=["jpg", "jpeg", "png", "webp"],
        key="identify_upload"
    )

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="Your uploaded plant", width=420)

        if st.button("Identify this plant 🌿", key="identify_button"):
            with st.spinner("Examining your plant..."):
                try:
                    result = analyze_plant_image(
                        image, "identify", language
                    )
                    st.session_state["plant_result"] = result
                except Exception as e:
                    st.error(
                        "Could not analyze the image. Check your API key, "
                        "model availability and internet connection."
                    )
                    st.caption(str(e))

    if st.session_state.get("plant_result"):
        st.markdown("---")
        st.subheader("🌱 Plant identification report")
        show_answer(st.session_state["plant_result"])

        st.download_button(
            "Download plant report",
            data=st.session_state["plant_result"],
            file_name="plantcare_report.txt",
            mime="text/plain"
        )

# ---------------- DISEASE DETECTOR ----------------
elif page == "🩺 Plant Disease Doctor":

    st.subheader("🩺 Plant health checker")
    st.write(
        "Upload a clear photo of a diseased leaf, stem, root, flower, "
        "fruit or the whole plant."
    )

    plant_part = st.selectbox(
        "What are you uploading?",
        [
            "Leaf",
            "Stem or branch",
            "Root",
            "Flower",
            "Fruit or vegetable",
            "Whole plant",
            "Other"
        ]
    )

    symptoms = st.text_area(
        "Describe the symptoms (optional)",
        placeholder=(
            "For example: yellow leaves, brown spots, white powder, "
            "insects, wilting or slow growth."
        )
    )

    disease_upload = st.file_uploader(
        "Upload affected plant photo",
        type=["jpg", "jpeg", "png", "webp"],
        key="disease_upload"
    )

    if disease_upload:
        disease_image = Image.open(disease_upload)
        st.image(disease_image, caption="Affected plant", width=420)

        if st.button("Analyze plant health 🩺"):
            with st.spinner("Analyzing visible symptoms..."):
                try:
                    prompt_extra = (
                        f"The uploaded part is: {plant_part}. "
                        f"User-reported symptoms: {symptoms or 'Not provided'}. "
                    )
                    # Include the user context in the task prompt.
                    disease_context = (
                        prompt_extra
                        + "Write the report in " + language + "."
                    )
                    result = analyze_plant_image(
                        disease_image, "disease", language
                    )

                    # Supplement the visual analysis with reported symptoms.
                    result += "\n\n### User-reported context\n" + (
                        disease_context
                    )
                    st.session_state["disease_result"] = result

                except Exception as e:
                    st.error(
                        "Analysis failed. Check the API key and model."
                    )
                    st.caption(str(e))

    if st.session_state.get("disease_result"):
        st.markdown("---")
        st.subheader("🌿 Plant health report")
        show_answer(st.session_state["disease_result"])

        st.download_button(
            "Download disease report",
            data=st.session_state["disease_result"],
            file_name="plant_health_report.txt",
            mime="text/plain"
        )

    st.warning(
        "This is an AI-generated preliminary assessment, not a "
        "confirmed diagnosis. Avoid applying treatments until the "
        "cause is reasonably clear. Follow product labels and seek "
        "local horticulture advice for severe or spreading problems."
    )

# ---------------- BALCONY GARDENING ----------------
elif page == "🌱 Balcony Gardening":

    st.subheader("🪴 Create your balcony garden")
    st.write(
        "Get a growing plan based on your available space, sunlight "
        "and the plants you want to grow."
    )

    col1, col2 = st.columns(2)

    with col1:
        space = st.selectbox(
            "Available space",
            ["Small balcony", "Medium balcony", "Large balcony",
             "Indoor windowsill", "Terrace"]
        )

        sunlight = st.selectbox(
            "Daily direct sunlight",
            ["Less than 2 hours", "2–4 hours",
             "4–6 hours", "More than 6 hours"]
        )

        plant_type = st.selectbox(
            "What would you like to grow?",
            [
                "Vegetables",
                "Herbs",
                "Flowers",
                "Fruits",
                "Indoor plants",
                "Medicinal plants",
                "Mixed garden"
            ]
        )

    with col2:
        experience = st.selectbox(
            "Your gardening experience",
            ["Beginner", "Some experience", "Experienced"]
        )

        climate = st.selectbox(
            "Your general climate",
            ["Hot and dry", "Hot and humid", "Moderate",
             "Cool", "Not sure"]
        )

        maintenance = st.selectbox(
            "Time available for care",
            ["10 minutes daily", "20 minutes daily",
             "30+ minutes daily"]
        )

    if st.button("Create my gardening plan 🌱"):
        prompt = f"""
Create a practical balcony gardening plan in {language}.

Available space: {space}
Sunlight: {sunlight}
Preferred plants: {plant_type}
Experience: {experience}
Climate: {climate}
Daily care time: {maintenance}

Include:
1. Suitable plant examples
2. Recommended pot sizes, where appropriate
3. Potting mix and drainage
4. Watering guidance
5. Sunlight and placement
6. Fertilizer guidance
7. A simple weekly care routine
8. Common mistakes and pest prevention
9. Safety considerations for children and pets
10. A beginner-friendly shopping checklist

Avoid guaranteeing that every plant will thrive in all climates.
"""
        with st.spinner("Preparing your gardening plan..."):
            try:
                st.session_state["garden_result"] = ask_text_ai(prompt)
            except Exception as e:
                st.error(f"Could not create the plan: {e}")

    if st.session_state.get("garden_result"):
        show_answer(st.session_state["garden_result"])

# ---------------- PLANT CHATBOT ----------------
elif page == "💬 Plant Chatbot":

    st.subheader("💬 Ask PlantCare AI")
    st.write(
        "Ask about plant names, care, watering, gardening, "
        "diseases, balcony plants or how to use this website."
    )

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if st.button("Clear conversation"):
        st.session_state["chat_history"] = []
        st.rerun()

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask anything about plants or this website..."
    )

    if question:
        st.session_state["chat_history"].append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        system_context = (
            "You are PlantCare AI, a friendly plant and gardening "
            "assistant. You also explain how this Streamlit website "
            "works: Home, Identify a Plant, Plant Disease Doctor, "
            "Balcony Gardening, Plant Chatbot and Plant Price Guide. "
            "Answer in " + language + ". Be practical and concise. "
            "Do not claim that this website has live shopping, live "
            "prices or laboratory-level disease detection."
        )

        # Pass recent conversation for follow-up questions.
        history = [
            {"role": "system", "content": system_context}
        ] + st.session_state["chat_history"][-12:]

        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_text_ai(
                        question,
                        history=history[:-1]
                    )
                st.markdown(answer)

            st.session_state["chat_history"].append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error(f"Chatbot error: {e}")

# ---------------- PLANT PRICE GUIDE ----------------
elif page == "🛒 Plant Price Guide":

    st.subheader("🛒 Plant price guide")
    st.write(
        "Explore indicative example prices in Indian rupees. "
        "These are sample estimates, not live shop quotations."
    )

    price_data = {
        "Vegetable seedlings": (20, 80),
        "Herb plants": (30, 150),
        "Flowering plants": (40, 250),
        "Small indoor plants": (60, 350),
        "Fruit saplings": (100, 600),
        "Small ornamental trees": (150, 1000),
        "Large potted plants": (300, 2000),
        "Seeds packet": (20, 150)
    }

    category = st.selectbox(
        "Select a plant category",
        list(price_data.keys())
    )

    plant_name = st.text_input(
        "Specific plant name (optional)",
        placeholder="For example: rose, tulsi, tomato, aloe vera"
    )

    size = st.selectbox(
        "Preferred size",
        ["Seeds", "Small plant", "Medium plant", "Large plant"]
    )

    low, high = price_data[category]

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Example lower price", f"₹{low}")

    with col2:
        st.metric("Example upper price", f"₹{high}")

    st.caption(
        "Actual prices vary by seller, city, plant variety, pot size, "
        "season, delivery and plant health."
    )

    if st.button("Get price and buying advice"):
        prompt = f"""
In {language}, provide a cautious buying guide for:
Plant: {plant_name or category}
Category: {category}
Desired size: {size}
Example reference range: ₹{low} to ₹{high}

Explain:
- Whether the reference range is a plausible rough estimate
- Factors that affect the price
- What to inspect before buying
- Questions to ask a local nursery
- How to transport and care for the plant

Do not invent current seller listings, stock, links or verified live prices.
Explain that the reference range is illustrative and may be inaccurate
for the specific plant or location.
"""
        with st.spinner("Preparing buying advice..."):
            try:
                show_answer(ask_text_ai(prompt))
            except Exception as e:
                st.error(f"Could not get advice: {e}")

# ---------------- ABOUT PAGE ----------------
elif page == "ℹ️ About":

    st.subheader("About PlantCare AI 🌿")

    st.write("""
    PlantCare AI is a plant-learning and gardening assistant built
    with Streamlit and Groq AI.

    **Main features**
    - Plant identification from uploaded photos
    - Plant names and explanations in different languages
    - Preliminary plant disease analysis
    - Personalized balcony gardening plans
    - A conversational plant chatbot
    - An indicative plant price guide

    **Limitations**
    - AI identification can be incorrect, especially for similar species.
    - Disease analysis cannot replace laboratory testing or expert inspection.
    - Price examples are estimates and are not live market listings.
    - Plant descriptions depend on the AI model's knowledge.
    """)

    st.markdown(
        "Built with **Streamlit + Groq + Python** 🌱"
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#477454;'>"
    "🌿 PlantCare AI | Learn • Grow • Protect 🌿"
    "</div>",
    unsafe_allow_html=True
)