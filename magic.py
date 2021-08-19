"""Interact with magicthegathering.io api."""
import mtgsdk

def search_by_name(name):
    """Gets a list of cards from io by name."""

    return mtgsdk.Card.where(name=name).all()


