from app.db.conn import AsyncSession
from app.db.repos.chat import ChatRepository
from app.db.repos.user import UserRepository


class DBReposContext:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.chat_repo = ChatRepository(session)
