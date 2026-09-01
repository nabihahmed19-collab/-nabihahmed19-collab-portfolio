# -*- coding: utf-8 -*-
"""
Single source of truth for all project content.
Generates:
  1. projects-data.js  (used by the homepage grid)
  2. one static .html detail page per project
Run this whenever project content changes, then re-upload the
output files. Nabiha does not need to run this herself day-to-day —
for small edits she can hand-edit the generated files directly.
"""
import json
import os

CATS = {
    "ml":    {"label": "Machine Learning",           "var": "--cat-ml",
              "icon": '<circle cx="8" cy="2.6" r="1.3"/><line x1="8" y1="3.9" x2="8" y2="6"/><line x1="8" y1="6" x2="3.6" y2="9"/><line x1="8" y1="6" x2="12.4" y2="9"/><circle cx="3.6" cy="10.3" r="1.3"/><circle cx="12.4" cy="10.3" r="1.3"/>'},
    "dl":    {"label": "Deep Learning",               "var": "--cat-dl",
              "icon": '<circle cx="3" cy="4" r="1.2"/><circle cx="3" cy="12" r="1.2"/><circle cx="8" cy="8" r="1.2"/><circle cx="13" cy="4" r="1.2"/><circle cx="13" cy="12" r="1.2"/><line x1="3" y1="4" x2="8" y2="8"/><line x1="3" y1="12" x2="8" y2="8"/><line x1="13" y1="4" x2="8" y2="8"/><line x1="13" y1="12" x2="8" y2="8"/>'},
    "data":  {"label": "Data Analysis with Python",   "var": "--cat-data",
              "icon": '<rect x="1.5" y="8" width="3" height="6" rx="0.5"/><rect x="6.5" y="3.5" width="3" height="10.5" rx="0.5"/><rect x="11.5" y="6" width="3" height="8" rx="0.5"/>'},
    "genai": {"label": "Gen AI",                      "var": "--cat-genai",
              "icon": '<path d="M8 1.3 L9.4 6.3 L14.4 7.7 L9.4 9.1 L8 14.1 L6.6 9.1 L1.6 7.7 L6.6 6.3 Z"/>'},
    "auto":  {"label": "Automation",                  "var": "--cat-auto",
              "icon": '<path d="M3 8a5 5 0 0 1 8.6-3.5" fill="none"/><path d="M13 8a5 5 0 0 1-8.6 3.5" fill="none"/><path d="M11.6 2.5v2.5h-2.5" fill="none"/><path d="M4.4 13.5v-2.5h2.5" fill="none"/>'},
}

CATEGORY_ORDER = ["ml", "dl", "data", "genai", "auto"]

PROJECTS = [
    {
        "slug": "multi-store-inventory-reallocation",
        "title": "Multi-Store Inventory Reallocation System",
        "cat": "auto",
        "status": "Completed",
        "summary": "An Excel system using SUMIFS and INDEX-MATCH logic to catch and correct a double-allocation bug across store inventories.",
        "metric": "27 verified transfers reconciled",
        "chart": {"type": "bar", "value": 100, "caption": "27/27 transfers verified"},
        "tags": ["Excel", "SUMIFS", "INDEX-MATCH"],
        "context": "A multi-store retail operation was reallocating stock between locations, with the whole process tracked and reconciled in a single shared Excel workbook.",
        "problem": "The existing SUMIFS-based reallocation formula was silently double-counting some stock transfers between stores. Inventory levels looked reconciled on the surface, but the underlying numbers were wrong — the kind of bug that can sit unnoticed in a spreadsheet for a long time because nothing throws an error.",
        "skills": ["Excel", "SUMIFS", "INDEX-MATCH", "Formula auditing", "Manual verification"],
        "approach": "Traced the double-count to how the SUMIFS logic handled overlapping conditions across stores, then rebuilt the reallocation logic by combining SUMIFS with INDEX-MATCH so the same transfer couldn't be counted twice.",
        "result": "27 affected transfers were verified by hand against the corrected logic before the fix was rolled out — every single one confirmed correct, not just spot-checked.",
        "links": [],
    },
    {
        "slug": "garment-worker-productivity",
        "title": "Garment Worker Productivity Classifier",
        "cat": "ml",
        "status": "Completed",
        "summary": "Cleaned a real garment factory dataset and trained classifiers to predict whether a team hits its productivity target.",
        "metric": "90% F1 score · 83% Random Forest OOB",
        "chart": {"type": "bar", "value": 90, "caption": "90% F1 score"},
        "tags": ["Python", "pandas", "scikit-learn", "Random Forest"],
        "context": "A garment factory's productivity records covering multiple departments, teams, and quarters — 1,197 recorded work sessions in total.",
        "problem": "The raw data had inconsistent categorical labels (duplicate department names with trailing whitespace), irrelevant columns, and no existing way to predict which teams would actually hit their productivity targets versus fall short.",
        "skills": ["Python", "pandas", "scikit-learn", "Decision Trees", "Random Forests", "Cross-validation", "One-hot encoding"],
        "approach": "Cleaned and re-encoded the dataset (fixed department labels, dropped uninformative columns, one-hot encoded quarter/day/team), then trained a Decision Tree classifier to predict whether a team would meet its productivity target, followed by a Random Forest to compare performance.",
        "result": "85% accuracy, 88% precision, 93% recall, and a 90% F1 score on the Decision Tree, holding at 82% mean accuracy across 10-fold cross-validation. The Random Forest reached an 83% out-of-bag score, confirming the result wasn't a lucky split.",
        "links": [],
    },
    {
        "slug": "fandango-ratings-comparison",
        "title": "Fandango Ratings: Before vs. After",
        "cat": "data",
        "status": "Completed",
        "summary": "Compared Fandango's movie rating distributions before and after public criticism that the site was inflating scores.",
        "metric": "Mean, median & mode compared across 2 years",
        "tags": ["Python", "pandas", "matplotlib"],
        "context": "Following public criticism that Fandango's movie rating system was inflating scores, comparing rating distributions before and after the site changed how ratings were displayed.",
        "problem": "Two separate raw datasets (2015 ratings, pre-controversy, and 2016 ratings, post-controversy) needed to be cleaned, filtered to comparable years, and matched onto the same rating scale before any real comparison was possible.",
        "skills": ["Python", "pandas", "matplotlib", "KDE distribution plots", "Descriptive statistics"],
        "approach": "Isolated the 2015 and 2016 subsets, compared their rating distributions using kernel density plots, then computed mean, median, and mode for both years side by side to quantify the shift precisely rather than relying on the chart alone.",
        "result": "The comparison showed a visible shift in the rating distributions between the two years — a clear, number-backed answer to whether ratings had actually changed after the criticism, not just how the chart looked at a glance.",
        "links": [],
    },
    {
        "slug": "lora-finetuning-yoda",
        "title": "LoRA Fine-Tuning of LFM2-1.2B",
        "cat": "genai",
        "status": "Completed",
        "summary": "Fine-tuned LiquidAI's LFM2-1.2B with LoRA to consistently respond in Yoda's speech pattern, as an MIT (6.S191) course project.",
        "metric": "Style-adherence score: 0.00 → 0.61",
        "chart": {"type": "compare", "values": [0, 61], "labels": ["Before", "After"], "caption": "Style-adherence score"},
        "tags": ["LoRA", "PEFT", "Hugging Face"],
        "context": "A hands-on fine-tuning exercise from an MIT (6.S191) course, applied to LiquidAI's open LFM2-1.2B language model.",
        "problem": "The base model had no particular stylistic personality. The goal was to make it consistently respond in a distinct, recognizable voice — Yoda's inverted syntax and speech pattern — without retraining the full 1.2-billion-parameter model from scratch.",
        "skills": ["LoRA", "PEFT", "Hugging Face Transformers", "Style-adherence evaluation"],
        "approach": "Applied LoRA (Low-Rank Adaptation) so only a small set of adapter weights trained instead of the full model, fine-tuning on style-targeted examples, and measured a style-adherence score before and after training rather than assuming the fine-tune worked.",
        "result": "Style-adherence score moved from 0.00 before training (no adherence at all) to 0.61 after — proof, not a guess, that the fine-tune actually changed the model's behavior.",
        "links": [
            {"label": "View on GitHub", "url": "https://github.com/nabihahmed19-collab/llm-finetuning-yoda-lora"},
        ],
    },
    {
        "slug": "cnn-age-gender-ethnicity",
        "title": "Multi-Output CNN: Age, Gender & Ethnicity",
        "cat": "dl",
        "status": "Completed",
        "summary": "A multi-output ResNet50 trained on UTKFace to predict age, gender, and ethnicity from a single face image.",
        "metric": "90.9% gender accuracy · ±6.6 yr age MAE",
        "chart": {"type": "bar", "value": 91, "caption": "90.9% gender accuracy"},
        "tags": ["ResNet50", "Computer Vision", "Multi-task Learning"],
        "context": "A single-image facial attribute prediction task using the UTKFace dataset.",
        "problem": "Predicting age, gender, and ethnicity from one photo means training three very different kinds of tasks — a near-binary classification, a multi-class classification, and a regression — inside one shared model. Naively combining their losses lets one task dominate the others during training.",
        "skills": ["Python", "TensorFlow/PyTorch", "ResNet50", "Transfer learning", "Multi-task loss balancing"],
        "approach": "Built a multi-output ResNet50 with three separate prediction heads, then tuned the loss weighting across the three tasks so each head actually learned rather than one drowning out the others.",
        "result": "90.9% gender classification accuracy and ±6.6-year mean absolute error on age prediction, in a single forward pass through one model.",
        "links": [
            {"label": "View on GitHub", "url": "https://github.com/nabihahmed19-collab/age-gender-ethnicity-resnet50"},
        ],
    },
    {
        "slug": "oral-cancer-cnn-fyp",
        "title": "Oral Cancer Detection (CNN) — Final Year Project",
        "cat": "dl",
        "status": "In progress",
        "summary": "A CNN classifying oral lesion images as benign or malignant, with a Streamlit interface built for clinicians.",
        "metric": "Binary classification · Streamlit demo",
        "tags": ["CNN", "TensorFlow/PyTorch", "Streamlit", "Medical Imaging"],
        "context": "My BSCS final-year project, aimed at supporting earlier screening for oral lesions.",
        "problem": "Public oral lesion image datasets are small and imbalanced toward benign cases, which makes a naive classifier look accurate while actually missing malignant cases — and any tool built on top of it needs to be usable by a clinician with no coding background.",
        "skills": ["Python", "CNNs", "TensorFlow/PyTorch", "Streamlit", "Class-imbalance handling"],
        "approach": "Built a CNN architecture that specifically accounts for the class imbalance, with validation designed to check performance on malignant cases directly rather than trusting overall accuracy, then wrapped the model in a Streamlit interface that takes an uploaded image and returns a classification.",
        "result": "Still in active development ahead of my final defense — the architecture and interface are both functional, with model tuning ongoing.",
        "links": [],
    },
    {
        "slug": "maazmail",
        "title": "MaazMail",
        "cat": "genai",
        "status": "In testing",
        "summary": "A cold email outreach SaaS built end to end with a collaborator — campaigns, contacts, and real Gmail sending.",
        "metric": "Full stack: FastAPI + React + PostgreSQL + Groq",
        "tags": ["FastAPI", "React", "PostgreSQL", "Groq"],
        "context": "A cold email outreach SaaS, built end to end with collaborator Maaz as a real product rather than a script.",
        "problem": "Small teams doing outbound outreach needed a tool to manage campaigns and contacts and actually send emails from a real inbox — not a sandboxed test account — with AI assistance drafting the emails themselves.",
        "skills": ["FastAPI", "React", "PostgreSQL", "Groq", "SMTP / Gmail App Passwords"],
        "approach": "Designed the PostgreSQL schema for campaigns and contacts, built the FastAPI backend handling campaign logic, wired up a React frontend for the user-facing side, used Groq to power AI-assisted email drafting, and connected real Gmail sending via SMTP with an App Password.",
        "result": "Verified working end to end on localhost with every major page functional, ahead of a public deploy.",
        "links": [],
    },
    {
        "slug": "querio",
        "title": "Querio",
        "cat": "genai",
        "status": "Live",
        "summary": "An agentic text-to-SQL system — describe what you want in plain English, and it writes and runs the query.",
        "metric": "Deployed on Hugging Face Spaces",
        "tags": ["Pydantic-AI", "Gradio", "Text-to-SQL"],
        "context": "An agentic text-to-SQL system built to remove the SQL barrier between a question and an answer.",
        "problem": "Most people who need data from a database can describe what they want in plain English but can't write the SQL to get it — and a generic language model doesn't reliably plan a multi-step query task or handle schemas it's never seen before.",
        "skills": ["Python", "Pydantic-AI", "Gradio", "Hugging Face Spaces", "Agentic planning"],
        "approach": "Built the system on Pydantic-AI's structured agent framework so the agent plans out the query step by step before generating SQL, executes it against the database, and returns a clean result — all through a Gradio interface with zero setup for anyone trying it.",
        "result": "Deployed publicly on Hugging Face Spaces, live and usable by anyone with the link.",
        "links": [
            {"label": "View on GitHub", "url": "https://github.com/nabihahmed19-collab/querio-text-to-sql"},
            {"label": "Try the Live Demo", "url": "https://huggingface.co/spaces/NabihaAhmed/querio-text-to-sql"},
        ],
    },
    {
        "slug": "ai-support-triage-agent",
        "title": "AI Customer Support Triage Agent",
        "cat": "genai",
        "status": "Live",
        "summary": "My first AI project — an agent that reads incoming support queries and routes them by urgency and topic.",
        "metric": "Publicly launched on Hugging Face Spaces",
        "tags": ["LLM Agents", "Hugging Face"],
        "context": "The first AI project — an agent built to handle the first-pass triage step support teams usually do manually.",
        "problem": "Reading every incoming support ticket just to figure out where it should go wastes real time, and most triage logic assumes a fixed set of categories that doesn't generalize well.",
        "skills": ["LLM agents", "Hugging Face Spaces", "Prompt design"],
        "approach": "Built an agent that reads a raw customer message and classifies both its urgency and its topic, so tickets land with the right team immediately instead of sitting in a general queue.",
        "result": "Publicly launched on Hugging Face Spaces — also the project that taught the most about taking a model from a notebook to something a stranger could actually open and use.",
        "links": [
            {"label": "View on GitHub", "url": "https://github.com/nabihahmed19-collab/ai-support-triage-agent"},
            {"label": "Try the Live Demo", "url": "https://huggingface.co/spaces/NabihaAhmed/support-triage-agent"},
        ],
    },
    {
        "slug": "amazon-seller-lead-scraper",
        "title": "Amazon Seller Lead Scraper",
        "cat": "auto",
        "status": "Completed",
        "summary": "A Selenium-based scraper that pulls Amazon seller leads and exports them straight to Excel for outreach.",
        "metric": "End-to-end automated export pipeline",
        "tags": ["Selenium", "Python", "Excel"],
        "context": "Built with Maaz to replace a manual, copy-paste lead research process for outreach.",
        "problem": "Manually browsing Amazon seller pages and copying data into a spreadsheet for outreach took real time and didn't scale past a handful of leads a day.",
        "skills": ["Python", "Selenium", "Excel export"],
        "approach": "Built a Selenium script that navigates seller pages, collects the relevant data, cleans it, and exports it directly to Excel in a format ready to hand to outreach.",
        "result": "Turned an afternoon of manual research into a single script run, end to end.",
        "links": [
            {"label": "View on GitHub", "url": "https://github.com/nabihahmed19-collab/amazon-seller-lead-scraper"},
        ],
    },
    {
        "slug": "offline-rag-chatbot",
        "title": "Offline RAG Chatbot for Legal Documents",
        "cat": "genai",
        "status": "Completed",
        "summary": "A fully offline retrieval-augmented chatbot that answers questions from legal PDFs, DOCX, and TXT files.",
        "metric": "100% offline, zero external API calls",
        "chart": {"type": "bar", "value": 100, "caption": "0 external API calls"},
        "tags": ["RAG", "Local LLM", "Document Q&A"],
        "context": "A retrieval-augmented chatbot built for legal documents that can't leave the machine they're stored on.",
        "problem": "Legal material is often confidential, so calling an external API for embeddings or generation isn't an option no matter how convenient — but the chatbot still needs to answer accurately, grounded only in the actual source documents.",
        "skills": ["Python", "Local LLMs", "RAG pipelines", "Document parsing (PDF/DOCX/TXT)"],
        "approach": "Built the full pipeline — chunking, embedding, retrieval, and generation — to run entirely on local models with no network calls, accepting a mixed folder of PDFs, DOCX, and plain text files as input.",
        "result": "100% offline with zero external API dependency, and every answer grounded strictly in retrieved passages rather than the model's general knowledge.",
        "links": [],
    },
]

# ---------- Generate projects-data.js (for the homepage grid) ----------
def js_string(s):
    return json.dumps(s)

def gen_projects_js():
    lines = ["const CATEGORIES = " + json.dumps(
        [{"key": k, "label": CATS[k]["label"]} for k in CATEGORY_ORDER], indent=2
    ) + ";\n"]
    lines.append("const PROJECTS = [")
    for p in PROJECTS:
        lines.append("  {")
        lines.append(f'    slug: {js_string(p["slug"])},')
        lines.append(f'    title: {js_string(p["title"])},')
        lines.append(f'    cat: {js_string(p["cat"])},')
        lines.append(f'    status: {js_string(p["status"])},')
        lines.append(f'    summary: {js_string(p["summary"])},')
        lines.append(f'    metric: {js_string(p["metric"])},')
        lines.append(f'    tags: {json.dumps(p["tags"])},')
        if "chart" in p:
            lines.append(f'    chart: {json.dumps(p["chart"])},')
        lines.append("  },")
    lines.append("];")
    return "\n".join(lines)

with open("projects-data.js", "w") as f:
    f.write(gen_projects_js())

# ---------- Generate one detail page per project ----------
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Nabiha Ahmed</title>
<meta name="description" content="{summary}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<style>:root {{ --card-accent: var({cat_var}); }}</style>
</head>
<body>

<nav class="topnav">
  <div class="topnav-inner">
    <a class="topnav-mark" href="index.html">NA</a>
    <a class="topnav-back" href="index.html#projects">&larr; Back to portfolio</a>
  </div>
</nav>

<header class="detail-hero">
  <div class="section-inner reveal">
    <div class="detail-category">
      <span class="category-icon" style="color: var({cat_var});"><svg viewBox="0 0 16 16" fill="currentColor" stroke="currentColor" stroke-width="1.3">{cat_icon}</svg></span>
      {cat_label}
    </div>
    <h1>{title}</h1>
    <p class="detail-summary">{summary}</p>
    <div class="detail-tags">
      {tags_html}
    </div>
    {links_html}
  </div>
</header>

<main class="detail-body">
  <div class="section-inner">

    <section class="detail-section reveal">
      <div class="detail-section-label">Context</div>
      <p>{context}</p>
    </section>

    <section class="detail-section reveal">
      <div class="detail-section-label">The Problem</div>
      <p>{problem}</p>
    </section>

    <section class="detail-section reveal">
      <div class="detail-section-label">Skills Used</div>
      <div class="skills-used-list">
        {skills_html}
      </div>
    </section>

    <section class="detail-section reveal">
      <div class="detail-section-label">Approach</div>
      <p>{approach}</p>
    </section>

    <section class="detail-section reveal">
      <div class="detail-section-label">Result</div>
      <p>{result}</p>
    </section>

  </div>
</main>

<footer class="detail-footer section-inner">
  <a href="index.html#projects">&larr; All projects</a>
  <a href="index.html#contact">Get in touch &rarr;</a>
</footer>

<script src="script.js"></script>
</body>
</html>
"""

def gen_detail_page(p):
    tags_html = "\n      ".join(f'<span class="detail-tag">{t}</span>' for t in p["tags"])
    skills_html = "\n        ".join(f'<span>{s}</span>' for s in p["skills"])
    if p["links"]:
        btns = "\n      ".join(
            f'<a class="detail-link-btn" href="{l["url"]}" target="_blank" rel="noopener">{l["label"]}</a>'
            for l in p["links"]
        )
        links_html = f'<div class="detail-links">\n      {btns}\n    </div>'
    else:
        links_html = ""
    return PAGE_TEMPLATE.format(
        title=p["title"],
        summary=p["summary"],
        cat_var=CATS[p["cat"]]["var"],
        cat_label=CATS[p["cat"]]["label"],
        cat_icon=CATS[p["cat"]]["icon"],
        tags_html=tags_html,
        skills_html=skills_html,
        links_html=links_html,
        context=p["context"],
        problem=p["problem"],
        approach=p["approach"],
        result=p["result"],
    )

for p in PROJECTS:
    with open(f'{p["slug"]}.html', "w") as f:
        f.write(gen_detail_page(p))

print(f"Generated projects-data.js and {len(PROJECTS)} detail pages.")
