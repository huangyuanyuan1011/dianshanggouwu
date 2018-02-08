$(document).ready(function(){
    document.documentElement.style.fontSize = innerWidth / 10 + "px";

    var url = location.href;
    pArr = url.split("/");
    span = $(document.getElementById(pArr[3]))
    str = "url(/static/shaxf/base/img/"+pArr[3]+"1.png) no-repeat"
    span.css("background", str)
    span.css("background-size", "0.52rem")
})