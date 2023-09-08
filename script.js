const button = document.getElementById("button")
const checkboxes = document.getElementsByClassName("checkbox")
const N = checkboxes.length

function getSelection() {
    const selected = []
    for (let i = 1; i < N + 1; i++) {
        const checkbox = document.getElementById(`${i}`)
        if (!checkbox) {
            console.log(`checkbox ${i} not found`)
            continue
        }
        const [wavelength, excitation] = data[i - 1]
        if (checkbox.checked) {
            selected.push([wavelength, excitation])
        }
    }
    return selected
}

Array.from(checkboxes).forEach((checkbox) =>
    checkbox.addEventListener("change", () => {
        const selected = getSelection()
        const counts = {}
        selected.forEach(([wavelength, excitation]) => {
            counts[excitation] = counts[excitation] ? counts[excitation] + 1 : 1
        })
        Object.entries(counts).forEach(([excitation, count]) => {
            const p = document.getElementById(excitation)
            if (p) {
                p.innerHTML = `${element} ${excitation}: ${count}`
            }
        })
    })
)

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

button.addEventListener("click", () => {
    const selected = getSelection()
    const selectedWavelengths = selected.map(
        ([wavelength, excitation]) => Math.round(wavelength * 1000) / 1000
    )
    console.log(selectedWavelengths)
    const text = "data:text/txt;charset=utf-8," + selectedWavelengths.join(" ")
    download(text, "wavelengths.txt")
})
