
var Service = {
    init: function () {
        this.initToken();
        this.initEvents();
    },
    initToken: function () {
        // csrf-token传递
        var token = $('meta[name="_csrf"]').attr('content');
        $.ajaxSetup({
            // csrf 发送ajax安全机制
            data: {csrfmiddlewaretoken: token}
        });
    },
    initEvents: function () {

        // 启动/停止服务
        $('.action-btn').on('click', function () {
            var $this = $(this);
            $this.attr("disabled", "disabled");
            $this.find("i").addClass('fa-spin');
            var serverName = $this.attr('name');
            var serverMode = $this.attr('data-action');
            var serverport = $this.attr('server_port');
            var url = '/servicelist/';
            var params = {
                'servername': serverName,
                'servermode': serverMode,
                "serverport": serverport
            };

            // 提交
            $.post(url, params, function (res) {

                // var result = JSON.parse(res);
                // alert(res.status);
                if (res.status === 1) {
                    layer.alert('启停服务成功！',
                        function () {
                        // 刷新
                        location.reload();
                            console.log(6666)
                    });
                } else {
                    // alert(res);
                    alert('启停服务失败！');
                    // location.reload();
                }
            });

        });

        // 下载列表弹窗
        $('.download-btn').on('click', function () {
            var $this = $(this);
            var $form = $this.siblings('form');
            var serverName = $this.attr('data-serverName');

            layer.open({
                type: 1,
                title: '下载日志',
                anim: 2,
                area: ['580px', '400px'],
                skin: 'layui-layer-ops', //样式类名
                shadeClose: 0, // 关闭遮罩关闭
                content: $form,
                btn: ['下载', '关闭'],
                success: function () {
                    Service.tableIsCheck();
                },
                yes: function (index) {

                    var logDir = $form.attr('data-logdir');
                    var selectedLog = [];
                    // 拼接logName参数
                    $form.find('.log-item:checked').each(function (index, item) {
                        var val = item.value;
                        selectedLog.push(val);
                    });

                    // 提交参数
                    var url = '/servicelist/';
                    var params = {
                        logname: JSON.stringify(selectedLog),
                        logdir: logDir
                    };

                    // 未选中日志文件
                    if (selectedLog.length === 0) {
                        layer.alert('请选择日志文件！');
                        return;
                    }

                    var msg = layer.msg('正在压缩日志...', {
                        icon: 16,
                        shade: 0.01
                    });

                    // 获取日志zip包
                    $.post(url, params, function (res) {
                        layer.close(msg);

                        var result = JSON.parse(res);
                        // var result = res;
                        // 获取日志文件zip
                        if (result.status === 1) {
                            var aLink = document.createElement('a');
                            var url = 'downlog/';
                            try {
                                aLink.setAttribute('href', url);
                                aLink.setAttribute("download", serverName + ".zip");
                                var clickEvent = new MouseEvent("click", {
                                    "view": window,
                                    "bubbles": true,
                                    "cancelable": false
                                });
                                aLink.dispatchEvent(clickEvent);
                            } catch (ex) {
                                console.log(ex);
                            }
                        } else {
                            layer.alert('下载日志文件失败！');
                            return false;
                        }
                    });

                    layer.close(index);
                }
            });

        });

    },
    tableIsCheck: function (options) {
        // 设定默认值:
        var defaults = {
            selectAll: $('.layui-layer #items'),
            items: $('.layui-layer .log-item')
        };

        var opts = $.extend({}, defaults, options);
        var selectAll = opts.selectAll;
        var items = opts.items;
        var invertSelect = null;
        var trs = items.parents('tr');

        //监听全选或全不选事件
        selectAll.click(function () {
            if (this.checked) {
                items.prop('checked', true);
                // trs.addClass('wj-table-selected');
            } else {
                items.prop('checked', false);
                // trs.removeClass('wj-table-selected');
            }
        });

        //监听反选事件
        /*invertSelect.click(function(){
            items.map(function(){
                if(this.checked){
                    this.checked = false;
                }else {
                    this.checked = true;
                }
            });
        });*/

        //监听手动选择事件
        items.click(function () {

            // 添加选中样式
            /*if(this.checked) {
                $(this).parents('tr').addClass('wj-table-selected');
            }else {
                $(this).parents('tr').removeClass('wj-table-selected');
            }*/

            var isAllChecked = true;
            items.map(function () {
                if (!this.checked) {
                    isAllChecked = false;
                }
            });

            if (isAllChecked) {
                selectAll.prop('checked', true);
            } else {
                selectAll.prop('checked', false);
            }
        });
    }
};

$(document).ready(function () {
    Service.init();
});
