from django.core.mail import send_mail

def send_winner_email(user, auction):
    """
    Sends an email to the auction winner notifying them of their win.
    
    Args:
        user: The User object representing the winner.
        auction: The Item object representing the won auction.
    """
    
    send_mail(
    "Auction Winner",
    "Congratulations, you have won the auction! Please proceed to buy the item.",
    None,
    [user.email],
    fail_silently=False,
)