def load_knowledge_base():
    kb = {}
    with open("knowledge_base.txt", "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                kb[key.strip().lower()] = value.strip()
    return kb

sections = load_knowledge_base()


def get_bot_reply(query: str, previous: list = None) -> dict:
    query = query.lower().strip()
    greetings = ["hi", "hello", "hey", "hola", "namaste"]

    # Greeting → show main buttons
    if any(g in query for g in greetings):
        return {
            "reply": "Hello! I'm Vishwas Saini's info bot. Choose what you'd like to know:",
            "options": ["INTRO", "QUALIFICATIONS", "QUALITIES", "SKILLS", "EXPERIENCE", "PROJECTS"]
        }

    # Intro → text + LinkedIn + Website
    elif query == "intro":
        return {
            "reply": sections.get("intro", "Intro not found."),
            "options": ["LINKEDIN", "WEBSITE", "MORE"]
        }

    # Qualifications, Qualities, Skills, Experience → text + MORE
    elif query in ["qualifications", "qualities", "skills", "experience"]:
        return {
            "reply": sections.get(query, f"{query.title()} not found."),
            "options": ["MORE"]
        }

    # Projects → text + Contact + GitHub, Render, Streamlit
    elif query == "projects":
        return {
            "reply": sections.get("projects", "Projects not found."),
            "options": ["CONTACT", "GITHUB", "RENDER", "STREAMLIT", "MORE"]
        }

    # Contact → text + MORE
    elif query == "contact":
        return {
            "reply": sections.get("contact", "Contact not found."),
            "options": ["MORE"]
        }

    # Links → open link + MORE
    elif query in ["linkedin", "github", "render", "streamlit", "website"]:
        links = {
            "linkedin": "https://www.linkedin.com/in/vishwassaini28",
            "github": "https://github.com/VishwasSaini28",
            "render": "https://render.com",
            "streamlit": "https://share.streamlit.io/user/vishwassaini28",
            "website": "https://your-website-url.com"  # replace with your actual site
        }
        display_name = query.title()
        return {
            "reply": f"Opening {display_name}...",
            "link": links[query],
            "options": ["MORE"]
        }

    # MORE → show main buttons again
    elif query == "more":
        return {
            "reply": "Choose another topic below:",
            "options": ["INTRO", "QUALIFICATIONS", "QUALITIES", "SKILLS", "EXPERIENCE", "PROJECTS"]
        }

    else:
        return {"reply": "Please say hi, hello, or hey to start."}
