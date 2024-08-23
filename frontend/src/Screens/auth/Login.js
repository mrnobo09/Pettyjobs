import React from "react";
import { useEffect,useState} from "react";
import {useSelector,useDispatch} from 'react-redux'
import BATlogo from '../../Assets/Images/BATlogo.png'
import { login } from "../../Actions/auth/login";

export default function Login(){
    const loginState = useSelector((state)=>state.login)
    const dispatch = useDispatch()
    const [formData,setformData] = useState(
        {
            username:'',
            password:'',
        }
    )

    const {username,password} = formData

    const onChange = e=> setformData({...formData,[e.target.name]:e.target.value})

    const handleSubmit =async (e) =>{
        e.preventDefault()
        await dispatch(login(username,password))
        console.log(loginState)
    }
    return(
        <div className="w-screen h-screen bg-[#ffffff] grid justify-center items-center">
            <div className = "w-[80vw] h-[50vh] grid items-center">
                <img className="justify-self-center self-center w-[18rem] square" src={BATlogo}/>
                    <form onSubmit={handleSubmit} className = "grid grid-flow-row gap-2 w-full max-w-[30rem] justify-self-center">
                        <input onChange={onChange} name='username' value={username} className="p-2 w-full bg-transparent border-solid border-b-2 border-[#002667] active:bg-transparent focus:outline-none focus:border-[#6394e7] transition duration-300 ease-in-out" type="name" name="username" placeholder="Username"></input>
                        <input onChange={onChange} name='password' value={password} className="p-2 w-full bg-transparent border-solid border-b-2 border-[#002667] active:bg-transparent focus:outline-none focus:border-[#6394e7] transition duration-300 ease-in-out" type="password" name="password" placeholder="Password"></input>
                        <button className="bg-[#002667] h-[3rem] rounded-md hover:bg-[#0040af] text-white" type="submit">Login</button>
                    </form>
            </div>
            
        </div>
    );
}