# myapp/tasks.py
from celery import task
from django.utils import timezone
from .models import auctionlist, bids, winner
from django.core.mail import send_mail
from django.utils import send_email_notification

def send_email_notification(subject, message, recipient_list):
    from_email = 'bhukyasharath1729@gmail.com'  # Replace with your email address
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@task
def check_auction_completion():
    # Remove items with None end_time from the active list
    auctionlist.objects.filter(active_bool=True, end_time__isnull=True).update(active_bool=False)

    # Get completed auctions
    completed_auctions = auctionlist.objects.filter(active_bool=True, end_time__lte=timezone.now())

    for auction in completed_auctions:
        highest_bid = bids.objects.filter(listingid=auction.id).order_by('-bid').first()

        if highest_bid:
            # Declare the winner and send a winner notification
            win = winner(bid_win_list=auction, user=highest_bid.user)
            win.save()
            
            # Send winner notification email
            subject = 'Congratulations! You won the auction!'
            message = f'You have won the auction for "{auction.title}" with a bid of ${highest_bid.bid}.'
            recipient_list = [highest_bid.user]
            send_email_notification(subject, message, recipient_list)
        else:
            # No bids, send notification to all other participants
            participants = bids.objects.filter(listingid=auction.id).values_list('user', flat=True).distinct()
            participants = [participant for participant in participants if participant != auction.user]
            
            # Send notification email to all other participants
            subject = 'Auction Ended'
            message = f'The auction for "{auction.title}" has ended, and you did not win the item.'
            recipient_list = participants
            send_email_notification(subject, message, recipient_list)

        # Mark the auction as completed
        auction.active_bool = False
        auction.save()
