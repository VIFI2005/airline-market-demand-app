
✈️ Airline Market Demand Dashboard

A full-stack Flask web application to analyze and visualize real-time airline booking data using the AviationStack API. The dashboard allows users to filter by route and date, see booking trends, export data, and optionally generate AI-powered insights.

> 🔗 Live Demo**: [https://ca3917a8-6919-4788-9911-1f80c248852b-00-1x9zbhfsxa78j.picard.replit.dev/]  

---

📊 Features

- 🔍 Real-Time Data** via AviationStack API
- 🎛️ Interactive Filters** (Source, Destination, Date)
- 📈 Visual Charts** (Popular Routes and Price Trends using Chart.js)
- 📥 CSV Export** for filtered flight data
- 🔐 Login Authentication** (Demo: `admin` / `pass123`)
- ⚡ Flask-Caching** to optimize API calls
- 🧠 AI Insights Placeholder** (supports integration with OpenAI API)

---

🖼️ Screenshots

<<img width="1710" height="977" alt="image" src="https://github.com/user-attachments/assets/c974f3a3-ac00-4add-acf5-e4b337a429ef" />



---

🧰 Tech Stack

| Category       | Tools Used                      |
|----------------|----------------------------------|
| Backend        | Python, Flask                   |
| Frontend       | HTML, Bootstrap 5, Chart.js     |
| Data Layer     | Pandas                          |
| External APIs  | AviationStack API               |
| Hosting        | Replit                          |
| Auth           | Basic Login (in-memory)         |
| Extras         | Flask-Caching, CSV Export       |

---

⚙️ Setup Instructions(If one has to Setup on His/Her own pc)
1. Clone the Repository
     '''bash
     git clone https://github.com/yourusername/airline-market-demand-app.git
     cd airline-market-demand-app

2. Create Virtual Environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate

3. Install Dependencies
   
4. Configure API Key
    Create a .env file in the project root:
    AVIATIONSTACK_API_KEY=your_api_key_here

5. Run the App
   python app.py


🔐 Login Credentials (Demo)
	•	Username: admin
	•	Password: pass123


