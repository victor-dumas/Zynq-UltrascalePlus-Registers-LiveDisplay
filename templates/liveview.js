function reqListener(req, reqTime, e) {
    var startTime = performance.now()

    // Request status is good
    if (req.status == 200) {
        response = JSON.parse(req.responseText);
        values = document.querySelectorAll('.value')
        Array.prototype.forEach.call(values, node => {
            Object.keys(response).forEach(addr => {
                if (addr == node.id) {
                    node.childNodes[0].nodeValue = response[addr]
                }
            });
        });
    } else {
        console.log("Request error(" + req.status + "): " + req);
    }
        
    var endTime = performance.now()
    console.log(`Call to reqListener took ${endTime - startTime}ms ${endTime - reqTime}ms`)
}

function transferFailed(e) {
    console.log("Error while transferring data");
}

function transferCanceled(e) {
    console.log("Transfer was cancelled");
}

// Request updated values for the entire page (making 100's of requests per seconds freezes the browser)
function getValues() {
    var json = new Object()
    json.values = []

    values = document.querySelectorAll('.value')
    Array.prototype.forEach.call(values, node => {
        json.values.push(node.id);
    });

    var reqTime = performance.now()
    // Prepare and sent the request
    var req = new XMLHttpRequest();
    req.open("POST", "values", true);
    req.overrideMimeType("application/json");
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.addEventListener("load", reqListener.bind(null, req, reqTime), false);
    req.addEventListener("error", transferFailed, false);
    req.addEventListener("abort", transferCanceled, false);
    req.send(JSON.stringify(json));
}

interval = setInterval(getValues, 1000);

//setTimeout(function() { clearInterval(interval); }, 10000);