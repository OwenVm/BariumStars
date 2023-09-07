const button = document.getElementById("button");
const checkboxes = document.getElementsByClassName("checkbox");
const N  = checkboxes.length;

function download(url, filename) {
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    setTimeout(function () {
        document.body.removeChild(a)
        window.URL.revokeObjectURL(url)
    }, 0)
}

button.addEventListener("click", function() {
    let selectedWavelengths = []
    for (let i = 1; i < N+1; i++) {
        const checkbox = document.getElementById(`${i}`);
        if (!checkbox) {
            console.log(`checkbox ${i} not found`);
            continue;
        }

        const [wavelength, excitation] = data[i-1];
        if (checkbox.checked) {
            selectedWavelengths.push(Math.round(wavelength*100)/100);
        }
    }
    console.log(selectedWavelengths);
    const text = "data:text/txt;charset=utf-8," + selectedWavelengths.join(" ")
    download(text, "wavelengths.txt")
})
