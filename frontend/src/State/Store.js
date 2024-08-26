import {configureStore} from '@reduxjs/toolkit'
import loginReducer from './auth/loginSlice'
const initialState = {

}

const Store = configureStore(
    {
        reducer:{
            login:loginReducer
        },
    }
)

export default Store