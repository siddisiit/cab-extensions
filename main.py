import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(title="Local Cab Service API")

# Enable CORS so your frontend can communicate with your backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase Credentials Configuration
# Replace these strings with your actual dashboard credentials
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "PASTE_YOUR_ACTUAL_SUPABASE_ANON_KEY_HERE"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"status": "online", "message": "Localized Cab Service Backend API"}

# 1. Endpoint for Riders to Request a Cab
@app.post("/book-ride")
def book_ride(pickup: str, destination: str):
    response = supabase.table("rides").insert({
        "pickup": pickup,
        "destination": destination,
        "status": "pending"
    }).execute()
    return {"message": "Ride requested successfully!", "data": response.data}

# 2. Endpoint for Drivers to View Active Requests
@app.get("/active-rides")
def get_active_rides():
    response = supabase.table("rides").select("*").eq("status", "pending").execute()
    return {"active_rides": response.data}
