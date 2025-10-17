"""Script to check database data for last week."""

import asyncio
from datetime import datetime, timedelta
from src.config.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def check_data():
    """Check database data for last week."""
    
    settings = Settings()
    engine = create_async_engine(settings.database_url)
    
    # Calculate week ago
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    async with engine.connect() as conn:
        # Top users for last week
        result = await conn.execute(text('''
            SELECT u.username, u.telegram_id, COUNT(m.id) as msg_count 
            FROM users u 
            JOIN messages m ON u.id = m.user_id 
            WHERE u.is_deleted = false 
              AND m.is_deleted = false 
              AND m.created_at >= :week_ago
            GROUP BY u.id, u.username, u.telegram_id 
            ORDER BY COUNT(m.id) DESC 
            LIMIT 5
        '''), {'week_ago': week_ago})
        rows = result.fetchall()
        print(f'[Database Top Users for Last Week (since {week_ago.strftime("%Y-%m-%d %H:%M")}):]')
        for row in rows:
            print(f'  {row.username} (telegram_id={row.telegram_id}): {row.msg_count} messages')
        
        # All users total
        print('\n[All Users Total (all time):]')
        result = await conn.execute(text('''
            SELECT u.username, COUNT(m.id) as msg_count 
            FROM users u 
            JOIN messages m ON u.id = m.user_id 
            WHERE u.is_deleted = false AND m.is_deleted = false 
            GROUP BY u.id, u.username 
            ORDER BY u.username
        '''))
        rows = result.fetchall()
        for row in rows:
            print(f'  {row.username}: {row.msg_count} messages')
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_data())

