import { api } from "../services/api";
import { useDispatch } from "react-redux";
import { setUserData, removeUserData } from "../store/userData";

export const useTelegramLogin = () => {
  const dispatch = useDispatch();

  const TelegramLogin = {
    init: function(options) {
      window.Telegram.Login.init(options, function(user) {
        if (user) {
          TelegramLogin.auth(user);
        }
      });
    },

    open: async function() {
      window.Telegram.Login.open();
    },

    auth: async function(user) {
      const auth_data = JSON.stringify(user)
      const data = await api.login(auth_data);
      if (data.status === 200) {
        dispatch(setUserData(data));
        console.log("Login successful");
      } else {
        console.log("Login failed");
      }
    },

    logOut: function () {
      api.logout();
      dispatch(removeUserData());
    }
  };

  return TelegramLogin;
}