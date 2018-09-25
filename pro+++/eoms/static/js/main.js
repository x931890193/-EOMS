$(function () {
    // localStorage.data = localStorage.
    //  登录表单提交
    $("#logo").submit(function (e) {

        e.preventDefault();
        var username = $("#signin-text").val();
        var password = $("#signin-password").val();

        if (!username) {
            alert("填写用户名")
            return;
        }
        if (!password) {
            alert("填写密码")
            return;
        }
        // 发起登录请求
        var params = {
            "username": $.base64.encode(username + getCookie('csrftoken')),
            "password": $.base64.encode(password + getCookie('csrftoken'))
        };

        $.ajax({
            url: "/login/",
            method: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            headers: { 'X-CSRFToken': getCookie('csrftoken'),
                //    获取自己cookie中的csrftoken     csrftoken   在钩子中放入的
            },
            success(response) {
                // console.log(response.user_id);
                console.log(response);
                if (response.errno == 200) {
                    // 刷新当前界面
                    // location.reload();
                    location.href = "/"
                    // alert("555555")


                } else {
                    /////////
                    alert(response.errmsg)
                      }
                             },
            error(e){
                // alert(6666666)

                if (e.status==500){alert("Unknown Error!")}

                }
        })
    })

        // 注册表单
    $("#reg").submit(function (e) {

        e.preventDefault();
        var username_reg = $("#signin-text_reg").val();
        var password_reg = $("#signin-password_reg").val();
        var comfirm_pass_reg = $("#comfirm-password_reg").val();
        var params = {
            "username": $.base64.encode(username_reg + getCookie('csrftoken')),
            "password": $.base64.encode(password_reg + getCookie('csrftoken')),
            "comfirm_pass": $.base64.encode(comfirm_pass_reg + getCookie('csrftoken')),
        };
        if (!username_reg) {
            alert("请输入用户名")
            return;
        }
        if (!password_reg) {
            alert("请填写密码！")
            return;
        }
        if (!comfirm_pass_reg) {
            alert("确认密码！")
            return;
        }
        if (password_reg !== comfirm_pass_reg) {
            alert("两次密码不一致！")
        }
        if (password_reg.length < 3 || username_reg <3 ){
            alert("密码过于简单!")
        }

        // 发起请求
        $.ajax({
            url: "/register/",
            method: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            headers: { 'X-CSRFToken': getCookie('csrftoken'),
                //    获取自己cookie中的csrftoken     csrftoken   在钩子中放入的
            },
            success(response) {
                // console.log(response.user_id);
                console.log(response);
                if (response.errno == 201) {
                    // 刷新当前界面
                    alert(response.errmsg);
                    // location.reload();
                    location.href = "/"
                    // alert("555555")


                } else {
                    /////////
                    alert(response.errmsg)
                      }
                             },
            error(e){
                console.log(e);
                if (e.errno=500){alert(e.statusText)}

                }
        })
    });

    $('#old_pass').focus(function ()//focus 事件
            {
                $('#old_pass').val('');
            });
    $('#new_pass').focus(function ()//focus 事件
            {
                $('#new_pass').val('');
            });
    $('#comfirm_pass').focus(function ()//focus 事件
            {
                $('#comfirm_pass').val('');
            });

       //  修改密码表单提交
    $(".form-auth-change").submit(function (e) {

        e.preventDefault();
        var old_pass = $("#old_pass").val();
        var new_pass = $("#new_pass").val();
        var comfirm_pass = $("#comfirm_pass").val();
        var params = {
            "old_pass": $.base64.encode(old_pass + getCookie('csrftoken')),
            "new_pass": $.base64.encode(new_pass + getCookie('csrftoken')),
            "comfirm_pass": $.base64.encode(comfirm_pass + getCookie('csrftoken')),
        };
        if (!old_pass) {
            alert("请输入原密码")
            return;
        }
        if (!new_pass) {
            alert("请填写新密码！")
            return;
        }
        if (!comfirm_pass) {
            alert("确认密码！")
            return;
        }
        if (new_pass !== comfirm_pass) {
            alert("两次密码不一致！")
        }
        if (old_pass.length < 3 || new_pass <3 || comfirm_pass < 3 ){
            alert("密码过于简单!")
        }

        // 发起修改请求
        $.ajax({
            url: "/changepassword/",
            method: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            headers: { 'X-CSRFToken': getCookie('csrftoken'),
                //    获取自己cookie中的csrftoken     csrftoken   在钩子中放入的
            },
            success(response) {
                // console.log(response.user_id);
                console.log(response);
                if (response.errno == 202) {
                    // 刷新当前界面
                    alert(response.errmsg);
                    // location.reload();
                    location.href = "/logout/"
                    // alert("555555")


                } else {
                    /////////
                    alert(response.errmsg)
                      }
                             },
            error(e){
                console.log(e)
                if (e.errno=500){alert(e.statusText)}

                }
        })
    });
    });





















function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
        }



function GetInfo() {
    $.ajax( {
    url:"/",
    type: 'get',
    headers: { 'X-CSRFToken': getCookie('csrftoken')},
    success: function(){}
        });

        }