import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("NOTIFICATION_FROM_EMAIL", "noreply@eventms.com")


def send_email(to_email: str, subject: str, html_content: str):
    if not SENDGRID_API_KEY:
        print(
            f"[EMAIL DISABLED] No SENDGRID_API_KEY set. Would send to {to_email}: {subject}"
        )
        return

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")


def send_booking_confirmation(
    client_email: str,
    client_name: str,
    event_name: str,
    event_date: str,
    venue_name: str,
    vendor_name: str,
    cost: float,
    booking_id: int,
):
    subject = f"Booking Confirmed: {event_name}"
    html = f"""
    <h2>Booking Confirmation</h2>
    <p>Dear {client_name},</p>
    <p>Your event has been booked successfully!</p>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
        <tr><td><b>Booking Ref</b></td><td>#{booking_id}</td></tr>
        <tr><td><b>Event</b></td><td>{event_name}</td></tr>
        <tr><td><b>Date</b></td><td>{event_date}</td></tr>
        <tr><td><b>Venue</b></td><td>{venue_name}</td></tr>
        <tr><td><b>Vendor</b></td><td>{vendor_name}</td></tr>
        <tr><td><b>Total Cost</b></td><td>${cost:.2f}</td></tr>
    </table>
    <p>Thank you for choosing our platform!</p>
    """
    send_email(client_email, subject, html)


def send_payment_receipt(
    client_email: str,
    client_name: str,
    payment_id: int,
    event_name: str,
    amount: float,
    method: str,
    status: str,
):
    subject = f"Payment Receipt #{payment_id}"
    html = f"""
    <h2>Payment Receipt</h2>
    <p>Dear {client_name},</p>
    <p>Your payment has been processed.</p>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
        <tr><td><b>Payment ID</b></td><td>#{payment_id}</td></tr>
        <tr><td><b>Event</b></td><td>{event_name}</td></tr>
        <tr><td><b>Amount</b></td><td>${amount:.2f}</td></tr>
        <tr><td><b>Method</b></td><td>{method}</td></tr>
        <tr><td><b>Status</b></td><td>{status}</td></tr>
    </table>
    <p>Thank you for your payment!</p>
    """
    send_email(client_email, subject, html)


def send_event_reminder(
    client_email: str,
    client_name: str,
    event_name: str,
    event_date: str,
    venue_name: str,
):
    subject = f"Reminder: {event_name} is coming up!"
    html = f"""
    <h2>Event Reminder</h2>
    <p>Dear {client_name},</p>
    <p>This is a friendly reminder about your upcoming event:</p>
    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse:collapse;">
        <tr><td><b>Event</b></td><td>{event_name}</td></tr>
        <tr><td><b>Date</b></td><td>{event_date}</td></tr>
        <tr><td><b>Venue</b></td><td>{venue_name}</td></tr>
    </table>
    <p>We look forward to making your event a success!</p>
    """
    send_email(client_email, subject, html)
