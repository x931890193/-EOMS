var eth = new Vue({
    el: '#serverIPForm',
    data: {
        serverIP: {
            isOuter: false,
            inner: {
                ip: "",
                netMask: "",
                gateway: "",
                dns: ""
            },
            outer: {
                ip: "",
                netMask: "",
                gateway: "",
                dns: ""
            },
            url: ''
        }
    },
    mounted: function () {
        // 页面初始化
        this.pageRender();
    },
    updated: function() {
        console.log('eth:===>' + JSON.stringify(this.eth));
    },
    methods: {
        pageRender: function () {
            this.initToken();
            this.getServerIP();
            this.eventsBind();
        },
        initToken: function () {
            // csrf-token传递
            var token = $('meta[name="_csrf"]').attr('content');
            $.ajaxSetup({
                // csrf 发送ajax安全机制
                data: {csrfmiddlewaretoken: token}
            });
        },
        getServerIP: function() {
            // mock数据
            var url = '/eth/check/';
            var params = {};
            $.getJSON(url, params, function (res) {
                if (res) {
                    // 赋值
                    eth.serverIP = res.data.serverIP;
                }
            });
        },
        eventsBind: function () {

            // 保存
            $('.server-ip-btn').on('click', function () {

                var isCheck = true;
                // IP校验
                $('.server-ip-form .ip-check').each(function (index, item) {

                    var ip = $.trim($(item).val());
                    var id = $(item).attr('id');
                    if(!eth.isIP(ip)) {
                        layer.tips("请输入正确的IP地址！", '#' + id, {
                            tips: [2, '#ba2723']
                        });
                        isCheck = false;
                        return false;
                    }
                });

                if(isCheck) {
                    // 地址校验
                    var outURL = eth.serverIP.url;
                    if(!eth.isURL(outURL) && !eth.isIP(outURL)) {
                        layer.tips("请输入正确的外网地址！", '#url', {
                            tips: [2, '#ba2723']
                        });
                        isCheck = false;
                        return;
                    }
                }

                // 校验通过，继续执行业务逻辑
                if(isCheck){
                    var url = '/eth/commit/';
                    var params = {
                        serverIP: JSON.stringify(eth.serverIP)
                    };

                    var msg = layer.msg('正在加载...', {
                        icon: 16,
                        shade: 0.6
                    });

                    // 提交
                    $.post(url, params, function (res) {

                        layer.close(msg);
                        var result = JSON.parse(res);
                        if (result.code === 1) {
                            layer.alert('修改服务IP成功！', function () {
                                // 刷新
                                location.reload();
                            });
                        } else {
                            layer.alert('修改服务IP失败！');
                        }
                    });
                }

            });

        },
        isIP: function (ip) {
            var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
            return reg.test(ip);
        },
        isURL: function (url) {
            // var reg = /(https?|ftp|file):\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|](:\d*)?/;
            var reg = /^[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|](:\d*)?/;
            return reg.test(url);
        }
    }
});
