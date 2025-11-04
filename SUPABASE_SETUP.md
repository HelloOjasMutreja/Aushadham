# Supabase Integration Setup Guide

This guide will help you set up Supabase as the database backend for the Aushadham Medical Healthcare Platform.

## Why Supabase?

Supabase provides a modern, scalable PostgreSQL database with:
- Real-time capabilities
- Built-in authentication
- Row Level Security (RLS)
- Automatic API generation
- Easy scaling and backups
- Free tier available

## Prerequisites

1. A Supabase account (sign up at https://supabase.com)
2. Python 3.8 or higher
3. The Aushadham application code

## Step 1: Create a Supabase Project

1. Go to https://supabase.com and sign in
2. Click "New Project"
3. Enter a project name (e.g., "aushadham")
4. Set a secure database password (save this!)
5. Choose a region close to your users
6. Click "Create new project"
7. Wait for the project to be ready (1-2 minutes)

## Step 2: Set Up Database Tables

1. In your Supabase project dashboard, click on "SQL Editor" in the left sidebar
2. Click "New Query"
3. Copy the entire contents of `supabase_schema.sql` from this repository
4. Paste it into the SQL editor
5. Click "Run" to execute the SQL script

This will create three tables:
- `users` - User accounts and authentication
- `saved_questionnaires` - Saved medical questionnaires
- `user_feedback` - User feedback on questionnaires

The script also sets up:
- Indexes for better query performance
- Row Level Security policies
- Foreign key relationships

## Step 3: Get Your Supabase Credentials

1. In your Supabase project dashboard, click on "Settings" (gear icon)
2. Go to "API" section
3. You'll need two keys:
   - **Project URL**: Found under "Project URL" (e.g., `https://xxxxx.supabase.co`)
   - **Anon/Public Key**: Found under "Project API keys" → "anon public"

## Step 4: Configure Environment Variables

1. Copy the `.env.example` file to create a `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Supabase credentials:
   ```env
   # Enable Supabase
   USE_SUPABASE=true
   
   # Supabase Configuration
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   
   # Flask Configuration (keep your existing values or generate new ones)
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   ```

3. **Important**: Never commit your `.env` file to version control! It contains sensitive credentials.

## Step 5: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `supabase` - Supabase Python client
- `postgrest` - PostgreSQL REST client
- All other existing dependencies

## Step 6: Run the Application

Start the Flask application:

```bash
python app.py
```

You should see a message indicating:
```
Using Supabase for database operations
```

If you see this message, congratulations! Your application is now using Supabase.

## Step 7: Test the Integration

Run the test suite to verify everything is working:

```bash
python test_api.py
```

Or test manually using curl:

```bash
# Register a new user
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'
```

## Switching Between SQLAlchemy and Supabase

The application supports both SQLAlchemy (local SQLite/PostgreSQL) and Supabase. To switch:

### To use Supabase:
Set in `.env`:
```env
USE_SUPABASE=true
SUPABASE_URL=your-url
SUPABASE_KEY=your-key
```

### To use SQLAlchemy (local database):
Set in `.env`:
```env
USE_SUPABASE=false
DATABASE_URL=sqlite:///aushadham.db
```

Or remove/comment out the `USE_SUPABASE` variable entirely.

## Monitoring and Management

### View Your Data
1. Go to your Supabase project dashboard
2. Click "Table Editor" to view and manage your data
3. You can see all users, questionnaires, and feedback

### Check Database Performance
1. Click "Database" → "Query Performance"
2. Monitor slow queries and optimize as needed

### Backup Your Data
Supabase automatically backs up your database. You can also:
1. Go to "Database" → "Backups"
2. Create manual backups anytime
3. Download backups for local storage

## Security Best Practices

1. **Never expose your service_role key** - Only use the anon/public key in your application
2. **Use environment variables** - Never hardcode credentials
3. **Enable RLS policies** - Already set up in the schema
4. **Rotate keys regularly** - Generate new API keys periodically
5. **Monitor usage** - Check the Supabase dashboard for unusual activity

## Troubleshooting

### Connection Issues
- Verify your `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check that your Supabase project is running
- Ensure you have internet connectivity

### Database Errors
- Check the Flask application logs for detailed error messages
- Verify the database schema was created correctly
- Check Supabase logs in the dashboard under "Logs" → "Postgres Logs"

### Authentication Issues
- Ensure JWT secrets are set correctly in `.env`
- Verify users are being created in the Supabase dashboard

### Falling Back to SQLAlchemy
If Supabase initialization fails, the application will automatically fall back to SQLAlchemy. Check the logs:
```
Supabase configuration found but initialization failed. Falling back to SQLAlchemy.
```

## Migration from Existing Database

If you have existing data in SQLite or another database:

1. Export your existing data to JSON or CSV
2. Use Supabase's data import feature:
   - Go to "Table Editor"
   - Select a table
   - Click "Insert" → "Import data from CSV"
3. Or write a migration script using both database connections

## Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Support

For issues specific to:
- **Aushadham application**: Open an issue in this repository
- **Supabase platform**: Visit [Supabase Support](https://supabase.com/support)
- **Python client**: Check [supabase-py GitHub](https://github.com/supabase-community/supabase-py)

## Cost Considerations

Supabase offers a free tier that includes:
- 500 MB database space
- 1 GB file storage
- 2 GB bandwidth
- 50,000 monthly active users

For production use with higher traffic, consider upgrading to a paid plan. See [Supabase Pricing](https://supabase.com/pricing) for details.
