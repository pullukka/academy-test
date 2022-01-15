function GetData(result){
    console.log(result.text)
    return(
        <div  className="result" >
        
        
            {result.text}

        </div>
    )

}

export default GetData;