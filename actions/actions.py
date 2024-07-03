import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetFare(Action):

    def name(self) -> str:
        return "action_get_fare"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:
        
        train_number = tracker.get_slot('train_number')
        from_station = tracker.get_slot('from_station')
        to_station = tracker.get_slot('to_station')

        url = f"https://irctc1.p.rapidapi.com/api/v2/getFare?trainNo={train_number}&fromStationCode={from_station}&toStationCode={to_station}"
        headers = {
            "rapidapi-key": "5071a6d972msh9d3622a6ab299d3p14ab97jsn5ee0b4d2b30a"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            fare_data = response.json().get('data')
            fare_details = self.format_fare_details(fare_data)
            dispatcher.utter_message(text=fare_details)
        else:
            dispatcher.utter_message(text="I couldn't fetch the fare details. Please try again.")
        return []

    def format_fare_details(self, fare_data):
        details = []
        for category, fares in fare_data.items():
            for fare in fares:
                class_type = fare['classType']
                cost = fare['fare']
                if cost:
                    details.append(f"Class {class_type}: {cost} INR")
        return "\n".join(details)




















