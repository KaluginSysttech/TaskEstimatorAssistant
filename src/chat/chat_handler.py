"""Handler for web chat messages."""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.chat.admin_handler import AdminHandler
    from src.llm.llm_client import LLMClient

logger = logging.getLogger(__name__)


class ChatHandler:
    """
    Handler for processing chat messages from web interface.

    Routes messages to appropriate handler based on mode:
    - normal: Delegates to LLMClient for conversational responses
    - admin: Delegates to AdminHandler for statistics queries
    """

    def __init__(
        self,
        llm_client: "LLMClient",
        admin_handler: "AdminHandler",
        max_history_messages: int = 20,
    ) -> None:
        """
        Initialize chat handler.

        Args:
            llm_client: Client for LLM interactions
            admin_handler: Handler for admin mode queries
            max_history_messages: Maximum number of history messages to include in context
        """
        self.llm_client = llm_client
        self.admin_handler = admin_handler
        self.max_history_messages = max_history_messages
        logger.info("ChatHandler initialized")

    async def handle_message(
        self,
        message: str,
        mode: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Process a chat message and return a response.

        Args:
            message: User message text
            mode: Chat mode ("normal" or "admin")
            history: Conversation history

        Returns:
            Response text from appropriate handler

        Raises:
            ValueError: If mode is invalid
        """
        logger.info(f"Processing chat message in mode: {mode}")
        logger.debug(f"Message: {message}")

        if history is None:
            history = []

        # Limit history to max_history_messages
        if len(history) > self.max_history_messages:
            history = history[-self.max_history_messages :]
            logger.debug(f"Limited history to last {self.max_history_messages} messages")

        try:
            if mode == "normal":
                # Normal mode: use LLM client
                logger.info("Routing to LLM client (normal mode)")
                response = await self.llm_client.get_response(message, history=history)

            elif mode == "admin":
                # Admin mode: use admin handler
                logger.info("Routing to admin handler (admin mode)")
                response = await self.admin_handler.handle_admin_query(message, history=history)

            else:
                raise ValueError(f"Invalid chat mode: {mode}. Must be 'normal' or 'admin'")

            logger.info(f"Successfully processed message in {mode} mode")
            return response

        except Exception as e:
            logger.error(f"Error handling chat message in {mode} mode: {e}", exc_info=True)
            raise

