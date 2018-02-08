$(document).ready(function(){
    $("#alltypebtn").bind("click", function(e){
        $("#typediv").toggle()
        $("#sortdiv").hide()
    })

    $("#showsortbtn").bind("click", function(e){
        $("#sortdiv").toggle()
        $("#typediv").hide()
    })

    function func(){
        $(this).hide()
    }
    $("#typediv").bind("click", func)
    $("#sortdiv").bind("click", func)


    //黄色小方块
    var url = location.href
    gidStr = url.split("/")[4]
    $span = $(document.getElementById(gidStr))
    $span.addClass("yellowSlide")




    //购物车
    $allAddButton = $(".addShopping")
    $allsubButton = $(".subShopping")


    $allAddButton.bind("click", function(){
        var productid = $(this).attr("pd")
        $.post("/addCart/1/", {"productid":productid}, function(data, status){
            if (data.data == -1) {
                location.href = 'http://127.0.0.1:8000/login/'
            } else if (data.data == -2) {

            } else {
                //修改span
                $(document.getElementById("pnum"+productid)).html(data.data+"")
            }
        })

    })


    $allsubButton.bind("click", function(){
        var productid = $(this).attr("pd")
        $.post("/addCart/2/", {"productid":productid}, function(data, status){
            if (data.data == -1) {
                location.href = 'http://127.0.0.1:8000/login/'
            } else if (data.data == -2) {

            } else {
                //修改span
                $(document.getElementById("pnum"+productid)).html(data.data+"")
            }
        })
    })

})