"""Interact with magicthegathering.io api."""
import mtgsdk

def search_by_name(name):
    """Gets a list of cards from io by name."""

    return mtgsdk.Card.where(name=name).all()


def search_by_id(id):
    """Finds the card by its id"""

    return mtgsdk.Card.find(id=id)