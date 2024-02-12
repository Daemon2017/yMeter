function measure() {
    document.getElementById("resultsID").innerHTML = "";
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var result = String.fromCharCode.apply(null, new Uint8Array(this.response));
            table = document.getElementById("resultsID");
            table.innerHTML = "";
            for (let row of CSV.parse(result)) {
              let tr = table.insertRow();
              for (let col of row) {
                let td = tr.insertCell();
                td.innerHTML = col;
              }
            }
        }
    }
    xhr.responseType = "arraybuffer";

    xhr.open("POST", "https://bbagglj1i928n0qhcggp.containers.yandexcloud.net/measure");
    xhr.setRequestHeader("ypg", document.getElementById("ypgID").value);
    xhr.setRequestHeader("amr", document.getElementById("amrID").value);
    xhr.setRequestHeader("rp", document.getElementById("rpID").value);
    xhr.setRequestHeader("Content-Type", "text/plain");

    var body = document.getElementById("referenceID").value + "\n" + document.getElementById("samplesID").value;

    xhr.send(body);
}