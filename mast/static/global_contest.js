let articleBody = document.getElementById('article-body');
let modalButtons = Array.from(document.getElementsByClassName("modalButton"));

async function getArticle(articleName, order) {
    fetch(`/static/${articleName}.json`, {
        method: 'GET'
    })
        .then(response => response.json())
        .then(data => {
            data = data.find(x => x.articleNumber === parseInt(order));
            createArticle(data.title, data.body, order);
        })
        .catch(ex => {
            console.log("Failed to load the source.")
            console.log(`ERROR: ${ex}`);
        });
}

async function getPicture(id, par) {
    fetch(`/static/articles/${id}.jpg`, {
        method: 'GET'
    })
        .then(response => response.blob())
        .then(image => {
            let outside = URL.createObjectURL(image);
            console.log(outside);
            let img = document.createElement("img");

            img.src = outside;
            img.width = 256;
            img.height = 256;
            img.style.setProperty("float", "right")
            par.prepend(img);
        })
        .catch(ex => {
            console.log("Failed to download the image for the article.");
            console.log(`See Error Message: ${ex}`);
        })
}

function createArticle(title, body, order) {
    let heading = document.createElement("h4");
    let par = document.createElement("p");
    heading.innerHTML = title;
    getPicture(order, par)
    par.innerHTML = body.replaceAll("\n", "<br><br>");
    articleBody.appendChild(heading);
    articleBody.appendChild(par);
}

modalButtons.forEach(modalButton => {

    modalButton.addEventListener('click', () => {

        articleBody.innerHTML = "";
        getArticle("matfyz_challenge", modalButton.dataset.order);
    });

})

