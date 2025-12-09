const searchButton = document.getElementById("searchbox-button");
const searchForm = document.getElementById("searchbox-form");
let counter = 0;

// Functions
function selectBorder() {
    const array = new Uint32Array(1);
    crypto.getRandomValues(array);
    const selectedBorder = array[0] % 4;
    return ["top", "right", "bottom", "left"][selectedBorder]
}
function selectCoords(border) {
    const imgSize = 166;
    const width = document.documentElement.clientWidth;
    const height = document.documentElement.clientHeight;

    const getRandomInRange = (min, max) => {
        const range = max - min;
        const array = new Uint32Array(1);
        crypto.getRandomValues(array);
        return min + (array[0] % range);
    };

    switch(border) {
        // [x, y]
        case "top":
            return [
                getRandomInRange(0, width - imgSize),
                -imgSize
            ];
        case "right":
            return [
                width,
                getRandomInRange(0, height - imgSize)
            ];
        case "bottom":
            return [
                getRandomInRange(0, width - imgSize),
                height
            ];
        case "left":
            return [
                -imgSize,
                getRandomInRange(0, height - imgSize)
            ];
    }
}
function createImage(border, coords) { 
    let image = document.createElement("img");
    image.setAttribute("src", `./assets/${border}.png`);
    image.setAttribute("class", "image");

    image.style.zIndex = 100;
    image.style.left = coords[0] + "px";
    image.style.top = coords[1] + "px";

    document.body.appendChild(image);
    return image;
}
function moveImage(border, coords, image) {
    const imgSize = 166;

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            switch(border) {
                case "top":
                    image.style.transform = `translateY(${imgSize}px)`;
                    setTimeout(()=>{
                        image.style.transform = `translateY(-${imgSize}px)`;
                        setTimeout(()=>{image.remove();}, 5000)
                    }, 15000)
                    break;
                    
                case "right":                    
                    image.style.transform = `translateX(-${imgSize}px)`;
                    setTimeout(()=>{
                        image.style.transform = `translateX(${imgSize}px)`;
                        setTimeout(()=>{image.remove();}, 5000)
                    }, 15000)
                    break;
                    
                case "bottom":
                    image.style.transform = `translateY(-${imgSize}px)`;
                    setTimeout(()=>{
                        image.style.transform = `translateY(${imgSize}px)`;
                        setTimeout(()=>{image.remove();}, 5000)
                    }, 15000)
                    break;
                    
                case "left":
                    image.style.transform = `translateX(${imgSize}px)`;
                    setTimeout(()=>{
                        image.style.transform = `translateX(-${imgSize}px)`;
                        setTimeout(()=>{image.remove();}, 5000)
                    }, 15000)
                    break;
            }
        });
    });
}

function executeSearch() {
    const formData = new FormData(searchForm);
    const query = formData.get("search");
 
    if (query) {
        window.open(`https://search.brave.com/search?q=${encodeURIComponent(query)}&source=desktop`);
    }
    else {
        counter+=1;

        if (counter===42) {
            border = selectBorder();
            coords = selectCoords(border);
            image = createImage(border, coords);
            moveImage(border, coords, image);
            counter = 0;
        }
    };
}

// Event listeners
searchButton.addEventListener("click", executeSearch)
searchForm.addEventListener("submit", executeSearch)
