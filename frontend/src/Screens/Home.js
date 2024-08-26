import { Link } from "react-router-dom";
import Job from "../Components/Job";
import search from '../Assets/Icons/search.png'
import user from '../Assets/Icons/user.png'
import list from '../Assets/Icons/list.png'
import history from '../Assets/Icons/history.png'



export default function Home(){
    return(
        <div className="w-screen h-screen grid font_montserrat">
            <div className="bg-[#0e2064] border-solid border-b-2 border-b-[#0e2064] w-full h-[4rem] flex justify-center items-center text-white fixed z-50">
                <h1 className="text-xl font-semibold">HOME</h1>
            </div>
            <div className="relative pt-[4rem]">
                
            </div>
            <div className="bg-[#0e2164] w-[90vw] border-solid border-2 border-[#0e2064] h-[4rem] justify-self-center self-end bottom-5 rounded-md fixed grid grid-cols-4 items-stretch">
                <div className="col-span-1 flex justify-center items-center faded-border"><Link><img src={search} width={30} /></Link></div>
                <div className="col-span-1 flex justify-center items-center faded-border"><Link><img src={user} width={30} /></Link></div>
                <div className="col-span-1 flex justify-center items-center faded-border"><Link><img src={list} width={30} /></Link></div>
                <div className="col-span-1 flex justify-center items-center"><Link><img src={history} width={30} /></Link></div>
            </div>


        </div>
    )
}