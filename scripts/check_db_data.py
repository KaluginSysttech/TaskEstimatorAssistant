"""Script to check database data."""

import asyncio
from src.config.settings import Settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def check_data():
    """Check database data."""
    
    settings = Settings()
    engine = create_async_engine(settings.database_url)
    
    async with engine.connect() as conn:
        # Top users
        result = await conn.execute(text('''
            SELECT u.username, u.telegram_id, COUNT(m.id) as msg_count 
            FROM users u 
            JOIN messages m ON u.id = m.user_id 
            WHERE u.is_deleted = false AND m.is_deleted = false 
            GROUP BY u.id, u.username, u.telegram_id 
            ORDER BY COUNT(m.id) DESC 
            LIMIT 5
        '''))
        rows = result.fetchall()
        print('[Database Top Users:]')
        for row in rows:
            print(f'  {row.username} (telegram_id={row.telegram_id}): {row.msg_count} messages')
        
        # Recent conversations
        print('\n[Recent Conversations:]')
        result = await conn.execute(text('''
            SELECT u.username, u.telegram_id, 
                   MIN(m.created_at) as first_msg, 
                   MAX(m.created_at) as last_msg,
                   COUNT(m.id) as msg_count 
            FROM users u 
            JOIN messages m ON u.id = m.user_id 
            WHERE u.is_deleted = false AND m.is_deleted = false 
            GROUP BY u.id, u.username, u.telegram_id 
            ORDER BY MAX(m.created_at) DESC 
            LIMIT 5
        '''))
        rows = result.fetchall()
        for row in rows:
            print(f'  {row.username}: {row.msg_count} messages (last: {row.last_msg})')
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_data())

