import { Route, Routes } from 'react-router-dom';
import Error404 from './pages/error404/Error404.jsx';
import Chat from './pages/chat/Chat.jsx';
import Home from './pages/home/Home.jsx';

function App() {
    return (
        <Routes>
            <Route index element={<Home />} />
            <Route path="/chat/:chatId" element={<Chat />} />
            <Route path="*" element={<Error404 />} />
        </Routes>
    );
}

export default App;