# from django.test import TestCase
# from django.core import mail
# from api.emails import send_winner_email
# from api.models import User, Item, Bid
# from django.utils import timezone

# class EmailTests(TestCase):
#     """
#     Test case for email functionalities in the auction application.
    
#     Tests the sending of winner notification emails.
#     """
#     def test_winner_email_sent(self):
#         # Create a test user
#         user1 = User.objects.create_user(username='testuser1', email='testuser1@example.com', password='testpassword1')
#         user2 = User.objects.create_user(username='testuser2', email='testuser2@example.com', password='testpassword2')
#         winner = User.objects.create_user(username='winneruser', email='winneruser@example.com', password='winnerpassword')
#         owner = User.objects.create_user(username='owneruser', email='owner@example.com', password='ownerpassword')
        
#         item = Item.objects.create(title='Test Item', description='This is a test item.', starting_price=10.00, auction_end=timezone.now(), user=owner)
        
#         bid1 = Bid.objects.create(user=user1, item=item, amount=15.00)
#         bid2 = Bid.objects.create(user=user2, item=item, amount=20.00)
#         bid3 = Bid.objects.create(user=winner, item=item, amount=25.00)

#         # Send the winner email
#         send_winner_email(winner, item)

#         # Check that an email was sent
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].to, ['winneruser@example.com'])
#         self.assertIn('Auction Winner', mail.outbox[0].subject)
