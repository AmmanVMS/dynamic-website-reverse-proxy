
/* Edit a url.
 *
 */
function edit(urlString, subDomain) {
    var url = new URL(urlString);
    document.getElementById("input-ip").value = url.hostname;
    document.getElementById("input-port").value = url.port;
    document.getElementById("input-name").value = subDomain;
}

