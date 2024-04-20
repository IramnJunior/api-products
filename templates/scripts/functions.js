async function send_informations() {
   await axios.get("https://products-manager-ten.vercel.app/get/credentials/")
        .then(response => {

            const response_data = dict_data(response.data);

            const userForms = document.getElementById("userId").value;
            const passwordForms = document.getElementById("passwordId").value;

            const userDB = response_data["user"];
            const passwordDB = response_data["password"];

            verify_credentials(userForms, passwordForms, userDB, passwordDB);
        })
        .catch(error => {
            console.log(error);
        })
}


const dict_data = (response) => {
    data = response[0];
    return data;
}


const verify_credentials = (userForms, passwordForms, userDB, passwordDB) => {
    if ((userForms == userDB) && (passwordForms == passwordDB)) {
        window.location.href = "https://products-manager-ten.vercel.app/home/products";
    } else {
        console.log("error");
    }
}