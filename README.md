# 📍 SIM Location Tracker

A Django-based system for legally compliant SIM card location tracking with robust privacy and security measures.  
This project demonstrates how to build a location lookup system while respecting user consent, privacy regulations, and secure development practices.

---

## 🚀 Key Features

### ⚖️ Legal Compliance
- **Consent Management** – Explicit user consent required before tracking  
- **Ownership Verification** – SMS verification via Twilio  
- **Audit Trail** – Complete logging of all searches  
- **Privacy Controls** – User data protection mechanisms  

### 🛠 Technical Features
- **Phone Number Validation** – Using [`phonenumbers`](https://pypi.org/project/phonenumbers/) library  
- **Carrier Information** – Basic carrier and country detection  
- **Location History** – Tracking of location changes over time  
- **Interactive Maps** – Integration with [Leaflet.js](https://leafletjs.com/)  
- **REST API** – Mobile app integration supported  

### 🔒 Security Features
- **User Authentication** – Django’s built-in authentication system  
- **CSRF Protection** – Built-in Django middleware  
- **Input Validation** – Phone number format validation  
- **Rate Limiting** – Optional with [`django-ratelimit`](https://pypi.org/project/django-ratelimit/)  

---

## 📡 API Endpoints

### 🔍 Search for Location
```http
POST /api/search/
Content-Type: application/json

{
    "phone_number": "+1234567890",
    "consent": true
}
```

### 📊 Get Search Results
```http
GET /api/search/{search_id}/
```

---

## 🏗 Real Implementation Requirements

To make this production-ready, you’ll need:

### 📞 Location Service Providers
- **Carrier APIs** – Direct integration with telecom providers  
- **Location Services** – Google Maps, HERE, or similar services  
- **Cell Tower Database** – OpenCelliD or commercial providers  

### 📑 Legal Compliance
- **Terms of Service** – Clear usage guidelines  
- **Privacy Policy** – GDPR/CCPA compliance  
- **Data Retention** – Automatic data deletion policies  
- **Consent Management** – Robust consent tracking system  

### ⚙️ Production Setup
- **Database** – PostgreSQL or similar  
- **Caching** – Redis for performance boost  
- **Queue System** – Celery for async background tasks  
- **Monitoring** – Logging and error tracking (Sentry, ELK stack, etc.)  
- **Security** – HTTPS, rate limiting, input sanitization  

---

## 📦 Tech Stack
- **Backend** – Django, Django REST Framework  
- **Frontend** – Leaflet.js (interactive maps)  
- **APIs** – Twilio (for SMS verification), carrier APIs (future)  
- **Database** – SQLite (dev), PostgreSQL (production)  
- **Security** – Django auth, CSRF protection, HTTPS  

---

## ⚠️ Disclaimer
This project is for **educational purposes only**.  
Tracking phone locations without proper authorization and consent may violate laws in your country. Ensure compliance with local regulations before deploying.

---

## 👨‍💻 Author
Developed by **Alok Kumar Panda**  
[LinkedIn](https://www.linkedin.com/in/alok-kumar-panda-864b421a4) | [Portfolio](https://portfolio-one-mu-78.vercel.app/)  

---
