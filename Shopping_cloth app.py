from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional, Dict
import json
from enum import Enum

class TravelType(Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    CAR = "car"

class PriceAlert(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"

@dataclass
class Destination:
    name: str
    country: str
    city: str
    airport_code: Optional[str] = None
    
@dataclass
class Flight:
    id: str
    departure: Destination
    arrival: Destination
    departure_time: datetime
    arrival_time: datetime
    price: float
    currency: str = "USD"
    airline: str = ""
    aircraft_type: str = ""
    
@dataclass
class Hotel:
    id: str
    name: str
    location: Destination
    rating: float
    price_per_night: float
    currency: str = "USD"
    amenities: List[str] = None
    images: List[str] = None
    availability: bool = True
    
@dataclass
class PriceTracker:
    item_id: str
    item_type: TravelType
    target_price: float
    current_price: float
    currency: str = "USD"
    alert_enabled: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

class LifeTripApp:
    def __init__(self):
        self.destinations = self._load_destinations()
        self.flights = []
        self.hotels = self._load_hotels()
        self.price_trackers = []
        self.user_searches = []
        
    def _load_destinations(self) -> List[Destination]:
        """Load popular destinations"""
        return [
            Destination("Phuket", "Thailand", "Phuket", "HKT"),
            Destination("Bangkok", "Thailand", "Bangkok", "BKK"),
            Destination("Osaka", "Japan", "Osaka", "KIX"),
            Destination("Tokyo", "Japan", "Tokyo", "NRT"),
            Destination("Seoul", "South Korea", "Seoul", "ICN"),
        ]
    
    def _load_hotels(self) -> List[Hotel]:
        """Load sample hotels"""
        return [
            Hotel(
                id="hotel_001",
                name="Myeongdong Osaka",
                location=Destination("Osaka", "Japan", "Osaka"),
                rating=4.5,
                price_per_night=120.0,
                amenities=["WiFi", "Pool", "Spa", "Restaurant"],
                images=["hotel1.jpg", "hotel2.jpg"]
            ),
            Hotel(
                id="hotel_002", 
                name="Luxury Resort Phuket",
                location=Destination("Phuket", "Thailand", "Phuket"),
                rating=4.8,
                price_per_night=250.0,
                amenities=["Beach Access", "Pool", "Spa", "Restaurant", "Bar"],
                images=["resort1.jpg", "resort2.jpg"]
            )
        ]
    
    def search_flights(self, departure: str, arrival: str, 
                      departure_date: datetime, return_date: Optional[datetime] = None) -> List[Flight]:
        """Search for flights between destinations"""
        # Mock flight search results
        mock_flights = [
            Flight(
                id="FL001",
                departure=Destination(departure, "Country", departure),
                arrival=Destination(arrival, "Country", arrival),
                departure_time=departure_date,
                arrival_time=departure_date + timedelta(hours=3),
                price=299.99,
                airline="Air Asia",
                aircraft_type="A320"
            ),
            Flight(
                id="FL002",
                departure=Destination(departure, "Country", departure),
                arrival=Destination(arrival, "Country", arrival),
                departure_time=departure_date + timedelta(hours=2),
                arrival_time=departure_date + timedelta(hours=5),
                price=399.99,
                airline="Thai Airways",
                aircraft_type="Boeing 777"
            )
        ]
        
        self.user_searches.append({
            "type": "flight",
            "departure": departure,
            "arrival": arrival,
            "date": departure_date,
            "timestamp": datetime.now()
        })
        
        return mock_flights
    
    def search_hotels(self, location: str, check_in: datetime, 
                     check_out: datetime, guests: int = 2) -> List[Hotel]:
        """Search for hotels in a specific location"""
        # Filter hotels by location
        location_hotels = [h for h in self.hotels if location.lower() in h.location.city.lower()]
        
        # Calculate nights
        nights = (check_out - check_in).days
        
        # Add total price calculation
        for hotel in location_hotels:
            hotel.total_price = hotel.price_per_night * nights
            
        self.user_searches.append({
            "type": "hotel",
            "location": location,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "timestamp": datetime.now()
        })
        
        return location_hotels
    
    def add_price_tracker(self, item_id: str, item_type: TravelType, 
                         target_price: float, current_price: float) -> PriceTracker:
        """Add a price tracker for flights or hotels"""
        tracker = PriceTracker(
            item_id=item_id,
            item_type=item_type,
            target_price=target_price,
            current_price=current_price
        )
        self.price_trackers.append(tracker)
        return tracker
    
    def check_price_alerts(self) -> List[Dict]:
        """Check for price drops and generate alerts"""
        alerts = []
        for tracker in self.price_trackers:
            if tracker.alert_enabled and tracker.current_price <= tracker.target_price:
                alerts.append({
                    "item_id": tracker.item_id,
                    "type": tracker.item_type.value,
                    "message": f"Price dropped to {tracker.current_price} {tracker.currency}!",
                    "savings": tracker.target_price - tracker.current_price,
                    "timestamp": datetime.now()
                })
        return alerts
    
    def get_popular_destinations(self) -> List[Destination]:
        """Get list of popular destinations"""
        return self.destinations
    
    def get_travel_ideas(self) -> List[Dict]:
        """Get travel ideas and suggestions"""
        return [
            {
                "destination": "Phuket, Thailand",
                "description": "Perfect beaches and vibrant nightlife",
                "best_time": "Nov - Apr",
                "avg_price": "$899",
                "image": "phuket.jpg"
            },
            {
                "destination": "Osaka, Japan", 
                "description": "Food capital with amazing culture",
                "best_time": "Mar - May, Sep - Nov",
                "avg_price": "$1,200",
                "image": "osaka.jpg"
            },
            {
                "destination": "Seoul, South Korea",
                "description": "Modern city with rich traditions",
                "best_time": "Apr - Jun, Sep - Nov", 
                "avg_price": "$950",
                "image": "seoul.jpg"
            }
        ]
    
    def book_flight(self, flight_id: str, passenger_details: Dict) -> Dict:
        """Book a flight"""
        # Mock booking process
        booking_ref = f"LT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        booking = {
            "booking_reference": booking_ref,
            "flight_id": flight_id,
            "passenger": passenger_details,
            "status": "confirmed",
            "booking_time": datetime.now(),
            "payment_status": "paid"
        }
        
        return booking
    
    def book_hotel(self, hotel_id: str, guest_details: Dict, 
                  check_in: datetime, check_out: datetime) -> Dict:
        """Book a hotel"""
        # Mock booking process
        booking_ref = f"HT{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        booking = {
            "booking_reference": booking_ref,
            "hotel_id": hotel_id,
            "guest": guest_details,
            "check_in": check_in,
            "check_out": check_out,
            "status": "confirmed",
            "booking_time": datetime.now(),
            "payment_status": "paid"
        }
        
        return booking

# Example usage and testing
if __name__ == "__main__":
    app = LifeTripApp()
    
    # Search for flights
    print("=== Flight Search ===")
    departure_date = datetime(2024, 12, 15, 10, 0)
    flights = app.search_flights("Bangkok", "Osaka", departure_date)
    
    for flight in flights:
        print(f"Flight {flight.id}: {flight.departure.name} → {flight.arrival.name}")
        print(f"Price: ${flight.price} | Airline: {flight.airline}")
        print(f"Departure: {flight.departure_time.strftime('%Y-%m-%d %H:%M')}")
        print("---")
    
    # Search for hotels
    print("\n=== Hotel Search ===")
    check_in = datetime(2024, 12, 15)
    check_out = datetime(2024, 12, 18)
    hotels = app.search_hotels("Osaka", check_in, check_out)
    
    for hotel in hotels:
        print(f"Hotel: {hotel.name}")
        print(f"Rating: {hotel.rating}/5 | Price: ${hotel.price_per_night}/night")
        print(f"Total: ${hotel.total_price} for {(check_out-check_in).days} nights")
        print("---")
    
    # Add price tracker
    print("\n=== Price Tracking ===")
    tracker = app.add_price_tracker("FL001", TravelType.FLIGHT, 250.0, 299.99)
    print(f"Price tracker added for flight FL001")
    print(f"Target: ${tracker.target_price}, Current: ${tracker.current_price}")
    
    # Get travel ideas
    print("\n=== Travel Ideas ===")
    ideas = app.get_travel_ideas()
    for idea in ideas:
        print(f"{idea['destination']}: {idea['description']}")
        print(f"Best time: {idea['best_time']} | Avg price: {idea['avg_price']}")
        print("---")
    
    # Mock booking
    print("\n=== Booking Example ===")
    passenger = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "passport": "A12345678"
    }
    
    booking = app.book_flight("FL001", passenger)
    print(f"Flight booked! Reference: {booking['booking_reference']}")
    print(f"Status: {booking['status']}")
