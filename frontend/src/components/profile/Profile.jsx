import { useTelegramLogin } from "../../utils/useTelegramLogin";
import { useSelector } from "react-redux";
import { BOT_ID } from "../../config";

const Profile = () => {
    const userData = useSelector(state => state.userData);
    const TelegramLogin = useTelegramLogin();

    TelegramLogin.init({
        bot_id: BOT_ID,    
        request_access: "write",
    });

    return <div>
        {userData ? ( 
            <>
                <p>User: {userData.first_name}</p>
                <button onClick={() => TelegramLogin.logOut()}>Logout</button>
            </>
        ) : (
            <>
                <button onClick={() => TelegramLogin.open()}>Login</button>
            </>
        )}
    </div>;
};

export default Profile;
