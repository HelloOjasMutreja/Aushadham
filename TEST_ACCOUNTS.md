# Test User Accounts

This document lists the pre-configured test user accounts available for testing the Aushadham platform.

## Available Test Accounts

### Test User 1
- **Username:** `testuser1`
- **Email:** `testuser1@example.com`
- **Password:** `password123`
- **Full Name:** Test User One
- **Phone:** 1234567890

### Test User 2
- **Username:** `testuser2`
- **Email:** `testuser2@example.com`
- **Password:** `password123`
- **Full Name:** Test User Two
- **Phone:** 9876543210

### Demo User
- **Username:** `demouser`
- **Email:** `demo@aushadham.com`
- **Password:** `demo123`
- **Full Name:** Demo User
- **Phone:** 5555555555

## Creating Test Users

To seed these test accounts in your database, run:

```bash
python seed_test_users.py
```

This script will:
- Create the test users if they don't exist
- Skip users that already exist
- Display a summary of all users in the database

## Using Test Accounts

You can log in with any of these accounts using either:
- The username (e.g., `testuser1`)
- The email address (e.g., `testuser1@example.com`)

Both login methods work with the corresponding password.

## Notes

- These accounts are for **testing purposes only**
- Do not use these accounts in production environments
- Passwords are intentionally simple for testing convenience
- The `seed_test_users.py` script is safe to run multiple times (it won't create duplicates)
