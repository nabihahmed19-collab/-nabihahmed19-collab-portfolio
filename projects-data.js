const CATEGORIES = [
  {
    "key": "ml",
    "label": "Machine Learning"
  },
  {
    "key": "dl",
    "label": "Deep Learning"
  },
  {
    "key": "data",
    "label": "Data Analysis with Python"
  },
  {
    "key": "genai",
    "label": "Gen AI"
  },
  {
    "key": "auto",
    "label": "Automation"
  }
];

const PROJECTS = [
  {
    slug: "multi-store-inventory-reallocation",
    title: "Multi-Store Inventory Reallocation System",
    cat: "auto",
    status: "Completed",
    summary: "An Excel system using SUMIFS and INDEX-MATCH logic to catch and correct a double-allocation bug across store inventories.",
    metric: "27 verified transfers reconciled",
    tags: ["Excel", "SUMIFS", "INDEX-MATCH"],
    chart: {"type": "bar", "value": 100, "caption": "27/27 transfers verified"},
  },
  {
    slug: "garment-worker-productivity",
    title: "Garment Worker Productivity Classifier",
    cat: "ml",
    status: "Completed",
    summary: "Cleaned a real garment factory dataset and trained classifiers to predict whether a team hits its productivity target.",
    metric: "90% F1 score \u00b7 83% Random Forest OOB",
    tags: ["Python", "pandas", "scikit-learn", "Random Forest"],
    chart: {"type": "bar", "value": 90, "caption": "90% F1 score"},
  },
  {
    slug: "fandango-ratings-comparison",
    title: "Fandango Ratings: Before vs. After",
    cat: "data",
    status: "Completed",
    summary: "Compared Fandango's movie rating distributions before and after public criticism that the site was inflating scores.",
    metric: "Mean, median & mode compared across 2 years",
    tags: ["Python", "pandas", "matplotlib"],
  },
  {
    slug: "lora-finetuning-yoda",
    title: "LoRA Fine-Tuning of LFM2-1.2B",
    cat: "genai",
    status: "Completed",
    summary: "Fine-tuned LiquidAI's LFM2-1.2B with LoRA to consistently respond in Yoda's speech pattern, as an MIT (6.S191) course project.",
    metric: "Style-adherence score: 0.00 \u2192 0.61",
    tags: ["LoRA", "PEFT", "Hugging Face"],
    chart: {"type": "compare", "values": [0, 61], "labels": ["Before", "After"], "caption": "Style-adherence score"},
  },
  {
    slug: "cnn-age-gender-ethnicity",
    title: "Multi-Output CNN: Age, Gender & Ethnicity",
    cat: "dl",
    status: "Completed",
    summary: "A multi-output ResNet50 trained on UTKFace to predict age, gender, and ethnicity from a single face image.",
    metric: "90.9% gender accuracy \u00b7 \u00b16.6 yr age MAE",
    tags: ["ResNet50", "Computer Vision", "Multi-task Learning"],
    chart: {"type": "bar", "value": 91, "caption": "90.9% gender accuracy"},
  },
  {
    slug: "oral-cancer-cnn-fyp",
    title: "Oral Cancer Detection (CNN) \u2014 Final Year Project",
    cat: "dl",
    status: "In progress",
    summary: "A CNN classifying oral lesion images as benign or malignant, with a Streamlit interface built for clinicians.",
    metric: "Binary classification \u00b7 Streamlit demo",
    tags: ["CNN", "TensorFlow/PyTorch", "Streamlit", "Medical Imaging"],
  },
  {
    slug: "maazmail",
    title: "MaazMail",
    cat: "genai",
    status: "In testing",
    summary: "A cold email outreach SaaS built end to end with a collaborator \u2014 campaigns, contacts, and real Gmail sending.",
    metric: "Full stack: FastAPI + React + PostgreSQL + Groq",
    tags: ["FastAPI", "React", "PostgreSQL", "Groq"],
  },
  {
    slug: "querio",
    title: "Querio",
    cat: "genai",
    status: "Live",
    summary: "An agentic text-to-SQL system \u2014 describe what you want in plain English, and it writes and runs the query.",
    metric: "Deployed on Hugging Face Spaces",
    tags: ["Pydantic-AI", "Gradio", "Text-to-SQL"],
  },
  {
    slug: "ai-support-triage-agent",
    title: "AI Customer Support Triage Agent",
    cat: "genai",
    status: "Live",
    summary: "My first AI project \u2014 an agent that reads incoming support queries and routes them by urgency and topic.",
    metric: "Publicly launched on Hugging Face Spaces",
    tags: ["LLM Agents", "Hugging Face"],
  },
  {
    slug: "amazon-seller-lead-scraper",
    title: "Amazon Seller Lead Scraper",
    cat: "auto",
    status: "Completed",
    summary: "A Selenium-based scraper that pulls Amazon seller leads and exports them straight to Excel for outreach.",
    metric: "End-to-end automated export pipeline",
    tags: ["Selenium", "Python", "Excel"],
  },
  {
    slug: "offline-rag-chatbot",
    title: "Offline RAG Chatbot for Legal Documents",
    cat: "genai",
    status: "Completed",
    summary: "A fully offline retrieval-augmented chatbot that answers questions from legal PDFs, DOCX, and TXT files.",
    metric: "100% offline, zero external API calls",
    tags: ["RAG", "Local LLM", "Document Q&A"],
    chart: {"type": "bar", "value": 100, "caption": "0 external API calls"},
  },
];