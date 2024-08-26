// loginSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
    access: null,
    refresh: null,
    isAuthenticated: localStorage.getItem('access') ? true:false,
    user: null,
};

const loginSlice = createSlice({
    name: "login",
    initialState,
    reducers: {
        loginSuccess(state, action) {
            const access = action.payload.access_token;
            const refresh = action.payload.refresh_token;
            const user = action.payload.user_data;
            localStorage.setItem('access', access);
            localStorage.setItem('refresh', refresh);
            
            state.access = access;
            state.refresh = refresh;
            state.user = user;
            state.isAuthenticated = true;
        },
        loginFail(state) {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            
            state.access = null;
            state.refresh = null;
            state.user = null;
            state.isAuthenticated = false;
        },
        logout(state) {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            
            state.access = null;
            state.refresh = null;
            state.user = null;
            state.isAuthenticated = false;
        }
    }
});


export const { loginSuccess,loginFail,logout } = loginSlice.actions;
export default loginSlice.reducer;
