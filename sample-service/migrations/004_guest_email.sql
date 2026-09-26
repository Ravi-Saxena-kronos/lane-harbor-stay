-- Applied in staging; API not yet updated (release-gate drift fixture).
ALTER TABLE reservations ADD COLUMN guest_email VARCHAR(255) NOT NULL DEFAULT '';
