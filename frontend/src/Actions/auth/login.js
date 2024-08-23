import axios from 'axios'
import { loginSuccess} from '../../State/auth/loginSlice';
import backendURL from '../../config';

export const login = (username,password) => async dispatch =>{
    const config = {
        headers :{'Content-Type' : 'application/json'}
    }
    const body = JSON.stringify({username,password})

    try{
        const response = await axios.post(`${backendURL}/auth/jwt/create/`,body,config)
        dispatch(loginSuccess(response.data))
        console.log(response.data)
    }catch(err){
        //dispatch(loginFail())

        console.log(err)
    }
}