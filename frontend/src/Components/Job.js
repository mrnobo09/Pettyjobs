import React from "react"
export default function Job(){
    return(
        <div className="relative w-full h-[8rem] p-2 grid grid-cols-4 border-solid border-t-2 border-b-2 ">
            <div class="self-center col-span-1">
                <img src="https://placehold.co/100" width={100}/>
            </div>
            <div className="col-span-3 ml-2">
                <h1 className="text-xl font-semibold">Job Lorem Ipsum</h1>
                <p>Lorem askdjasnf asjfnasfasnfs afjkasfkas asfjasfkasj</p>
            </div>
        </div>
    )
}