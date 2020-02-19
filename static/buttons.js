function submit() {
    const dataURI = canvas.toDataURL();
    document.getElementById("uri").innerHTML = dataURI;
    document.getElementById("completed").innerHTML = "Your LaTeX conversion is";

    $.ajax({
        type: "POST",
        url: "/process",
        data: {param: dataURI}
    }).done(function( o ) {

    });

}
function restart() {
    document.getElementById("uri").innerHTML = "";
    document.getElementById("completed").innerHTML = "";
    restartarray();
    redraw();
}