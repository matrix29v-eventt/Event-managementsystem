from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment="Event Management System ER Diagram", format="png")

# Entities (tables)
dot.node("Client", "Client\n(id, name, email, phone)")
dot.node("Venue", "Venue\n(id, name, location, capacity)")
dot.node("Vendor", "Vendor\n(id, name, service_type, contact)")
dot.node("Event", "Event\n(id, name, date, client_id, venue_id)")
dot.node("Booking", "Booking\n(id, event_id, vendor_id, service_cost)")
dot.node("Payment", "Payment\n(id, event_id, booking_id, amount, method, status, date)")

# Relationships
dot.edge("Client", "Event", label="1 : N")
dot.edge("Venue", "Event", label="1 : N")
dot.edge("Event", "Booking", label="1 : N")
dot.edge("Vendor", "Booking", label="1 : N")
dot.edge("Event", "Payment", label="1 : N")
dot.edge("Booking", "Payment", label="0..1 : N")

# Save & render ER diagram
dot.render("diagrams/er_diagram", view=True)
