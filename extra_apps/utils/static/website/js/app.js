$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$('#search-input').focus(function () {
    $('#search-input').width('20rem');
})

$('#search-input').blur(function () {
    $('#search-input').width('15rem');
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ps_encrypt(word, public_key) {
    let password = word;
    //获取公钥
    let PUBLIC_KEY = public_key;
    //rsa加密
    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(PUBLIC_KEY);
    password = encrypt.encrypt(password);//加密后的字符串
    return password;
}


function formatDateTime(value) {
    let date = new Date(value);
    let year = date.getFullYear();    //获取当前年份
    let mon = date.getMonth() + 1;      //获取当前月份
    let da = date.getDate();          //获取当前日
    let a = new Array("日", "一", "二", "三", "四", "五", "六"); //中文星期数组
    let day = date.getDay();          //获取当前星期几
    let h = date.getHours();          //获取小时
    let m = date.getMinutes();        //获取分钟
    let s = date.getSeconds();
    return year + "年" + mon + "月" + da + "日" + " " + h + "时" + m + "分" + s + "秒" + " " + "星期" + a[day];
}