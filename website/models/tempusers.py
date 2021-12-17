from website.models.master import Model

# how will temporary users work?

# temporary users are not authenticated,
# they are invited by a superadministrator via qrcode.
# generating qr code page requires user_id and queue_id
# superadmin selects a queue to add a temporary user, then
# temporary user is generated and ticket is created.

# temporary user receives the ticket and can visit the temporary page
# ticket will expire

# how will super transmit ticket items?
# do temp users need to be in the database?