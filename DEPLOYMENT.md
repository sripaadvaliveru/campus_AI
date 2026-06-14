# Deployment Guide — CampusAI Chatbot

This guide outlines the steps to deploy your updated chatbot to the cloud using **Streamlit Community Cloud** (recommended) or **Hugging Face Spaces** (free alternative).

---

## 🔑 Crucial Security Reminder
> [!WARNING]
> **Never commit your `.env` file** or write your `GOOGLE_API_KEY` directly in your code. The `.env` file is excluded in `.gitignore` to protect your credentials. You will set this API key as a secure environment variable/secret on the hosting platform instead.

---

## 📂 Pre-Deployment Checklist
Because serverless platforms do not have GPU acceleration and have strict memory limits, building the semantic vector index on startup can be slow or fail.
1. Make sure you have the SQLite database (`campus.db`) and the pre-built vector index files (`vector_store/campus.index` and `vector_store/documents.pkl`) in your workspace.
2. Since we have updated `.gitignore` to allow these pre-built index files and database to be committed, they will be pushed to GitHub automatically. This keeps the deployment fast and reliable.

---

## Option 1: Streamlit Community Cloud (Recommended)
Streamlit Community Cloud connects directly to your GitHub repository and deploys the app for free.

### Step 1: Push code to GitHub
Initialize a git repository inside the `campus-chatbot` folder, commit the files, and push to GitHub:
```bash
# Navigate to the project root directory
cd campus-chatbot

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "feat: Initial commit with strategic report data and UI fixes"

# Create a new repository on GitHub and link it
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

### Step 2: Set up Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **"Create app"** (or **"New app"**).
3. Select your repository, branch (`main`), and set the main file path to:
   ```text
   app.py
   ```

### Step 3: Add Google API Key Secret
1. Before clicking deploy, click on **"Advanced settings"** (or click the gear icon next to your app in the dashboard).
2. In the **Secrets** section, paste your Gemini API key:
   ```toml
   GOOGLE_API_KEY = "your_actual_google_gemini_api_key"
   ```
3. Click **"Save"** and then **"Deploy!"**. Your app will build and go live in 1-2 minutes.

---

## Option 2: Hugging Face Spaces (Free Alternative)
Hugging Face Spaces is another excellent free platform that natively hosts Streamlit applications.

### Step 1: Create a Space on Hugging Face
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and log in.
2. Click **"Create new Space"**.
3. Set your Space Name and select **Streamlit** as the SDK.
4. Set the space visibility to **Public** or **Private** and click **Create Space**.

### Step 2: Push your repository
You can either upload your files directly through the Hugging Face web UI, or clone the Hugging Face space repository locally and push your code:
```bash
# Clone the HF space repo
git clone https://huggingface.co/spaces/yourusername/your-space-name

# Copy all project files from campus-chatbot into the cloned folder, then push:
git add .
git commit -m "Deploy CampusAI Chatbot"
git push
```

### Step 3: Configure Gemini API Key
1. Go to your Hugging Face Space page.
2. Click on the **"Settings"** tab.
3. Scroll down to **"Variables and secrets"** and click **"New secret"**.
4. Set the key name to `GOOGLE_API_KEY` and the value to your Gemini API key.
5. Click **"Save"**. The Space will automatically rebuild and run the app.
