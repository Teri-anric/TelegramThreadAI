import { createSlice } from "@reduxjs/toolkit";

const userDataSlice = createSlice({
    name: "userData",
    initialState: () => {
        try {
            const savedUserData = localStorage.getItem("user_data");
            return savedUserData ? JSON.parse(savedUserData) : null;
        } catch (e) {
            return null;
        }
    },
    reducers: {
        setUserData: (state, action) => {
            localStorage.setItem("user_data", JSON.stringify(action.payload));
            return action.payload;
        },
        removeUserData: () => {
            localStorage.removeItem("user_data");
            return null;
        }
    },
});

export const { setUserData, removeUserData } = userDataSlice.actions;

export default userDataSlice.reducer;