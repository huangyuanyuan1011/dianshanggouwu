$(document).ready(function(){
    function getCookie(name){
        var c = document.cookie.match("\\b" + name + "=([^;]*)\\b")
        return c ? c[1] : undefined
    }
    //验证账号是否被占用
    $("#accunt").bind("blur", function(e){
        //验证长度
        if ($(this).val().length < 6 || $(this).val().length > 12) {
            $("#accunterr").show()
            return
        }
        //验证是否占用
        $.post("/register/", {"userAccount":$(this).val()}, function(data, status){
            if (data.data) {
                $("#checkerr").show()
            }
        })
//        $.ajax({
//                url:"/register/",
//                method:"post",
//                data:{"userAccount":$(this).val()},
//                success:function(data, status){
//                    console.log(data)
//                    console.log(status)
//                },
//                headers:{
//                    "X-XSRFToken":getCookie("csrftoken")
//                }
//            })
    })
    $("#accunt").bind("focus", function(e){
        $("#accunterr").hide()
        $("#checkerr").hide()
        $(this).val("")
    })


    $("#pass").bind("focus", function(e){
        $("#passerr").hide()
        $(this).val("")
    })
    $("#pass").bind("blur", function(e){
        //验证长度
        if ($(this).val().length < 6 || $(this).val().length > 16) {
            $("#passerr").show()
            return
        }
    })

    $("#passwd").bind("focus", function(e){
        $("#passwderr").hide()
        $(this).val("")
    })
    $("#passwd").bind("blur", function(e){
        //验证长度
        if ($(this).val() != $("#pass").val()) {
            $("#passwderr").show()
            return
        }
    })






})