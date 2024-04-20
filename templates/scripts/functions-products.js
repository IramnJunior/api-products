const data = document.querySelectorAll("input[name='btnradio']");

data.forEach(data => {
    data.addEventListener("change", findSelectd = () => {
        const selected = document.querySelector("input[name='btnradio']:checked").value;

        const addInfos = document.getElementById("addInfos");
        const editInfos = document.getElementById("editInfos");
        const deleteInfos = document.getElementById("deleteInfos");

        addInfos.style.display = "none";
        editInfos.style.display = "none";
        deleteInfos.style.display = "none";


    switch(selected) 
    {
        case "Adicionar":
            addInfos.style.display = "grid";
            
            document.getElementById("sentButton").onclick = async function sent_products()
            {
                const name = document.getElementById("name-id-add").value;
                const description = document.getElementById("description-id-add").value;
                const price = document.getElementById("price-id-add").value;
                const price_tax = document.getElementById("price-tax-id-add").value;

                await axios.post("http://products-manager-ten.vercel.app/add/", {
                    name: `${name}`,
                    description: `${description}`,
                    price: `${price}`,
                    tax: `${price_tax}`
                }, {
                    headers: {
                        "Content-Type": "application/json"
                    }
                }).then(response => {
                    console.log("item added successfully")
                }).catch(error => {
                    console.log(error);
                })

                get_products_data()
            }

            
            break;

        case "Editar":
            editInfos.style.display = "grid";

            document.getElementById("sentButton").onclick = async function sent_products()
            {
                const id = document.getElementById("input-id-edit").value;
                const name = document.getElementById("name-id-edit").value;
                const description = document.getElementById("description-id-edit").value;
                const price = document.getElementById("price-id-edit").value;
                const price_tax = document.getElementById("price-tax-id-edit").value;

                await axios.put(`http://products-manager-ten.vercel.app/edit/${id}`, {
                    name: `${name}`,
                    description: `${description}`,
                    price: `${price}`,
                    tax: `${price_tax}`
                }, {
                    headers: {
                        "Content-Type": "application/json"
                    }
                }).then(response => {
                    console.log("item edited successfully");
                }).catch(error => {
                    console.log(error);
                })

                get_products_data()
            }

            
            break;

        case "Apagar":
            deleteInfos.style.display = "grid";

            document.getElementById("sentButton").onclick = async function sent_products()
            {
                const id = document.getElementById("input-id-delete").value;

                await axios.delete(`http://products-manager-ten.vercel.app/delete/${id}`)
                           .then(response => {
                            console.log(`Deleted data with ID: ${id}`);
                           })
                           .catch(error => {
                            console.log(error)
                           })

                get_products_data()
            }

            
            break;
    }
    })
})


async function get_products_data() {
    await axios.get("http://products-manager-ten.vercel.app/get/products/")
    .then(response => {
        const data = response.data
        document.getElementById('products-id').innerHTML = ''
        for (let product of data) {
            document.getElementById('products-id').innerHTML += `
                <p>
                    Id: ${product['id']}<br>
                    Name: ${product['name']}<br>
                    Description: ${product['description']}<br>
                    Price: ${product['price']}<br>
                    Tax: ${product['tax']}<br>
                    Sale Price: ${product['sale_price']}<br>
                </p>
            `
        }
    })
}

get_products_data()