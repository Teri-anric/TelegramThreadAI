import { useParams } from 'react-router-dom';

const Chat = () => {
    const { chatId } = useParams();

    return (
        <div>
            <h1>Chat {chatId}</h1>
        </div>
    );
}

export default Chat;