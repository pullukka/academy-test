import axios from 'axios';
 
import React,{Component} from 'react';
/* import { render } from 'react-dom';
import GetData from './components/GetData'; */
 
class App extends Component {
  
    state = {
 
      // Initially, no file is selected
      selectedFile: null,
      Result:null
    };
    
    // On file select (from the pop up)
    onFileChange = event => {
    
      // Update the state
      this.setState({ selectedFile: event.target.files[0] });
    
    };
    
    // On file upload (click the upload button) wait for response
    onFileUpload = async () => {
    
      async function test(dataFromForm) 
        {
          let UploadResult = axios.post("http://localhost:63121/upload", dataFromForm)

          console.log(await UploadResult)
          console.log(await (await UploadResult).data)

          
            
          return (
            <div>
              <h2>File Details:</h2>
              <p>File Name: {await UploadResult }</p>
            </div>
          );
        }
       
    
      // Create an object of formData
      const formData = new FormData();
    
      // Update the formData object
      formData.append(
        "file",
        this.state.selectedFile,
        this.state.selectedFile.name
      );

      
      // https://zetcode.com/javascript/axios/
      // Request made to the backend api
      // Send formData object and catch response
      
      await test(formData)
      

    };

    
   
    // echo file details
    fileData = () => {
    
      if (this.state.selectedFile) {

        return (
          <div>
            <h2>File Details:</h2>
            <p>File Name: {this.state.selectedFile.name}</p>
          </div>
        );
      }
    };
    
    render() {
    
      return (
        <div>
            <h1>
              Upload csv records
            </h1>

          <form method="POST" encType="multipart/form-data" onSubmit={this.handleSubmit}></form>
          
        <input type="file" id="file" name="FileN" accept="results/csv" onChange={ this.onFileChange}></input>
        <button type="submit" onClick={ this.onFileUpload}>
                  Upload!
                </button>
                {this.fileData()}
                

        </div>
      );
        

    }


    
  }

 
 
  export default App;