# Migrating Existing Data to Supabase

This guide helps you migrate your existing Aushadham data from SQLite/PostgreSQL to Supabase.

## Prerequisites

- Existing Aushadham database with data
- Supabase project set up (see [SUPABASE_SETUP.md](SUPABASE_SETUP.md))
- Python environment with required packages

## Migration Strategy

There are two approaches to migrate your data:

### Option 1: Manual Export/Import (Recommended for Small Datasets)

Best for databases with less than 1000 records.

#### Step 1: Export Data from SQLite

```python
# export_data.py
import sqlite3
import json

def export_database(db_path='aushadham.db'):
    """Export all data from SQLite to JSON"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    data = {}
    
    # Export users
    cursor.execute("SELECT * FROM users")
    data['users'] = [dict(row) for row in cursor.fetchall()]
    
    # Export questionnaires
    cursor.execute("SELECT * FROM saved_questionnaires")
    data['questionnaires'] = [dict(row) for row in cursor.fetchall()]
    
    # Export feedback
    cursor.execute("SELECT * FROM user_feedback")
    data['feedback'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    # Save to JSON
    with open('database_export.json', 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"Exported {len(data['users'])} users")
    print(f"Exported {len(data['questionnaires'])} questionnaires")
    print(f"Exported {len(data['feedback'])} feedback entries")

if __name__ == '__main__':
    export_database()
```

Run the export:
```bash
python export_data.py
```

#### Step 2: Import Data to Supabase

```python
# import_data.py
import json
import os
from dotenv import load_dotenv
from supabase_service import SupabaseService

load_dotenv()

def import_database(json_file='database_export.json'):
    """Import data from JSON to Supabase"""
    
    # Initialize Supabase
    service = SupabaseService(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Load data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    print("Starting import...")
    
    # Import users (preserve IDs)
    for user in data['users']:
        try:
            # Insert with specific ID
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'password_hash': user['password_hash'],
                'full_name': user.get('full_name'),
                'phone': user.get('phone'),
                'created_at': user['created_at']
            }
            service.client.table('users').insert(user_data).execute()
            print(f"✓ Imported user: {user['username']}")
        except Exception as e:
            print(f"✗ Failed to import user {user['username']}: {e}")
    
    # Import questionnaires
    for quest in data['questionnaires']:
        try:
            quest_data = {
                'id': quest['id'],
                'user_id': quest['user_id'],
                'session_id': quest['session_id'],
                'symptom': quest['symptom'],
                'initial_description': quest.get('initial_description'),
                'answers': json.loads(quest['answers']) if isinstance(quest['answers'], str) else quest['answers'],
                'report': json.loads(quest['report']) if isinstance(quest['report'], str) else quest['report'],
                'severity': quest.get('severity'),
                'created_at': quest['created_at']
            }
            service.client.table('saved_questionnaires').insert(quest_data).execute()
            print(f"✓ Imported questionnaire: {quest['session_id']}")
        except Exception as e:
            print(f"✗ Failed to import questionnaire {quest['session_id']}: {e}")
    
    # Import feedback
    for fb in data['feedback']:
        try:
            fb_data = {
                'id': fb['id'],
                'user_id': fb['user_id'],
                'questionnaire_id': fb.get('questionnaire_id'),
                'rating': fb.get('rating'),
                'comment': fb.get('comment'),
                'feedback_type': fb.get('feedback_type'),
                'created_at': fb['created_at']
            }
            service.client.table('user_feedback').insert(fb_data).execute()
            print(f"✓ Imported feedback: {fb['id']}")
        except Exception as e:
            print(f"✗ Failed to import feedback {fb['id']}: {e}")
    
    print("\nImport complete!")

if __name__ == '__main__':
    import_database()
```

Run the import:
```bash
python import_data.py
```

### Option 2: Direct Database Migration (For Larger Datasets)

Best for databases with 1000+ records.

#### Step 1: Install Migration Tool

```bash
pip install sqlalchemy-migrate
```

#### Step 2: Create Migration Script

```python
# migrate_direct.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from supabase_service import SupabaseService

load_dotenv()

def migrate_table(source_engine, dest_service, table_name, id_col='id'):
    """Migrate a single table"""
    print(f"\nMigrating {table_name}...")
    
    # Read from source
    with source_engine.connect() as conn:
        result = conn.execute(f"SELECT * FROM {table_name}")
        rows = result.fetchall()
        columns = result.keys()
    
    # Write to destination
    success = 0
    failed = 0
    
    for row in rows:
        try:
            data = dict(zip(columns, row))
            dest_service.client.table(table_name).insert(data).execute()
            success += 1
        except Exception as e:
            print(f"Failed to migrate row {data.get(id_col)}: {e}")
            failed += 1
    
    print(f"✓ Migrated {success} rows, {failed} failed")

def main():
    # Connect to source database
    source_url = os.getenv('DATABASE_URL', 'sqlite:///aushadham.db')
    source_engine = create_engine(source_url)
    
    # Connect to Supabase
    dest_service = SupabaseService(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    # Migrate tables
    migrate_table(source_engine, dest_service, 'users')
    migrate_table(source_engine, dest_service, 'saved_questionnaires')
    migrate_table(source_engine, dest_service, 'user_feedback')
    
    print("\n✓ Migration complete!")

if __name__ == '__main__':
    main()
```

Run the migration:
```bash
python migrate_direct.py
```

## Post-Migration Checklist

1. **Verify Data Integrity**
   - Check row counts match
   - Verify foreign key relationships
   - Test authentication with existing users

2. **Test Application**
   ```bash
   # Set Supabase environment
   export USE_SUPABASE=true
   
   # Run tests
   python test_api.py
   ```

3. **Backup Old Database**
   ```bash
   cp aushadham.db aushadham.db.backup
   ```

4. **Update Environment**
   Update your `.env` file:
   ```env
   USE_SUPABASE=true
   SUPABASE_URL=your-url
   SUPABASE_KEY=your-key
   ```

5. **Monitor Performance**
   - Check Supabase dashboard for query performance
   - Monitor API response times
   - Watch for any errors in logs

## Rollback Plan

If you need to rollback to SQLite:

1. Set environment:
   ```env
   USE_SUPABASE=false
   DATABASE_URL=sqlite:///aushadham.db
   ```

2. Restore backup if needed:
   ```bash
   cp aushadham.db.backup aushadham.db
   ```

3. Restart application

## Common Migration Issues

### Issue: ID Sequence Mismatch

**Problem**: Auto-increment IDs don't match after import

**Solution**: Reset PostgreSQL sequences in Supabase SQL Editor:
```sql
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('saved_questionnaires_id_seq', (SELECT MAX(id) FROM saved_questionnaires));
SELECT setval('user_feedback_id_seq', (SELECT MAX(id) FROM user_feedback));
```

### Issue: JSON Field Errors

**Problem**: JSON fields not importing correctly

**Solution**: Ensure JSON is properly formatted:
```python
import json
# Convert string to JSON
if isinstance(data['answers'], str):
    data['answers'] = json.loads(data['answers'])
```

### Issue: Foreign Key Violations

**Problem**: Child records reference non-existent parent records

**Solution**: 
1. Import users first
2. Import questionnaires second
3. Import feedback last

### Issue: Duplicate Key Errors

**Problem**: Records with same ID already exist

**Solution**: Clear Supabase tables before import:
```sql
TRUNCATE users, saved_questionnaires, user_feedback CASCADE;
```

## Performance Tips

1. **Batch Inserts**: For large datasets, insert in batches of 100-1000 records
2. **Disable Triggers**: Temporarily disable triggers during migration if needed
3. **Parallel Processing**: Use Python's `multiprocessing` for very large datasets
4. **Monitor Progress**: Add progress bars using `tqdm`:
   ```python
   from tqdm import tqdm
   for row in tqdm(rows):
       # import row
   ```

## Testing the Migration

Run comprehensive tests after migration:

```bash
# Test with Supabase backend
export USE_SUPABASE=true
python test_api.py

# Run integration tests
python test_supabase_integration.py
```

## Getting Help

- Check Supabase logs: Dashboard → Logs → Postgres Logs
- Review application logs for errors
- Test specific endpoints with curl
- Consult [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for troubleshooting

## Next Steps

After successful migration:

1. Set up regular backups in Supabase
2. Configure monitoring and alerts
3. Review and optimize database indexes
4. Consider enabling Point-in-Time Recovery (PITR)
5. Update deployment configurations

Congratulations! Your data is now in Supabase. 🎉
