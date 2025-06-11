
# 🛒 smart-shopper-walmart_hackthon

An intelligent E-Commerce platform built for Walmart as part of **Sparkathon 2025**. This project leverages **Natural Language Processing (NLP)** and **price optimization algorithms** to provide personalized shopping experiences, smarter recommendations, and maximized savings for users.


---

## 🚀 Demo

**Frontend:** [http://localhost:3000](http://localhost:3000)  
**Backend:** [http://localhost:8000](http://localhost:8000)

---

## 🧠 Key Highlights

- 🔍 NLP-Powered Recommendation System  
- 💸 Dynamic Price Optimization  
- 🛒 Full-featured Shopping Cart  
- 🔐 User Authentication System  
- 📊 MongoDB-Powered Data Store  
- ⚡ React.js + Flask Integration  

---

## 🧰 Tech Stack

### 🎨 Frontend
- **React.js**
- **React Router DOM**
- **Axios**

### 🧠 Backend
- **Flask**
- **MongoDB (via PyMongo)**
- **Flask-CORS**
- **Custom Middleware for Authentication**

### 🧪 NLP & AI
- **NLTK (Natural Language Toolkit)**
- **Scikit-learn's TfidfVectorizer**

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dev04sa/smart-shopper-walmart_hackthon.git
cd smart-shopper-walmart_hackthon
````

---

### 2. Install Frontend Dependencies

```bash
cd client
npm install
```

---

### 3. Install Backend Dependencies

```bash
cd ../server
pip install -r requirements.txt
```

---

### 4. Set Up MongoDB

* You can either:

  * Run MongoDB locally (`mongodb://localhost:27017`)
  * Or use **MongoDB Atlas** – update your connection string in `app.py`.

```python
# Example in app.py
client = pymongo.MongoClient("your_mongodb_connection_url")
```

---

### 5. Start the Application

#### ➤ Frontend (Client)

```bash
cd client
npm start
```

Runs on: [http://localhost:3000](http://localhost:3000)

#### ➤ Backend (Server)

```bash
cd server
python app.py
```

Runs on: [http://localhost:8000](http://localhost:8000)

---

## 🔑 Features Overview

### 1. **User Authentication**

* Signup/Login functionality
* JWT-based secure session handling
* Role-based access to features

### 2. **NLP Recommendation System**

* Uses `NLTK` and `TfidfVectorizer`
* Analyzes user search history and preferences
* Returns context-aware, top-N product suggestions

### 3. **Price Optimization**

* Algorithmically adjusts and optimizes product prices
* Aims to provide users with best-value deals

### 4. **Cart and Checkout**

* Add to cart, remove, update quantity
* Seamless checkout experience

### 5. **Admin Utilities (optional)**

* Upload/manage product listings
* Track user behavior for feedback learning

---



---

## 💡 Future Enhancements

* 🧾 Order History & Tracking
* 🧠 Advanced ML-based Price Prediction
* 🗣️ Voice-based search using NLP
* 📱 Mobile App using Flutter or React Native

---

## 👤 Contributor

**Devendra Singh**
🔗 [GitHub – @dev04sa](https://github.com/dev04sa)

---

## 📜 License

This project is developed as part of a hackathon and is currently open for educational and showcase purposes. For commercial use, please contact the contributor.

---

```

