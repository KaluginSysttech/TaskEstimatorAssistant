"""FastAPI routes for chat API."""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_chat_handler, get_chat_repository
from src.api.models import ChatMessageRequest, ChatMessageResponse
from src.chat.chat_handler import ChatHandler
from src.db.repository import ChatRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post(
    "/chat/message",
    response_model=ChatMessageResponse,
    summary="Send a chat message",
    description="""
    Send a message to the chat and receive a response.
    
    Supports two modes:
    - **normal**: Regular conversation with LLM assistant
    - **admin**: Statistics queries with mock responses
    
    The session_id should be a UUID generated on the client side.
    History is automatically retrieved from the database.
    """,
    responses={
        200: {
            "description": "Successful response with assistant's reply",
            "content": {
                "application/json": {
                    "example": {
                        "response": "Привет! Я AI-ассистент для помощи с оценкой задач.",
                        "mode": "normal",
                        "timestamp": "2025-10-17T16:30:00Z"
                    }
                }
            }
        },
        400: {
            "description": "Invalid request (empty message, invalid mode, etc.)",
        },
        500: {
            "description": "Internal server error (LLM error, database error, etc.)",
        }
    }
)
async def send_chat_message(
    request: ChatMessageRequest,
    chat_handler: ChatHandler = Depends(get_chat_handler),
    chat_repo: ChatRepository = Depends(get_chat_repository),
) -> ChatMessageResponse:
    """
    Process a chat message and return a response.
    
    Args:
        request: Chat message request with message, mode, and session_id
        chat_handler: Injected chat handler
        chat_repo: Injected chat repository
        
    Returns:
        ChatMessageResponse: Response with assistant's reply
        
    Raises:
        HTTPException: 400 if request is invalid, 500 if processing fails
    """
    logger.info(
        f"Received chat message: mode={request.mode}, "
        f"session_id={request.session_id}, "
        f"message_length={len(request.message)}"
    )
    
    try:
        # Get chat history from database
        history = await chat_repo.get_chat_history(
            session_id=request.session_id,
            limit=20  # Last 20 messages
        )
        logger.debug(f"Retrieved {len(history)} messages from history")
        
        # Save user message to database
        await chat_repo.add_chat_message(
            session_id=request.session_id,
            role="user",
            content=request.message,
            mode=request.mode,
        )
        logger.debug("Saved user message to database")
        
        # Process message through handler
        response_text = await chat_handler.handle_message(
            message=request.message,
            mode=request.mode,
            history=history,
        )
        
        # Save assistant response to database
        await chat_repo.add_chat_message(
            session_id=request.session_id,
            role="assistant",
            content=response_text,
            mode=request.mode,
        )
        logger.debug("Saved assistant response to database")
        
        logger.info(f"Successfully processed chat message: response_length={len(response_text)}")
        
        return ChatMessageResponse(
            response=response_text,
            mode=request.mode,
            timestamp=datetime.utcnow(),
        )
        
    except ValueError as e:
        # Invalid mode or other validation error
        logger.error(f"Validation error processing chat message: {e}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # Unexpected error
        logger.error(f"Error processing chat message: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message. Please try again."
        )

