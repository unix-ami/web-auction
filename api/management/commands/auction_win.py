"""
Management command to process ended auctions and
notify winning bidders via email.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Item, Bid
from api.emails import send_winner_email

class Command(BaseCommand):
    """
    Command to check for ended auctions and notify winners
    
    This command checks for auctions that have ended, determines the highest bidder,
    updates the bid status to 'WON', and sends an email notification to the winner.
    """
    
    help = 'Check for ended auctions and notify winners'

    def handle(self, *args, **kwargs):
        """Handle the command to check for ended auctions and notify winners."""
        now = timezone.now()
        ended_auctions = Item.objects.filter(auction_end__lte=now)

        for auction in ended_auctions:

            highest_bid = Bid.objects.filter(item=auction).order_by('-amount').first()

            if highest_bid:
                winner = highest_bid.user

                # Change bid from pending to WON
                highest_bid.status = 'WON'
                highest_bid.save()

                #  Send winner email
                send_winner_email(winner, auction)

            auction.save()