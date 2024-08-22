import React from "react";
import { useEffect } from "react";
import BATlogo from '../../Assets/Images/BATlogo.png'

export default function Login(){
    useEffect(()=>{
        console.log("Hello World")
    },[])
    return(
        <div className="w-screen h-screen bg-[#002667] grid justify-center items-center">
            <div className = "w-[80vw] h-[50vh] grid items-center">
                <img className="justify-self-center self-center w-[18rem] square" src={BATlogo}/>
                    <form className = "grid grid-flow-row gap-2 w-full max-w-[30rem] justify-self-center">
                        <input className="p-2 bg-white w-full border-solid border-b-2 border-[#002667] active:bg-transparent focus:outline-none focus:border-[#6394e7] transition duration-300 ease-in-out" type="name" name="username" placeholder="Username"></input>
                        <input className="p-2 w-full bg-white border-solid border-b-2 border-[#002667] active:bg-transparent focus:outline-none focus:border-[#6394e7] transition duration-300 ease-in-out" type="password" name="password" placeholder="Password"></input>
                        <button className="bg-[#ffbb00] h-[3rem] rounded-md hover:bg-[#0040af] text-white" type="submit">Login</button>
                    </form>
            </div>
            
        </div>
    );
}