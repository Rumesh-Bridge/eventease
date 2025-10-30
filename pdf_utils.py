import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import models

def create_booking_pdf(booking: models.Booking) -> io.BytesIO:
    """
    Generates a PDF confirmation for a given booking.
    Returns the PDF as a in-memory byte buffer.
    """
    # Create an in-memory byte buffer
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file"
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up some constants
    width, height = letter
    margin = 1 * inch
    
    # --- Start writing the PDF ---
    c.setFont("Helvetica-Bold", 18)
    c.drawString(margin, height - margin, "EventEase Booking Confirmation")
    
    c.setFont("Helvetica", 12)
    c.drawString(margin, height - margin - (0.5 * inch), 
                 f"Booking ID: #{booking.id}")
    c.drawString(margin, height - margin - (0.7 * inch),
                 f"Booked on: {booking.booking_time.strftime('%B %d, %Y')}")

    # --- Booking Details ---
    y = height - margin - (1.5 * inch)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Event Details")
    
    c.setFont("Helvetica", 12)
    c.drawString(margin + (0.2 * inch), y - (0.3 * inch), 
                 f"Event: {booking.event.title}")
    c.drawString(margin + (0.2 * inch), y - (0.5 * inch), 
                 f"Date: {booking.event.date_time.strftime('%B %d, %Y at %I:%M %p')}")
    c.drawString(margin + (0.2 * inch), y - (0.7 * inch), 
                 f"Location: {booking.event.location}")

    # --- User Details ---
    y = y - (1.2 * inch)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Attendee Details")
    
    c.setFont("Helvetica", 12)
    c.drawString(margin + (0.2 * inch), y - (0.3 * inch), 
                 f"Name: {booking.user.name}")
    c.drawString(margin + (0.2 * inch), y - (0.5 * inch), 
                 f"Email: {booking.user.email}")
    c.drawString(margin + (0.2 * inch), y - (0.7 * inch), 
                 f"Seats Booked: {booking.number_of_seats}")

    # --- Footer ---
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin, margin, "Thank you for booking with EventEase!")
    
    # --- Finish Up ---
    c.showPage()
    c.save()

    # Move the buffer's position to the beginning
    buffer.seek(0)
    return buffer