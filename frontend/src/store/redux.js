import { configureStore } from "@reduxjs/toolkit";
import userDataReducer from "./userData";

const store = configureStore({
    reducer: {
        userData: userDataReducer,
    }
});

export default store;   