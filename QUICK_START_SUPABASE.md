# Quick Start Guide - Supabase Integration

This is a quick reference guide to get started with Supabase integration for the Aushadham platform.

## 🚀 5-Minute Setup

### Step 1: Create Supabase Project (2 minutes)
1. Go to https://supabase.com
2. Sign up/Sign in
3. Click "New Project"
4. Fill in details and create

### Step 2: Setup Database (1 minute)
1. In Supabase dashboard, go to "SQL Editor"
2. Copy-paste the SQL from `supabase_schema.sql`
3. Click "Run"

### Step 3: Configure Environment (1 minute)
1. Copy `.env.example` to `.env`
2. Get your credentials from Supabase (Settings → API)
3. Update `.env`:
```env
USE_SUPABASE=true
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-anon-key
```

### Step 4: Run Application (1 minute)
```bash
pip install -r requirements.txt
python app.py
```

Done! Your app is now using Supabase! 🎉

## 📊 What Gets Stored in Supabase?

- **Users** - All user accounts and authentication data
- **Questionnaires** - Saved medical questionnaires with answers
- **Feedback** - User ratings and comments
- **Sessions** - Active questionnaire sessions

## 🔄 Switching Backends

### Use Supabase:
```env
USE_SUPABASE=true
```

### Use Local SQLite:
```env
USE_SUPABASE=false
# or just remove the line
```

## ✅ Verify It's Working

Check the application logs when starting:
- Supabase: `INFO:__main__:Using Supabase for database operations`
- SQLAlchemy: `INFO:__main__:Using SQLAlchemy for database operations`

## 🧪 Testing

Run the test suite:
```bash
python test_api.py
```

The tests work with both backends automatically!

## 📚 More Information

- Full setup guide: [SUPABASE_SETUP.md](SUPABASE_SETUP.md)
- API documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Main README: [README.md](README.md)

## 🆘 Common Issues

**Issue**: "Supabase configuration found but initialization failed"
- **Solution**: Check your `SUPABASE_URL` and `SUPABASE_KEY` in `.env`

**Issue**: Tables don't exist
- **Solution**: Run the SQL from `supabase_schema.sql` in Supabase SQL Editor

**Issue**: Can't connect to Supabase
- **Solution**: Check your internet connection and Supabase project status

## 💰 Pricing

Supabase free tier includes:
- 500 MB database
- 1 GB storage
- 2 GB bandwidth
- 50,000 monthly active users

Perfect for development and small production deployments!

## 🔒 Security Tips

1. Never commit `.env` file to git
2. Use environment variables in production
3. Rotate API keys regularly
4. Enable Row Level Security (RLS) - already done in schema!
5. Monitor usage in Supabase dashboard

## 🎯 Next Steps

1. Customize the schema for your needs
2. Add more tables as needed
3. Set up monitoring and alerts
4. Configure backups
5. Deploy to production

Happy coding! 🚀
