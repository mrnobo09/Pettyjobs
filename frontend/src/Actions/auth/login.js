import axios from 'axios'
import { loginSuccess,loginFail} from '../../State/auth/loginSlice';
import backendURL from '../../config';

export const login = (username,password) => async dispatch =>{
    const config = {
        headers :{'Content-Type' : 'application/json'}
    }
    const body = JSON.stringify({username,password})
    try{
        const response = await axios.post(`${backendURL}/auth/jwt/create/`,body,config)
        const config_2 = {
            headers :{
                'Content-Type' : 'application/json',
                'Authorization' : `JWT ${response.data.access}`,
                'Accept' : 'application/json'
            }
        }
        const response_2 = await axios.get(`${backendURL}/auth/users/me/`,config_2)
        const data = {...response.data,user:response_2.data}
        console.log(data)
        dispatch(loginSuccess(data))
        console.log(response.data)
    }catch(err){
        dispatch(loginFail())

        console.log(err)
    }
}