// Navigate here: https://www.namecheap.com/domains/#pricing
// and run this code in the console

function download(filename, text) {
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);

    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

async function scrape() {
    // Get domains table and it's rows
    var t = document.getElementsByClassName("gb-table gb-table--responsive")[0];
    var tRows = t.children[1].children;
    var initialLength = tRows.length;

    console.log("Please wait...");

    // Find and click the "Choose from" dropdown and select "All"
    var dd = document.getElementsByClassName("gb-select__toggle");
    var di = document.getElementsByClassName("gb-select__item");
    for (let i = 0; i < di.length; i++) {
        const element = di[i];
        if(element.innerText.toLowerCase() == "all") {
            for (let j = 0; j < dd.length; j++) {
                const ddelem = dd[j];
                ddelem.click();
            }
            element.click();
            break;
        }
    }

    console.log("Waiting for the list to update...");

    var grown = false;
    while(!grown) {
        await new Promise(r => setTimeout(r, 500));
        if(tRows.length > (initialLength*2) | tRows.length > 500) grown = true;
    }

    var result = {"result": []};

    console.log("Finalizing result (" + tRows.length + " rows)...");

    for (let i = 0; i < tRows.length; i++) {
        const row = tRows[i];
        var properties = row.children;
        var tld = properties[0].querySelectorAll(".gb-tld-name")[0].innerText;
        tld = tld.substr(1, tld.length);
        var register = properties[1].children[0].innerText;
        var renew = properties[2].children[0].innerText;
        result["result"].push({"tld": tld, "register": register, "renew": renew});
    }

    download("tlds.json", JSON.stringify(result))
    console.log("Saved to file!");
}

scrape();