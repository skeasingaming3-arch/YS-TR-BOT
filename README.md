# Quotex Confluence Signal Web Application

## 🚀 Deployment Instructions for GitHub & Render

1. Create a GitHub Repository and upload:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   
2. Go to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** -> **Web Service**.
4. Connect your GitHub repository.
5. Configure parameters:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click **Create Web Service**. 

আপনার ওয়েব অ্যাপের নিজস্ব URL পেয়ে যাবেন, যা দিয়ে যেকোনো মোবাইল বা কম্পিউটার ব্রাউজার থেকে সরাসরি সিগন্যাল পাবেন!
