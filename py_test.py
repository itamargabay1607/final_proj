import pytest
from flight import Flight, FlightFullyBookedError


def purchase_multiple_tickets(flight, number_of_tickets):
    assert flight.remaining_tickets > number_of_tickets

def calculate_flight_duration(flight):
    duration = flight.origin_country - flight.destination_country
    assert duration == flight.origin_country - flight.destination_country

def check_password_validity(password):
    if len(password) < 8:
        assert false

    if len(password) < 6:
        assert false

    if len(password) > 20:
        assert false

    if not any(char.isdigit() for char in password):
        assert false

    if not any(char.isupper() for char in password):
        assert false

    if not any(char.islower() for char in password):
        assert false


# check_password_valid