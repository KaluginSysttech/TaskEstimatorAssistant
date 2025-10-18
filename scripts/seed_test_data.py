"""Script to seed test data for dashboard testing."""

import asyncio
from datetime import datetime, timedelta
import random
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.db.models import Base, User, Message
from src.config.settings import Settings


async def seed_test_data():
    """Seed database with test data."""
    
    settings = Settings()
    engine = create_async_engine(settings.database_url, echo=True)
    
    # Create async session factory
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    print("[SEED] Seeding test data...")
    
    async with async_session() as session:
        try:
            # Create test users
            users_data = [
                (100001, "alice_dev"),
                (100002, "bob_tester"),
                (100003, "charlie_user"),
                (100004, "diana_admin"),
                (100005, "eve_customer"),
                (100006, "frank_support"),
                (100007, "grace_team"),
                (100008, "henry_qa"),
                (100009, "ivy_manager"),
                (100010, "jack_engineer"),
            ]
            
            users = []
            for telegram_id, username in users_data:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    is_deleted=False
                )
                session.add(user)
                users.append(user)
            
            await session.flush()
            print(f"[OK] Created {len(users)} test users")
            
            # Create messages for the last 30 days
            now = datetime.utcnow()
            total_messages = 0
            
            for day_offset in range(30):
                # Date for this iteration
                current_date = now - timedelta(days=29 - day_offset)
                
                # More messages on weekdays, less on weekends
                is_weekend = current_date.weekday() >= 5
                base_messages = 50 if not is_weekend else 30
                
                # Random variation
                num_messages = random.randint(base_messages, base_messages + 50)
                
                for _ in range(num_messages):
                    # Random user
                    user = random.choice(users)
                    
                    # Random hour (more activity during day)
                    hour_weights = [2 if 8 <= h < 22 else 1 for h in range(24)]
                    hour = random.choices(range(24), weights=hour_weights)[0]
                    
                    # Random minute
                    minute = random.randint(0, 59)
                    
                    message_time = current_date.replace(
                        hour=hour,
                        minute=minute,
                        second=random.randint(0, 59),
                        microsecond=0
                    )
                    
                    # Create user message
                    user_message = Message(
                        user_id=user.id,
                        role="user",
                        content=random.choice([
                            "Hello! How can I use this bot?",
                            "What features are available?",
                            "Can you help me with something?",
                            "Show me statistics",
                            "Tell me about your capabilities",
                            "How do I get started?",
                            "What's the weather like?",
                            "Help me understand this feature",
                            "Can you explain how this works?",
                            "I need assistance with a task",
                        ]),
                        content_length=50,
                        created_at=message_time,
                        is_deleted=False
                    )
                    session.add(user_message)
                    
                    # Create assistant response (a bit later)
                    response_time = message_time + timedelta(seconds=random.randint(2, 10))
                    assistant_message = Message(
                        user_id=user.id,
                        role="assistant",
                        content=random.choice([
                            "I'd be happy to help! Let me explain...",
                            "Sure! Here's what you need to know...",
                            "Great question! The answer is...",
                            "Let me show you how that works...",
                            "I can definitely assist you with that...",
                            "Here's the information you requested...",
                            "That's a common question. Here's the answer...",
                            "I understand. Let me clarify...",
                            "Perfect! Here's what I recommend...",
                            "Absolutely! Let me walk you through this...",
                        ]),
                        content_length=80,
                        created_at=response_time,
                        is_deleted=False
                    )
                    session.add(assistant_message)
                    total_messages += 2
            
            await session.commit()
            print(f"[OK] Created {total_messages} test messages over 30 days")
            
            # Print summary
            print("\n[SUMMARY] Test Data Summary:")
            print(f"   Users: {len(users)}")
            print(f"   Messages: {total_messages}")
            print(f"   Date range: {(now - timedelta(days=29)).strftime('%Y-%m-%d')} to {now.strftime('%Y-%m-%d')}")
            print(f"\n[OK] Database seeded successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f"[ERROR] Error seeding data: {e}")
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_test_data())

