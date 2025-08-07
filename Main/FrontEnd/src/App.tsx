import './App.css'
import {ChangeEvent, useState} from "react";
import axios from "axios";

function App() {

    const [file, setFile] = useState<string | undefined>();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [fileUploaded, setFileUploaded] = useState<boolean>(false);
    const [animationGenerated, setAnimationGenerated] = useState<boolean>(false);


    //Set image file to the browser only--------------------------------------------------------------------------------
    function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
        setSelectedFile(e.target.files? e.target.files[0] : null)
        setFile(URL.createObjectURL(e.target.files ? e.target.files[0] : undefined));
    }
    //------------------------------------------------------------------------------------------------------------------


    



    //Uploads image to the backend server-------------------------------------------------------------------------------
    async function handleUploadImage() {
        if (!selectedFile) {
            window.alert("Please upload an image");
            return;
        }

        try {
            const formData: FormData = new FormData();
            formData.append("file", selectedFile);
            const response = await axios.post("http://127.0.0.1:5000/api/upload-file", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setFileUploaded(true);
            console.log(response.data);
        } catch (error: unknown) {
            console.error("Error uploading the image:", error);
        }
    }
    //------------------------------------------------------------------------------------------------------------------






    //Generates animation-----------------------------------------------------------------------------------------------
    async function handleGenerateAnimation() {
        if (!fileUploaded) {
            window.alert("Please upload an image");
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:5000/api/generate-animation");
            alert(`Python: ${response.data.output}`);
            console.log("Output:", response.data.output);
        } catch (error: unknown) {
            console.error("Error: ", error);npm
        }
        setAnimationGenerated(true);
    }
    //------------------------------------------------------------------------------------------------------------------






    //Shows animation---------------------------------------------------------------------------------------------------
    async function handleShowAnimation() {
        if (!fileUploaded) {
            window.alert("Please upload an image");
            return;
        }

        try {
            const response = await axios.post("http://127.0.0.1:5000/api/show-animation");
            alert(`Python: ${response.data.output}`);
            console.log("Output:", response.data.output);
        } catch (error: unknown) {
            console.error("Error: ", error);npm
        }
    }
    //------------------------------------------------------------------------------------------------------------------






    return (
        <div className={"container"}>
            <div className="img-container">
                {
                    file ?
                        <img src={file} alt=""/>
                        :
                        <p>No Image Selected</p>
                }
            </div>
            <div className={"file-container"}>
                <p>
                    {
                        selectedFile? selectedFile.name : "No Image Selected"
                    }
                </p>
                <label htmlFor={"fileInput"} className={"custom-file-upload-btn"}>
                    <p>Choose Image</p>
                    <input className="input-file" type="file" id="fileInput" accept="image/*"
                           onChange={handleFileChange}/>
                </label>
            </div>
            <button className={"upload-image-btn"} onClick={handleUploadImage}>
                Upload Image
            </button>

            <div className={"instructions"}>
                <div className={"instruction1"}>
                    {
                        selectedFile === null ?
                            <>
                                <svg width="54" height="54" viewBox="0 0 54 54" fill="none"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M27 0C12.0847 0 0 12.0847 0 27C0 41.9153 12.0847 54 27 54C41.9153 54 54 41.9153 54 27C54 12.0847 41.9153 0 27 0ZM40.2387 34.0875C40.7504 34.5992 40.7504 35.4266 40.2387 35.9383L35.9274 40.2387C35.4157 40.7504 34.5883 40.7504 34.0766 40.2387L27 33.0968L19.9125 40.2387C19.4008 40.7504 18.5734 40.7504 18.0617 40.2387L13.7613 35.9274C13.2496 35.4157 13.2496 34.5883 13.7613 34.0766L20.9032 27L13.7613 19.9125C13.2496 19.4008 13.2496 18.5734 13.7613 18.0617L18.0726 13.7504C18.5843 13.2387 19.4117 13.2387 19.9234 13.7504L27 20.9032L34.0875 13.7613C34.5992 13.2496 35.4266 13.2496 35.9383 13.7613L40.2496 18.0726C40.7613 18.5843 40.7613 19.4117 40.2496 19.9234L33.0968 27L40.2387 34.0875Z"
                                        fill="#C1121F"/>
                                </svg>
                                <p>
                                    File is not selected
                                </p>
                            </>
                            :
                            <>
                                <svg width="55" height="54" viewBox="0 0 55 54" fill="none"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M54.2002 27C54.2002 41.9117 42.1119 54 27.2002 54C12.2885 54 0.200195 41.9117 0.200195 27C0.200195 12.0883 12.2885 0 27.2002 0C42.1119 0 54.2002 12.0883 54.2002 27ZM24.0771 41.2963L44.1094 21.264C44.7896 20.5838 44.7896 19.4808 44.1094 18.8006L41.646 16.3372C40.9657 15.6568 39.8628 15.6568 39.1824 16.3372L22.8454 32.6741L15.218 25.0467C14.5377 24.3665 13.4348 24.3665 12.7544 25.0467L10.291 27.5102C9.61078 28.1904 9.61078 29.2934 10.291 29.9736L21.6136 41.2962C22.2939 41.9765 23.3968 41.9765 24.0771 41.2963Z"
                                        fill="#3DAF00"/>
                                </svg>
                                <p>
                                    File Selection completed
                                </p>
                            </>
                    }
                </div>

                <div className={"instruction2"}>
                    {
                        fileUploaded ?
                            <>
                                <svg width="55" height="54" viewBox="0 0 55 54" fill="none"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M54.2002 27C54.2002 41.9117 42.1119 54 27.2002 54C12.2885 54 0.200195 41.9117 0.200195 27C0.200195 12.0883 12.2885 0 27.2002 0C42.1119 0 54.2002 12.0883 54.2002 27ZM24.0771 41.2963L44.1094 21.264C44.7896 20.5838 44.7896 19.4808 44.1094 18.8006L41.646 16.3372C40.9657 15.6568 39.8628 15.6568 39.1824 16.3372L22.8454 32.6741L15.218 25.0467C14.5377 24.3665 13.4348 24.3665 12.7544 25.0467L10.291 27.5102C9.61078 28.1904 9.61078 29.2934 10.291 29.9736L21.6136 41.2962C22.2939 41.9765 23.3968 41.9765 24.0771 41.2963Z"
                                        fill="#3DAF00"/>
                                </svg>
                                <p>
                                    File uploaded
                                </p>
                            </>
                            :
                            <>
                                <svg width="54" height="54" viewBox="0 0 54 54" fill="none"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M27 0C12.0847 0 0 12.0847 0 27C0 41.9153 12.0847 54 27 54C41.9153 54 54 41.9153 54 27C54 12.0847 41.9153 0 27 0ZM40.2387 34.0875C40.7504 34.5992 40.7504 35.4266 40.2387 35.9383L35.9274 40.2387C35.4157 40.7504 34.5883 40.7504 34.0766 40.2387L27 33.0968L19.9125 40.2387C19.4008 40.7504 18.5734 40.7504 18.0617 40.2387L13.7613 35.9274C13.2496 35.4157 13.2496 34.5883 13.7613 34.0766L20.9032 27L13.7613 19.9125C13.2496 19.4008 13.2496 18.5734 13.7613 18.0617L18.0726 13.7504C18.5843 13.2387 19.4117 13.2387 19.9234 13.7504L27 20.9032L34.0875 13.7613C34.5992 13.2496 35.4266 13.2496 35.9383 13.7613L40.2496 18.0726C40.7613 18.5843 40.7613 19.4117 40.2496 19.9234L33.0968 27L40.2387 34.0875Z"
                                        fill="#C1121F"/>
                                </svg>
                                <p>
                                    File is not uploaded
                                </p>
                            </>
                    }
                </div>
            </div>

            <button className={"generate-animation-btn"} disabled={!fileUploaded} style={fileUploaded? {cursor: "pointer"} : {background: "#b3b3b3", color: "#e1e1e1", cursor: "default"}} onClick={handleGenerateAnimation}>
                Generate Animation
            </button>

            <button className={"run-application-btn"} disabled={!animationGenerated} style={animationGenerated? {cursor: "pointer"} : {background: "#b3b3b3", color: "#e1e1e1", cursor: "default"}} onClick={handleShowAnimation}>
                Show Animation
            </button>
        </div>
    )
}

export default App;
