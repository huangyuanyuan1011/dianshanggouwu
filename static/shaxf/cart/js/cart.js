$(document).ready(function(){

    //购物车
    $allAddButton = $(".addShopping")
    $allsubButton = $(".subShopping")


    $allAddButton.bind("click", function(){
        var productid = $(this).attr("pd")
        $.post("/addCart/1/", {"productid":productid}, function(data, status){
            if (data.data == -1) {

            } else if (data.data == -2) {

            } else {
                //修改span
                $(document.getElementById("pnum"+productid)).html(data.data+"")
                //修改价格
                $(document.getElementById("pprice"+productid)).html(data.price+"")
            }
        })

    })


    $allsubButton.bind("click", function(){
        var productid = $(this).attr("pd")
        $.post("/addCart/2/", {"productid":productid}, function(data, status){
            if (data.data == -1) {

            } else if (data.data == -2) {

            } else {
                //修改span
                $(document.getElementById("pnum"+productid)).html(data.data+"")
                //修改价格
                $(document.getElementById("pprice"+productid)).html(data.price+"")
            }
        })
    })



    $(".ischose").bind("click", function(e){
         var productid = $(this).attr("pd")
        $.post("/addCart/3/", {"productid":productid}, function(data, status){
            if (data.data == -1) {

            } else if (data.data == -2) {

            } else {
                //修改span
                var str = ""
                if (data.chose) {
                    str = "√"
                }
                $(document.getElementById("pchose"+productid)).html(str)
            }
        })
    })




    //下单
    $("#ok").bind("click", function(e){
        var f = confirm("确认下单？")
        if (f) {
            $.post("/deal/", function(data, status){
                if (data.data == 0){
                    location.href = "http://127.0.0.1:8000/cart/"
                }
            })
        }
    })

    $("#allOk").bind("click", function(e){
            $.post("/allOk/",function(data, status){
                if (data.data == 0){
                    location.href = "http://127.0.0.1:8000/cart/"
                }
                if (data.data == 2){
                     //修改span
                var str = ""
                if (data.chose) {
                    str = "√"
                }
                $('#chose').html(str)
            }
           })
    })

})