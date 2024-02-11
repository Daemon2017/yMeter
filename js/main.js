function subtract() {
    document.getElementById("resultsID").value = "";
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

    xhr.open("POST", "http://localhost:8080/measure");
    xhr.setRequestHeader("Content-Type", "text/plain");

    var body = document.getElementById("referenceID").value + "\n" + document.getElementById("samplesID").value;

    xhr.send(body);
}