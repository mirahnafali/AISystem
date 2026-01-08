# AI Flight Price Prediction System - v1

An intelligent flight price prediction system that collects, analyzes, and predicts airline ticket prices to help users determine the optimal time to purchase tickets.

## 🎯 Project Overview

This system uses machine learning to analyze flight pricing patterns and predict future price trends. By continuously collecting data from the Amadeus Flight API, the algorithm learns pricing behaviors across different routes, airlines, and time periods to provide actionable insights on when to buy tickets.

## 🚀 Project Goals

1. **Data Collection Phase** - Continuously gather flight pricing data from multiple airlines and routes
2. **Model Training** - Build and train ML models to identify pricing patterns and predict future prices
3. **Price Prediction** - Provide real-time predictions on whether ticket prices will rise or fall
4. **Deployment** - Deploy to AWS cloud infrastructure for 24/7 automated data collection and predictions

## 📊 Features

### Current Implementation (v1)
- ✅ Amadeus API integration for flight data collection
- ✅ Multi-route tracking (BOS→LAX, JFK→SFO)
- ✅ Multi-airline monitoring (American Airlines, Delta, United)
- ✅ Price history tracking with timestamps
- ✅ Data storage in CSV format
- ✅ Feature extraction for ML training

### Planned Features
- 🔄 Real-time price prediction algorithm
- 🔄 AWS deployment for continuous operation
- 🔄 Historical price trend analysis
- 🔄 Price alert notifications
- 🔄 Web dashboard for visualization
- 🔄 Multi-class fare tracking (Economy, Business, First)

## 🛠️ Tech Stack

### Core Technologies
- **Language:** Python 3.x
- **APIs:** Amadeus Flight Offers Search API

### Data Layer
- **Data Collection:** Amadeus Python SDK
- **Data Processing:** Pandas, NumPy
- **Data Storage:** 
  - Current: CSV files
  - Planned: PostgreSQL / MongoDB

### Machine Learning
- **ML Frameworks:** 
  - TensorFlow / PyTorch (for neural networks)
  - Scikit-learn (for traditional ML models)
  - XGBoost (for gradient boosting)
- **Feature Engineering:** Pandas, NumPy
- **Model Evaluation:** Matplotlib, Seaborn

### Deployment & Infrastructure
- **Cloud Platform:** AWS
  - EC2 for compute
  - Lambda for serverless functions
  - RDS for database
  - S3 for data storage
  - CloudWatch for monitoring
- **Scheduling:** AWS EventBridge / Cron jobs
- **API Development:** FastAPI / Flask

### Development Tools
- **Environment Management:** python-dotenv, virtualenv
- **Version Control:** Git
- **Code Quality:** pytest, pylint
- **Notebooks:** Jupyter

## 📁 Project Structure

```
ticket-algorithm-v1-main/
├── data/                                  # Data storage
│   ├── .gitkeep                          # Keeps directory in git
│   └── flight_prices.csv                 # Collected flight data
├── notebooks/                            # Jupyter notebooks for exploration
│   ├── data_collection_initial_features.ipynb
│   └── 02_data_collection.ipynb
├── src/                                  # Source code
│   ├── __init__.py                       # Package initialization
│   ├── data_collector.py                 # Main data collection script
│   └── price_testing.py                  # Price variation analysis
├── config/                               # Configuration files
│   └── .env.example                      # Environment template
├── .gitignore                            # Git ignore rules
├── requirements.txt                      # Python dependencies
├── LICENSE                               # Project license
└── README.md                             # Project documentation
```

## 🔧 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mirahnafali/AISystem.git
   cd AISystem
   ```

2. **Install dependencies:**
   ```bash
   pip install amadeus python-dotenv pandas numpy jupyter
   ```

3. **Configure API credentials:**
   - Create a `.env` file in the root directory
   - Add your Amadeus API credentials:
     ```
     AMADEUS_CLIENT_ID=your_client_id_here
     AMADEUS_CLIENT_SECRET=your_client_secret_here
     ```
   - Get free API credentials at [Amadeus for Developers](https://developers.amadeus.com/)

4. **Run the data collection:**
   ```bash
   jupyter notebook data_collection_initial_features.ipynb
   ```

## 📈 Data Collection Features

The system tracks the following data points for each flight:

| Feature | Description |
|---------|-------------|
| `Observation_ID` | Unique identifier for each data collection point |
| `Flight_Unique_ID` | Unique identifier for specific flight instance |
| `Collection_Timestamp` | When the data was collected (UTC) |
| `Departure_DateTime` | Scheduled departure time |
| `Airline_Code` | IATA airline code (AA, DL, UA, etc.) |
| `Route` | Origin-Destination pair |
| `Flight_Number` | Flight number |
| `Aircraft_Type_Code` | Aircraft model code |
| `Number_of_Stops` | Direct flight or connections |
| `PE_Current` | Current economy class price |
| `Price_Bucket_1-5` | Different fare tier prices |

## 🎯 Roadmap

### Phase 1: Data Collection (Current)
- [x] Amadeus API integration
- [x] Basic data collection pipeline
- [x] CSV storage implementation
- [ ] Expand route coverage
- [ ] Add more airlines

### Phase 2: Data Analysis & Model Training
- [ ] Exploratory Data Analysis (EDA)
- [ ] Feature engineering
- [ ] Model selection and training
- [ ] Model evaluation and optimization
- [ ] Price prediction algorithm development

### Phase 3: Deployment & Automation
- [ ] AWS EC2/Lambda deployment
- [ ] Automated data collection scheduling
- [ ] Database integration (PostgreSQL/DynamoDB)
- [ ] RESTful API for predictions
- [ ] Real-time price monitoring

### Phase 4: User Interface
- [ ] Web dashboard development
- [ ] Price alert system
- [ ] Historical trend visualization
- [ ] Mobile app (future consideration)

## 🧪 Testing

Currently testing:
- API response handling
- Data parsing and cleaning
- Price variation tracking
- Multi-route collection

## 📝 License

This project is licensed under the terms included in the LICENSE file.

## 👤 Author

**Mirahn Afali**
- GitHub: [@mirahnafali](https://github.com/mirahnafali)

## 🤝 Contributing

This is currently a personal research project. Contributions, issues, and feature requests are welcome once the project reaches beta stage.

## 📧 Contact

For questions or collaboration opportunities, please open an issue on GitHub.

---

**Note:** This is an educational/research project. Always verify pricing information directly with airlines before making purchasing decisions.
