var Sysecurity = new Vue({
    el: '#portForm',
    data: {
        SSH: {
            isOpen: true,
            port: null
        }
    },
    mounted: function () {
        // 页面初始化
        this.pageRender();
    },
    methods: {
        pageRender: function () {
            this.initToken();
            this.getPort();
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
        getPort: function () {
            var url = '/sysecurity/check/';
            var params = {};
            $.getJSON(url, params, function (res) {
                if (res) {
                    // 赋值
                    Sysecurity.SSH = res.data.ssh;
                }
            });
        },
        eventsBind: function () {

            // 保存
            $('.save-port-btn').on('click', function () {
                // 端口号
                var port = Sysecurity.SSH.port;

                // 校验通过，继续执行业务逻辑
                if (Sysecurity.SSH.isOpen && !Sysecurity.isPort(port)) {
                    layer.tips("请输入正确的端口号！", '#port', {
                        tips: [2, '#ba2723']
                    });
                    return false;
                }

                var url = '/sysecurity/check/';
                var params = {
                    isOpen: Sysecurity.SSH.isOpen,
                    port: port
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
                        layer.alert('修改SSH登录端口成功！', function () {
                            // 刷新
                            location.reload();
                        });
                    } else {
                        layer.alert('修改SSH登录端口失败！');
                    }
                });

            });

        },
        isPort: function (port) {
            // 校验10000以上但不以22结尾的端口号
            var reg = /^[1-6]\d{2}(\d[^2]|[^2]\d)$/;

            return reg.test(port);
        }
    }
});

